import requests
import schedule
import datetime
import time
import getpass
from auth import login, logout

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
        print(f"vpn 차단 : {post_data[texts[0]]//60}시간", end = ", ")
        print(f"통신사 IP 차단 : {post_data[texts[1]]}분")

def run(user_id, pw):

    now = datetime.datetime.now()
    print(now)
    session = login(user_id, pw)
    blocker(session)
    logout(session)
        
if __name__ == "__main__":

    user_id = input("아이디 입력 : ")
    pw = getpass.getpass("비밀번호 입력 : ")

    schedule.every(59).minutes.do(run, user_id, pw)

    run(user_id, pw)
    while True:
        schedule.run_pending()
        time.sleep(10)
