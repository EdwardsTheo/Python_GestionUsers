# Import all files needed to run the program 

import add
import delete
import display
import modify



def main_menu(users) :   # Main menu to select action
    
    print("Welcome to your main program !")
    show_menu()
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
        
        show_menu()
        command = input()

def show_menu() : # Display menu for the users 
    print("\n")
    print("Please enter a number to select an action :")
    print("1 : Display menu")
    print("2 : Add a user")
    print("3 : Delete a user")
    print("4 : Modify the informations of a user")
    print("0 : Leave the program")


# modify.print_exemple()
users = add.initate_dict() # Create the dictionary with two users inside, one admin, one simple user
main_menu(users)

    