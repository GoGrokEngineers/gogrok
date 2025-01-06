import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.core.cache import cache
from django.utils.text import slugify


class CompetitionRoomConsumer(AsyncWebsocketConsumer):
    
    async def connect(self):
        self.comp_uid = self.scope['url_route']['kwargs']['comp_uid']
        self.room_group_name = f'waiting_room_{self.comp_uid}'

        if not await self.validate_comp_uid():
            await self.close()
            return

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

        await self.send_initial_participant_status()

        comp_data = self.get_competition_data()
        
        # Parse comp_data if it's a string
        if isinstance(comp_data, str):
            comp_data = json.loads(comp_data)

     

    def get_competition_data(self):
        # Fetch data from Redis, DB, or other sources
        # Example: Redis fetch (assume serialized JSON)
        comp_data = '{"participants": {"user1": {"start": true}, "user2": {"start": false}}}'
        return comp_data

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        action = data.get('action')
        nickname = data.get('nickname', '')

        if action and hasattr(self, f"handle_{action}"):
            handler_method = getattr(self, f"handle_{action}")
            await handler_method(nickname)
        else:
            await self.send_error('Invalid action or missing action.')

    async def handle_join(self, nickname):
        comp_data = await self.get_comp_data()


        if not comp_data:
            await self.send_error("Competition does not exist or has expired.")

    
        if comp_data["is_started"]:
            await self.send_error('The competition has already started.')

        if await self.is_participant_limit_reached(comp_data):
            await self.send_error('The competition is at full capacity.')
            return

        if await self.is_nickname_taken(comp_data, nickname):  # Check for duplicate nickname
            await self.send_error('This nickname is already taken.')
            return

        # Add participant
        participant_id = len(comp_data["participants"]) + 1
        comp_data["participants"][nickname] = self.create_participant(participant_id)

        await self.update_comp_data(comp_data)
        await self.send_initial_participant_status()

        # Notify others in the room
        await self.broadcast_event('user_joined', nickname, comp_data)


    async def user_joined(self, event):
        nickname = event.get("nickname")
        participants = event.get("participants")

        await self.send(text_data=json.dumps({
            'type': 'user_joined',
            'nickname': nickname,
            'participants': participants
        }))

    
    async def user_left(self, event):
        nickname = event.get("nickname")
        participants = event.get("participants")

        await self.send(text_data=json.dumps({
            'type': 'user_left',
            'nickname': nickname,
            'participants': participants
        }))


    async def handle_leave(self, nickname):
        comp_data = await self.get_comp_data()

        if not comp_data:
            await self.send_error('Competition does not exist or has expired.')
            return

        if nickname not in comp_data["participants"]:
            await self.send_error('Participant not found.')
            return

        del comp_data["participants"][nickname]
        await self.update_comp_data(comp_data)
        await self.send_initial_participant_status()

        await self.broadcast_event('user_left', nickname, comp_data)


    async def handle_start(self, nickname):
        comp_data = await self.get_comp_data()

        if not comp_data:
            await self.send_error('Competition does not exist or has expired.')
            return

        if nickname not in comp_data["participants"]:
            await self.send_error('Participant not found.')
            return

        comp_data["participants"][nickname]["start"] = True
        await self.update_comp_data(comp_data)

        if await self.are_all_participants_ready(comp_data):
                await self.start_competition(comp_data)
        else:
            # Notify that the competition can't start yet
            await self.send(text_data=json.dumps({
                'type': 'not_all_ready',
                'message': 'Not all participants are ready or the competition is not at full capacity.'
            }))



    async def are_all_participants_ready(self, comp_data):
        """
        Checks if all participants have the 'start' flag set to True and 
        if the number of participants matches the competition's capacity.
        Returns True if all are ready, otherwise False.
        """


        if len(comp_data.get("participants", {})) != comp_data.get("capacity", 0):
            return False

        for participant in comp_data.get("participants", {}).values():
            if not participant.get("start", False):  # If any participant isn't ready, return False
                return False
        return True
    
    async def start_competition(self, comp_data):
        """
        This method is called when all participants are ready and the capacity is met.
        It starts the competition and sends a broadcast message to everyone.
        """
      
        comp_data["is_started"] = True
        await self.update_comp_data(comp_data)

        # Notify all participants that the competition has started
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'competition_started',
                'message': 'The competition has started!'
            }
        )
        
        await self.send(text_data=json.dumps({'type': 'competition_started', 'message': 'The competition has started!'}))

    async def competition_started(self, event):
        await self.send(text_data=json.dumps({
            'type': 'competition_started',
            'message': event['message']
        }))
        


    async def send_initial_participant_status(self):
        comp_data = await self.get_comp_data()

        if not comp_data:
            return

        ready_to_start, not_ready_to_start = self.get_participant_status(comp_data)
        
        await self.send(text_data=json.dumps({
            'type': 'initial_participant_status',
            'ready_to_start': ready_to_start,
            'not_ready_to_start': not_ready_to_start
        }))

    async def update_and_broadcast_participant_status(self, comp_data):
        ready_to_start, not_ready_to_start = self.get_participant_status(comp_data)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'update_start_status',
                'ready_to_start': ready_to_start,
                'not_ready_to_start': not_ready_to_start
            }
        )

    async def broadcast_event(self, event_type, nickname, comp_data):
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': event_type,
                'nickname': nickname,
                'participants': list(comp_data["participants"].keys())
            }
        )

    async def update_start_status(self, event):
        await self.send(text_data=json.dumps({
            'type': 'update_start_status',
            'ready_to_start': event['ready_to_start'],
            'not_ready_to_start': event['not_ready_to_start']
        }))

    async def validate_comp_uid(self):
        comp_data = cache.get(self.comp_uid)
        return bool(comp_data and not comp_data.get("is_started"))

    async def get_comp_data(self):
        return cache.get(self.comp_uid)

    async def update_comp_data(self, comp_data):
        cache.set(self.comp_uid, comp_data)

    async def send_error(self, message):
        await self.send(text_data=json.dumps({'success': False, 'message': message}))

    async def is_participant_limit_reached(self, comp_data):
        return len(comp_data["participants"]) >= comp_data["capacity"]

    async def is_nickname_taken(self, comp_data, nickname):
        return nickname in comp_data["participants"]

    def create_participant(self, participant_id):
        return {
            "id": participant_id,
            "start": False,
            "is_solved": False,
            "solved_at": None,
            "time_took": None,
        }

    def is_valid_nickname(self, nickname):
        return bool(nickname and nickname.isalnum())

    def get_participant_status(self, comp_data):
        """
        This method returns two lists:
        - ready_to_start: participants who have their 'start' flag set to True
        - not_ready_to_start: participants who have their 'start' flag set to False
        """
      
        if isinstance(comp_data, str):
            comp_data = json.loads(comp_data)

        participants = comp_data.get("participants", {})
        if not isinstance(participants, dict):
            raise ValueError("Invalid data: participants should be a dictionary.")

        ready_to_start = []
        not_ready_to_start = []

        for nickname, data in participants.items():
            # Deserialize participant data if it's a string
            if isinstance(data, str):
                try:
                    data = json.loads(data)
                except json.JSONDecodeError as e:
                    print(f"Error decoding JSON for participant {nickname}: {data}")
                    continue  # Skip this participant if deserialization fails

            # Ensure participant data is a dictionary and check "start" status
            if isinstance(data, dict) and data.get("start"):
                ready_to_start.append(nickname)
            else:
                not_ready_to_start.append(nickname)

        return ready_to_start, not_ready_to_start
