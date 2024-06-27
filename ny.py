import cv2
import numpy as np
import mediapipe as mp
from collections import deque

# Giving different arrays to handle colour points of different colours
bpoints = [deque(maxlen=1024)]
gpoints = [deque(maxlen=1024)]
rpoints = [deque(maxlen=1024)]
ypoints = [deque(maxlen=1024)]

# These indexes will be used to mark the points in particular arrays of specific colour
blue_index = 0
green_index = 0
red_index = 0
yellow_index = 0

# The kernel to be used for dilation purpose
kernel = np.ones((5, 5), np.uint8)

colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (0, 255, 255)]
colorIndex = 0

# Here is code for Canvas setup
paintWindow = np.zeros((471, 636, 3)) + 255

# Define button properties
button_radius = 30
button_positions = {
    "CLEAR": (603, 50),
    "BLUE": (603, 150),
    "GREEN": (603, 250),
    "RED": (603, 350),
    "YELLOW": (603, 450)
}

# Draw buttons
for label, center in button_positions.items():
    color = (0, 0, 0) if label == "CLEAR" else colors[list(button_positions.keys()).index(label) - 1]
    cv2.circle(paintWindow, center, button_radius, color, -1)
    cv2.putText(paintWindow, label, (center[0] - 25, center[1] + 5), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2, cv2.LINE_AA)

cv2.namedWindow('Paint', cv2.WINDOW_AUTOSIZE)

# Initialize mediapipe
mpHands = mp.solutions.hands
hands = mpHands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mpDraw = mp.solutions.drawing_utils

# Initialize the webcam
cap = cv2.VideoCapture(0)
ret = True
while ret:
    # Read each frame from the webcam
    ret, frame = cap.read()

    x, y, c = frame.shape

    # Flip the frame vertically
    frame = cv2.flip(frame, 1)
    framergb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Draw the color selection buttons
    for label, center in button_positions.items():
        color = (0, 0, 0) if label == "CLEAR" else colors[list(button_positions.keys()).index(label) - 1]
        cv2.circle(frame, center, button_radius, color, -1)
        cv2.putText(frame, label, (center[0] - 25, center[1] + 5), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2, cv2.LINE_AA)

    # Highlight the selected color
    selected_center = list(button_positions.values())[colorIndex + 1]
    cv2.circle(frame, selected_center, button_radius, (255, 255, 255), 2)

    # Get hand landmark prediction
    result = hands.process(framergb)

    # Post process the result
    if result.multi_hand_landmarks:
        landmarks = []
        for handslms in result.multi_hand_landmarks:
            for lm in handslms.landmark:
                lmx = int(lm.x * 640)
                lmy = int(lm.y * 480)
                landmarks.append([lmx, lmy])

            # Drawing landmarks on frames
            mpDraw.draw_landmarks(frame, handslms, mpHands.HAND_CONNECTIONS)
        fore_finger = (landmarks[8][0], landmarks[8][1])
        center = fore_finger
        thumb = (landmarks[4][0], landmarks[4][1])
        cv2.circle(frame, center, 3, (0, 255, 0), -1)
        if (thumb[1] - center[1] < 30):
            bpoints.append(deque(maxlen=512))
            blue_index += 1
            gpoints.append(deque(maxlen=512))
            green_index += 1
            rpoints.append(deque(maxlen=512))
            red_index += 1
            ypoints.append(deque(maxlen=512))
            yellow_index += 1
        elif center[0] >= 573:
            if np.linalg.norm(np.array(center) - np.array(button_positions["CLEAR"])) <= button_radius:
                bpoints = [deque(maxlen=512)]
                gpoints = [deque(maxlen=512)]
                rpoints = [deque(maxlen=512)]
                ypoints = [deque(maxlen=512)]

                blue_index = 0
                green_index = 0
                red_index = 0
                yellow_index = 0

                paintWindow[:, 0:573, :] = 255
            elif np.linalg.norm(np.array(center) - np.array(button_positions["BLUE"])) <= button_radius:
                colorIndex = 0  # Blue
            elif np.linalg.norm(np.array(center) - np.array(button_positions["GREEN"])) <= button_radius:
                colorIndex = 1  # Green
            elif np.linalg.norm(np.array(center) - np.array(button_positions["RED"])) <= button_radius:
                colorIndex = 2  # Red
            elif np.linalg.norm(np.array(center) - np.array(button_positions["YELLOW"])) <= button_radius:
                colorIndex = 3  # Yellow
        else:
            if colorIndex == 0:
                bpoints[blue_index].appendleft(center)
            elif colorIndex == 1:
                gpoints[green_index].appendleft(center)
            elif colorIndex == 2:
                rpoints[red_index].appendleft(center)
            elif colorIndex == 3:
                ypoints[yellow_index].appendleft(center)
    else:
        bpoints.append(deque(maxlen=512))
        blue_index += 1
        gpoints.append(deque(maxlen=512))
        green_index += 1
        rpoints.append(deque(maxlen=512))
        red_index += 1
        ypoints.append(deque(maxlen=512))
        yellow_index += 1

    # Draw lines of all the colors on the canvas and frame
    points = [bpoints, gpoints, rpoints, ypoints]
    for i in range(len(points)):
        for j in range(len(points[i])):
            for k in range(1, len(points[i][j])):
                if points[i][j][k - 1] is None or points[i][j][k] is None:
                    continue
                cv2.line(frame, points[i][j][k - 1], points[i][j][k], colors[i], 2)
                cv2.line(paintWindow, points[i][j][k - 1], points[i][j][k], colors[i], 2)

    cv2.imshow("Output", frame)
    cv2.imshow("Paint", paintWindow)

    if cv2.waitKey(1) == ord('q'):
        break

# Release the webcam and destroy all active windows
cap.release()
cv2.destroyAllWindows()
