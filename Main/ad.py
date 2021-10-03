from os import close
from colorama import init, deinit 
from user import User 
from getpass import getpass
# import readline  #### DECOMMENT THIS IF YOU USE LINUX
import re, bcrypt
from pyreadline  import Readline; readline = Readline()
from serial import Serial
import sys
from colors import color

class AD : # Class that contains all the def that are needed in AD
    path = None
    userlist = []
    last_id = 1
    current_user = None

    def initiate_users (self) : # Function that read every line of the file "user" and initiate them into the code
        file = open(self.path, "r") # Open the file
        line = file.readline()
        while line : 
            user_info = line.split(";")
            #The next line is used to get informations from the file "users" and make them into an object "User"
            self.userlist.append(User(user_info[0],user_info[1],user_info[2],user_info[3],user_info[4],user_info[5],user_info[6]))
            self.last_id = int(user_info[0])+1 
            line = file.readline()
        file.close() 
        return self.userlist

    def __init__ (self, path) : # This is the first thing that class AD does it starts everything in this function
        self.path = path 
        self.initiate_users() 
        self.login()

############################################ DISPLAY ####################################### 
    
    def print_menu_users(self) : # Display menu
        print("\n")
        color.main("\n ********* Display Menu ********** \n")
        color.prompt("1 : Display all users")
        color.prompt("2 : Display user by login")
        color.prompt("3 : Return to main menu")

    def print_all_users (self) : # Function that print all users present in file 
        for user in self.userlist :
            print(user)

    def display_login(self) : # Print informations of a single user
        color.prompt("\n Give the pseudo to receive all the informations of the user \n")
        pseudo = input("Pseudo   :    ")
        self.find_user(pseudo)
        
    def find_user(self, pseudo) : # Find an user with his pseudo
        for user in self.userlist : 
            if user.pseudo.find(pseudo) == 0 :
                print(user)
                break
        if user.pseudo.find(pseudo) == 0 :
            color.prompt("\nUser was found")
        else :
            color.prompt("\nUser wasn't found")
            
        

############################################ ADD #########################################     


    def add_user (self) : # Function to add an user 
        color.main("\n *********** ADD MENU ************** \n")
        file = open(self.path, "a+")
        if file : 
        
            #### Get the input from the admin and check differents conditions to add a new user, STRIP to erase blank spaces given by the user
            
            first_name = input("Enter the first name of the user   :   ").strip()
            last_name = input("Enter the last name of the user   :   ").strip()
            last_name = last_name.upper()
            email = input("Enter the email : ").strip()
            self.check_email(email)
            pseudo = input("Enter the pseudo of the user   :   ").strip()
            pseudo = self.check_pseudo_loop(pseudo)
            color.warning("****** Remember the Rules : Lenght superior to 8, one capital and small caps, a number and one special char ****** ")
            passwd = getpass("Enter the password of the user   :    \n")
            passwd = passwd.strip()
            passwd = self.check_password(passwd)
            passwd = self.hash_password(passwd)
            status = input("Enter the status of the user   :    ").strip()

            new_user = User(self.last_id, first_name, last_name, email, pseudo, passwd, status)
            new_user.user_id = self.last_id # Get the id of the last user
            self.last_id += 1 # Just add one to get the id pf the new user
            file.write(new_user.format_for_file()) 
            file.close()
            self.userlist.append(new_user) # Add the new user at the end of the file 

            color.success("The user as been added to the system ! ")
       
    
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
                color.warning("\n !!!!! Please select a correct email syntax !!!!!!")
            check = 0
            email = input("Enter the email again   :   ").strip()    
        return check

    def check_existing_email(self, email) : # Check if the email is already used by someone 
        check = True
        with open('users') as f:
            if email in f.read():
                check = False
                color.warning("\n !!!!!! This email is already used !!!!!!! ")
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
                color.warning("\n !!!!!!! This pseudo is already taken !!!!!! ")  
                pseudo = input("pseudo  :").strip()
            else :
                check = True
        return pseudo 
                
    def generate_pseudo(self, fname, name) : # Use this if you want to generate pseudo  
        first_l = fname[0].lower()
        pseudo = first_l + name 
        return pseudo

    def check_password(self, password) : # Function to check if the password if checking all the rules
        check = False
        while check is False:  
            if (len(password)<8):
                break
            elif not re.search("[a-z]", password):
                break
            elif not re.search("[A-Z]", password):
                break
            elif not re.search("[0-9]", password):
                break
            elif not re.search("[_@!%&#?*$]", password):
                break
            elif re.search("\s", password):
                break
            else:
                check = True
                print("Valid Password")
                break
        if check is False:
            color.warning("Not a Valid Password, select an other one\nRemember the Rules : Lenght superior to 8, one capital and small caps, a number and one special char : ")
            password = getpass("Password : ").strip()
        else :
            return password


