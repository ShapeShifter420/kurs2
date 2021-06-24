import json
import os

from flask import Flask, session, render_template, send_file, request, send_from_directory, redirect, url_for
from web_app.models import alg_model
import requests

from web_app.alg_factory import factory

app = Flask(__name__)
app.debug = False
app.secret_key = b'\xcbt\x0f\xbfAQd\x16\x91\xa4\x1f\x8b\xa2j\xc8k\x19^\xf19\xf4Bq\xe1'

load_keys = {}


def init_keys():
    with (open("../keys.json")) as keys:
        global load_keys
        load_keys = json.load(keys)


@app.route('/')
def hello():
    return render_template('/views/index.html')


@app.route('/list')
def get_list():
    args = {'data': get_full_alg()}
    return render_template('/views/list.html', args=args)


@app.route('/result')
def get_result():
    args = {'data': get_full_alg()}
    return render_template('/views/list.html', args=args)


@app.route('/task', methods=['GET', 'POST'])
def get_task1():
    href = request.args['href']
    if request.method == 'POST':
        args = request.form.to_dict()
        add_alg(href, args)
        return redirect('/')
    return render_template(f'/views/tasks/{href}.html')


@app.route('/get')
def get_color():
    href = request.args['href']
    return render_template('/views/getter.html', data=requests.get('http://localhost:8000/api/'+href_adapter(href)).content)



def start():
    app.run(host='0.0.0.0')


def start80():
    app.run(host='0.0.0.0', port=80)


def create_new_json(args):
    return json.dumps(args)


def get_full_alg():
    return full_alg


def add_alg(href, args):
    print(href, args)
    if 'color_space' in args.keys():
        args['color_space'] = args['color_space'].split(',')
    if 'color_range' in args.keys():
        tange = args['color_range'].split('|')
        tange[0] = [int(t) for t in tange[0].split(',')]
        tange[1] = [int(t) for t in tange[1].split(',')]
        args['color_range'] = tange
    if 'images' in args.keys():
        args['images'] = args['images'].split(',')
    if 'encode' in args.keys():
        args['encode'] = args['encode'] == 'on'
    factory.make_request(href_adapter(href), args)


def href_adapter(href):
    return adapter[href]


full_alg = [alg_model('task1', 'Преобразование Фурье'), alg_model('task2', 'Сложение изображений'), alg_model('task3', 'Выделение рамок')
            , alg_model('task4', 'Изменение цветового пространства'), alg_model('task5', 'Наложение Шума'),
            alg_model('task6', 'Стенография'), alg_model('task7', 'Карандаш'), alg_model('task8', 'Рандом')]
adapter = {'task1': 'frequency_filtering', 'task2': 'fold_images', 'task3': 'search_all_rectangles_of_color',
           'task4': 'new_color_space',
           'task5': 'color_noize', 'task6': 'cipher', 'task7': 'pencel', 'alg1': 'get_color_spaces', 'alg2': 'get_default_color_range','task8':'topbrait'}
if __name__ == '__main__':
    init_keys()
