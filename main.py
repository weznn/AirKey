pip install opencv-python mediapipe pyautogui

import cv2
import mediapipe as mp
import pyautogui
import math

# El takibi
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_draw = mp.solutions.drawing_utils

# Kamera
cap = cv2.VideoCapture(0)

# Klavye düzeni
keys = [
    ["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
    ["A", "S", "D", "F", "G", "H", "J", "K", "L"],
    ["Z", "X", "C", "V", "B", "N", "M", "Backspace"],
    ["←", "↓", "Space", "↑", "→", "Enter"]
]

# Tuş boyutları
key_w, key_h = 60, 60

# Fonksiyon: tuşları çiz
def draw_keyboard(img):
    key_list = []
    for i, row in enumerate(keys):
        for j, key in enumerate(row):
            if key == "Space":
                w = key_w * 3
            elif key in ["Enter", "Backspace"]:
                w = key_w * 2
            else:
                w = key_w

            x = 100 + sum([
                key_w * 3 + 10 if k == "Space" else
                key_w * 2 + 5 if k in ["Enter", "Backspace"] else
                key_w + 5
                for k in row[:j]
            ])
            y = 100 + i * (key_h + 10)
            cv2.rectangle(img, (x, y), (x + w, y + key_h), (255, 0, 0), -1)
            cv2.putText(img, key, (x + 10, y + 40), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)
            key_list.append((key, x, y, w))
    return key_list

# Ana döngü
while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)
    key_list = draw_keyboard(img)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            index_finger = hand_landmarks.landmark[8]
            thumb_tip = hand_landmarks.landmark[4]

            h, w, _ = img.shape
            index_x, index_y = int(index_finger.x * w), int(index_finger.y * h)
            thumb_x, thumb_y = int(thumb_tip.x * w), int(thumb_tip.y * h)

            cv2.circle(img, (index_x, index_y), 10, (0, 255, 0), cv2.FILLED)

            for key, x, y, key_width in key_list:
                if x < index_x < x + key_width and y < index_y < y + key_h:
                    cv2.rectangle(img, (x, y), (x + key_width, y + key_h), (0, 255, 0), -1)
                    cv2.putText(img, key, (x + 10, y + 40), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)

                    distance = math.hypot(index_x - thumb_x, index_y - thumb_y)
                    if distance < 40:
                        if key == "Backspace":
                            pyautogui.press("backspace")
                        elif key == "Enter":
                            pyautogui.press("enter")
                        elif key == "Space":
                            pyautogui.press("space")
                        elif key == "←":
                            pyautogui.press("left")
                        elif key == "→":
                            pyautogui.press("right")
                        elif key == "↓":
                            pyautogui.press("down")
                        elif key == "↑":
                            pyautogui.press("up")
                        else:
                            pyautogui.press(key.lower())
                        cv2.putText(img, f"Pressed {key}", (x, y - 20), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)

    cv2.imshow("Sanal Klavye", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
