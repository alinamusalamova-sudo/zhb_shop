from flask import Flask, render_template
app = Flask(__name__)

images = [
    {"filename": "img_1.png", "title": "ты справишься!"},
    {"filename": "img_2.png", "title": "хорошего дня!!"},
    {"filename": "img_3.png", "title": "котик №2"},
    {"filename": "img_4.png", "title": "еще котик"},
    {"filename": "img_5.png", "title": "бибизяна"},
    {"filename": "img_6.png", "title": "с наступающим!"},
    {"filename": "img_7.png", "title": "будь хэппи"},
    {"filename": "img_8.png", "title": "котиков много не бывает"}
]

@app.get("/")
def index():
    return '''
    <h1> Привет! Здесь картинная галерея </h1>
    <p><a href = "/gallery"> Смотреть картинки </a></p>
    '''
@app.get("/gallery")
def gallery():
    return render_template("gallery.html", images = images)

if __name__ == "__main__":
    app.run(debug=True)
