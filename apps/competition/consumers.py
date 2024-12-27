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

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        action = data.get('action')
        nickname = data.get('nickname', '')
        if action == 'join':
            await self.handle_join(nickname)
        elif action == 'leave':
            await self.handle_leave(nickname)
        elif action == 'start':
            await self.channel_layer.group_send(
                self.room_group_name,
                {'type': 'start_competition'}
            )

    async def handle_join(self, nickname):
        if not self.is_valid_nickname(nickname):
            await self.send_error('Invalid nickname format.')
            return

        comp_data = await self.get_comp_data()
        if not comp_data:
            await self.send_error('Competition does not exist or has expired.')
            return

        if comp_data["is_started"]:
            await self.send_error('The competition has already started.')
            return

        if len(comp_data["participants"]) >= comp_data["capacity"]:
            await self.send_error('The competition is at full capacity.')
            return

        if nickname in comp_data["participants"]:
            await self.send_error('This nickname is already taken.')
            return

        # Add participant
        participant_id = len(comp_data["participants"]) + 1
        comp_data["participants"][nickname] = {
            "id": participant_id,
            "start": False,
            "is_solved": False,
            "solved_at": None,
            "time_took": None,
        }
        await self.update_comp_data(comp_data)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'user_joined',
                'nickname': nickname,
                'participants': list(comp_data["participants"].keys())
            }
        )

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

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'user_left',
                'nickname': nickname,
                'participants': list(comp_data["participants"].keys())
            }
        )

    async def user_joined(self, event):
        await self.send(text_data=json.dumps(event))

    async def user_left(self, event):
        await self.send(text_data=json.dumps(event))

    async def start_competition(self, event):
        await self.send(text_data=json.dumps({'type': 'start_competition'}))

    async def validate_comp_uid(self):
        comp_data = cache.get(self.comp_uid)
        return bool(comp_data and not comp_data.get("is_started"))

    async def get_comp_data(self):
        return cache.get(self.comp_uid)

    async def update_comp_data(self, comp_data):
        cache.set(self.comp_uid, comp_data)

    async def send_error(self, message):
        await self.send(text_data=json.dumps({'success': False, 'message': message}))

    def is_valid_nickname(self, nickname):
        return bool(nickname and nickname.isalnum())
