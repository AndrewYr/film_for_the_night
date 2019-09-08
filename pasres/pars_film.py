from bs4 import BeautifulSoup
import json
import re
from app import db, models
from proxy_requests import ProxyRequests
from config import URL
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine


def parse_films():
    engine = create_engine('sqlite:///:memory:', echo=True)

    data = {}
    for film in models.Film.query.filter_by(rating_kp=None).all():#
        while True:
            try:
                r = ProxyRequests(f'{URL}{film.links}')
            except:
                break
            r.get()
            r.encoding = 'utf-8'
            text = r.request
            soup = BeautifulSoup(text, 'html.parser')
            genres = soup.find('span', {'itemprop': 'genre'})
            if genres:
                genres = genres.find_all('a')
                countrys = soup.find_all('div', {'style': 'position: relative'})[1].find_all('a')
                persons = soup.find_all('li', {'itemprop': 'actors'})
                for director in soup.find_all('td', {'itemprop': 'director'}):
                    persons.append(director)
                break
        list_genres = []
        for genre in genres:
            if not models.Genre.query.filter_by(name=genre.text).first():
                while True:
                    new_genre = models.Genre(name=genre.text)
                    db.session.add(new_genre)
                    try:
                        db.session.commit()
                        list_genres.append(new_genre)
                        break
                    except Exception:
                        db.session.rollback()
            else:
                list_genres.append(models.Genre.query.filter_by(name=genre.text).first())

        list_countrys = []
        for country in countrys:
            if not models.Country.query.filter_by(name=country.text).first():
                while True:
                    new_country = models.Country(name=country.text)
                    db.session.add(new_country)
                    try:
                        db.session.commit()
                        list_countrys.append(new_country)
                        break
                    except Exception:
                        db.session.rollback()
            else:
                list_countrys.append(models.Country.query.filter_by(name=country.text).first())

        list_person = []
        for person in persons:
            if person.find('a').text.replace(' ', '') == '...':
                break
            person_link = person.find('a').get('href')
            if not models.Person.query.filter_by(id_person_kp=int(re.findall(r'\d{1,}', person_link)[0])).first():
                while True:
                    # person_link = person.find('a').get('href')
                    if models.Person.query.filter_by(id_person_kp=int(re.findall(r'\d{1,}', person_link)[0])).first():
                        break
                    id_person_kp = int(re.findall(r'\d{1,}', person_link)[0])
                    new_person = models.Person(name=person.text, links=person_link, id_person_kp=id_person_kp)
                    db.session.add(new_person)
                    try:
                        db.session.commit()
                        list_person.append(new_person)
                        break
                    except Exception:
                        db.session.rollback()
            else:
                if not models.Person.query.filter_by(id_person_kp=int(re.findall(r'\d{1,}', person_link)[0])).first() in list_person:
                    list_person.append(models.Person.query.filter_by(id_person_kp=int(re.findall(r'\d{1,}', person_link)[0])).first())

        # if not film.description:
        while True:
            try:
                film.name = soup.find('span', {'class': 'moviename-title-wrapper'}).text
                film.name_original = film.name if not soup.find('span', {'class': 'alternativeHeadline'}).text else soup.find('span', {'class': 'alternativeHeadline'}).text
                film.description = soup.find('div', {'itemprop': 'description'}).text.replace(chr(151), '-')
                film.rating_kp = float(soup.find('span', {'class': 'rating_ball'}).text)
                film.rating_imdb = float(re.findall(r'[\d][^ ]+', soup.find('div', {
                    'style': 'color:#999;font:100 11px tahoma, verdana'}).text)[0])
                film.date_released = int(soup.find('div', {'style': 'position: relative'}).find('a').text)
                try:
                    db.session.commit()
                except Exception:
                    db.session.rollback()
                    continue
                film.genre.clear()
                film.country.clear()
                film.person.clear()

                while True:
                    for i in list_genres:
                        film.genre.append(i)
                    for i in list_countrys:
                        film.country.append(i)
                    for i in list_person:
                        film.person.append(i)
                    db.session.add(film)
                    try:
                        db.session.commit()
                        break
                    except Exception:
                        db.session.rollback()
                break

            except:
                db.session.rollback()



parse_films()