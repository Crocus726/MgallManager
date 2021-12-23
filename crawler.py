import requests
import logging
from copy import deepcopy
from bs4 import BeautifulSoup


class Crawler:
    def __init__(self, session: requests.Session, gall_id):

        self.session = deepcopy(session)
        self.gall_id = gall_id
        self.BASE_URL = "https://gall.dcinside.com/mgallery/board/lists/"
        self.management_url = "https://gall.dcinside.com/mgallery/management/gallery"
        self.params = {"id": self.gall_id}
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36"
        }

        self.logger = logging.getLogger()
        Log_Format = "%(levelname)s %(asctime)s - %(message)s"
        logging.basicConfig(filename="manager.log", format=Log_Format)

    def get_post_nums(self, delete_user_list):

        response = requests.get(self.BASE_URL, params=self.params, headers=self.headers)
        html_data = BeautifulSoup(response.content, "html.parser")
        post_num_list = []

        try:
            titles = html_data.find("tbody").find_all("tr")

            for i in titles:
                nick = i.find("td", class_="gall_writer ub-writer").text
                post_num = i.find("td", class_="gall_num").text

                if any(i in nick for i in delete_user_list):
                    post_num_list.append(int(post_num))

        except Exception as e:
            self.logger.critical("CRAWLER : cannot get post nums from server", exc_info=True)

        return post_num_list

    def get_blocktime(self):

        response = self.session.get(self.management_url, params=self.params)
        if response.status_code != 200:
            return None

        html_parse = BeautifulSoup(response.text, features="html.parser")

        try:
            proxy_txt = html_parse.find("span", class_="proxy_txt").text
            mobile_txt = html_parse.find("span", class_="mobile_txt").text

            if len(proxy_txt) == 0:
                proxy_txt = "제한 없음"
            if len(mobile_txt) == 0:
                mobile_txt = "제한 없음"

            return [proxy_txt, mobile_txt]

        except Exception as e:
            self.logger.critical("CRAWLER : cannot load block time info from server", exc_info=True)
            return None
