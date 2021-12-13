import sys
import time
import schedule
from datetime import datetime

from auth import login, logout
from blocker import Blocker
from deleter import Deleter

def main(user_id, user_pw, gall_id):

    print(datetime.now())
    session = login(user_id, user_pw)
    blocker = Blocker(session, gall_id)
    blocker.block()
    logout(session)

def delete(user_id, user_pw, gall_id):

    session = login(user_id, user_pw)
    deleter = Deleter(session, gall_id)
    deleter.delete()
    logout(session)


if __name__ == "__main__":

    gall_id = sys.argv[1]
    user_id = sys.argv[2]
    user_pw = sys.argv[3]
   
    # main(user_id, user_pw, gall_id)
    delete(user_id, user_pw, gall_id)
    # schedule.every(59).minutes.do(main, user_id, user_pw, gall_id)
    schedule.every(30).seconds.do(delete, user_id, user_pw, gall_id)

    while True:
        schedule.run_pending()
        time.sleep(10)