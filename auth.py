import requests
from bs4 import BeautifulSoup

def login(user_id, pw):

    url = 'https://dcid.dcinside.com/join/member_check.php'

    session = requests.session()
    session.headers = {
        "X-Requested-With" : "XMLHttpRequest",
        'Referer':'https://www.dcinside.com/',
        'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'
    }

    soup = BeautifulSoup(requests.get("https://www.dcinside.com/").text, features='html.parser')
    loginForm = soup.find('form', attrs={'id': 'login_process'})
    auth = loginForm.find_all('input', attrs = {'type':'hidden'})[2]

    login_data = {
        's_url': '//www.dcinside.com/',
        'ssl': 'Y',
        auth['name'] : auth['value'],
        'user_id' : user_id,
        'pw' : pw,
    }

    response = session.post(url, data=login_data)
    if "history.back(-1);" in response.text:
        print("Cannot create login session.")
        exit()
    
    else :
        print("Login session created successfully.")
        return session

def logout(session: requests.Session):
    session.close()
    print("Successfully logged out.")