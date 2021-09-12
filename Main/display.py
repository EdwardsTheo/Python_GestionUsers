# File that keep the functions for displaying all the users in the in the dictonary

import csv
import add
import delete
import display
import function
import modify

def main_display(users) :

    print_menu_users()

    d_command = input()

    while d_command != "3" :
        if d_command == "1" : 
            display_all(users)
        elif d_command == "2" : 
            display_login(users)

        print_menu_users()
        d_command = input()

       
def print_menu_users() :
    print("\n")
    print("1 : Display all users")
    print("2 : Display user by login")
    print("3 : Return to main menu")

def display_all(users) : # Display all the users present in the dictionary 'users'
    for p_id, p_info in users.items():
        print("\nPerson ID:", p_id)
        for key in p_info:
            print(key, " : ", p_info[key])

def display_login(users) : # Print the users select by the admin 
    pseudo = input("Give the pseudo to receive all the informations of the user \n")
    key = function.find_key_pseudo(users, pseudo)  # Check is the pseudo exist and return the key 

    if key != False : 
        print(key, " : ", users[key])
    else :
        print("\n No user exist with this pseudo ! Please select an existing user")




