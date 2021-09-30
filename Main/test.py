path = None
userlist = []
last_id = 1
current_user = None
from user import User 



file = open("users", "r") #open the file

line = file.readline() #readline assigned to "line"
while line : #as long as there is a line to read the while will continue
    user_info = line.split(";") #we split the data in "users" by ";" and assign it to "user_info"
    #The next line is used to get informations from the file "users" and make them into an object "User"
    userlist.append(User(user_info[0],user_info[1],user_info[2],user_info[3],user_info[4],user_info[5],user_info[6]))
    last_id = int(user_info[0])+1 #this is to get the id
    line = file.readline() #apply the line so it will stop the while after we read every line
file.close() #close the file

def check_pseudo(userlist, pseudo) : # Check if the pseudo exist inside the file 
        for user in userlist :
            if user.pseudo == pseudo :
                return user
        return False

def check_pseudo_loop(userlist, pseudo) :
        user = False
        while not user :
            user = check_pseudo(userlist, pseudo)
            if not user : 
                print("Select a existing user ! \n")  
                pseudo = input()
        return pseudo 

check_pseudo_loop(userlist, "thoms")