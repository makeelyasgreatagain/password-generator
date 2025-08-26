import string
import random

length = int(input("Please Provide password length: "))
charlist = string.ascii_letters + string.digits + string.punctuation
password = ""

for i in range(length):
    password += random.choice(charlist)

print("Genereted password is: " + password)
