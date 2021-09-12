def find_key_pseudo(users, pseudo) :
    id = False
    for p_id, p_info in users.items():
        for key in p_info:
            if pseudo == p_info[key] : 
                id = p_id
                break
    return id

def check_pseudo(users, pseudo) :
    pseudo_check = False
    for p_id, p_info in users.items():
        for key in p_info:
            if pseudo == p_info[key] : 
                pseudo_check = p_info
                break
    return pseudo_check


def check_pwd(users, pseudo_list, pwd) :
    pwd_check = False
    if pwd == pseudo_list["pwd"] :
        pwd_check = True
    return pwd_check