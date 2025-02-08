import cv2
import mediapipe as mp
import numpy as np
import math

# Setting up MediaPipe Hands for hand tracking
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.7, min_tracking_confidence=0.7)

# Canvas to draw on - starts as a blank black screen
canvas = np.zeros((720, 1280, 3), dtype=np.uint8)
draw_color = (0, 0, 255)  # Default color is red

# Flags for drawing and erasing
drawing = False
erasing = False
prev_x, prev_y = None, None  # Track the last position of the drawing point
prev_eraser_hover = False  # To avoid toggling the eraser every frame

# Palette colors and positions
palette = [
    (0, 0, 255),     # Red
    (0, 255, 0),     # Green
    (255, 0, 0),     # Blue
    (0, 255, 255),   # Yellow
    (255, 0, 255),   # Magenta
    (255, 255, 0),   # Cyan
    (255, 255, 255)  # White
]
palette_positions = [(50 + i * 100, 50) for i in range(len(palette))]  # Color buttons at the top
eraser_button_pos = (1000, 100)  # Eraser button position

def calculate_distance(x1, y1, x2, y2):
    # Simple function to calculate distance between two points
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

# Set up the camera feed
cap = cv2.VideoCapture(0)
cap.set(3, 1280)  # Set width
cap.set(4, 720)   # Set height

cv2.namedWindow("Hand Tracking") 
cv2.moveWindow("Hand Tracking", 800, 320)

prev_drawing = False  # Keeps track of whether the user was drawing in the last frame

while True:
    success, frame = cap.read()
    if not success:
        break  # Stop if the camera feed fails

    frame = cv2.flip(frame, 1)  # Flip horizontally to make it feel like a mirror
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    # Static UI - Palette and Eraser
    static_ui = np.zeros_like(frame)
    for i, color in enumerate(palette):
        cv2.rectangle(static_ui, (palette_positions[i][0] - 40, palette_positions[i][1] - 40),
                    (palette_positions[i][0] + 40, palette_positions[i][1] + 40), color, -1)

    cv2.rectangle(static_ui, (eraser_button_pos[0] - 120, eraser_button_pos[1] - 60),
                (eraser_button_pos[0] + 80, eraser_button_pos[1] + 40), (0, 0, 0), -1)
    cv2.putText(static_ui, "Erase", (eraser_button_pos[0] - 70, eraser_button_pos[1]),
                cv2.FONT_ITALIC, 1.5, (0, 255, 17), 2)
    frame = cv2.addWeighted(frame, 0.6, static_ui, 1.2, 0)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            h, w, c = frame.shape

            # Get coordinates of important landmarks
            thumb_ip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_IP]  
            index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]  
            index_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP]  
            middle_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_MCP]  
            thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP] 

            thumb_x, thumb_y = int(thumb_ip.x * w), int(thumb_ip.y * h)
            index_x, index_y = int(index_tip.x * w), int(index_tip.y * h)
            index_mcp_x, index_mcp_y = int(index_mcp.x * w), int(index_mcp.y * h)
            middle_mcp_x, middle_mcp_y = int(middle_mcp.x * w), int(middle_mcp.y * h)
            thumb_tip_x, thumb_tip_y = int(thumb_tip.x * w), int(thumb_tip.y * h)

            # Calculate distances between thumb and index/middle finger MCPs
            thumb_index_distance = calculate_distance(thumb_x, thumb_y, index_mcp_x, index_mcp_y)
            thumb_middle_distance = calculate_distance(thumb_x, thumb_y, middle_mcp_x, middle_mcp_y)

            # Determine if we're drawing or erasing based on finger positions
            if thumb_index_distance < 50 or thumb_middle_distance < 50:
                drawing = True
                erasing = False
            else:
                drawing = False

            # Check if index finger is selecting a color
            for i, (x, y) in enumerate(palette_positions):
                if x - 40 < index_x < x + 40 and y - 40 < index_y < y + 40:
                    draw_color = palette[i]
                    break
            
            # Toggle eraser mode when hovering over the eraser button
            current_eraser_hover = eraser_button_pos[0] - 40 < index_x < eraser_button_pos[0] + 40 and eraser_button_pos[1] - 40 < index_y < eraser_button_pos[1] + 40

            if current_eraser_hover and not prev_eraser_hover:
                erasing = not erasing  # Toggle erasing mode
                drawing = not erasing  # Ensure we don't draw and erase simultaneously
                prev_x, prev_y = None, None  # Reset drawing position

            prev_eraser_hover = current_eraser_hover

            # Draw or erase on the canvas
            if drawing:
                if not prev_drawing:
                    prev_x, prev_y = None, None
                if 100 < index_x < 1180 and 100 < index_y < 620:  # Ensure within drawing boundaries
                    if prev_x is not None and prev_y is not None:
                        distance = calculate_distance(prev_x, prev_y, index_x, index_y)
                        if distance < 45:
                            cv2.line(canvas, (prev_x, prev_y), (index_x, index_y), draw_color, 5)
                        else:
                            prev_x, prev_y = None, None
                    prev_x, prev_y = index_x, index_y
                else:
                    prev_x, prev_y = None, None
                prev_drawing = True
            elif erasing:
                if 100 < index_x < 1180 and 100 < index_y < 620:
                    cv2.circle(frame, (index_x, index_y), 30, (0, 0, 255), 2)  # Visualize the eraser
                    cv2.circle(canvas, (index_x, index_y), 30, (0, 0, 0), -1)  # Erase on the canvas
                prev_x, prev_y = None, None
                prev_drawing = False  
            else:
                prev_drawing = False
                prev_x, prev_y = None, None

    # Smooth the canvas by gaussian blur
    if drawing or erasing:
        smooth_canvas = cv2.GaussianBlur(canvas, (3, 3), 0)
    else:
        smooth_canvas = canvas

    # Add a boundary and label for drawing area
    cv2.rectangle(smooth_canvas, (100, 100), (1180, 620), (0, 255, 0), 2)
    cv2.putText(smooth_canvas, "Draw or Erase", (105, 90),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # showing the frames
    cv2.imshow("Virtual Canvas", smooth_canvas)
    frame_skeleton = cv2.resize(frame, (450, 300))  # resizing hand tracking window
    cv2.imshow("Hand Tracking", frame_skeleton)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):  # Quit on pressing 'q' on keyboard
        break
    elif key == ord('c'):  # Clear canvas on pressing 'c'
        canvas.fill(0)

cap.release()
cv2.destroyAllWindows()
