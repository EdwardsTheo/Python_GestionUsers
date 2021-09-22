## FILE TO TEST THE PASSWORD CHECKING !!!!!!!!!! NOT USED IN THE MAIN PROGRAM

a_file = open("users")
lines_to_read = [0]

for position, line in enumerate(a_file):
    if position in lines_to_read:
        line_file = line

print(type(line_file))
li = list(line_file.split(";"))

print(li[5])

a_file.close()

# FIND ID OF USER 

def return_id_user(self, pseudo) : 
        check = True
        with open('users') as f:
            if pseudo in f.read():
                print(pseudo)
                check = False
            return check
