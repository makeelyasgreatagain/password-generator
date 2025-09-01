import string
import random

charlist = string.ascii_letters + string.digits + string.punctuation
password = ""

while True:
    length = int(input("Please Provide password length: "))
    if length >= 8:
        for i in range(length):
            password += random.choice(charlist)
        print("Genereted password is: " + password)
        break
    else:
        print("I can't generate shorter than 8 characters password due to security reasons.")
