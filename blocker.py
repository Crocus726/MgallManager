from copy import deepcopy
import requests


class Blocker:
    def __init__(self, session: requests.Session, gall_id):

        self.session = deepcopy(session)
        self.gall_id = gall_id
        self.post_data = {
            "ci_t": None,
            "gallery_id": self.gall_id,
            "_GALLTYPE_": "M",
            "proxy_time": 2880,
            "mobile_time": 60,
            "proxy_use": 1,
            "mobile_use": 1,
            "img_block_use": -1,
            "img_block_time": None,
        }
        self.logger = None

    def set_post_data(self):

        BASE_URL = "https://gall.dcinside.com/mgallery/board/lists/"
        params = {"id": self.gall_id}

        try:
            self.session.get(BASE_URL, params=params)
            self.post_data["ci_t"] = self.session.cookies["ci_c"]

        except Exception:
            self.logger.critical("BLOCKER : cannot get cookie from session")

    def block(self):

        self.set_post_data()
        block_url = "https://gall.dcinside.com/ajax/managements_ajax/update_ipblock"

        try:
            response = self.session.post(block_url, data=self.post_data)
            self.logger.info("BLOCKER : updated block settings")

        except Exception:
            self.logger.critical("BLOCKER : cannnot update block settings")

        return "success" in response.text
