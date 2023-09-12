import cv2
import mediapipe as mp

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

# Initialize OpenCV
cap = cv2.VideoCapture(0)

# Define a dictionary of gestures and their corresponding actions
GESTURE_MAPPING = {
    "thumbs_up": "Thumbs Up!",
    "peace": "Peace Sign!",
    "point": "Point!",
    # Define more gestures and actions here
}

# Create a variable to track the currently detected gesture
current_gesture = None

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        continue

    # Convert the BGR image to RGB
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the frame with MediaPipe Hands
    results = hands.process(frame_rgb)

    def condition_for_thumbs_up(hand_landmarks):
        # Ensure that hand landmarks are available
        if hand_landmarks is not None:
            # Define conditions for the "thumbs_up" gesture
            thumb_tip = hand_landmarks.landmark[4]  # Thumb tip landmark
            index_tip = hand_landmarks.landmark[8]  # Index finger tip landmark
            middle_tip = hand_landmarks.landmark[12]  # Middle finger tip landmark

            # Calculate the distance between the thumb tip and the index finger tip
            distance = ((thumb_tip.x - index_tip.x)**2 + (thumb_tip.y - index_tip.y)**2)**0.5

            # Check if the thumb tip is above and to the right of the index finger tip
            if thumb_tip.y < index_tip.y and thumb_tip.x > index_tip.x and distance < 0.05:
                return True  # Thumbs up gesture is detected

        return False  # Thumbs up gesture is not detected

    def condition_for_peace_sign(hand_landmarks):
        # Ensure that hand landmarks are available
        if hand_landmarks is not None:
            # Define conditions for the "peace sign" gesture
            index_tip = hand_landmarks.landmark[8]  # Index finger tip landmark
            middle_tip = hand_landmarks.landmark[12]  # Middle finger tip landmark
            ring_tip = hand_landmarks.landmark[16]  # Ring finger tip landmark

            # Calculate the distance between index finger tip and middle finger tip
            index_middle_distance = ((index_tip.x - middle_tip.x)**2 + (index_tip.y - middle_tip.y)**2)**0.5

            # Calculate the distance between middle finger tip and ring finger tip
            middle_ring_distance = ((middle_tip.x - ring_tip.x)**2 + (middle_tip.y - ring_tip.y)**2)**0.5

            # Check if the distances between fingers are within a certain range
            if 0.03 < index_middle_distance < 0.1 and 0.03 < middle_ring_distance < 0.1:
                return True  # Peace sign gesture is detected

        return False  # Peace sign gesture is not detected
    
    def condition_for_point(hand_landmark):
        if hand_landmark is not None:
            index_tip = hand_landmark.landmark[8]
            thumb_tip = hand_landmark.landmark[4]
            thumb_mcp = hand_landmark.landmark[2]
            
            index_thumb_tip_dist = (index_tip.x - thumb_mcp.x)
            thumb_dist = (thumb_tip.x - thumb_mcp.x)
            tt_dist = ((index_tip.x - thumb_tip.x)**2 + (index_tip.y - thumb_tip.y)**2)**0.5
            hypo = (index_thumb_tip_dist**2 + thumb_dist**2)**0.5

            if abs(tt_dist - hypo) < 0.1 and abs(index_tip.x - thumb_mcp.x) < 0.05:
                return True
            
        return False

        


    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Define conditions for gesture recognition
            if condition_for_thumbs_up(hand_landmarks):
                current_gesture = "thumbs_up"
            elif condition_for_peace_sign(hand_landmarks):
                current_gesture = "peace"
            # Define conditions for more gestures here
            elif condition_for_point(hand_landmarks):
                current_gesture = "point"

            # Draw landmarks on the image
            mp_drawing = mp.solutions.drawing_utils
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    # Display the detected gesture and associated action
    if current_gesture:
        action_message = GESTURE_MAPPING.get(current_gesture, "Unknown Gesture")
        cv2.putText(frame, action_message, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow('Hand Gesture Recognition', frame)

    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
