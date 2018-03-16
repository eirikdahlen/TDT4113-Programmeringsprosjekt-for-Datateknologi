from random import randint
import crypto_utils

# *********************** Cipher *************************

class Cipher:

    def __init__(self):
        self.characters = [chr(i) for i in range(32, 127)]

    def encode(self, text, key):
        return

    def decode(self, text, key):
        return

    def generate_keys(self):
        return


    def verify(self, text, key):
        code = self.encode(text, key[0])
        return self.decode(code, key[1]) == text


# *********************** Person *************************

class Person:

    def __init__(self, cipher):
        self.key = None
        self.cipher = cipher

    def set_key(self, key):
        self.key = key

    def get_key(self):
        return self.key

    def set_cipher(self, cipher):
        self.cipher = cipher

    def operate_cipher(self, text):
        return

# *********************** Sender *************************

class Sender(Person):

    def __init__(self, cipher):
        Person.__init__(self, cipher)

    def operate_cipher(self, text):
        return self.cipher.encode(text, self.get_key())

    def get_cipher(self):
        return self.cipher

# *********************** Receiver *************************

class Receiver(Person):

    def __init__(self, cipher):
        Person.__init__(self, cipher)

    def operate_cipher(self, text):
        return self.cipher.decode(text, self.get_key())

    def get_cipher(self):
        return self.cipher

# *********************** Hacker *************************

class Hacker(Receiver):

    def __init__(self):
        Cipher.__init__(self)
        file = open("english_words.txt", 'r')
        read = file.read()
        self.english_words = set(read.split('\n'))
        file.close()

    def hackerman(self, text, cipher):
        self.set_cipher(cipher)

        if isinstance(cipher, Caesar) or isinstance(cipher, Multiplicative):
            return self.decode_cae_mult(text)

        elif isinstance(cipher, Affine):
            return self.decode_affine(text)

        elif isinstance(cipher, Unbreakable):
            return self.decode_unbr(text)


    def decode_cae_mult(self, text):
        best_text = ""
        most_num_eng_words = 0
        for key in self.get_cipher().possible_keys():
            self.set_key(key)
            decrypted_text = self.operate_cipher(text)
            decrypted_words = decrypted_text.split()
            num_eng_words = 0
            for word in decrypted_words:
                if word in self.english_words:
                    num_eng_words += 1
            if num_eng_words > most_num_eng_words:
                best_text = decrypted_text
                most_num_eng_words = num_eng_words
        return best_text

    def decode_affine(self, text):
        best_text = ""
        most_num_eng_words = 0
        for key1 in self.get_cipher().possible_keys():
            for key2 in self.get_cipher().possible_keys():
                self.set_key((key1, key2))
                decrypted_text = self.operate_cipher(text)
                decrypted_words = decrypted_text.split()
                num_eng_words = 0
                for word in decrypted_words:
                    if word in self.english_words:
                        num_eng_words += 1
                if num_eng_words > most_num_eng_words:
                    best_text = decrypted_text
                    most_num_eng_words = num_eng_words
        return best_text

    def decode_unbr(self, text):
        best_text = ""
        most_num_eng_words = 0
        keys = self.get_cipher().possible_keys()
        for key in keys:
            word = keys[key]
            decryption_key = self.generate_decryption_key(word)
            self.set_key(decryption_key)
            decrypted_text = self.operate_cipher(text)
            decrypted_words = decrypted_text.split()
            num_eng_words = 0
            for word in decrypted_words:
                if word in self.english_words:
                    num_eng_words += 1
            if num_eng_words > most_num_eng_words:
                best_text = decrypted_text
                most_num_eng_words = num_eng_words
        return best_text

    def generate_decryption_key(self, sender_key):
        receiver_key = ""
        for char in sender_key:
            index = (95 - self.get_cipher().characters.index(char)) % 95
            receiver_key += self.get_cipher().characters[index]
        return receiver_key



# *********************** Caesar *************************

class Caesar(Cipher):

    def generate_keys(self):
        sender_key = randint(0, 95)
        receiver_key = 95 - sender_key
        return [sender_key, receiver_key]

    def encode(self, text, key):
        code = ""
        for symbol in text:
            index = self.characters.index(symbol)
            code += self.characters[(index + key) % 95]
        return code

    def decode(self, text, key):
        code = ""
        for symbol in text:
            index = self.characters.index(symbol)
            code += self.characters[(index + key) % 95]
        return code

    def possible_keys(self):
        return list(range(95))

# *********************** Multiplicative *************************

class Multiplicative(Cipher):

    def generate_keys(self):
        sender_key = randint(0, 95)
        receiver_key = crypto_utils.modular_inverse(sender_key, 95)
        while (sender_key * receiver_key) % 95 != 1 or sender_key == receiver_key:
            sender_key = randint(0, 95)
            receiver_key = crypto_utils.modular_inverse(sender_key, 95)
        return [sender_key, receiver_key]

    def encode(self, text, key):
        code = ""
        for symbol in text:
            index = self.characters.index(symbol)
            code += self.characters[(index * key) % 95]
        return code

    def decode(self, text, key):
        return self.encode(text, key)

    def possible_keys(self):
        return list(range(95))

