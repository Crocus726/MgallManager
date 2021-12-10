import requests
import threading
import schedule
import datetime
import time
from bs4 import BeautifulSoup

def login():

    url = 'https://dcid.dcinside.com/join/member_check.php'

    session = requests.session()
    session.headers = {
        "X-Requested-With" : "XMLHttpRequest",
        'Referer':'https://www.dcinside.com/',
        'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'
    }

    soup = BeautifulSoup(requests.get("https://www.dcinside.com/").text, features='html.parser')
    loginForm = soup.find('form', attrs={'id': 'login_process'})
    auth = loginForm.find_all('input', attrs = {'type':'hidden'})[2]

    user_id = input("아이디 입력 : ")
    pw = input("비밀번호 입력 : ")


    login_data = {
        's_url': '//www.dcinside.com/',
        'ssl': 'Y',
        auth['name'] : auth['value'],
        'user_id' : user_id,
        'pw' : pw,
    }

    response = session.post(url, data=login_data)
    if "history.back(-1);" in response.text:
        print("Cannot create login session!")
        return 0
    
    else :
        print("Login session created successfully")

        BASE_URL = "https://gall.dcinside.com/mgallery/board/lists/"
        params = { 'id': 'pessimism',}
        response = session.get(BASE_URL, params=params)
        return session

def logout(session: requests.Session):
    session.close()


def blocker(session: requests.Session):

    url = "https://gall.dcinside.com/ajax/managements_ajax/update_ipblock"
    session.headers["Referer"] = "https://gall.dcinside.com/mgallery/management/gallery?id=pessimism"
    a = session.cookies['ci_c']
    post_data = {
        "ci_t": session.cookies['ci_c'],
        "gallery_id": "pessimism",
        "_GALLTYPE_": "M",
        "proxy_time": 2880,
        "mobile_time": 60,
        "proxy_use": 1,
        "mobile_use": 1,
        "img_block_use": -1,
        "img_block_time": None
    }
    texts = ["proxy_time", "mobile_time"]
    if post_data["proxy_time"] > 0:
            post_data["proxy_use"] = 1
    else:
        post_data["proxy_use"] = 0

    if post_data["mobile_time"] > 0:
        post_data["mobile_use"] = 1
    else:
        post_data["mobile_use"] = 0

    response = session.post(url, data=post_data)
    if "fail" in response.text:
        print("Cannot manage gallery settings.")
    elif "success" in response.text:
        print(f"vpn 차단 : {post_data[texts[0]]//60} 시간")
        print(f"통신사 IP 차단 : {post_data[texts[1]]} 분")

def run():

    now = datetime.datetime.now()
    print(now)
    session = login()
    blocker(session)
    logout(session)
        
if __name__ == "__main__":

    schedule.every(59).minutes.do(run)

    run()
    while True:
        schedule.run_pending()
        time.sleep(10)
