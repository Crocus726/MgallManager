from copy import deepcopy
import requests


class Blocker:
    def __init__(self, session: requests.Session, gall_id):

        self.session = deepcopy(session)
        self.base_url = "https://gall.dcinside.com/mgallery/board/lists/"
        self.block_url = "https://gall.dcinside.com/ajax/managements_ajax/update_ipblock"
        self.gall_id = gall_id
        self.post_data = {
            "ci_t": None,
            "gallery_id": self.gall_id,
            "_GALLTYPE_": "M",
            "proxy_time": None,
            "mobile_time": None,
            "proxy_use": None,
            "mobile_use": None,
            "img_block_use": -1,
            "img_block_time": None,
        }
        self.logger = None

    def set_post_data(self):
        params = {"id": self.gall_id}

        if self.post_data["proxy_time"] is None:
            self.post_data["proxy_use"] = 0
        else:
            self.post_data["proxy_use"] = 1

        if self.post_data["mobile_time"] is None:
            self.post_data["mobile_use"] = 0
        else:
            self.post_data["mobile_use"] = 1

        try:
            self.session.get(self.base_url, params=params)
            self.post_data["ci_t"] = self.session.cookies["ci_c"]

        except Exception:
            self.logger.critical("BLOCKER : cannot get cookie from session")

    def block(self, proxy_time, mobile_time):

        self.post_data["proxy_time"] = proxy_time
        self.post_data["mobile_time"] = mobile_time
        self.set_post_data()

        try:
            response = self.session.post(self.block_url, data=self.post_data)
            self.logger.info("BLOCKER : updated block settings")

        except Exception:
            self.logger.critical("BLOCKER : cannnot update block settings")

        return "success" in response.text