# *********************** Affine *************************

class Affine(Cipher):

    def __init__(self):
        Cipher.__init__(self)

    def encode(self, text, key):
        crypted_message = ""
        for char in text:
            mult_index = (self.characters.index(char)*key[0]) % 95
            new_index = (mult_index + key[1]) % 95
            crypted_char = self.characters[new_index]
            crypted_message += crypted_char
        return crypted_message

    def decode(self, text, key):
        decrypted_message = ""
        for char in text:
            add_index = (self.characters.index(char) + key[1]) % 95
            mult_index = (add_index * key[0]) % 95
            new_index = mult_index
            decrypted_char = self.characters[new_index]
            decrypted_message += decrypted_char
        return decrypted_message

    def generate_keys(self):
        sender_add_key = randint(0, 95)
        receiver_add_key = 95 - sender_add_key
        sender_mult_key = randint(0, 95)
        receiver_mult_key = crypto_utils.modular_inverse(sender_mult_key, 95)
        while not receiver_mult_key:
            sender_mult_key = randint(0, 95)
            receiver_mult_key = crypto_utils.modular_inverse(sender_mult_key, 95)
        return [(sender_mult_key, sender_add_key), (receiver_mult_key, receiver_add_key)]

    def possible_keys(self):
        return list(range(95))

# *********************** Unbreakable *************************

class Unbreakable(Cipher):

    def __init__(self):
        Cipher.__init__(self)
        file = open("english_words.txt", 'r')
        self.english_words = {}
        key = 0
        for line in file:
            self.english_words[key] = line.strip()
            key += 1
        file.close()

    def generate_keys(self):
        new_key = input("Skriv inn et engelsk ord: ")
        if new_key == "default":
            new_key = self.english_words[randint(0, len(self.english_words) - 1)]
        else:
            while new_key not in self.english_words.values():
                new_key = input("Ugyldig ord --> Skriv inn et engelsk ord: ")
                if new_key == "default":
                    new_key = self.english_words[randint(0, len(self.english_words) - 1)]
        print("Nøkkelordet er", new_key)
        receiver_key = ""
        for char in new_key:
            index = (95 - self.characters.index(char)) % 95
            receiver_key += self.characters[index]
        return [new_key, receiver_key]

    def encode(self, text, key):
        key_word = ""
        for i in range(len(text)):
            char = key[i % len(key)]
            char_index = self.characters.index(char)
            crypto_index = (char_index + self.characters.index(text[i])) % 95
            key_word += self.characters[crypto_index]
        return key_word

    def decode(self, text, key):
        key_word = ""
        for i in range(len(text)):
            char = key[i % len(key)]
            char_index = self.characters.index(char)
            crypto_index = (char_index + self.characters.index(text[i])) % 95
            key_word += self.characters[crypto_index]
        return key_word

    def possible_keys(self):
        return self.english_words

# *********************** RSA *************************

class RSA(Cipher):

    def __init__(self):
        Cipher.__init__(self)

    def generate_keys(self):
        p = crypto_utils.generate_random_prime(8)
        q = -1
        while q == -1 or q == p:
            q = crypto_utils.generate_random_prime(8)
        n = p * q
        phi = (p - 1)*(q - 1)
        e = randint(2, phi - 1)
        d = crypto_utils.modular_inverse(e, phi)
        while not d:
            p = crypto_utils.generate_random_prime(8)
            q = -1
            while q == -1 or q == p:
                q = crypto_utils.generate_random_prime(8)
            n = p * q
            phi = (p - 1)*(q - 1)
            e = randint(2, phi - 1)
            d = crypto_utils.modular_inverse(e, phi)
        sender_key = (n, e)
        receiver_key = (n, d)
        return [sender_key, receiver_key]

    def encode(self, text, key):
        numbers = crypto_utils.blocks_from_text(text, 2)
        crypted_numbers = []
        for number in numbers:
            crypted_number = pow(number, key[1], key[0])
            crypted_numbers.append(crypted_number)
        return crypted_numbers

    def decode(self, text, key):
        decrypted_numbers = []
        for number in text:
            decrypted_number = pow(number, key[1], key[0])
            decrypted_numbers.append(decrypted_number)
        return crypto_utils.text_from_blocks(decrypted_numbers, 2)


