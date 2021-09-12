# Import all files needed to run the program 

import add
import delete
import display
import modify
import function

def main_menu_users(users): # Menu controller for a simple user
    print("Welcome to the users interface !")
    show_menu_user()

    command = input()
    
    while command != "0" : # While loop to keep the user in the program 
        if command == "1" : 
            display.users_display(users)  
        elif command == "2" :
            modify.update_pwd(users)  
        else :
            print("Choose a valid number !")

        show_menu_user()    
        command = input()

def main_menu_admin(users) :   # Menu controller of an admin
    
    print("Welcome to your main program !")
    show_menu_admin()
    command = input()
    
    while command != "0" : # While loop to keep the user in the program 
        if command == "1" : 
            display.main_display(users)  
        elif command == "2" :
            add.main_add()  
        elif command == "3" :
            delete.main_delete()  
        elif command == "4" :
            modify.main_modify()  
        elif command == "0" :
            print("Good bye :)")
        else :
            print("Choose a valid number !")
        
        show_menu_admin()
        command = input()

def show_menu_admin() : # Display menu for the admin 
    print("\n")
    print("Please enter a number to select an action :")
    print("1 : Display menu")
    print("2 : Add a user")
    print("3 : Delete a user")
    print("4 : Modify the informations of a user")
    print("0 : Leave the program")

def show_menu_user() : # Display menu for the users 
    print("\n")
    print("Please enter a number to select an action :")
    print("1 : Display my informations")
    print("2 : Update my password")

def login() : # Main fonction to login the users inside the program 
    users = add.initate_dict() # Create the dictionary with two users inside, one admin, one simple user
    
    check = False
    pseudo = input("Please enter your pseudo \n")
    pseudo_check = function.check_pseudo(users, pseudo)  # Check if the pseudo exist 

    if pseudo_check != False : 
        pwd = input("Now enter the password \n")
        pwd_check = function.check_pwd(users, pseudo_check, pwd)  # Check if the password exist
        count = 3
        while count != 1 :
            if pwd_check != False : 
                if pseudo_check["status"] == "admin" :
                    main_menu_admin(users)
                else : 
                    main_menu_users(users)
                count = 3
            else : 
                count -= 1 
                print('Please enter the right password', count, "chances left")
                pwd = input("Enter the password \n")
                pwd_check = function.check_pwd(users, pseudo_check, pwd)  # Check if the password exist
    else : 
        print("Please select a existing user !")

login()

    