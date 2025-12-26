from flask import Flask, render_template

app = Flask(__name__)

movies = [
    {"title": "Inception", "year": 2010, "rating": 8.8},
    {"title": "Dune", "year": 2021, "rating": 8.1},
    {"title": "Interstellar", "year": 2014, "rating": 8.6},
    {"title": "Titanic", "year": 1997, "rating": 7.9}
]

@app.get("/")
def index():
    return '''
    <h1> Привет! Здесь фильмы! </h1>
    <p><a href = "/movies"> Смотреть фильмы </a></p>
    '''

@app.get("/movies")
def show_movies():
    return render_template("movies.html", movies=movies)

if __name__ == "__main__":
    app.run(debug=True)