############################################ MODIFIY ###################################################

    def main_modify(self) : 

        color.main("\n *********** MODIFY MENU ************** \n")

        pseudo_modify = input("Please select the pseudo of the user to modify is informations   :   ").strip()
        user = self.check_pseudo(pseudo_modify)

        if not user :
            color.warning("Please select an existing user")
        else : 
            check_pwd = False
            color.warning("\n ****** If you don't want to change, just press enter to keep the same informations ********* \n")
            fname = self.input_with_prefill("First name of the user : ", user.fname, check_pwd) 
            name = self.input_with_prefill("Last name of the user : ", user.name) 
            name = name.upper()
            
            email = self.input_with_prefill("Email of the user : ", user.email) 
            if email != user.email : email = self.check_email(email)
            
            pseudo = self.input_with_prefill("Pseudo of the user : ", user.pseudo)
            if pseudo != user.pseudo : pseudo = self.check_pseudo_loop(pseudo)
            
            password = getpass("Password of the user : ")
            password = password.strip()
            
            if not password : password = user.password
            else :
                password = self.check_password(password) 
                password = self.hash_password(password)
            
            status = self.input_with_prefill("Status of the user : ", user.status)# Status
            new_user = User(user.user_id, fname, name, email, pseudo, password, status)

            list_users = self.file_to_list() # Create list with all existing user 
            new_users_list = self.new_list(list_users, user.user_id, new_user) # Create new list with new user at the correct position
            self.print_to_file(new_users_list) # Re write in the files

            color.success(" \n !!!!!! Succesfully updated !!!!!! \n ")

    def input_with_prefill(self, prompt, text, check_pwd = False):  # Create an input with prefill informations, check_pwd required only if you want to fill for a pwd
        def hook():
            readline.insert_text(text)
            readline.redisplay()
        readline.set_pre_input_hook(hook)
        
        if check_pwd : 
            result = getpass(prompt) # MAKE THE PASSWORD INVISIBLE
        else : 
            result = input(prompt).strip()
        
        readline.set_pre_input_hook()
        return result
    
    def file_to_list(self) :  # Take the input of the file and put it in a list
        a_file = open("users", "r")
        list_users = []
        
        for line in a_file:
            stripped_line = line.strip()
            line_list = stripped_line.split()
            list_users.append(line_list)
        
        a_file.close()
        return list_users
    
    def new_list(self, list_users, id, new_user) : # New list with the user informations changed 
        i = 0 
        id = int(id)
        id = id - 1
        
        for element in list_users :
            if id == i : 
                list_users[i][0] = new_user.format_for_file() 
                new_str = list_users[i][0].rstrip()  # Do this to avoid blank lines in file 
                list_users[i][0] = new_str
            i += 1 
        
        return list_users

    def print_to_file(self, new_user_list) : # Print a list of users in file
        i = 0
        f = open('users', 'r+')
        f.truncate(0)
        a_file = open("users", "w")
        
        for element in new_user_list:
            elem_to_print = str(element[0])
            a_file.write(elem_to_print + "\n")
            i += 1 
        
        a_file.close()

        ###################### MODIFY PASSWORD FOR USER ###################################

    def modify_update_password(self, pseudo) :

        color.main("\n *********** MODIFY PASSWORD ************** \n")

        user = self.check_pseudo(pseudo)
        password = getpass("Enter your new password, Press enter to use the same   :   ") # MDP
        
        if not password : password = user.password
        else :
            password = self.check_password(password) 
            password = self.hash_password(password)
        
        new_user = User(user.user_id, user.fname, user.name, user.email, pseudo, password, user.status)
        list_users = self.file_to_list() # Create list with all existing user 
        new_users_list = self.new_list(list_users, user.user_id, new_user) # Create new list with new user at the correct position
        self.print_to_file(new_users_list) #Re write in the file
        
        color.success("\n !!!!! Your password has been succesfuly updated !!!!!! \n")


############################################ DELETE ####################################################
    
    def main_delete(self, pseudo) :

        color.main("\n *********** DELETE MENU ************** \n")

        pseudo_delete = input("Enter the pseudo to delete all the informations about the user    :    ").strip()
        line_id = self.find_line_user(pseudo_delete)
        
        if line_id != False : 
            
            if pseudo == pseudo_delete :
                color.warning("Did you really just try to delete yourself ?") # No explaination here 
            else :
                color.success("\n !!!!!! User deleted !!!!!!! \n")
                self.delete_pseudo_line(line_id)
        else :
            color.warning("\n !!!!!! Select an existing pseudo !!!!!! \n")
    
    def delete_pseudo_line(self, line_id) : # Delete the line where the user in 
        a_file = open("users", "r")
        lines = a_file.readlines()
        a_file.close()
        
        del lines[line_id]
        new_file = open("users", "w+")
        
        for line in lines:
            new_file.write(line)

        new_file.close()

    def find_line_user(self, pseudo): # Find in which line of the file the user is 
        i = 0
        check = False
        userlist = self.initiate_users()
        
        for user in userlist :
            if user.pseudo == pseudo :
                check = i
                break
            i +=1
        return check
        
