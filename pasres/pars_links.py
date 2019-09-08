from bs4 import BeautifulSoup
import json
import re
from app import db, models
from proxy_requests import ProxyRequests
from config import URL

def parse_links():
    page = 1
    last_page = 1
    data = {}

    while page <= last_page:
        r = ProxyRequests(f'{URL}/top/navigator/m_act[rating]/1%3A/order/rating/page/{page}/#results')
        r.get()
        r.encoding = 'utf-8'
        text = r.request
        soup = BeautifulSoup(text)
        if last_page == 1:
            try:
                last_link = soup.find_all('li', {'class': 'arr'})[-1].find('a').get('href')
                last_page = int(re.findall(r'\d{2,}', last_link)[0])
            except:
                continue

        movie_link = soup.find_all('div', {'class': '_NO_HIGHLIGHT_'})
        if not movie_link:
            continue

        for i in movie_link:
            i_soup = BeautifulSoup(f'b{i}').find('div', {'class': 'name'}).find('a')
            i_text = i_soup.text
            i_link = i_soup.get('href')
            id_film = int(re.findall(r'\d{1,}', i_link)[1])
            if models.Film.query.filter_by(id_film=id_film).first() == None:
                film = models.Film(id_film=id_film, links=i_link, name=i_text)
                db.session.add(film)
                try:
                    db.session.commit()
                except Exception:
                    db.session.rollback()
                    data[i_text] = {page:i_link}
                    continue

        page += 1
    with open('data.txt', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False)

parse_links()