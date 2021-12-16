import requests
from bs4 import BeautifulSoup


def login(user_id, pw):

    url = "https://dcid.dcinside.com/join/member_check.php"

    session = requests.session()
    session.headers = {
        "X-Requested-With": "XMLHttpRequest",
        "Referer": "https://www.dcinside.com/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36"
    }

    soup = BeautifulSoup(
        requests.get("https://www.dcinside.com/").text, features="html.parser"
    )
    loginForm = soup.find("form", attrs={"id": "login_process"})
    auth = loginForm.find_all("input", attrs={"type": "hidden"})[2]

    login_data = {
        "s_url": "//www.dcinside.com/",
        "ssl": "Y",
        auth["name"]: auth["value"],
        "user_id": user_id,
        "pw": pw,
    }

    response = session.post(url, data=login_data)
    if "history.back(-1);" in response.text:
        exit()

    else:
        return session


def logout(session: requests.Session):
    session.close()


def check_auth(session: requests.Session, gall_id):

    url = "https://gall.dcinside.com/mgallery/management"
    params = {"id": gall_id}

    response = session.get(url, params=params)
    return not ("replace" in response.text)

def banned_users():

    banned_user_list = []

    f = open("banned_users.txt", mode="r")
    for line in f:
        currentline = line.split(",")
        for i in currentline:
            banned_user_list.append(i)

    f.close()
    return banned_user_list

def auth():

    f = open("auth.txt", mode="r")
    line = f.readline().split(" ")
    user_id, user_pw = line

    return user_id, user_pw
