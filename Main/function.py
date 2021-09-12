def find_key_pseudo(users, pseudo) :
    id = False
    for p_id, p_info in users.items():
        for key in p_info:
            if pseudo == p_info[key] : 
                id = p_id
                break
    return id