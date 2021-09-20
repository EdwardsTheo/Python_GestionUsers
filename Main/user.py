class User : #Creation of User class
    name = ""
    fname = ""
    email = ""
    pseudo = ""
    password = ""
    status = ""
    user_id = 1 #default id
     
    def __init__ (self, user_id, name, fname, email, pseudo, password, status) : #initiate the User class
        self.user_id = user_id
        self.name = name
        self.fname = fname
        self.email = email
        self.pseudo = pseudo
        self.password = password
        self.status = status

    def format_for_file (self) : #makes the format correct fr file
        return f"{self.user_id};{self.name};{self.fname};{self.email};{self.pseudo};{self.password};{self.status}\n"

    def __str__ (self) : #change every user info to a string
        return f"\n\nid : {self.user_id} \nname : {self.name} \nfname : {self.fname} \nemail : {self.email} \npseudo : {self.pseudo} \npassword : {self.password} \nstatus : {self.status}\n"
    
    