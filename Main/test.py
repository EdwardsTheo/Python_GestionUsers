import bcrypt

passwd = "secret"
hashed = '$2b$12$VdNn/ZyWs0Z9Tk0yaryZd.ClB8usBY3oDzhp.quctNuJJSdNvuQTG'

check = bcrypt.checkpw(passwd.encode("utf-8"), hashed.encode("utf-8"))
print(check)


