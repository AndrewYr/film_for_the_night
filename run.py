#!flask/bin/python
from app import app
from app import views

app.run(debug=True)

if __name__ == '__main__':
    views.index()