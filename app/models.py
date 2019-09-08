from app import db

genres = db.Table('genres',
    db.Column('genre_id', db.Integer, db.ForeignKey('genre.id')),
    db.Column('film_id', db.Integer, db.ForeignKey('film.id'))
)

countrys = db.Table('countrys',
    db.Column('country_id', db.Integer, db.ForeignKey('country.id')),
    db.Column('film_id', db.Integer, db.ForeignKey('film.id'))
)

persons = db.Table('persons',
    db.Column('persons_id', db.Integer, db.ForeignKey('person.id')),
    db.Column('film_id', db.Integer, db.ForeignKey('film.id'))
)

careers = db.Table('careers',
    db.Column('career_id', db.Integer, db.ForeignKey('career.id')),
    db.Column('person_id', db.Integer, db.ForeignKey('person.id'))
)


class Film(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_film = db.Column(db.Integer, index=True, unique=True)
    links = db.Column(db.String(256), index=True, unique=True)
    name = db.Column(db.String(120), index=True, unique=True)
    name_original = db.Column(db.String(120), index=True, unique=True)
    description = db.Column(db.String(), index=True, unique=True)
    rating_kp = db.Column(db.Float, index=True, unique=True)
    rating_imdb = db.Column(db.Float, index=True, unique=True)
    genre = db.relationship('Genre', secondary=genres, backref=db.backref('films', lazy='dynamic'))
    country = db.relationship('Country', secondary=countrys, backref=db.backref('film', lazy='dynamic'))
    person = db.relationship('Person', secondary=persons, backref=db.backref('film', lazy='dynamic'))
    date_released = db.Column(db.Integer, index=True, unique=True)

    def __repr__(self):
        return '<User %r>' % (self.nickname)


class Genre(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), index=True, unique=True)

    def __repr__(self):
        return '<User %r>' % (self.nickname)


class Country(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), index=True, unique=True)

    def __repr__(self):
        return '<User %r>' % (self.nickname)


class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_person_kp = db.Column(db.Integer, index=True, unique=True)
    name = db.Column(db.String(120), index=True, unique=True)
    name_original = db.Column(db.String(120), index=True, unique=True)
    links = db.Column(db.String(256), index=True, unique=True)
    career = db.relationship('Career', secondary=careers, backref=db.backref('careers', lazy='dynamic'))

    def __repr__(self):
        return '<User %r>' % (self.nickname)


class Career(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), index=True, unique=True)

    def __repr__(self):
        return '<User %r>' % (self.nickname)