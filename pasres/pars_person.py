from bs4 import BeautifulSoup
import json
import re
from app import db, models
from proxy_requests import ProxyRequests
from config import URL
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

def parse_person():
    data = {}
    for person in models.Person.query.all():#.filter_by(name_original=None)
        while True:
            try:
                r = ProxyRequests(f'{URL}{person.links}')
            except:
                break
            r.get()
            r.encoding = 'utf-8'
            text = r.request
            soup = BeautifulSoup(text, 'html.parser')
            if not soup.find('h1', {'itemprop': 'name'}):
                continue
            alternateName = soup.find('span', {'itemprop': 'alternateName'})
            if alternateName:
                person.name_original = alternateName.text
            else:
                person.name_original = person.name
            db.session.add(person)
            db.session.commit()

            list_career = []
            director = soup.find('a', {'href': '#director'})
            if director:
                egge = director.text.replace(' ', '')
                if not models.Career.query.filter_by(name=egge).first():
                    new_career = models.Career(name=egge)
                    db.session.add(new_career)
                    db.session.commit()
                    list_career.append(new_career)
                else:
                    list_career.append(models.Career.query.filter_by(name=egge).first())

            actor = soup.find('a', {'href': '#actor'})
            if actor:
                egge = actor.text.replace(' ', '')
                if not models.Career.query.filter_by(name=egge).first():
                    new_career = models.Career(name=egge)
                    db.session.add(new_career)
                    db.session.commit()
                    list_career.append(new_career)
                else:
                    list_career.append(models.Career.query.filter_by(name=egge).first())

            person.career.clear()
            for i in list_career:
                person.career.append(i)
            db.session.add(person)
            db.session.commit()
            break


parse_person()
