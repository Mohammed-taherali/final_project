# lst = ["a","b","c"]

# print(lst)
# t = ""
# print(t.strip().upper())
# lst = []

# print(lst)

# t = "fas"

# print(float(t))

# abcd = "None"

# if abcd:
#     print("hi")

# else:
#     print("BYE!")

from werkzeug.security import generate_password_hash,check_password_hash

hash_pass = generate_password_hash("Mohammed")
print(hash_pass)
# print(check_password_hash(hash_pass, "mohammed"))

print(check_password_hash("pbkdf2:sha256:260000$wSkbU8M4q5mwpBTr$ace9fa7841a7bb058f1df4126157e6f1a5c0782b9080cc0fb5bb3a49571e0763", "jhalrapatan420"))