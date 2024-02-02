import cv2
from keras.models import model_from_json
import numpy as np
from twilio.rest import Client
import random
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
import warnings


class AccidentDetectionModel:
    class_nums = ['Accident', 'No Accident']

    def __init__(self, model_json_file, model_weights_file):
        try:
            with open(model_json_file, 'r') as json_file:
                loaded_model_json = json_file.read()
                self.loaded_model = model_from_json(loaded_model_json)

            self.loaded_model.load_weights(model_weights_file)
        except Exception as e:
            raise RuntimeError(f"Error loading model: {e}")

    def predict_accident(self, img):
        try:
            self.preds = self.loaded_model.predict(img)
            return AccidentDetectionModel.class_nums[np.argmax(self.preds)], self.preds
        except Exception as e:
            raise RuntimeError(f"Error predicting accident: {e}")

def generate_location():
    latitude_ranges = [(8.4, 15.0), (20.0, 25.0), (30.0, 37.6)]
    longitude_ranges = [(68.7, 75.0), (80.0, 85.0), (90.0, 97.25)]

    max_attempts = 5

    for _ in range(max_attempts):
        try:
            geolocator = Nominatim(user_agent="accident_detection_app")

            latitude_range = random.choice(latitude_ranges)
            longitude_range = random.choice(longitude_ranges)

            latitude = round(random.uniform(*latitude_range), 6)
            longitude = round(random.uniform(*longitude_range), 6)

            print(f"Random Location: Latitude {latitude}, Longitude {longitude}")

            location = geolocator.reverse((latitude, longitude), language='en', timeout=10)

            if location and 'address' in location.raw:
                place_name = location.address
                print(f"Place Name: {place_name}")

                return latitude, longitude, place_name

        except (AttributeError, GeocoderTimedOut) as e:
            print(f"Error generating random location: {e}")

    print("Error: Unable to determine the accident location after multiple attempts.")
    return None, None, None

def send_sms_twilio():
    account_sid = 'AC73e32b2265b51c773bd5c1bc945f998b'
    auth_token = '294234ca45c3fbc5d9b942add77a32e5'

    from_number = '+16592186007'
    to_number = '+916382150416'

    client = Client(account_sid, auth_token)

    accident_latitude, accident_longitude, place_name = generate_location()

    if accident_latitude is not None and accident_longitude is not None and place_name is not None:
        message_body = f"ACCIDENT DETECTED\nLocation: {place_name}, Latitude {accident_latitude}, Longitude {accident_longitude}"

        message = client.messages.create(
            body=message_body,
            from_=from_number,
            to=to_number
        )

        print(f"SMS sent: {message.sid}")
        return place_name, accident_latitude, accident_longitude

    else:
        print("Error: Unable to determine the accident location.")
        return None, None, None


def start_application():
    sms_sent = False  
    video = None  
    location_info = None
    try:
        model = AccidentDetectionModel("model.json", 'model_weights.h5')
        font = cv2.FONT_HERSHEY_SIMPLEX

        video_path = 'C:\\Users\\ukjag\\Downloads\\head_on_collision_101.mp4'
        video = cv2.VideoCapture(video_path)

        if not video.isOpened():
            print(f"Error: Couldn't open the video source. Check the file path: {video_path}")
            raise RuntimeError("Couldn't open the video source.")

        while True:
            ret, frame = video.read()

            if not ret:
                break

            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            roi = cv2.resize(gray_frame, (250, 250))

            pred, prob = model.predict_accident(roi[np.newaxis, :, :])
            prob_percentage = round(prob[0][0] * 100, 2)

            cv2.putText(frame, f"Prediction: {pred} - Probability: {prob_percentage}%", (10, 30), font, 0.7, (255, 0, 0), 2)

            if pred == "Accident" and not sms_sent:
                cv2.rectangle(frame, (0, 0), (280, 40), (0, 0, 0), -1)
                cv2.putText(frame, f"{pred} {prob_percentage}%", (20, 30), font, 1, (255, 0, 0), 2)  


                location_info = send_sms_twilio()
                if location_info is not None:
                    sms_sent = True  

            cv2.imshow('Video', cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))

            if cv2.waitKey(33) & 0xFF == ord('q'):
                break

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        if video is not None:
            video.release()
        cv2.destroyAllWindows()

    if location_info is not None:
        place_name, accident_latitude, accident_longitude = location_info
        print(f"Accident detected near {place_name}, Latitude: {accident_latitude}, Longitude: {accident_longitude}.")
    else:
        print("No accident detected.")
if __name__ == '__main__':
    start_application()
