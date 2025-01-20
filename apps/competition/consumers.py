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
        return cache.get(self.comp_uid)

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        action = data.get('action')
        nickname = data.get('nickname', '')
        submission = data.get('submission', '')

        if action and hasattr(self, f"handle_{action}"):
            handler_method = getattr(self, f"handle_{action}")
            if submission:
                await handler_method(nickname, submission)
            else:
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
        await self.close()

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
        

    async def handle_submission_evaluation(self, nickname, submission=""):
        if not nickname:
            await self.send_error("Missing required field: nickname")
            return
        

        comp_data = await self.get_comp_data()
        if not comp_data:
            await self.send_error("Competition does not exist or has expired.")
            return
        
        if nickname not in comp_data.get("participants", {}):
            await self.send_error("Participant not found in this competition.")
            return
        


        
        """
        Processes:
        -----------------
        1. Input Validation:
        - Validate the incoming data for required fields: `comp_uid`, `nickname`, and `code`.
        - If validation fails, send an error message to the client and terminate the process.

        2. Competition Data Retrieval:
        - Fetch the competition data associated with the provided `comp_uid`.
        - If competition data is missing or invalid, notify the client with an error and stop processing.

        3. Participant Validation:
        - Check if the `nickname` exists in the competition's list of participants.
        - If not found, notify the client that the participant is not registered in this competition.

        4. Task Retrieval:
        - Retrieve the associated task using the task title from the competition data.

        5. Code Evaluation:
        - Evaluate the submitted code by running it against all predefined test cases for the task.
        - This includes:
            a. Executing the code in a controlled environment to prevent security risks.
            b. Collecting results for each test case (pass/fail status, execution time, and error messages).

        6. Result Analysis:
        - Determine whether all test cases passed:
            a. If All Passed:
                - Mark the participant as having solved the task.
                - Record the time of solution and the time taken since the competition started.
                - Append the participant's result with a "Solved" status to the competition's results.
                - Prepare a success message for the client.
            b. If Not All Passed:
                - Append the participant's result with a "Failed" status to the competition's results.
                - Prepare a message indicating test cases failed.

        7. Competition Data Update:
        - Update the competition data in the cache to reflect the new submission results.

        8. Send Feedback to Client:
        - Send a real-time response to the WebSocket client containing:
            a. Submission status (success/failure).
            b. Detailed results of the test cases.
            c. An appropriate success or failure message.

        9. Error Handling:
        - Gracefully handle exceptions during processing (invalid data, task retrieval failures).
        - Log errors for debugging and notify the client with a descriptive error message.

        Notes:
        ------
        - Ensure the evaluation environment is secure and isolated to avoid malicious code execution.
        - Maintain consistent data structure for responses to simplify client-side handling.
        - Use asynchronous operations to handle multiple submissions concurrently and efficiently.

        Example Response:
        -----------------
        {
            "type": "submission_result",
            "success": True,
            "message": "All test cases passed! Task solved successfully.",
            "results": [
                {"test_case": 1, "result": "pass"},
                {"test_case": 2, "result": "pass"},
                ...
            ]
        }
        """




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