# ****************TESTING****************
def caesar():
    cipher = Caesar()
    keys = cipher.generate_keys()
    print("----------------SENDER_CAESAR---------------------")
    sender = Sender(cipher)
    sender.set_key(keys[0])
    print("Sender har nøkkel: " + str(sender.get_key()))
    melding = "Hei, hva skjer? Hilsen Eirik"
    crm = sender.operate_cipher(melding)
    print("Sender følgende melding: " + melding)
    print("Kryptert melding: "+ crm)
    print("----------------RECEIVER_CAESAR-------------------")
    receiver = Receiver(cipher)
    receiver.set_key(keys[1])
    print("Receiver har nøkkel: " + str(receiver.get_key()))
    print("Receiver har mottat følgende kryptert melding: " + crm)
    mottatt_melding = receiver.operate_cipher(crm)
    print("Dekryptert melding: " + mottatt_melding)
    print("Verifisert: " + str(cipher.verify(melding, keys)))
    print()

def multi():
    cipher = Multiplicative()
    keys = cipher.generate_keys()
    print("----------------SENDER_MULTIPLICATIVE---------------------")
    sender = Sender(cipher)
    sender.set_key(keys[0])
    print("Sender har nøkkel: " + str(sender.get_key()))
    melding = "Testing testing 123--;''#&?"
    crm = sender.operate_cipher(melding)
    print("Sender følgende melding: " + melding)
    print("Kryptert melding: " + crm)
    print("----------------RECEIVER_MULTIPLICATIVE-------------------")
    receiver = Receiver(cipher)
    receiver.set_key(keys[1])
    print("Receiver har nøkkel: " + str(receiver.get_key()))
    print("Receiver har mottat følgende kryptert melding: " + crm)
    mottatt_melding = receiver.operate_cipher(crm)
    print("Dekryptert melding: " + mottatt_melding)
    print("Verifisert: " + str(cipher.verify(melding, keys)))
    print()

def affine():
    cipher = Affine()
    keys = cipher.generate_keys()
    print("----------------SENDER_AFFINE---------------------")
    sender = Sender(cipher)
    sender.set_key(keys[0])
    print("Sender har nøkkel: " + str(sender.get_key()))
    melding = "Blackboard suger"
    crm = sender.operate_cipher(melding)
    print("Sender følgende melding: " + melding)
    print("Kryptert melding: " + crm)
    print("----------------RECEIVER_AFFINE-------------------")
    receiver = Receiver(cipher)
    receiver.set_key(keys[1])
    print("Receiver har nøkkel: " + str(receiver.get_key()))
    print("Receiver har mottat følgende kryptert melding: " + crm)
    mottatt_melding = receiver.operate_cipher(crm)
    print("Dekryptert melding: " + mottatt_melding)
    print("Verifisert: " + str(cipher.verify(melding, keys)))
    print()

def unbreakable():
    cipher = Unbreakable()
    print("----------------SENDER_UNBREAKABLE---------------------")
    keys = cipher.generate_keys()
    print(keys)
    sender = Sender(cipher)
    sender.set_key(keys[0])
    print("Sender har nøkkel: " + str(sender.get_key()))
    melding = "IM PICKLE RICK!!!!!"
    crm = sender.operate_cipher(melding)
    print("Sender følgende melding: " + melding)
    print("Kryptert melding: " + crm)
    print("----------------RECEIVER_UNBREAKABLE-------------------")
    receiver = Receiver(cipher)
    receiver.set_key(keys[1])
    print("Receiver har nøkkel: " + str(receiver.get_key()))
    print("Receiver har mottat følgende kryptert melding: " + crm)
    mottatt_melding = receiver.operate_cipher(crm)
    print("Dekryptert melding: " + mottatt_melding)
    print("Verifisert: " + str(cipher.verify(melding, keys)))
    print()

def rsa():
    cipher = RSA()
    print("----------------SENDER_RSA---------------------")
    keys = cipher.generate_keys()
    sender = Sender(cipher)
    sender.set_key(keys[0])
    print("Sender har nøkkel: " + str(sender.get_key()))
    melding = "Dette ER en TEST!????"
    crm = sender.operate_cipher(melding)
    print("Sender følgende melding: " + melding)
    print("Kryptert melding: " + str(crm))
    print("----------------RECEIVER_RSA-------------------")
    receiver = Receiver(cipher)
    receiver.set_key(keys[1])
    print("Receiver har nøkkel: " + str(receiver.get_key()))
    print("Receiver har mottat følgende kryptert melding: " + str(crm))
    mottatt_melding = receiver.operate_cipher(crm)
    print("Dekryptert melding: " + mottatt_melding)
    print("Verifisert: " + str(cipher.verify(melding, keys)))
    print()

def hacker():
    print("----------------HACKER-----------------------")
    hacker = Hacker()
    cipher = Unbreakable()
    sender = Sender(cipher)
    keys = cipher.generate_keys()
    sender.set_key(keys[0])
    cr_text = sender.operate_cipher("now what is going on")
    print("Meldingen er:", hacker.hackerman(cr_text, cipher))






def main():
    caesar()
    multi()
    affine()
    unbreakable()
    rsa()
    hacker()

main()
