# File that keep the functions to add user in the dictonary

def initate_dict() : # Initiate the dico 
    users = {1: {'name': 'John', 'fname' : 'Admin', 'email' : 'btheo@myges.fr', 'pseudo' : 'admin', 'pwd' : "admin", 'status' : 'admin'},
          2: {'name': 'Dupont', 'fname' : 'Pierre', 'email' : 'pdupont@myges.fr', 'pseudo' : 'pdupont', 'pwd' : "user", 'status' : 'pdupont'}}
    
    return users

users = initate_dict()