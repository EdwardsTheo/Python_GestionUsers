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
            
            first_name = input("Enter the first name of the user : ")
            last_name = input("Enter the last name of the user : ")
            email = input("Enter the email : ")
            self.check_email(email)
            pseudo = input("Enter the pseudo of the user : ")
            pseudo = self.check_pseudo_loop(pseudo)
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
                pseudo = input()
            else :
                check = True
        return pseudo 
                


############################################ MODIFIY ###################################################
# Enter code here for modify function

############################################ DELETE ####################################################
    
    def main_delete(self, pseudo) :
        pseudo_delete = input("Enter the pseudo to delete all the informations about the user \n")
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
        print(line_id)
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
            pseudo = input("Enter your pseudo \n") 
            user = self.check_pseudo(pseudo) # Check if the pseudo exist
            if not user : 
                print("Select a existing user ! \n")          
            
        count = 3 
        while True :  
            print()
            password = input("Now enter the password \n")
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
        with open('users') as f:
            lines = f.read().splitlines()
        i = 0
        for element in lines :
            if pseudo in element :
                break
            i += 1 
        return i

    def find_existing_passwd(self, id) :
        a_file = open("users")
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

    def main_menu_admin(self, pseudo) :   # Menu controller for the admin
        print("Welcome to your main program !")
        
        while True : # While loop to keep the user in the program 
            self.show_menu_admin() # Print the menu
            command = input() # Input from user to select an action
            if command == "1" : 
                self.display_main_display()  
            elif command == "2" :
                self.add_user()  
            elif command == "3" :
                self.main_delete(pseudo)  # TODO
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