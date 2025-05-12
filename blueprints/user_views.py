from flask import Flask, render_template, url_for, request
import os


basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
app = Flask(__name__, static_folder=os.path.join(basedir, 'static'))



@app.route('/main')
@app.route('/', methods=['POST', 'GET'])
def main():
    return  '''<div class="p-3 mb-2 bg-info text-dark"><h1>Maritime<h1></div>
    <nav class="navbar navbar-expand-lg bg-body-tertiary">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-9ndCyUaIbzAi2FUVXJi0CjmCapSmO7SnpJef0486qhLnuZ2cdeRhO02iuK6FUUVM" crossorigin="anonymous">
  <div class="container-fluid">
    <a class="navbar-brand" href="">Навигация</a>
    <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Переключатель навигации">
      <span class="navbar-toggler-icon"></span>
    </button>
    <div class="collapse navbar-collapse" id="navbarNav">
      <ul class="navbar-nav">
        <li class="nav-item">
          <a class="nav-link active" aria-current="page" href="main">Главная</a>
        </li>
        <li class="nav-item">
          <a class="nav-link" href="rooms">Номера</a>
        </li>
        <li class="nav-item">
          <a class="nav-link" href="routers">Маршруты</a>
        </li>
        <li class="nav-item">
          <a class="nav-link" href="pro">Контакты</a>
        </li>
      </ul>
    </div>
  </div>
</nav>

<div id="carouselExampleIndicators" class="carousel slide" data-bs-ride="carousel">
  <div class="carousel-indicators">
    <button type="button" data-bs-target="#carouselExampleIndicators" data-bs-slide-to="0" class="active" aria-current="true" aria-label="Slide 1"></button>
    <button type="button" data-bs-target="#carouselExampleIndicators" data-bs-slide-to="1" aria-label="Slide 2"></button>
    <button type="button" data-bs-target="#carouselExampleIndicators" data-bs-slide-to="2" aria-label="Slide 3"></button>
  </div>
  <div class="carousel-inner">
    <div class="carousel-item active">
      <img src="/static/images/first.jpg" class="d-block w-100" alt="изображение не прогружено">
    </div>
    <div class="carousel-item">
      <img src="/static/images/second.jpg" class="d-block w-100" alt="изображение не прогружено">
    </div>
    <div class="carousel-item">
      <img src="/static/images/third.jpg" class="d-block w-100" alt="изображение не прогружено">
    </div>
    </div>
  <button class="carousel-control-prev" type="button" data-bs-target="#carouselExampleIndicators" data-bs-slide="prev">
    <span class="carousel-control-prev-icon" aria-hidden="true"></span>
    <span class="visually-hidden">Previous</span>
  </button>
  <button class="carousel-control-next" type="button" data-bs-target="#carouselExampleIndicators" data-bs-slide="next">
    <span class="carousel-control-next-icon" aria-hidden="true"></span>
    <span class="visually-hidden">Next</span>
  </button>
</div><div class="p-3 mb-2 bg-dark text-white"><h1>Адрес:</h1><br><h>Город Владивосток, район "Крутой"<h><br><a href="https://instagram.com/maritime_resort" target="_blank">
  <i class="fab fa-instagram"></i> @maritime_resort
</a></div>
'''


@app.route('/rooms')
def rooms():
    return '''<div class="p-3 mb-2 bg-info text-dark"><h1>Maritime<h1></div> <nav class="navbar navbar-expand-lg bg-body-tertiary">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-9ndCyUaIbzAi2FUVXJi0CjmCapSmO7SnpJef0486qhLnuZ2cdeRhO02iuK6FUUVM" crossorigin="anonymous">
  <div class="container-fluid">
    <a class="navbar-brand" href="">Навигация</a>
    <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Переключатель навигации">
      <span class="navbar-toggler-icon"></span>
    </button>
    <div class="collapse navbar-collapse" id="navbarNav">
      <ul class="navbar-nav">
        <li class="nav-item">
            <a class="nav-link" href="main">Главная</a>

        </li>
        <li class="nav-item">
            <a class="nav-link active" aria-current="page" href="rooms">Номера</a>

        </li>
        <li class="nav-item">
          <a class="nav-link" href="routers">Маршруты</a>
        </li>
        <li class="nav-item">
          <a class="nav-link" href="pro">Контакты</a>
        </li>
      </ul>
    </div>
  </div>
</nav><div class="card">
  <img src="/static/images/room-1.jpg" class="card-img-top">
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-9ndCyUaIbzAi2FUVXJi0CjmCapSmO7SnpJef0486qhLnuZ2cdeRhO02iuK6FUUVM" crossorigin="anonymous">
  <div class="card-body">
    <h5>Люкс с видом на море</h5>
    <p>5000 ₽/ночь</p>
    <a href="/room/1" class="btn btn-primary">Подробнее</a>
  </div>
</div>
<div class="card">
  <img src="/static/images/room-2.jpg" class="card-img-top">
  <div class="card-body">
    <h5>Стандартный номер</h5>
    <p>2000 ₽/ночь</p>
    <a href="/room/2" class="btn btn-primary">Подробнее</a>
  </div>
</div>
'''



if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
