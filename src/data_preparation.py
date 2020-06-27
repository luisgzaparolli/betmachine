from bs4 import BeautifulSoup
import requests

def get_links(url):
    html = requests.get(url, headers={'User-Agent': 'test'}).content
    soup = BeautifulSoup(html, 'lxml')
    games = soup.find_all('tr', {'class': 'match complete'})
    links = ['https://footystats.org/' + item.find('a')['href'] for item in games]
    return links

def get_games():
    url = 'https://footystats.org/england/premier-league/fixtures'
    html = requests.get(url, headers={'User-Agent': 'test'}).content
    soup = BeautifulSoup(html, 'lxml')
    games=soup.find('div', {'class': 'full-matches-table mt1e'}).find_all('tr', {'class':'match incomplete'})
    links = ['https://footystats.org/' + item.find('a')['href'] for item in games]
    return links
