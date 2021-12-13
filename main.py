import sys
import schedule
import datetime
import time
import requests
from auth import login, logout
from blocker import Blocker

def main(session: requests.Session, gall_id):

    now = datetime.datetime.now()
    print(now)
    blocker = Blocker(session, gall_id)
    blocker.block()
    logout(session)

if __name__ == "__main__":

    gall_id = sys.argv[1]
    user_id = sys.argv[2]
    user_pw = sys.argv[3]
   
    session = login(user_id, user_pw)
    if session == 0:
        exit()

    schedule.every(60).minutes.do(main, session, gall_id)

    main(session, gall_id)
    while True:
        schedule.run_pending()
        time.sleep(10)