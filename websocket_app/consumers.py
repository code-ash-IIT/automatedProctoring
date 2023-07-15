# consumers.py
from channels.generic.websocket import AsyncWebsocketConsumer
# from asgiref.sync import async_to_sync
# from channels.layers import get_channel_layer
import cv2
import dlib

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import numpy as np

class ProctorConsumer(AsyncWebsocketConsumer):
    channel_layer = get_channel_layer()

    async def connect(self):
        # Perform necessary setup tasks
        # ...
        print("Websocket Connected...")
        await self.accept()

    async def disconnect(self, close_code):
        # Perform necessary cleanup tasks
        print("Websocket Disconnected...")
        # pass

    async def receive(self, text_data):
        print("Message Receive from Websocket Connected... {text_data}")
        # Handle incoming WebSocket messages
        if text_data == 'start_verification':
            # Start the face verification process
            await self.start_face_verification()

        elif text_data == 'stop_verification':
            # Stop the face verification process
            await self.stop_face_verification()

    async def start_face_verification(self):
        # Load the face recognition model
        model_path = 'proctoring_project/models/shape_predictor_68_face_landmarks.dat'
        face_rec_model = dlib.face_recognition_model_v1(model_path)

        # Configure video streaming from the student's webcam
        video_capture = cv2.VideoCapture(0)

        # Capture snapshots at specific intervals
        snapshot_interval = 10  # Interval in seconds
        snapshot_count = 0

        while True:
            # Read frame from video stream
            ret, frame = video_capture.read()

            # Perform face verification on captured snapshots
            if snapshot_count % snapshot_interval == 0:
                # Preprocess the image
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = face_rec_model.detector(gray)

                # Check if a face is detected
                if len(faces) > 0:
                    # Get the face landmarks
                    shape = face_rec_model.shape_predictor(gray, faces[0])

                    # Get the face embedding
                    face_descriptor = face_rec_model.compute_face_descriptor(gray, shape)

                    # Compare the face embedding to verify the identity
                    # Implement your logic here for matching the face embedding with authorized face embeddings
                    # You can use distance metrics like Euclidean distance or cosine similarity

                    # Save the captured snapshot
                    snapshot_filename = f'snapshot_{snapshot_count}.jpg'
                    snapshot_path = f'proctoring_project/static/photos/{snapshot_filename}'
                    cv2.imwrite(snapshot_path, frame)
                    # Increment snapshot count
                    snapshot_count += 1

                # Broadcast the video frame to all connected professor clients
                await self.channel_layer.group_send(
                    "professor_group",  # Group name for professor clients
                    {
                        "type": "video_stream",
                        "stream_data": frame.tobytes(),  # Convert the frame to bytes
                    }
                )

            # Display the video stream in the proctor.html template
            # Implement your code to pass the frame or snapshots to the template for rendering

            # Break the loop if 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # Release the video capture and close any open windows
        video_capture.release()
        cv2.destroyAllWindows()

    def stop_face_verification(self):
        # Implement any necessary cleanup tasks
        pass

    @classmethod
    def video_stream(cls, event):
        # Send the video stream to the WebSocket connection
        stream_data = event["stream_data"]
        channel_name = event["channel_name"]

        # Convert the stream data back to a frame
        frame = np.frombuffer(stream_data, dtype=np.uint8).reshape((480, 640, 3))

        # Convert the frame to a JPEG image
        _, jpeg_frame = cv2.imencode('.jpg', frame)

        # Send the JPEG frame to the WebSocket
        async_to_sync(cls.channel_layer.send)(
            channel_name,
            {
                "type": "websocket.send",
                "text": jpeg_frame.tobytes(),
            }
        )




# class ProctorConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         # Perform necessary setup tasks
#         # ...

#         await self.accept()

#     async def disconnect(self, close_code):
#         # Perform necessary cleanup tasks
#         pass

#     async def receive(self, text_data):
#         # Handle incoming WebSocket messages
#         if text_data == 'start_verification':
#             # Start the face verification process
#             self.start_face_verification()

#         elif text_data == 'stop_verification':
#             # Stop the face verification process
#             self.stop_face_verification()

#     def start_face_verification(self):
#         # Load the face recognition model
#         model_path = 'proctoring_project/models/shape_predictor_68_face_landmarks.dat'
#         face_rec_model = dlib.face_recognition_model_v1(model_path)

#         # Configure video streaming from the student's webcam
#         video_capture = cv2.VideoCapture(0)

#         # Capture snapshots at specific intervals
#         snapshot_interval = 10  # Interval in seconds
#         snapshot_count = 0

#         while True:
#             # Read frame from video stream
#             ret, frame = video_capture.read()

#             # Perform face verification on captured snapshots
#             if snapshot_count % snapshot_interval == 0:
#                 # Preprocess the image
#                 gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#                 faces = face_rec_model.detector(gray)

#                 # Check if a face is detected
#                 if len(faces) > 0:
#                     # Get the face landmarks
#                     shape = face_rec_model.shape_predictor(gray, faces[0])

#                     # Get the face embedding
#                     face_descriptor = face_rec_model.compute_face_descriptor(gray, shape)

#                     # Compare the face embedding to verify the identity
#                     # Implement your logic here for matching the face embedding with authorized face embeddings
#                     # You can use distance metrics like Euclidean distance or cosine similarity

#                     # Save the captured snapshot
#                     snapshot_filename = f'snapshot_{snapshot_count}.jpg'
#                     snapshot_path = f'proctoring_project/static/photos/{snapshot_filename}'
#                     cv2.imwrite(snapshot_path, frame)
#                     # Increment snapshot count
#                     snapshot_count += 1

#             # Display the video stream in the proctor.html template
#             # Implement your code to pass the frame or snapshots to the template for rendering

#             # Break the loop if 'q' is pressed
#             if cv2.waitKey(1) & 0xFF == ord('q'):
#                 break

#         # Release the video capture and close any open windows
#         video_capture.release()
#         cv2.destroyAllWindows()

#     def stop_face_verification(self):
#         # Implement any necessary cleanup tasks
#         pass



# from channels.generic.websocket import AsyncWebsocketConsumer

# class VideoConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         # Perform any necessary setup when a WebSocket connection is established
#         # For example, you can authenticate and authorize the user
        
#         # Accept the WebSocket connection
#         await self.accept()

#     async def disconnect(self, close_code):
#         # Perform any necessary cleanup when a WebSocket connection is closed
#         pass

#     async def receive(self, text_data):
#         # Process the received data from the WebSocket connection
#         # This is where you can handle the video stream from the student
        
#         # Broadcast the video stream to all connected professor clients
#         await self.channel_layer.group_send(
#             "professor_group",  # Group name for professor clients
#             {
#                 "type": "video_stream",
#                 "stream_data": text_data  # Replace with the actual video stream data
#             }
#         )

#     async def video_stream(self, event):
#         # Send the video stream to the WebSocket connection
#         await self.send(text_data=event["stream_data"])