from copy import deepcopy
import requests
import logging


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

    def set_post_data(self):

        BASE_URL = "https://gall.dcinside.com/mgallery/board/lists/"
        params = {"id": self.gall_id}
        self.session.get(BASE_URL, params=params)
        self.post_data["ci_t"] = self.session.cookies["ci_c"]

    def block(self):

        self.set_post_data()
        url = "https://gall.dcinside.com/ajax/managements_ajax/update_ipblock"
        response = self.session.post(url, data=self.post_data)

        return "success" in response.text
