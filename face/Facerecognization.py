from deepface import DeepFace
from flask import Flask, Response, request, jsonify  
from flask_cors import CORS  
import cv2  
import os  
import requests
import time

app = Flask(__name__)  
CORS(app)

image_folder = r"C:/Users/mabdu/OneDrive/Documents/Face-Detection/face/client/src/images"  

if not os.path.exists(image_folder):  
    raise FileNotFoundError(f"Directory not found: {image_folder}")  

known_face_encodings = []  
known_face_names = []  
user_data = {}  

# Process the known images and compute embeddings using DeepFace
for filename in os.listdir(image_folder):  
    image_path = os.path.join(image_folder, filename)  
    if filename.endswith(".jpg") or filename.endswith(".png"):  
        try:
            # Use DeepFace to find embeddings
            result = DeepFace.represent(image_path, model_name="VGG-Face", enforce_detection=False)
            known_face_encodings.append(result[0]['embedding'])
            known_face_names.append(filename)
            user_data[filename] = {  
                "filename": filename,  
                "description": "Some description related to the user",  
                "additional_info": "Other relevant information"  
            }
        except Exception as e:
            print(f"Error processing {filename}: {e}")

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

        # Process frame with DeepFace
        try:
            # Convert frame to RGB for DeepFace processing
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            result = DeepFace.find(rgb_frame, db_path=image_folder, model_name="VGG-Face", enforce_detection=False)
            
            # Initialize default values for bounding box and name
            left = top = right = bottom = 0  # Default values if no face is detected
            name_with_percentage = "Unknown"  # Default name

            if len(result) > 0:
                # Assuming we are using the first match (you can customize this logic)
                matched_name = result[0]['identity'][0].split("\\")[-1]
                min_distance = result[0]['distance'][0]
                
                if min_distance < 0.6:
                    name_with_percentage = f"{matched_name} ({(1 - min_distance) * 100:.2f}%)"
                    
                    # Debug: Check if the name is set correctly
                    print(f"Identified: {name_with_percentage}")
                    
                    # Send request to fetch user info
                    response = requests.get(f"http://localhost:3001/api/user/{matched_name}")
                    if response.status_code == 200:
                        user_info = response.json()
                        # Debug: Check the user information
                        print("User Data:", user_info)
                    else:
                        print("User not found")
                
                # Assuming the results include a bounding box (you can modify based on result structure)
                # If no bounding box provided by DeepFace, we can detect it using OpenCV
                if 'region' in result[0]:
                    # Extract face bounding box coordinates from DeepFace result
                    face_region = result[0]['region']
                    left, top, width, height = face_region['x'], face_region['y'], face_region['w'], face_region['h']
                    right, bottom = left + width, top + height

                    # Adjust the frame to fit the detected face
                    face_frame = frame[top:bottom, left:right]

                    # Resize the cropped face frame to a fixed size (if required)
                    resized_face_frame = cv2.resize(face_frame, (640, 480))  # Example resizing to fit the display
                    frame = resized_face_frame
                else:
                    name_with_percentage = "Unknown"  
            
                # Draw rectangle and label on the original frame (for debugging)
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)  
                cv2.putText(frame, name_with_percentage, (left + 6, bottom - 6), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)  
            else:
                name_with_percentage = "Unknown"
                # Optionally, use face detection methods from OpenCV to find bounding boxes
                # Example (if you want to detect faces with OpenCV itself):
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
                faces = face_cascade.detectMultiScale(gray, 1.1, 4)
                for (x, y, w, h) in faces:
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    cv2.putText(frame, "Face Detected", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

        except Exception as e:
            print(f"Error during frame processing: {e}")
        
        # Ensure the frame is correctly encoded and ready to be displayed
        ret, buffer = cv2.imencode('.jpg', frame)  
        if not ret:  
            print("Failed to encode frame.")  
            continue  

        frame_bytes = buffer.tobytes()  

        # Yield the frame as part of a response stream (Flask or similar)
        yield (b'--frame\r\n'  
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')  

        # Optionally display the frame locally for debugging
        cv2.imshow("Frame", frame)  # Show the processed frame in a window

        # Exit the loop if the user presses 'q' (for testing purposes)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        time.sleep(0.03)

    cap.release()
    cv2.destroyAllWindows()

    cap = cv2.VideoCapture(0)  
    if not cap.isOpened():  
        print("Error: Could not open video capture.")  
        return  

    while True:  
        success, frame = cap.read()  
        if not success:  
            print("Failed to grab frame.")  
            break  

        # Process frame with DeepFace
        try:
            # Convert frame to RGB for DeepFace processing
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            result = DeepFace.find(rgb_frame, db_path=image_folder, model_name="VGG-Face", enforce_detection=False)
            
            # Initialize default values for bounding box and name
            left = top = right = bottom = 0  # Default values if no face is detected
            name_with_percentage = "Unknown"  # Default name

            if len(result) > 0:
                # Assuming we are using the first match (you can customize this logic)
                matched_name = result[0]['identity'][0].split("\\")[-1]
                min_distance = result[0]['distance'][0]
                
                if min_distance < 0.6:
                    name_with_percentage = f"{matched_name} ({(1 - min_distance) * 100:.2f}%)"
                    
                    # Debug: Check if the name is set correctly
                    print(f"Identified: {name_with_percentage}")
                    
                    # Send request to fetch user info
                    response = requests.get(f"http://localhost:3001/api/user/{matched_name}")
                    if response.status_code == 200:
                        user_info = response.json()
                        # Debug: Check the user information
                        print("User Data:", user_info)
                    else:
                        print("User not found")
                
                # Assuming the results include a bounding box (you can modify based on result structure)
                # If no bounding box provided by DeepFace, we can detect it using OpenCV
                if 'region' in result[0]:
                    # Extract face bounding box coordinates from DeepFace result
                    face_region = result[0]['region']
                    left, top, width, height = face_region['x'], face_region['y'], face_region['w'], face_region['h']
                    right, bottom = left + width, top + height

                    # Adjust the frame to fit the detected face
                    face_frame = frame[top:bottom, left:right]

                    # Resize the cropped face frame to a fixed size (if required)
                    resized_face_frame = cv2.resize(face_frame, (640, 480))  # Example resizing to fit the display
                    frame = resized_face_frame
                else:
                    name_with_percentage = "Unknown"  
            
                # Draw rectangle and label on the original frame (for debugging)
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)  
                cv2.putText(frame, name_with_percentage, (left + 6, bottom - 6), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)  
            else:
                name_with_percentage = "Unknown"
                # Optionally, use face detection methods from OpenCV to find bounding boxes
                # Example (if you want to detect faces with OpenCV itself):
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
                faces = face_cascade.detectMultiScale(gray, 1.1, 4)
                for (x, y, w, h) in faces:
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    cv2.putText(frame, "Face Detected", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

        except Exception as e:
            print(f"Error during frame processing: {e}")
        
        # Ensure the frame is correctly encoded and ready to be displayed
        ret, buffer = cv2.imencode('.jpg', frame)  
        if not ret:  
            print("Failed to encode frame.")  
            continue  

        frame_bytes = buffer.tobytes()  

        # Yield the frame as part of a response stream (Flask or similar)
        yield (b'--frame\r\n'  
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')  

        # Optionally display the frame locally for debugging
        cv2.imshow("Frame", frame)  # Show the processed frame in a window

        # Exit the loop if the user presses 'q' (for testing purposes)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        time.sleep(0.03)

    cap.release()
    cv2.destroyAllWindows()

    cap = cv2.VideoCapture(0)  
    if not cap.isOpened():  
        print("Error: Could not open video capture.")  
        return  

    while True:  
        success, frame = cap.read()  
        if not success:  
            print("Failed to grab frame.")  
            break  

        # Process frame with DeepFace
        try:
            # Convert frame to RGB for DeepFace processing
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            result = DeepFace.find(rgb_frame, db_path=image_folder, model_name="VGG-Face", enforce_detection=False)
            
            # Initialize default values for bounding box and name
            left = top = right = bottom = 0  # Default values if no face is detected
            name_with_percentage = "Unknown"  # Default name

            if len(result) > 0:
                # Assuming we are using the first match (you can customize this logic)
                matched_name = result[0]['identity'][0].split("\\")[-1]
                min_distance = result[0]['distance'][0]
                
                if min_distance < 0.6:
                    name_with_percentage = f"{matched_name} ({(1 - min_distance) * 100:.2f}%)"
                    
                    # Debug: Check if the name is set correctly
                    print(f"Identified: {name_with_percentage}")
                    
                    # Send request to fetch user info
                    response = requests.get(f"http://localhost:3001/api/user/{matched_name}")
                    if response.status_code == 200:
                        user_info = response.json()
                        # Debug: Check the user information
                        print("User Data:", user_info)
                    else:
                        print("User not found")
                
                # Assuming the results include a bounding box (you can modify based on result structure)
                # If no bounding box provided by DeepFace, we can detect it using OpenCV
                if 'region' in result[0]:
                    # Extract face bounding box coordinates from DeepFace result
                    face_region = result[0]['region']
                    left, top, width, height = face_region['x'], face_region['y'], face_region['w'], face_region['h']
                    right, bottom = left + width, top + height

                    # Adjust the frame to fit the detected face
                    face_frame = frame[top:bottom, left:right]

                    # Resize the cropped face frame to a fixed size (if required)
                    resized_face_frame = cv2.resize(face_frame, (640, 480))  # Example resizing to fit the display
                    frame = resized_face_frame
                else:
                    name_with_percentage = "Unknown"  
            
                # Draw rectangle and label on the original frame (for debugging)
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)  
                cv2.putText(frame, name_with_percentage, (left + 6, bottom - 6), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)  
            else:
                name_with_percentage = "Unknown"
                # Optionally, use face detection methods from OpenCV to find bounding boxes
                # Example (if you want to detect faces with OpenCV itself):
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
                faces = face_cascade.detectMultiScale(gray, 1.1, 4)
                for (x, y, w, h) in faces:
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    cv2.putText(frame, "Face Detected", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

        except Exception as e:
            print(f"Error during frame processing: {e}")
        
        # Show the updated frame
        ret, buffer = cv2.imencode('.jpg', frame)  
        if not ret:  
            print("Failed to encode frame.")  
            continue  

        frame = buffer.tobytes()  
        yield (b'--frame\r\n'  
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  
        time.sleep(0.03)

    cap = cv2.VideoCapture(0)  
    if not cap.isOpened():  
        print("Error: Could not open video capture.")  
        return  

    while True:  
        success, frame = cap.read()  
        if not success:  
            print("Failed to grab frame.")  
            break  

        # Process frame with DeepFace
        try:
            # DeepFace needs the image to be in RGB format
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            result = DeepFace.find(rgb_frame, db_path=image_folder, model_name="VGG-Face", enforce_detection=False)
            
            # Initialize bounding box variables
            left = top = right = bottom = 0  # Default values if no face is detected
            name_with_percentage = "Unknown"  # Default name

            # Check if any matches were found
            if len(result) > 0:
                # Assuming we are using the first match (you can customize this logic)
                matched_name = result[0]['identity'][0].split("\\")[-1]
                min_distance = result[0]['distance'][0]
                
                if min_distance < 0.6:
                    name_with_percentage = f"{matched_name} ({(1 - min_distance) * 100:.2f}%)"
                    
                    # Debug: Check if the name is set correctly
                    print(f"Identified: {name_with_percentage}")
                    
                    # Send request to fetch user info
                    response = requests.get(f"http://localhost:3001/api/user/{matched_name}")
                    if response.status_code == 200:
                        user_info = response.json()
                        # Debug: Check the user information
                        print("User Data:", user_info)
                    else:
                        print("User not found")
                else:
                    name_with_percentage = "Unknown"  
            
                # Assuming the results include a bounding box (you can modify based on result structure)
                # Mock example for setting bounding box coordinates (if no bounding box returned by DeepFace):
                left, top, right, bottom = 100, 100, 300, 300  # Set to actual values from the result
                
                # Draw rectangle and label on the frame
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)  
                cv2.putText(frame, name_with_percentage, (left + 6, bottom - 6), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)  
            else:
                name_with_percentage = "Unknown"
                # Optionally, use face detection methods from OpenCV to find bounding boxes
                # Example (if you want to detect faces with OpenCV itself):
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
                faces = face_cascade.detectMultiScale(gray, 1.1, 4)
                for (x, y, w, h) in faces:
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    cv2.putText(frame, "Face Detected", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

        except Exception as e:
            print(f"Error during frame processing: {e}")
        
        # Show the updated frame
        ret, buffer = cv2.imencode('.jpg', frame)  
        if not ret:  
            print("Failed to encode frame.")  
            continue  

        frame = buffer.tobytes()  
        yield (b'--frame\r\n'  
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  
        time.sleep(0.03)

    cap = cv2.VideoCapture(0)  
    if not cap.isOpened():  
        print("Error: Could not open video capture.")  
        return  

    while True:  
        success, frame = cap.read()  
        if not success:  
            print("Failed to grab frame.")  
            break  

        # Process frame with DeepFace
        try:
            # DeepFace needs the image to be in RGB format
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            result = DeepFace.find(rgb_frame, db_path=image_folder, model_name="VGG-Face", enforce_detection=False)
            
            # Initialize bounding box variables
            left = top = right = bottom = 0  # Default values if no face is detected
            
            # Check if any matches were found
            if len(result) > 0:
                # Assuming we are using the first match (you can customize this logic)
                matched_name = result[0]['identity'][0].split("\\")[-1]
                min_distance = result[0]['distance'][0]
                
                if min_distance < 0.6:
                    name_with_percentage = f"{matched_name} ({(1 - min_distance) * 100:.2f}%)"
                    
                    # Send request to fetch user info
                    response = requests.get(f"http://localhost:3001/api/user/{matched_name}")
                    if response.status_code == 200:
                        user_info = response.json()
                        print("User Data:", user_info) 
                    else:
                        print("User not found")
                else:
                    name_with_percentage = "Unknown"  

                # Assuming the results include a bounding box (you can modify based on result structure)
                # Note: If DeepFace doesn't return bounding boxes, you can use cv2's face detection methods
                # for bounding boxes. Here's a mock example for setting bounding box coordinates:
                left, top, right, bottom = 100, 100, 300, 300  # Set to actual values from the result
                
                # Draw rectangle and label on the frame
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)  
                cv2.putText(frame, name_with_percentage, (left + 6, bottom - 6), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)  
            else:
                name_with_percentage = "Unknown"
                # Optionally, use face detection methods from OpenCV to find bounding boxes
                # Example (if you want to detect faces with OpenCV itself):
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
                faces = face_cascade.detectMultiScale(gray, 1.1, 4)
                for (x, y, w, h) in faces:
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        except Exception as e:
            print(f"Error during frame processing: {e}")
        
        ret, buffer = cv2.imencode('.jpg', frame)  
        if not ret:  
            print("Failed to encode frame.")  
            continue  

        frame = buffer.tobytes()  
        yield (b'--frame\r\n'  
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  
        time.sleep(0.03)

    cap = cv2.VideoCapture(0)  
    if not cap.isOpened():  
        print("Error: Could not open video capture.")  
        return  

    while True:  
        success, frame = cap.read()  
        if not success:  
            print("Failed to grab frame.")  
            break  

        # Process frame with DeepFace
        try:
            # DeepFace needs the image to be in RGB format
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            result = DeepFace.find(rgb_frame, db_path=image_folder, model_name="VGG-Face", enforce_detection=False)
            
            # Check if any matches were found
            if len(result) > 0:
                # Assuming we are using the first match (you can customize this logic)
                matched_name = result[0]['identity'][0].split("\\")[-1]
                min_distance = result[0]['distance'][0]
                
                if min_distance < 0.6:
                    name_with_percentage = f"{matched_name} ({(1 - min_distance) * 100:.2f}%)"
                    
                    # Send request to fetch user info
                    response = requests.get(f"http://localhost:3001/api/user/{matched_name}")
                    if response.status_code == 200:
                        user_info = response.json()
                        print("User Data:", user_info) 
                    else:
                        print("User not found")
                else:
                    name_with_percentage = "Unknown"  

                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)  
                cv2.putText(frame, name_with_percentage, (left + 6, bottom - 6), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)  
            else:
                name_with_percentage = "Unknown"

        except Exception as e:
            print(f"Error during frame processing: {e}")
        
        ret, buffer = cv2.imencode('.jpg', frame)  
        if not ret:  
            print("Failed to encode frame.")  
            continue  

        frame = buffer.tobytes()  
        yield (b'--frame\r\n'  
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  
        time.sleep(0.03)

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

if __name__ == "__main__":  
    app.run(host='0.0.0.0', port=5001)
