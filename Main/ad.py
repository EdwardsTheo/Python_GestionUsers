import bcrypt
from user import User 
import re

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
                print(user)
                return 
        print("user doesn't exist") 

############################################ ADD #########################################     


    def add_user (self) : # Function to add an user 
        file = open(self.path, "a+")
        if file : 
        
            #### Get the input from the admin and check differents conditions to add a new user
            
            first_name = input("Enter the first name of the user : ")
            last_name = input("Enter the last name of the user : ")
            email = input("Enter the email : ")
            self.check_email(email)
            pseudo = input("Enter the pseudo of the user : ")
            self.check_pseudo(pseudo)
            passwd = input("Enter the password of the user : ")
            passwd = self.hash_password(passwd)
            status = input("Enter the status of the user : ")

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
            email = input("Enter the email again : ")    
        return check

    def check_existing_email(self, email) : # Check if the email is already used by someone 
        check = True
        with open('users') as f:
            if email in f.read():
                print(email)
                check = False
                print("This email is already used !")
            return check
        
    def check_pseudo(self, pseudo) : # Same as the email but for the pseudo
        check = 0
        while check != 1 :
            check_exist = self.check_existing_pseudo(pseudo)
            if check_exist == True :
                check += 1 
            else :
                pseudo = input("This pseudo is already used please select an other : ")
    
    def check_existing_pseudo(self, pseudo) :
                check = True
                with open('users') as f:
                    if pseudo in f.read():
                        check = False
                    return check     
    
    def hash_password(self, passwd) : # Hash the password for the user
        passwd = passwd.encode("utf-8")
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(passwd, salt)
        return hashed


############################################ LOGIN #####################################################     
 
    def login(self) : # Main fonction to login the user inside the program 

        user = password_check = False 

        while True : 
            while not user : 
                pseudo = input("Enter your pseudo \n") 
                user = self.check_pseudo(pseudo) # Check if the pseudo exist
                if not user : 
                    print("Select a existing user ! \n")          
            count = 3 

            while not password_check and count >= 1 :  # !!!!!!!!!!!!! The password checking phase is not finished !!!!!!!!!
                print()
                password = input("Now enter the password \n")
                
                password_check = self.check_passwd(password) # !!!!!!! Function Not usable !!!!!!!!! Auto login
                if not password_check : 
                    count -= 1 
                    print(f"incorrect password | Try left : {count} ") 
            if count == 0 : 
                print("\n~~~~~~~~~~ You are now disconnected ~~~~~~~~~~") 
                break 
            self.current_user = user 
            # Check if the user is admin or simple user
            if user.status.find("admin") == 0 :
                self.main_menu_admin()
            else : 
                self.main_menu_users() 

            break #exit from the infinite while

    def check_pseudo(self, pseudo) : # Check if the pseudo exist inside the file 
        for user in self.userlist :
            if user.pseudo == pseudo :
                return user
        return False

    def check_passwd(self, passwd) : # Function to check the password when the user connect !!!!!! NOT FINISHED !!!!!!!!!
        check = False
        passwd = passwd.encode("utf-8")
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(passwd, salt)

        if bcrypt.checkpw(passwd, hashed):
            check = True
        return check

################################################### MENU ############################################################

    def main_menu_users(self): # Menu controller for a simple user
        print("Welcome to the users interface !")
        
        while True : # While loop to keep the user in the program 
            self.show_menu_user() # Print the menu  
            command = input() # Input from user to select an action
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

    def main_menu_admin(self) :   # Menu controller for the admin
        print("Welcome to your main program !")
        
        while True : # While loop to keep the user in the program 
            self.show_menu_admin() # Print the menu
            command = input() # Input from user to select an action
            if command == "1" : 
                self.display_main_display()  
            elif command == "2" :
                self.add_user()  
            elif command == "3" :
                delete.main_delete()  # TODO
            elif command == "4" :
                modify.main_modify()  # TODO
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
        d_command = input() 

        while d_command != "3" : 
            if d_command == "1" : 
                self.print_all_users()
            elif d_command == "2" : 
                self.display_login()

            self.print_menu_users()
            d_command = input()
            
    def print_menu_users(self) : # Display menu
        print("\n")
        print("1 : Display all users")
        print("2 : Display user by login")
        print("3 : Return to main menu")