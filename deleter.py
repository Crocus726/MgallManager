from copy import deepcopy
import requests
import logging
from crawler import Crawler


class Deleter:
    def __init__(self, session: requests.Session, gall_id):

        self.session = deepcopy(session)
        self.gall_id = gall_id
        self.post_data = {
            "ci_t": None,
            "id": self.gall_id,
            "nos[]": None,
            "_GALLTYPE_": "M",
        }
        self.post_list = None

    def set_post_data(self):

        BASE_URL = "https://gall.dcinside.com/mgallery/board/lists/"
        params = {"id": self.gall_id}
        self.session.get(BASE_URL, params=params)
        self.post_data["ci_t"] = self.session.cookies["ci_c"]
        self.post_data["nos[]"] = self.post_list

    def delete(self, post_list):

        logger = logging.getLogger()
        Log_Format = "%(levelname)s %(asctime)s - %(message)s"

        self.post_list = post_list
        self.set_post_data()

        # self.post_data["nos[]"]
        if len(self.post_data["nos[]"]) == 0:

            return None

        else:
            url = "https://gall.dcinside.com/ajax/minor_manager_board_ajax/delete_list"
            response = self.session.post(url, data=self.post_data)

            if "success" in response.text:
                logging.basicConfig(
                    filename="deleter.log", level=logging.INFO, format=Log_Format
                )
                logger.info("Deleted Selected Postings " + str(self.post_data["nos[]"]))

            else:
                logging.basicConfig(
                    filename="deleter.log", level=logging.WARNING, format=Log_Format
                )
                logger.warning("Cannnot delete posts.")

            return ("success" in response.text)
