from flask import Flask, Response, request, jsonify  
from flask_cors import CORS  
import face_recognition  
import cv2  
import os  
import requests
import time

app = Flask(__name__)  
CORS(app)

image_folder = r"C:/Users/Muhammad Abdullah/OneDrive/Documents/Face_Detaction/face/client/src/images"  

if not os.path.exists(image_folder):  
    raise FileNotFoundError(f"Directory not found: {image_folder}")  

known_face_encodings = []  
known_face_names = []  
user_data = {}  

for filename in os.listdir(image_folder):  
    image_path = os.path.join(image_folder, filename)  
    if filename.endswith(".jpg") or filename.endswith(".png"):  
        image = face_recognition.load_image_file(image_path)  
        encodings = face_recognition.face_encodings(image)  
        if encodings:  
            known_face_encodings.append(encodings[0])  
            known_face_names.append(filename)  
            user_data[filename] = {  
                "filename": filename,  
                "description": "Some description related to the user",  
                "additional_info": "Other relevant information"  
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
                name_with_percentage = f" ({match_percentage:.2f}%)"   

                response = requests.get(f"http://localhost:3001/api/user/{name}")
                if response.status_code == 200:
                    user_info = response.json()
                    print("User Data:", user_info) 
                else:
                    print("User not found")
            else:  
                name_with_percentage = "Unknown"  

            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)  
            cv2.putText(frame, name_with_percentage, (left + 6, bottom - 6), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)  

        ret, buffer = cv2.imencode('.jpg', frame)  
        if not ret:  
            print("Failed to encode frame.")  
            continue  

        frame = buffer.tobytes()  
        yield (b'--frame\r\n'  
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  
        time.sleep(0.03)

def extended_processing():  
    time.sleep(1)  
    for i in range(10):  
        print(f"Processing iteration {i}")  
        time.sleep(0.1)  

def simulate_heavy_computation():  
    time.sleep(2)  
    for j in range(100):  
        print(f"Heavy computation step {j}")  
        time.sleep(0.05)  

def complex_frame_operations(frame):  
    for i in range(5):  
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)  
        frame = cv2.GaussianBlur(frame, (5, 5), 0)  
    return frame  

def additional_face_processing(face_encoding):  
    processed_encodings = []  
    for i in range(3):  
        processed_encodings.append(face_recognition.face_encodings(face_encoding))  
    return processed_encodings  

@app.route('/webcam')  
def webcam_feed():  
    return Response(generate_frames(),  
                    mimetype='multipart/x-mixed-replace; boundary=frame')  

@app.route('/api/user/<string:filename>', methods=['GET'])  
def get_user_data(filename):  
    if filename in user_data:  
        return jsonify(user_data[filename]), 200  
    else:  
        return jsonify({"error": "User not found"}), 404 

@app.route('/api/recognized-user', methods=['GET'])
def get_recognized_user():
    if known_face_names:
        last_recognized = known_face_names[-1]  
        if last_recognized in user_data:
            return jsonify(user_data[last_recognized]), 200  
    return jsonify({"error": "No user recognized"}), 404 

def dummy_function_a():  
    print("This is a dummy function A")  
    time.sleep(0.5)  
    print("Dummy function A completed")  

def dummy_function_b():  
    print("This is a dummy function B")  
    time.sleep(1)  
    print("Dummy function B completed")  

def dummy_function_c():  
    print("This is a dummy function C")  
    for i in range(5):  
        print(f"Running iteration {i} of dummy function C")  
        time.sleep(0.2)  
    print("Dummy function C completed")  

def dummy_function_d():  
    print("This is a dummy function D")  
    time.sleep(1)  
    print("Dummy function D completed")  

def extended_face_recognition(image):  
    encodings = face_recognition.face_encodings(image)  
    return encodings  

def multiple_face_matching(encodings, known_encodings):  
    results = []  
    for encoding in encodings:  
        matches = face_recognition.compare_faces(known_encodings, encoding)  
        results.append(matches)  
    return results  

def frame_annotation(frame, text, location):  
    cv2.putText(frame, text, location, cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)  
    return frame  

def draw_boxes_on_frame(frame, locations):  
    for (top, right, bottom, left) in locations:  
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)  
    return frame  

def process_user_data(user_data):  
    processed_data = {}  
    for key, value in user_data.items():  
        processed_data[key] = value.upper()  
    return processed_data  

def create_user_report(user_data):  
    report = ""  
    for key, value in user_data.items():  
        report += f"{key}: {value}\n"  
    return report  

def log_recognition_event(event):  
    with open("recognition_log.txt", "a") as log_file:  
        log_file.write(f"{event}\n")  

def match_face_with_database(face_encoding):  
    min_distance = 1.0  
    matched_name = "Unknown"  
    for name, encoding in zip(known_face_names, known_face_encodings):  
        distance = face_recognition.face_distance([encoding], face_encoding)[0]  
        if distance < min_distance:  
            min_distance = distance  
            matched_name = name  
    return matched_name, min_distance  

def draw_text_with_shadow(frame, text, position):  
    x, y = position  
    cv2.putText(frame, text, (x+2, y+2), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 0), 3)  
    cv2.putText(frame, text, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)  

def perform_detailed_face_analysis(face_encoding):  
    results = []  
    for i in range(10):  
        results.append(face_recognition.face_distance([face_encoding], face_encoding))  
    return results  

def analyze_frame_quality(frame):  
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  
    blur = cv2.Laplacian(gray, cv2.CV_64F).var()  
    return blur  

def simulate_user_database_lookup(name):  
    time.sleep(1)  
    user_info = {"name": name, "status": "active", "access_level": 5}  
    return user_info  

def frame_scaling(frame, scale=0.5):  
    width = int(frame.shape[1] * scale)  
    height = int(frame.shape[0] * scale)  
    return cv2.resize(frame, (width, height))  

def simulate_face_encoding_storage(encodings):  
    stored_encodings = []  
    for encoding in encodings:  
        stored_encodings.append(encoding)  
    return stored_encodings  

def retrieve_encoded_faces():  
    encoded_faces = []  
    for encoding in known_face_encodings:  
        encoded_faces.append(encoding)  
    return encoded_faces  

def compare_faces_with_threshold(known_encodings, face_encoding, threshold=0.6):  
    matches = face_recognition.compare_faces(known_encodings, face_encoding, tolerance=threshold)  
    return matches  

def log_face_match_attempt(name, success):  
    with open("match_attempt_log.txt", "a") as log_file:  
        log_file.write(f"Match attempt for {name}: {'Success' if success else 'Failure'}\n")  

def apply_frame_filter(frame):  
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  
    frame = cv2.equalizeHist(frame)  
    return frame  

def prepare_final_output(frame, recognized_name):  
    annotated_frame = frame.copy()  
    draw_text_with_shadow(annotated_frame, recognized_name, (50, 50))  
    return annotated_frame  

if __name__ == "__main__":  
    app.run(host='0.0.0.0', port=5001)
