def banned_users():

    banned_user_list = []
    
    f = open("banned_users.txt", mode='r')
    for line in f:
        currentline = line.split(",")
        for i in currentline:
            banned_user_list.append(i)

    f.close()
    return banned_user_list

if __name__ == "__main__":

    lists = banned_users()
    print(lists)

    pass