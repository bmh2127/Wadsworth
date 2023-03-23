import time
import json
import os
import threading
from datetime import datetime
from playsound import playsound
import webbrowser

def open_youtube_video(url='https://www.youtube.com/watch?v=VdOkQ6THDVw'):
    webbrowser.open(url)
def play_sound(sound_file):
    playsound(sound_file)

def prompt_for_task_input():
    description = input("Please enter the task description: ")
    category = input("Please enter the task category: ")

    return {
        'description': description,
        'category': category
    }

def save_task_to_file(task, filename="tasks.json"):
    tasks = []

    if os.path.exists(filename):
        with open(filename, 'r') as f:
            tasks = json.load(f)
    else:
        with open(filename, 'w') as f:
            json.dump([], f)

    tasks.append(task)

    with open(filename, 'w') as f:
        json.dump(tasks, f)

def timer_thread(end_event, timer_duration, youtube_url):
    start_time = time.time()
    remaining_time = timer_duration

    while not end_event.is_set():
        remaining_time = int(max(timer_duration - (time.time() - start_time), 0))
        minutes, seconds = divmod(remaining_time, 60)
        print(f"Time remaining: {minutes:02d}:{seconds:02d}", end="\r")

        if remaining_time == 0:
            end_event.set()
            open_youtube_video(youtube_url)
            break

        time.sleep(1)

    return start_time

def main():
    print("Pomodoro Timer started. 25 minutes countdown...")
    print("Press ENTER to end the timer manually.")

    end_event = threading.Event()
    timer = threading.Thread(target=timer_thread,
                             args=(end_event, 25 * 60, "https://www.youtube.com/watch?v=VdOkQ6THDVw"))
    timer.start()

    input()  # Wait for the user to press ENTER
    if not end_event.is_set():
        print("Did you complete the task? (yes/no)")
        user_input = input().lower()
        if user_input == "yes":
            completed = True
        else:
            completed = False
    else:
        completed = True
        timer.join()  # Stop the timer thread if it wasn't ended manually

    start_time = timer_thread(end_event, 25 * 60,
                              "https://www.youtube.com/watch?v=VdOkQ6THDVw")  # Get the start time from the timer_thread function

    print("\nTime's up or manually ended! Please enter your task details.")
    task = prompt_for_task_input()
    completion_time = (time.time() - start_time) / 60  # Calculate completion time in minutes
    task['completion_time'] = completion_time
    task['completed'] = completed  # Add the 'completed' flag to the task dictionary

    # Add datetime information to the task dictionary
    task['date'] = datetime.now().strftime('%Y-%m-%d')
    task['start_time'] = datetime.fromtimestamp(start_time).strftime('%H:%M:%S')
    task['end_time'] = datetime.now().strftime('%H:%M:%S')

    save_task_to_file(task)
    print("Task saved successfully.")

if __name__ == "__main__":
    main()