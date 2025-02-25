import cv2
from deepface import DeepFace
import pygame
import os
import sys
import random
from datetime import datetime
import tkinter as tk
from tkinter import Toplevel, Scrollbar, Listbox, Label, Button
import matplotlib.pyplot as plt

# Initialize Pygame (not for window, just for avatar handling)
pygame.init()

# Load the avatars
avatars = {
    'happy': pygame.image.load('avatars/happy.jpeg'),
    'sad': pygame.image.load('avatars/sad.jpeg'),
    'angry': pygame.image.load('avatars/angry.jpeg'),
    'surprise': pygame.image.load('avatars/surprise.jpeg'),
    'fear': pygame.image.load('avatars/fear.jpeg'),
    'disgust': pygame.image.load('avatars/disgust.jpeg')
}

# Create a list to store the mood history (max 10 entries)
mood_history = []

def insert_emotion(emotion):
    mood_history.append({
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'emotion': emotion
    })
    if len(mood_history) > 10:
        mood_history.pop(0)

# Original mood history popup (unchanged)
def show_mood_history_popup():
    popup = tk.Tk()
    popup.title("Mood History")

    scrollbar = Scrollbar(popup)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    mood_listbox = Listbox(popup, height=10, width=50, yscrollcommand=scrollbar.set, bg=bg_color, fg=fg_color)
    mood_listbox.pack(pady=10)

    for entry in reversed(mood_history):
        mood_listbox.insert(tk.END, f"{entry['timestamp']}: {entry['emotion']}")

    scrollbar.config(command=mood_listbox.yview)

    close_button = tk.Button(popup, text="Close", command=popup.destroy, bg=btn_color, fg=fg_color)
    close_button.pack(pady=5)

    popup.configure(bg=bg_color)
    popup.mainloop()






import pygame
import sys
import random

def start_game():
    if not mood_history:
        print("No emotion detected yet. Please wait for emotion detection.")
        return

    # Get the last detected emotion
    last_emotion = mood_history[-1]['emotion']
    print(f"Starting game in '{last_emotion}' mode!")

    # Initialize Pygame window
    pygame.init()
    screen_width = 800
    screen_height = 400
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption('Emotion-Powered Endless Runner')
    clock = pygame.time.Clock()

    # Colors
    white = (255, 255, 255)
    black = (0, 0, 0)
    red = (255, 0, 0)

    # Character settings
    player_size = 50
    player_x = 100
    player_y = screen_height - player_size - 10
    player_velocity_y = 0
    gravity = 1
    is_jumping = False
    player_speed = 5  # Default player speed

    # Obstacle settings
    obstacle_width = 20
    obstacle_height = 50
    obstacle_x = screen_width
    obstacle_y = screen_height - obstacle_height - 10
    obstacle_speed = 5

    # Emotion-based game mode adjustments
    if last_emotion == "happy":
        obstacle_speed = 7  # Increase obstacle speed when happy
        player_speed = 6
    elif last_emotion == "sad":
        obstacle_speed = 3  # Slow down everything when sad
        player_speed = 3
    elif last_emotion == "stressed":
        gravity = 2  # Increase gravity when stressed
        player_speed = 5
        obstacle_speed = 6
    elif last_emotion == "neutral":
        obstacle_speed = 5  # Normal speed for neutral mood
        player_speed = 5
    elif last_emotion == "angry":
        obstacle_speed = 10  # Very fast when angry
        player_speed = 10

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            # Jumping mechanism
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not is_jumping:
                    player_velocity_y = -15
                    is_jumping = True

        # Game mechanics
        player_y += player_velocity_y
        player_velocity_y += gravity

        # Prevent player from falling through the ground
        if player_y >= screen_height - player_size - 10:
            player_y = screen_height - player_size - 10
            is_jumping = False

        # Move obstacle
        obstacle_x -= obstacle_speed
        if obstacle_x < 0:
            obstacle_x = screen_width
            obstacle_speed = random.randint(5, 10)  # Randomize speed for variability

        # Move player (if needed for future implementations)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] and player_x < screen_width - player_size:
            player_x += player_speed

        # Collision detection
        if player_x + player_size > obstacle_x and player_x < obstacle_x + obstacle_width:
            if player_y + player_size > obstacle_y:
                print("Game Over!")
                running = False

        # Drawing elements
        screen.fill(white)
        pygame.draw.rect(screen, black, (player_x, player_y, player_size, player_size))  # Player
        pygame.draw.rect(screen, red, (obstacle_x, obstacle_y, obstacle_width, obstacle_height))  # Obstacle

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()




















# Original emotion graph function (unchanged)
def show_emotion_graph():
    if not mood_history:
        print("No mood history available for graph.")
        return

    emotions = [entry['emotion'] for entry in mood_history]
    emotion_counts = {emotion: emotions.count(emotion) for emotion in set(emotions)}

    plt.figure(figsize=(8, 6))
    plt.bar(emotion_counts.keys(), emotion_counts.values(), color='skyblue')
    plt.xlabel('Emotions')
    plt.ylabel('Count')
    plt.title('Emotion Frequency in Recent History')
    plt.show()

