from app import app
from flask import Flask, jsonify
from flask import abort, make_response, request
from app import models
import json


@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"


@app.route('/todo/api/v1.0/film_on_rating', methods=['GET'])
def get_film_on_rating():
    genre1 = int(request.args.get('id_1'))
    # models.Genre.query.filter(models.Genre.id >= 1).all()
    # list_film = models.Genre.query.filter_by(id=genre1).first().films.all()
    # first_1 = int(request.args.getlist('r_1')[0])
    # end_1 = int(request.args.getlist('r_1')[0])

    # while True:
    #     for film in list_film:
    #         if film.rating_kp >=first_1 and film.rating_kp <= end_1:
    return jsonify({'genre': ''})


@app.route('/todo/api/v1.0/genre', methods=['GET'])
def get_genre():

    genres = [{'id': i.id, 'name': i.name} for i in models.Genre.query.all()]
    return jsonify({'genre': genres})


@app.route('/todo/api/v1.0/genre/<int:genre_id>', methods=['GET'])
def get_genre_id(genre_id):
    films = [{'id': i.id,
              'name': i.name,
              'name_original': i.name_original,
              'description': i.description,
              'rating_kp': i.rating_kp,
              'rating_imdb': i.rating_imdb,
              'date_released': i.date_released,
              'genre': [{'id': f.id, 'name': f.name} for f in i.genre],
              'country': [{'id': c.id, 'name': c.name} for c in i.country],
              'person': [{'id': p.id, 'name': p.name, 'name_original': p.name_original} for p in i.person]
              }
             for i in models.Genre.query.filter_by(id=genre_id).first().films.all()]
    if len(films) == 0:
        abort(404)
    return jsonify({'genre': films})


@app.route('/todo/api/v1.0/country', methods=['GET'])
def get_country():
    countrys = [{'id': i.id, 'name': i.name} for i in models.Country.query.all()]
    return jsonify({'country': countrys})

@app.route('/todo/api/v1.0/country/<int:country_id>', methods=['GET'])
def get_country_id(country_id):
    films = [{'id': i.id,
              'name': i.name,
              'name_original': i.name_original,
              'description': i.description,
              'rating_kp': i.rating_kp,
              'rating_imdb': i.rating_imdb,
              'date_released': i.date_released,
              'genre': [{'id': f.id, 'name': f.name} for f in i.genre],
              'country': [{'id': c.id, 'name': c.name} for c in i.country],
              'person': [{'id': p.id, 'name': p.name, 'name_original': p.name_original} for p in i.person]
              }
             for i in models.Country.query.filter_by(id=country_id).first().films.all()]
    if len(films) == 0:
        abort(404)
    return jsonify({'genre': films})

@app.route('/todo/api/v1.0/career', methods=['GET'])
def get_career():
    careers = [{'id': i.id, 'name': i.name} for i in models.Career.query.all()]
    return jsonify({'country': careers})


@app.route('/todo/api/v1.0/film', methods=['GET'])
def get_film():
    films = [{'id': i.id,
               'name': i.name,
               'name_original': i.name_original,
               'description': i.description,
               'rating_kp': i.rating_kp,
               'rating_imdb': i.rating_imdb,
               'date_released': i.date_released,
              'genre': [{'id': f.id, 'name': f.name}for f in i.genre],
               'country': [{'id': c.id, 'name': c.name}for c in i.country],
               'person': [{'id': p.id, 'name': p.name, 'name_original': p.name_original}for p in i.person]
               }
              for i in models.Film.query.all()]
    return jsonify({'genre': films})


@app.route('/todo/api/v1.0/film/<int:film_id>', methods=['GET'])
def get_film_id(film_id):
    films = [{'id': i.id,
              'name': i.name,
              'name_original': i.name_original,
              'description': i.description,
              'rating_kp': i.rating_kp,
              'rating_imdb': i.rating_imdb,
              'date_released': i.date_released,
              'genre': [{'id': f.id, 'name': f.name} for f in i.genre],
              'country': [{'id': c.id, 'name': c.name} for c in i.country],
              'person': [{'id': p.id, 'name': p.name, 'name_original': p.name_original} for p in i.person]
              }
             for i in models.Film.query.filter_by(id=film_id)]
    if len(films) == 0:
        abort(404)
    return jsonify({'genre': films})


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

