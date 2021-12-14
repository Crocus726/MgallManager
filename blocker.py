import requests
import logging


class Blocker:
    def __init__(self, session: requests.Session, gall_id):

        self.session = session
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

        logger = logging.getLogger()
        Log_Format = "%(levelname)s %(asctime)s - %(message)s"

        self.set_post_data()
        url = "https://gall.dcinside.com/ajax/managements_ajax/update_ipblock"
        response = self.session.post(url, data=self.post_data)

        if "success" in response.text:

            proxy_time = self.post_data["proxy_time"] // 60
            mobile_time = self.post_data["mobile_time"]

            logging.basicConfig(filename="deleter.log", level=logging.INFO, format=Log_Format)
            logger.info(f"VPN 차단 : {proxy_time}시간", end=", ")
            logger.info(f"통신사 IP 차단 : {mobile_time}분")

        else:
            logging.basicConfig(
                filename="deleter.log", level=logging.INFO, format=Log_Format
            )
            logger.warning("Cannot manage gallery settings.")