# New function: Show a non-intrusive dashboard
def show_dashboard():
    dashboard = Toplevel()
    dashboard.title("Emotion Detection Dashboard")
    dashboard.geometry("500x500")

    Label(dashboard, text="Mood History", font=('Arial', 14)).pack(pady=10)

    scrollbar = Scrollbar(dashboard)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    mood_listbox = Listbox(dashboard, height=10, width=50, yscrollcommand=scrollbar.set, bg=bg_color, fg=fg_color)
    mood_listbox.pack(pady=10)

    scrollbar.config(command=mood_listbox.yview)

    def update_mood_history():
        mood_listbox.delete(0, tk.END)
        for entry in reversed(mood_history):
            mood_listbox.insert(tk.END, f"{entry['timestamp']}: {entry['emotion']}")
        dashboard.after(1000, update_mood_history)

    update_mood_history()

    def show_emotion_graph_from_dashboard():
        show_emotion_graph()

    Button(dashboard, text="Show Emotion Graph", command=show_emotion_graph_from_dashboard, bg=btn_color, fg=fg_color).pack(pady=10)
    Button(dashboard, text="Close Dashboard", command=dashboard.destroy, bg=btn_color, fg=fg_color).pack(pady=10)

cap = cv2.VideoCapture(0)

root = tk.Tk()
root.title("Emotion Detection")
root.geometry("1000x700")

dark_mode = False
bg_color = "white"
fg_color = "black"
btn_color = "lightgrey"

def toggle_theme():
    global dark_mode, bg_color, fg_color, btn_color
    dark_mode = not dark_mode
    if dark_mode:
        bg_color = "black"
        fg_color = "white"
        btn_color = "grey"
    else:
        bg_color = "white"
        fg_color = "black"
        btn_color = "lightgrey"
    
    root.configure(bg=bg_color)
    video_label.config(bg=bg_color, fg=fg_color)
    mood_history_button.config(bg=btn_color, fg=fg_color)
    emotion_graph_button.config(bg=btn_color, fg=fg_color)
    start_stop_button.config(bg=btn_color, fg=fg_color)
    theme_toggle_button.config(bg=btn_color, fg=fg_color)
    dashboard_button.config(bg=btn_color, fg=fg_color)

video_label = tk.Label(root, bg=bg_color, fg=fg_color)
video_label.pack(side=tk.LEFT, padx=10, pady=10)

mood_history_button = tk.Button(root, text="Show Mood History", command=show_mood_history_popup, bg=btn_color, fg=fg_color)
mood_history_button.pack(pady=10)

emotion_graph_button = tk.Button(root, text="Show Emotion Graph", command=show_emotion_graph, bg=btn_color, fg=fg_color)
emotion_graph_button.pack(pady=10)

dashboard_button = tk.Button(root, text="Open Dashboard", command=show_dashboard, bg=btn_color, fg=fg_color)
dashboard_button.pack(pady=10)

camera_running = True

def toggle_camera():
    global camera_running, cap
    if camera_running:
        camera_running = False
        cap.release()
        video_label.config(image='')
        start_stop_button.config(text='Start Camera')
    else:
        camera_running = True
        cap = cv2.VideoCapture(0)
        start_stop_button.config(text='Stop Camera')
        update_frame()
def update_frame():
    if not camera_running:
        return

    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        return

    result = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)
    dominant_emotion = result[0]['dominant_emotion']
    insert_emotion(dominant_emotion)

    cv2.putText(frame, dominant_emotion, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 3, cv2.LINE_AA)

    if dominant_emotion in avatars:
        avatar = avatars[dominant_emotion]
        avatar = pygame.transform.scale(avatar, (150, 150))  # Resize for a non-intrusive display
        avatar = pygame.transform.rotate(avatar, -270)  # Rotate the avatar by -90 degrees

        avatar_array = pygame.surfarray.array3d(avatar)
        avatar_array = cv2.cvtColor(avatar_array, cv2.COLOR_RGB2BGR)

        # Position avatar in the bottom-right corner
        frame_height, frame_width = frame.shape[:2]
        avatar_height, avatar_width = avatar_array.shape[:2]

        x_offset = frame_width - avatar_width - 10  # Padding from the right
        y_offset = frame_height - avatar_height - 10  # Padding from the bottom

        frame[y_offset:y_offset+avatar_height, x_offset:x_offset+avatar_width] = avatar_array

    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    img = cv2.resize(cv2image, (640, 480))
    img = tk.PhotoImage(data=cv2.imencode('.png', img)[1].tobytes())
    video_label.config(image=img)
    video_label.image = img
    root.after(10, update_frame)


start_stop_button = tk.Button(root, text='Stop Camera', command=toggle_camera, bg=btn_color, fg=fg_color)
start_stop_button.pack(pady=10)

theme_toggle_button = tk.Button(root, text="Toggle Theme", command=toggle_theme, bg=btn_color, fg=fg_color)
theme_toggle_button.pack(pady=10)



# Add a "Start Game" button to the Tkinter interface
start_game_button = tk.Button(root, text="Start Game", command=start_game, bg=btn_color, fg=fg_color)
start_game_button.pack(pady=10)





update_frame()

root.configure(bg=bg_color)
root.mainloop()

cap.release()
cv2.destroyAllWindows()
pygame.quit()





















