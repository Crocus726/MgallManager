import requests
import sys
from bs4 import BeautifulSoup
from auth import login, logout

class Crawler:

    def __init__(self, session: requests.Session, gall_id):
        
        self.session = session
        self.gall_id = gall_id
        self.BASE_URL = "https://gall.dcinside.com/mgallery/board/lists/"
        self.params = {'id': self.gall_id}
    
    def search_posts_titles(self):
        
        response = self.session.get(self.BASE_URL, params=self.params)
        html_data = BeautifulSoup(response.content, 'html.parser')

        contents = html_data.find('tbody').find_all('tr')

        for i in contents:
            print('-'*15)

            title_tag = i.find('a')
            title = title_tag.text
            print("title : ", title)
    

if __name__ == "__main__":

    gall_id = sys.argv[1]
    user_id = sys.argv[2]
    user_pw = sys.argv[3]
    session = login(user_id, user_pw)
    crawler = Crawler(session, gall_id)
    crawler.search_posts_titles()

    pass