import random

primes_list = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317, 331, 337, 347, 349]

def n_bits_prime(n):
    while True:
        prime_number = random.randrange((2 ** (n-1)) + 1, (2 ** n) - 1)
        for divisor in primes_list:
            if prime_number % divisor == 0 and divisor ** 2 <= prime_number:
                break
        else:
            return prime_number
  
def check_prime_strength(prime_number): 
    max_divisions_two = 0
    ec = prime_number - 1
    while ec % 2 == 0:
        ec >>= 1
        max_divisions_two += 1
    assert 2 ** max_divisions_two * ec == prime_number - 1
  
    def trial_composite(round_tester):
        if pow(round_tester, ec, prime_number) == 1: 
            return False
        for i in range(max_divisions_two): 
            if pow(round_tester, 2 ** i * ec, prime_number) == prime_number - 1: 
                return False
        return True
  
    for i in range(20): 
        round_tester = random.randrange(2, prime_number) 
        if trial_composite(round_tester):
            return False
    return True

def is_coprime(number1, number2):
    while number2 != 0:
        number1, number2 = number2, number1 % number2
    return number1 == 1

def mod_inverse(number1, number2):

    def eea(number1, number2):
        if number2 == 0:
            return (1,0)
        (q,r) = (number1 // number2, number1 % number2)
        (s,t) = eea(number2, r)
        return (t, s - (q * t))

    inv = eea(number1, number2)[0]
    if inv < 1:
        inv += number2
    return inv

def get_keys():
    n = 1024
    prime_key_1 = 0
    prime_key_2 = 0
    while True:
        prime_key = n_bits_prime(n)
        if check_prime_strength(prime_key):
            if prime_key_1 == 0:
                prime_key_1 = prime_key
                continue
            elif prime_key_2 == 0:
                prime_key_2 = prime_key
                break
    public_key_number = prime_key_1 * prime_key_2
    phi_n = (prime_key_1 - 1) * (prime_key_2 - 1)
    e = 0
    for number in range(2, phi_n):
        if is_coprime(phi_n, number):
            e = number
            break
    public_key = str(public_key_number) + "X" + str(e)
    private_key = str(mod_inverse(e, phi_n))
    return {"private": private_key, "public": public_key}

def encrypt(message, public_key):
    seperator_position = public_key.index("X")
    e = int(public_key[seperator_position + 1:])
    public_key_number = int(public_key[:seperator_position])
    encrypted_message = ""
    charecters = list(message)
    for charecter_index in range(len(charecters)):
        encrypted_message += str(ord(charecters[charecter_index]))
        if charecter_index != len(charecters) - 1:
            encrypted_message += "300"
    encrypted_message = str(int((int(encrypted_message) ** e) % public_key_number))        
    return encrypted_message

def decrypt(message, private_key, public_key): 
    seperator_position = public_key.index("X")
    public_key_number = int(public_key[:seperator_position])
    charecters = str(pow(int(message), int(private_key), public_key_number)).replace("300", " ").split(" ")
    actual_message = ""
    for charecter in charecters:
        actual_message += chr(int(charecter))
    return actual_message

keys = get_keys()
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
print("Encrypted Message:")
print()
msg = encrypt(message, keys["public"])
print(msg)
print()
print("Decrypted Message:")
print()
print(decrypt(msg, keys["private"], keys["public"]))
print()
