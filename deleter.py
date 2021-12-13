import requests
from crawler import Crawler

class Deleter:

    def __init__(self, session: requests.Session, gall_id):
        
        self.session = session
        self.gall_id = gall_id
        self.post_data = {
            "ci_t": None,
            "id": self.gall_id,
            "nos[]": None,
            "_GALLTYPE_": "M",
        }
    
    def set_post_data(self):

        BASE_URL = "https://gall.dcinside.com/mgallery/board/lists/"
        params = {'id': self.gall_id}
        self.session.get(BASE_URL, params=params)
        self.post_data["ci_t"] = self.session.cookies['ci_c']
    
    def get_posting_nums(self):
        
        # 닉네임이 Xxx인 유저의 글 번호를 받아와서 정수 리스트로 주면 됨.
        self.post_data["nos[]"] = [21205, 21206]


    def delete(self):
        
        self.set_post_data()
        self.get_posting_nums()
        url = "https://gall.dcinside.com/ajax/minor_manager_board_ajax/delete_list"
        response = self.session.post(url, data=self.post_data)

        if "success" in response.text:
            print("Deleted Selected Postings")
        else:
            print("Cannnot delete posts.")