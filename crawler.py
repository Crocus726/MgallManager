import requests
from bs4 import BeautifulSoup
from utils import banned_users


class Crawler:
    def __init__(self, session: requests.Session, gall_id):

        self.session = session
        self.gall_id = gall_id
        self.BASE_URL = "https://gall.dcinside.com/mgallery/board/lists/"
        self.params = {"id": self.gall_id}
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36"
        }

    def search_post_nums(self):

        response = requests.get(
            self.BASE_URL, params=self.params, headers=self.headers
        )
        html_data = BeautifulSoup(response.content, "html.parser")

        titles = html_data.find("tbody").find_all("tr")

        post_num_list = []

        for i in titles:

            nick = i.find("td", class_="gall_writer ub-writer").text
            post_num = i.find("td", class_="gall_num").text
            banned_user_list = banned_users()

            if any(i in nick for i in banned_user_list):
                post_num_list.append(int(post_num))

        return post_num_list
