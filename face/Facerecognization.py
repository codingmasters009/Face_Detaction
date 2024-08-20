from flask import Flask, Response, request, jsonify  
from flask_cors import CORS  
import face_recognition  
import cv2  
import os  

app = Flask(__name__)  
CORS(app)  

# Path to the image folder in your React project  
image_folder = r"C:/Users/Muhammad Abdullah/OneDrive/Documents/Face_Detaction/face/client/src/images"  

if not os.path.exists(image_folder):  
    raise FileNotFoundError(f"Directory not found: {image_folder}")  

# Load known face encodings and names  
known_face_encodings = []  
known_face_names = []  

# Assuming each image filename corresponds to user data or some other info.  
user_data = {}  

for filename in os.listdir(image_folder):  
    image_path = os.path.join(image_folder, filename)  
    if filename.endswith(".jpg") or filename.endswith(".png"):  
        image = face_recognition.load_image_file(image_path)  
        encodings = face_recognition.face_encodings(image)  
        if encodings:  # Make sure there is at least one encoding found  
            known_face_encodings.append(encodings[0])  
            known_face_names.append(filename)  
            user_data[filename] = {  
                "filename": filename,  
                "description": "Some description related to the user",  # Replace with actual user data  
                "additional_info": "Other relevant information"  # Additional user details can go here  
            }  

def generate_frames():  
    cap = cv2.VideoCapture(0)  
    if not cap.isOpened():  
        print("Error: Could not open video capture.")  
        return  

    while True:  
        success, frame = cap.read()  
        if not success:  
            print("Failed to grab frame.")  
            break  

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  
        face_locations = face_recognition.face_locations(rgb_frame)  
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)  

        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):  
            distances = face_recognition.face_distance(known_face_encodings, face_encoding)  
            min_distance_index = distances.argmin()  
            min_distance = distances[min_distance_index]  

            if min_distance < 0.6:  
                name = known_face_names[min_distance_index]  
                match_percentage = (1 - min_distance) * 100  
                name_with_percentage = f"{name} ({match_percentage:.2f}%)"   
            else:  
                name_with_percentage = "Unknown"  

            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)  
            cv2.putText(frame, name_with_percentage, (left + 6, bottom - 6), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)  

        # Encode the frame in JPEG format for streaming  
        ret, buffer = cv2.imencode('.jpg', frame)  
        if not ret:  
            print("Failed to encode frame.")  
            continue  

        frame = buffer.tobytes()  
        yield (b'--frame\r\n'  
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  

@app.route('/webcam')  
def webcam_feed():  
    return Response(generate_frames(),  
                    mimetype='multipart/x-mixed-replace; boundary=frame')  

@app.route('/api/user/<string:filename>', methods=['GET'])  
def get_user_data(filename):  
    # Fetch user data based on the image filename  
    if filename in user_data:  
        return jsonify(user_data[filename]), 200  
    else:  
        return jsonify({"error": "User not found"}), 404  

if __name__ == "__main__":  
    app.run(host='0.0.0.0', port=5001)