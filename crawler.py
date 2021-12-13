import requests
import sys
from bs4 import BeautifulSoup
from auth import login, logout

class Crawler:

    def __init__(self, gall_id):
        
        # self.session = requests.Session()
        self.gall_id = gall_id
        self.BASE_URL = "https://gall.dcinside.com/mgallery/board/lists/"
        self.params = {'id': self.gall_id}
        self.headers = {
        'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'
        }
    
    def search_posts_titles(self):
        
        response = requests.get(self.BASE_URL, params=self.params, headers=self.headers)
        html_data = BeautifulSoup(response.content, 'html.parser')

        titles = html_data.find('tbody').find_all('tr')

        for i in titles:
            #print(i)

            title_tag = i.find('a')
            nick = i.find('td', class_ = "gall_writer ub-writer").text
            post_num = i.find('td', class_ = "gall_num")
            nick = nick.replace('\n',"")
            post_num = post_num.text
            title = title_tag.text
            print(nick)
            #print("글쓴이 :", nick, end = ", ")
            print("글번 :", post_num, end = ", ")
            print("title :", title)
        
            
    

if __name__ == "__main__":

    gall_id = sys.argv[1]

    crawler = Crawler( gall_id)
    crawler.search_posts_titles()

    pass