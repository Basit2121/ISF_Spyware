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

#encrypt_file('payload.py', 'config.txt', 3)