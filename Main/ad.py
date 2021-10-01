from os import close
import bcrypt
from user import User 
import re
from getpass import getpass
import readline

class AD : # Class that contains all the def that are needed in AD
    path = None
    userlist = []
    last_id = 1
    current_user = None

    def initiate_users (self) : # Function that read every line of the file "user" and initiate them into the code
        file = open(self.path, "r") #open the file
        line = file.readline() #readline assigned to "line"
        while line : #as long as there is a line to read the while will continue
            user_info = line.split(";") #we split the data in "users" by ";" and assign it to "user_info"
            #The next line is used to get informations from the file "users" and make them into an object "User"
            self.userlist.append(User(user_info[0],user_info[1],user_info[2],user_info[3],user_info[4],user_info[5],user_info[6]))
            self.last_id = int(user_info[0])+1 #this is to get the id
            line = file.readline()#apply the line so it will stop the while after we read every line
        file.close() #close the file
        return self.userlist

    def __init__ (self, path) : #This is the first thing that class AD does it starts everything in this function
        self.path = path #make the path known
        self.initiate_users() #start the function initiate users
        self.login() #start the function login

############################################ DISPLAY ####################################### 
    
    def print_all_users (self) : # function that print all users
        for user in self.userlist :
            print(user)

    def display_login(self) : # Print informations for a single users
        pseudo = input("Give the pseudo to receive all the informations of the user \n")
        self.find_user(pseudo)
        
    def find_user(self, pseudo) : # Find an user with his pseudo
        for user in self.userlist : 
            if user.pseudo.find(pseudo) == 0 :
                return 
            else :
                print("user doesn't exist") 

############################################ ADD #########################################     


    def add_user (self) : # Function to add an user 
        file = open(self.path, "a+")
        if file : 
        
            #### Get the input from the admin and check differents conditions to add a new user
            
            first_name = input("Enter the first name of the user : ").strip
            last_name = input.upper("Enter the last name of the user : ").strip
            email = input("Enter the email : ").strip
            self.check_email(email)
            pseudo = input("Enter the pseudo of the user : ").strip
            pseudo = self.check_pseudo_loop(pseudo)
            passwd = getpass("Enter the password of the user : \n Remember the Rules : Lenght superior to 8, one capital and small caps, a number and one special char").strip
            passwd = self.check_password(passwd)
            passwd = self.hash_password(passwd)
            status = input("Enter the status of the user : ").strip

            new_user = User(self.last_id, first_name, last_name, email, pseudo, passwd, status)
            new_user.user_id = self.last_id # Get the id of the last user
            self.last_id += 1 # Just add one to get the id for the new user
            file.write(new_user.format_for_file()) 
            file.close()
            self.userlist.append(new_user) # Add the new user at the end of the file 
       
    
    def check_email (self, email) :
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'  # Regex to check for the email syntax
        check = 0

        while check != 2 : 
            if(re.fullmatch(regex, email)):
                check += 1
                check_exist = self.check_existing_email(email)  
                if check_exist == True : 
                    break
            else :
                print("please select a correct email syntax")
            check = 0
            email = input("Enter the email again : ").strip    
        return check

    def check_existing_email(self, email) : # Check if the email is already used by someone 
        check = True
        with open('users') as f:
            if email in f.read():
                check = False
                print("This email is already used !")
            return check
        
    def hash_password(self, passwd) : # Hash the password for the user
        passwd = passwd.encode("utf-8")
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(passwd, salt)
        hashed = hashed.decode("utf-8")
        return hashed

    def check_pseudo_loop(self, pseudo) :
        check = False
        while check != True :
            user = self.check_pseudo(pseudo)
            if user : 
                print("This pseudo is already taken, choose an other !")  
                pseudo = input().strip
            else :
                check = True
        return pseudo 
                
    def generate_pseudo(self, fname, name) : # Use this if you want to generate pseudo automaticly 
        first_l = fname[0].lower()
        pseudo = first_l + name 
        return pseudo

    def check_password(self, password) :
        check = 0
        while True:  
            if (len(password)<8):
                check = -1
                break
            elif not re.search("[a-z]", password):
                check = -1
                break
            elif not re.search("[A-Z]", password):
                check = -1
                break
            elif not re.search("[0-9]", password):
                check = -1
                break
            elif not re.search("[_@$]", password):
                check = -1
                break
            elif re.search("\s", password):
                check = -1
                break
            else:
                check = 0
                print("Valid Password")
                break
        if check == -1:
            password = getpass("Not a Valid Password, select an other one").strip
        else :
            return password