############################################ LOGIN #####################################################     
 
    def login(self) : # Main fonction to login the user inside the program 
        init()
        color.main("\n\n ******* WELCOME ! THIS PROGRAM WAS MADE BY LOEIZ-BI AND BAPTISTE ******** \n\n")
        user = password_check = False 

        while not user : 
            pseudo = input("- Enter your pseudo to login  : ").strip()
            user = self.check_pseudo(pseudo) # Check if the pseudo exist
            if not user : 
                color.warning("\n !!!! Select an existing user !!!!! \n")        
            
        count = 3 
        while True :  
            print()
            password = getpass("- Enter the password  :  ")
            id = self.find_id_user(pseudo)
            passwd = self.find_existing_passwd(id)
            password_check = self.check_passwd(password, passwd) 
            
            if password_check :
                break
            else :
                color.warning("\n !!!!!! Wrong password !!!!!! " + str(count -1) + " more try")
                count -= 1  
            
            if count == 0 :
                quit()
        
        self.current_user = user 
        # Check if the user is admin or simple user
        if user.status.find("admin") == 0 :
            self.main_menu_admin(pseudo)
        else : 
            self.main_menu_users(pseudo) 

    def check_pseudo(self, pseudo) : # Check if the pseudo exist inside the file 
        for user in self.userlist :
            if user.pseudo == pseudo :
                return user
        return False
    
    def find_id_user(self, pseudo) : # Find the id of the given user  
        for user in self.userlist :
            if user.pseudo == pseudo :
                return user.user_id
        return False

    def find_existing_passwd(self, id) : # Return the password of the given user 
        a_file = open("users")
        id = int(id)
        id = id - 1
        line_to_read = [id]
        
        for position, line in enumerate(a_file):
            if position in line_to_read:
                line_file = line

        li = list(line_file.split(";"))
        return li[5]

    def check_passwd(self, passwd, hashed) : # Compare the password given in input with the one existing for the user
        check = bcrypt.checkpw(passwd.encode("utf-8"), hashed.encode("utf-8"))
        return check

################################################### MENU ############################################################

    def main_menu_users(self, pseudo): # Menu controller for a simple user
        color.main("\n\n ********Welcome on the user interface !*********** ")
        
        while True : # While loop to keep the user in the program 
            color.main("\n *********** MAIN MENU **************")
            self.show_menu_user() # Print the menu  
            command = input().strip() # Input from user to select an action
            
            if command == "1" : 
                self.display_current_user()  
            elif command == "2" :
                self.modify_update_password(pseudo) # TODO
            elif command == "0" :
                color.main("\n ********** Good bye !  ************")
                deinit()
                break
            else :
                print("Choose a valid number !")

    def display_current_user (self) : #display the current user
        print(self.current_user)

    def main_menu_admin(self, pseudo) :   # Menu controller for the admin
        color.main("\n\n ********Welcome on the admin interface !*********** ")
        
        
        while True : # While loop to keep the user in the program 
            color.main("\n *********** MAIN MENU **************")
            self.show_menu_admin() # Print the menu
            command = input("\nYour choice   :   ").strip() # Input from user to select an action
            
            if command == "1" : 
                self.display_main_display()  
            elif command == "2" :
                self.add_user()  
            elif command == "3" :
                self.main_delete(pseudo)  
            elif command == "4" :
                self.main_modify()  
            elif command == "5" :
                self.modify_update_password(pseudo) 
            elif command == "0" :
                color.main("\n ********** Good bye !  ************")
                deinit()
                break
            else :
                print("Choose a valid number !")

    def show_menu_admin(self) : # Display menu for the admin 
        print("\n")
        color.prompt("Please enter a number to select an action : \n")
        color.prompt("1 : Display menu")
        color.prompt("2 : Add a user")
        color.prompt("3 : Delete a user")
        color.prompt("4 : Modify the informations of a user")
        color.prompt("5 : Modify your password")
        color.prompt("0 : Leave the program")

    def show_menu_user(self) : # Display menu for the simple users
        print("\n")
        color.prompt("Please enter a number to select an action : \n")
        color.prompt("1 : Display my informations")
        color.prompt("2 : Update my password")
        color.prompt("0 : Leave the program")

    def display_main_display(self) : # Main display menu
        self.print_menu_users() 
        d_command = input("\nYour choice   :   ").strip() # Input from user to select an action

        while d_command != "3" : 
            if d_command == "1" : 
                self.print_all_users()
            elif d_command == "2" : 
                self.display_login()

            self.print_menu_users()
            d_command = input().strip()
            
