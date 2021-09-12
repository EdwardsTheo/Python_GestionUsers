def initate_dict() : # Initiate the dico 
    users = {1: {'name': 'John', 'fname' : 'Admin', 'email' : 'btheo@myges.fr', 'pseudo' : 'admin', 'pwd' : "blbl", 'status' : 'admin'},
          2: {'name': 'Dupont', 'fname' : 'Pierre', 'email' : 'pdupont@myges.fr', 'pseudo' : 'pdupont', 'pwd' : "pass", 'status' : 'user'}}
    
    return users


def find_key_pseudo(users, pseudo) :
    id = False
    for p_id, p_info in users.items():
        for key in p_info:
            if pseudo == p_info[key] : 
                id = p_id
                break
    return id


def display_login(users) : # Print the users select by the admin 
    pseudo = input("Give the pseudo to receive all the informations of the user \n")
    keyF = find_key_pseudo(users, pseudo)  # Check is the pseudo exist and return the key 

    if keyF != False : 
        print("\nInformations about the users : ", pseudo, "\n")
        for p_id, p_info in users.items(): 
            for key in p_info:
                if keyF == p_id :
                    print(key, " : ", p_info[key])

    else :
        print("\nNo user exist with this pseudo ! Please select an existing user")

users = initate_dict()
display_login(users)