############################################ MODIFIY ###################################################

    def main_modify(self) : 
        pseudo_modify = input("Please select the pseudo of the user to modify is informations \n").strip
        user = self.check_pseudo(pseudo_modify)
        if not user :
            print("Please select an existing user")
        else : 
            check_pwd = False
            print("If you don't want to change, just press enter \n")
            fname = self.input_with_prefill("First name of the user : ", user.fname) # First Name 
            name = self.input_with_prefill("Last name of the user : ", user.name) # Last Name 
            name = name.upper()
            email = self.input_with_prefill("Email of the user : ", user.email) # Email
            if email != user.email : email = self.check_email(email)
            pseudo = self.input_with_prefill("Pseudo of the user : ", user.pseudo)# Pseudo 
            if pseudo != user.pseudo : pseudo = self.check_pseudo_loop(pseudo)
            password = getpass("Password of the user : ")# MDP
            if not password : password = user.password
            else : password = self.hash_password(password)
            status = self.input_with_prefill("Status of the user : ", user.status)# Status
            new_user = User(user.user_id, fname, name, email, pseudo, password, status)

            # Create list with all existing user 
            list_users = self.file_to_list()
            # Create new list with new user at the correct position
            new_users_list = self.new_list(list_users, user.user_id, new_user)
            # Re write in the files
            self.print_to_file(new_users_list)

# Pute the line at the exact place

    def input_with_prefill(self, prompt, text, check_pwd = False):
        def hook():
            readline.insert_text(text)
            readline.redisplay()
        readline.set_pre_input_hook(hook)
        if check_pwd : 
            result = getpass(prompt) # MAKE THE PASSWORD INVISIBLE
        else : result = input(prompt).strip
        readline.set_pre_input_hook()
        return result
    
    def file_to_list(self) :
        a_file = open("users", "r")
        list_users = []
        for line in a_file:
            stripped_line = line.strip()
            line_list = stripped_line.split()
            list_users.append(line_list)
        a_file.close()
        return list_users
    
    def new_list(self, list_users, id, new_user) :
        i = 0 
        id = int(id)
        id = id - 1
        for element in list_users :
            if id == i : 
                list_users[i][0] = new_user.format_for_file() 
                list_users[i] = list(map(str.strip, list_users[i]))
            i += 1 
        return list_users

    def print_to_file(self, new_user_list) : 
        i = 0
        f = open('users', 'r+')
        f.truncate(0)
        a_file = open("users", "w")
        for element in new_user_list:
            elem_to_print = str(element[0])
            a_file.write(elem_to_print + "\n")
            i += 1 
        a_file.close()
    

############################################ DELETE ####################################################
    
    def main_delete(self, pseudo) :
        pseudo_delete = input("Enter the pseudo to delete all the informations about the user \n").strip
        line_id = self.find_line_user(pseudo_delete)
        if line_id != False : 
            if pseudo == pseudo_delete :
                print("Did you really just try to delete yourself ?")
            else :
                print("\n User deleted")
                self.delete_pseudo_line(line_id)
        else :
            print("Select an existing pseudo !")
    
    def delete_pseudo_line(self, line_id) :
        a_file = open("users", "r")
        lines = a_file.readlines()
        a_file.close()
        
        del lines[line_id]
        new_file = open("users", "w+")
        
        for line in lines:
            new_file.write(line)

        new_file.close()

    def find_line_user(self, pseudo):
        i = 0
        check = False
        userlist = self.initiate_users()
        for user in userlist :
            if user.pseudo == pseudo :
                check = i
                break
            i +=1
        return check
        

