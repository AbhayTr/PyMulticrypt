import random
import textwrap

class End2End:

    def __init__(self, key_path = "keys.dat", new = False):
        self.primes_list = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317, 331, 337, 347, 349]
        try:
            if new:
                raise Exception("Generate New Key Pair.")
            keys = open(key_path, "r").readlines()
            self.private_key = keys[0]
            self.public_key = keys[1]
        except:
            fresh_keys = self.get_keys()
            self.private_key = fresh_keys["private"]
            self.public_key = fresh_keys["public"]
            save_keys = open(key_path, "w")
            save_keys.write(self.private_key + "\n")
            save_keys.write(self.public_key)
            save_keys.close()

    def n_bits_prime(self, n):
        while True:
            prime_number = random.randrange((2 ** (n-1)) + 1, (2 ** n) - 1)
            for divisor in self.primes_list:
                if prime_number % divisor == 0 and divisor ** 2 <= prime_number:
                    break
            else:
                return prime_number

    def check_prime_strength(self, prime_number):
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

    def is_coprime(self, number1, number2):
        while number2 != 0:
            number1, number2 = number2, number1 % number2
        return number1 == 1

    def mod_inverse(self, number1, number2):

        def modulo_inverse(number1, number2):
            if number2 == 0:
                return (1,0)
            (q,r) = (number1 // number2, number1 % number2)
            (s,t) = modulo_inverse(number2, r)
            return (t, s - (q * t))

        inv = modulo_inverse(number1, number2)[0]
        if inv < 1:
            inv += number2
        return inv

    def compress_number(self, number):
        number_pieces_list = textwrap.wrap(number, 1)
        compressed_number_string = ""
        for number_piece in number_pieces_list:
            try:
                compressed_number_string += chr(int(number_piece))
            except:
                position_of_exception = 0
                for digit in range(len(number_piece)):
                    try:
                        check = int(number_piece[digit])
                    except:
                        position_of_exception = digit
                        break
                digits_before_exception = number_piece[:position_of_exception]
                exception_charecter = number_piece[position_of_exception]
                digits_after_exception = number_piece[position_of_exception + 1:]
                if digits_before_exception != "":
                    compressed_number_string += chr(int(digits_before_exception))
                compressed_number_string += exception_charecter
                if digits_after_exception != "":
                    compressed_number_string += chr(int(digits_after_exception))
        return compressed_number_string

    def deflate_number_string(self, number_string, exception_charecter):
        deflated_number = ""
        for charecter in number_string:
            if charecter != exception_charecter:
                deflated_number += str(ord(charecter))
            else:
                deflated_number += charecter
        return deflated_number

    def get_keys(self):
        prime_key_1 = 0
        prime_key_2 = 0
        while True:
            prime_key = self.n_bits_prime(1024)
            if self.check_prime_strength(prime_key):
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
            if self.is_coprime(phi_n, number):
                e = number
                break
        public_key = str(public_key_number) + "X" + str(e)
        private_key = str(self.mod_inverse(e, phi_n)) + "X" + str(public_key_number)
        return {"private": private_key, "public": public_key}

    def keys(self):
        return {"public": self.public_key, "private": self.private_key}

    def rsa_encrypt(self, message, public_key):
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

    def rsa_decrypt(self, message, private_key):
        seperator_position = private_key.index("X")
        public_key_number = int(private_key[seperator_position + 1:])
        private_key_number = int(private_key[:seperator_position])
        charecters = str(pow(int(message), private_key_number, public_key_number)).split("300")
        actual_message = ""
        for charecter in charecters:
            actual_message += chr(int(charecter))
        return actual_message

    def encrypt(self, message):
        key = self.n_bits_prime(256)
        charecters = list(message)
        encrypted_message_stage1 = ""
        for charecter_index in range(len(charecters)):
            encrypted_message_stage1 += str(ord(charecters[charecter_index]))
            if charecter_index != len(charecters) - 1:
                encrypted_message_stage1 += "X"
        charecters2 = list(encrypted_message_stage1)
        encrypted_message_stage2 = ""
        for charecter_index2 in range(len(charecters2)):
            encrypted_message_stage2 += str(ord(charecters2[charecter_index2]))
            if charecter_index2 != len(charecters2) - 1:
                encrypted_message_stage2 += "42"
        encrypted_message = str(int(encrypted_message_stage2) * key) + "K" + self.rsa_encrypt(str(key), self.public_key)
        return self.compress_number(encrypted_message)

    def decrypt(self, message):
        message = self.deflate_number_string(message, "K")
        seperator_position = message.index("K")
        encrypted_key = message[seperator_position + 1:]
        encrypted_message = message[:seperator_position]
        key = int(self.rsa_decrypt(encrypted_key, self.private_key))
        encrypted_message = int(encrypted_message) // key
        charecters = str(encrypted_message).split("42")
        actual_message_stage1 = ""
        for charecter in charecters:
            actual_message_stage1 += chr(int(charecter))
        charecters2 = actual_message_stage1.split("X")
        actual_message = ""
        for charecter2 in charecters2:
            actual_message += chr(int(charecter2))
        return actual_message
