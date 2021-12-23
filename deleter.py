from copy import deepcopy
import requests


class Deleter:
    def __init__(self, session: requests.Session, gall_id):

        self.session = deepcopy(session)
        self.base_url = "https://gall.dcinside.com/mgallery/board/lists/"
        self.delete_url = "https://gall.dcinside.com/ajax/minor_manager_board_ajax/delete_list"
        self.gall_id = gall_id
        self.post_data = {
            "ci_t": None,
            "id": self.gall_id,
            "nos[]": None,
            "_GALLTYPE_": "M",
        }
        self.post_list = None

        self.logger = None

    def set_post_data(self):

        params = {"id": self.gall_id}
        self.session.get(self.base_url, params=params)
        self.post_data["ci_t"] = self.session.cookies["ci_c"]
        self.post_data["nos[]"] = self.post_list

    def delete(self, post_list):

        self.post_list = post_list
        self.set_post_data()

        if len(self.post_data["nos[]"]) == 0:
            return None

        else:
            response = self.session.post(self.delete_url, data=self.post_data)

            if "success" in response.text:
                self.logger.info("DELETER : deleted selected postings " + str(self.post_data["nos[]"]))

            else:
                self.logger.warning("DELETER : cannnot delete posts")

            return ("success" in response.text)
