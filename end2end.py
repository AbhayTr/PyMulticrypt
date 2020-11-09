import hashlib
import random
from datetime import datetime

def is_coprime(number1, number2):
    while number2 != 0:
        number1, number2 = number2, number1 % number2
    return number1 == 1

def get_keys(unique_id = ""):
    number_private_factors = 21
    private_key = str(random.randint(0,500000) + datetime.timestamp(datetime.now())) + unique_id
    public_key = 1
    public_key_prime = 1
    for encrypting in range(number_private_factors):
        sha256_private_key = hashlib.sha256(private_key.encode()).hexdigest()
        current_key = ""
        for charecter in sha256_private_key:
            current_key += str(ord(charecter)) + str(random.randint(0, 9))
        if public_key == 1:
            private_key = current_key
        else:
            private_key += "X" + current_key
        current_key = int(current_key)
        public_key = public_key * current_key
        public_key_prime = public_key_prime * (current_key - 1)
    public_key_relative_prime = 0
    for number in range(2, public_key_prime + 1):
        if is_coprime(public_key_prime, number):
            public_key_relative_prime = number
            break
    public_key = str(public_key) + "X" + str(public_key_relative_prime)
    private_key += "X" + str(public_key_prime)
    return {"private": private_key, "public": public_key}

def encrypt(public_key, message):
    seperator_position = public_key.index("X")
    relative_prime = int(public_key[seperator_position + 1:])
    public_key = int(public_key[:seperator_position])
    encrypted_message = ""
    charecters = list(message)
    for charecter_index in range(len(charecters)):
        encrypted_charecter = public_key % (ord(charecters[charecter_index]) ** relative_prime)
        encrypted_message += str(encrypted_charecter)
        if charecter_index != len(charecters) - 1:
            encrypted_message += "X"
    return encrypted_message

def decrypt(private_key, public_key, message):
    private_factors = private_key.replace("X", " ").split(" ")
    decrypt_factor = int(private_factors[len(private_factors) - 1])
    charecters = message.replace("X", " ").split(" ")
    seperator_position = public_key.index("X")
    relative_prime = int(public_key[seperator_position + 1:])
    public_key = int(public_key[:seperator_position])
    decrypt_power = 0
    for number in range(1, decrypt_factor + 1):
        if (relative_prime * number) % decrypt_factor == 1:
            decrypt_power = number
            break
    actual_message = ""
    for charecter in charecters:
        actual_charecter = chr((int(charecter) ** decrypt_power) % public_key)
        actual_message += actual_charecter
    return actual_message

keys = get_keys(input("Enter Username: "))
print()
print("Private Key:")
print()
print(keys["private"])
print()
print("Public Key:")
print()
print(keys["public"])
print()
message = input("Enter Message: ")
print()
print("Actual Message: " + message)
print()
print("Encrypted Message:")
print()
msg = encrypt(keys["public"], message)
print(msg)
print()
print("Decrypted Message:")
print()
print(decrypt(keys["private"], keys["public"], msg))
print()
