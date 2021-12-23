import time
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
        return None

    else:
        return session


def logout(session: requests.Session):
    session.close()


def checkauth(session: requests.Session, gall_id):
    url = "https://gall.dcinside.com/mgallery/management"
    params = {"id": gall_id}

    response = session.get(url, params=params)
    if response.status_code != 200:
        return False

    return not ("replace" in response.text)


def get_cur_date():
    now = time.localtime()
    current_date = "%04d-%02d-%02d" \
        % (now.tm_year, now.tm_mon, now.tm_mday)

    return current_date


def get_cur_time():
    now = time.localtime()
    current_time = "%04d-%02d-%02d %02d:%02d:%02d" \
        % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)

    return current_time
