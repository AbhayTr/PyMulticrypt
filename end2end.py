import hashlib
import random
from datetime import datetime

def get_keys(username):
    number_private_factors = random.randint(3, 10)
    private_key = str(random.randint(0,500000) + datetime.timestamp(datetime.now())) + username
    public_key = 1
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
    return {"private": private_key, "public": public_key}

keys = get_keys(input("Enter Username: "))
print("Private Key:")
print()
print(keys["private"])
print()
print("Public Key:")
print()
print(keys["public"])
print()
        