# Enter code here for delete function
############################################ LOGIN #####################################################     
 
    def login(self) : # Main fonction to login the user inside the program 

        user = password_check = False 

        while not user : 
            pseudo = input("Enter your pseudo \n").strip 
            user = self.check_pseudo(pseudo) # Check if the pseudo exist
            if not user : 
                print("Select a existing user ! \n")          
            
        count = 3 
        while True :  
            print()
            password = getpass("Now enter the password \n")
            id = self.find_id_user(pseudo)
            passwd = self.find_existing_passwd(id)
            password_check = self.check_passwd(password, passwd) 
            if password_check :
                break
            else :
                print("Wrong password " + str(count -1) + " more try")
                count -= 1  
            if count == 0 :
                quit()
        
        self.current_user = user 
        # Check if the user is admin or simple user
        if user.status.find("admin") == 0 :
            self.main_menu_admin(pseudo)
        else : 
            self.main_menu_users() 

    def check_pseudo(self, pseudo) : # Check if the pseudo exist inside the file 
        for user in self.userlist :
            if user.pseudo == pseudo :
                return user
        return False
    
    def find_id_user(self, pseudo) :
        for user in self.userlist :
            if user.pseudo == pseudo :
                return user.user_id
        return False

    def find_existing_passwd(self, id) :
        a_file = open("users")
        id = int(id)
        id = id - 1
        line_to_read = [id]
        for position, line in enumerate(a_file):
            if position in line_to_read:
                line_file = line

        li = list(line_file.split(";"))
        return li[5]

    def check_passwd(self, passwd, hashed) : 
        check = bcrypt.checkpw(passwd.encode("utf-8"), hashed.encode("utf-8"))
        return check

################################################### MENU ############################################################

    def main_menu_users(self): # Menu controller for a simple user
        print("Welcome to the users interface !")
        
        while True : # While loop to keep the user in the program 
            self.show_menu_user() # Print the menu  
            command = input().strip # Input from user to select an action
            if command == "1" : 
                self.display_current_user()  
            elif command == "2" :
                modify.update_password() # TODO
            elif command == "0" :
                print ("Good bye ;)")
                break
            else :
                print("Choose a valid number !")

    def display_current_user (self) : #display the current user
        print(self.current_user)

    def main_menu_admin(self, pseudo) :   # Menu controller for the admin
        print("Welcome to your main program !")
        
        while True : # While loop to keep the user in the program 
            self.show_menu_admin() # Print the menu
            command = input().strip # Input from user to select an action
            if command == "1" : 
                self.display_main_display()  
            elif command == "2" :
                self.add_user()  
            elif command == "3" :
                self.main_delete(pseudo)  # TODO
            elif command == "4" :
                self.main_modify()  # TODO
            elif command == "0" :
                print("Good bye :)")
                break
            else :
                print("Choose a valid number !")

    def show_menu_admin(self) : # Display menu for the admin 
        print("\n")
        print("Please enter a number to select an action :")
        print("1 : Display menu")
        print("2 : Add a user")
        print("3 : Delete a user")
        print("4 : Modify the informations of a user")
        print("0 : Leave the program")

    def show_menu_user(self) : # Display menu for the simple users
        print("\n")
        print("Please enter a number to select an action :")
        print("1 : Display my informations")
        print("2 : Update my password")
        print("0 : Leave the program")

    def display_main_display(self) : # Main display menu
        self.print_menu_users() 
        d_command = input().strip

        while d_command != "3" : 
            if d_command == "1" : 
                self.print_all_users()
            elif d_command == "2" : 
                self.display_login()

            self.print_menu_users()
            d_command = input().strip
            
    def print_menu_users(self) : # Display menu
        print("\n")
        print("1 : Display all users")
        print("2 : Display user by login")
        print("3 : Return to main menu")