from bs4 import BeautifulSoup
import requests


def cur_time():
    page = requests.get('https://free.timeanddate.com/clock/i96o8yf3/n1440/tt0/tw0/tm3/td2/th1/ta1/tb1')
    soup = BeautifulSoup(page.text, 'html.parser')
    clock = soup.find(id='t1')
    return clock.text.split(', ')


class MyTime:
    def __init__(self):
        self.time = cur_time()
