import sys
import time
import schedule

from utils import login, logout, auth
from blocker import Blocker
from deleter import Deleter


def blocker(user_id, user_pw, gall_id):

    session = login(user_id, user_pw)
    blocker = Blocker(session, gall_id)
    blocker.block()
    logout(session)

def deleter(user_id, user_pw, gall_id):

    session = login(user_id, user_pw)
    deleter = Deleter(session, gall_id)
    deleter.delete()
    logout(session)


if __name__ == "__main__":

    gall_id = sys.argv[1]
    mode = sys.argv[2]
    user_id, user_pw = auth()

    if mode == "block":
        blocker(user_id, user_pw, gall_id)
        schedule.every(59).minutes.do(blocker, user_id, user_pw, gall_id)

    elif mode == "delete":
        deleter(user_id, user_pw, gall_id)
        schedule.every(1).minutes.do(deleter, user_id, user_pw, gall_id)

    while True:
        schedule.run_pending()
        time.sleep(10)
