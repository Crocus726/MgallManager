import sys
import time
import requests
import schedule
from datetime import datetime

from auth import login, logout
from blocker import Blocker
from deleter import Deleter

def main(session: requests.Session, gall_id):

    now = datetime.now()
    print(now)
    # blocker = Blocker(session, gall_id)
    # blocker.block()
    deleter = Deleter(session, gall_id)
    deleter.delete()
    logout(session)

if __name__ == "__main__":

    gall_id = sys.argv[1]
    user_id = sys.argv[2]
    user_pw = sys.argv[3]
   
    session = login(user_id, user_pw)
    if session == 0:
        exit()

    main(session, gall_id)
    schedule.every(60).minutes.do(main, session, gall_id)

    while True:
        schedule.run_pending()
        time.sleep(10)