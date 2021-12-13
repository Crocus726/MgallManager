import schedule
import datetime
import time
import getpass
from auth import login, logout
from blocker import blocker

def main(user_id, pw):

    now = datetime.datetime.now()
    print(now)
    session = login(user_id, pw)
    blocker(session)
    logout(session)

if __name__ == "__main__":

    user_id = input("아이디 입력 : ")
    pw = getpass.getpass("비밀번호 입력 : ")

    schedule.every(59).minutes.do(main, user_id, pw)

    main(user_id, pw)
    while True:
        schedule.run_pending()
        time.sleep(10)