from user import User #import User from user

class AD : #Class that contains all the def that are needed in AD
    path = None
    userlist = []
    last_id = 1
    current_user = None

    def print_all_users (self) : # function that print all users
        for user in self.userlist :
            print(user)

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

    def add_user (self) : # this function is used to add a user
        file = open(self.path, "a+")#this open the file and gives us the right to write in it
        if file : 
            #The next line is used to get the input from the admin user and put them into "new_user"
            new_user = User(self.last_id, input("name :"),input("fname :"),input("email :"),input("pseudo :"),input("password :"),input("status :"))
            new_user.user_id = self.last_id #we get the last_id we added so we know which one the next will get
            self.last_id += 1 #we give the new user the last id (3 for example +1 )
            file.write(new_user.format_for_file()) #this is to write a new line with all the informations in the file "users"
            file.close()#close the file
            self.userlist.append(new_user) #this add the new_user to the ongoing code 

    def login(self) : # Main fonction to login the users inside the program 

        user = password_check = False #we assign false to user and password_check

        while True : #infinite while
            while not user : # Check if the pseudo exist 
                pseudo = input("Enter your pseudo \n") #attribute the input to pseudo variable
                user = self.check_pseudo(pseudo) #we check the pseudo with the function "check_pseudo" 
                if not user : #if there is no pseudo in users that correspond to the one entered
                    print("Select a existing user ! \n")          
            count = 3 #count ultil "you are disconnected"

            while not password_check and count >= 1 :  # Check if the password exist and count is higher or equal to 1
                password = input("Now enter the password \n")
                password_check = self.check_password(password, user) #we check the password with the function "check_password"
                if not password_check : #if the password entered isn't right 
                    count -= 1 #1 less chance of login before you get disconnected
                    print(f"incorrect password | Try left : {count} ")#print numbers of try left
            if count == 0 : #if count go to zero then disconnect
                print("\n~~~~~~~~~~ You are now disconnected ~~~~~~~~~~") 
                break #break out of the code and get disconnected
            self.current_user = user 
            if user.status.find("admin") == 0 : #if the status of the user is admin then we go to main menu admin 
                self.main_menu_admin()
            else : # else we go to main menu users
                self.main_menu_users() 

            break #exit from the infinite while

    def main_menu_users(self): # Menu controller for a simple user
        print("Welcome to the users interface !")
        
        while True : # While loop to keep the user in the program | redirect to other functions
            self.show_menu_user() #use the function show menu user  
            command = input() # menu variable to choose where to go
            if command == "1" : 
                self.display_current_user()  
            elif command == "2" :
                modify.update_password()
            elif command == "0" :
                print ("Good bye ;)")
                break
            else :
                print("Choose a valid number !")

    def display_current_user (self) : #display the current user
        print(self.current_user)

    def main_menu_admin(self) :   # Menu controller of an admin  
        print("Welcome to your main program !")
        
        while True : # While loop to keep the user in the program | redirect to other functions
            self.show_menu_admin() #use the function show menu admin  
            command = input() # menu variable to choose where to go
            if command == "1" : 
                self.display_main_display()  
            elif command == "2" :
                self.add_user()  
            elif command == "3" :
                delete.main_delete()  
            elif command == "4" :
                modify.main_modify()  
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

    def show_menu_user(self) : # Display menu for the users 
        print("\n")
        print("Please enter a number to select an action :")
        print("1 : Display my informations")
        print("2 : Update my password")
        print("0 : Leave the program")

    def check_pseudo(self, pseudo) : # used to check pseudo
        for user in self.userlist :
            if user.pseudo == pseudo :
                return user
        return False

    def check_password(self, password, user) : # used to check password
        if user.password == password :
            return True
        return False

    def display_main_display(self) : # main display menu
        self.print_menu_users() #print menu users
        d_command = input() # menu variable to choose where to go

        while d_command != "3" : 
            if d_command == "1" : 
                self.print_all_users()
            elif d_command == "2" : 
                self.display_login()

            self.print_menu_users()
            d_command = input()
            
    def print_menu_users(self) :#print menu users
        print("\n")
        print("1 : Display all users")
        print("2 : Display user by login")
        print("3 : Return to main menu")

    def display_login(self) : # Print the users select by the admin 
        pseudo = input("Give the pseudo to receive all the informations of the user \n")
        self.find_user(pseudo)
        
    def find_user(self, pseudo) : # used to find a user with is pseudo in the code
        for user in self.userlist : 
            if user.pseudo.find(pseudo) == 0 :
                print(user)
                return 
        print("user doesn't exist") 