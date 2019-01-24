import flask
import json
from PIL import Image
from RedisHandler import RedisHandler
app = flask.Flask(__name__)

rh = RedisHandler()

'''Загрузчик для изображения'''
@app.route('/resizer/load', methods=['GET', 'POST'])
def resize_image():
    file = flask.request.files['file']

    if not 'file' in flask.request.files or not 'size' in flask.request.values or file.filename == 'file':
        return flask.abort(400, 'missed file or size params')

    '''Разбиваем файл на название и формат'''
    splitted_filename = file.filename.split('.')
    filename = splitted_filename[0]
    format = splitted_filename[1]

    if not format in ('jpg', 'png', 'jpeg'):
        return flask.abort(400, 'wrong image format')

    '''Обрабатываем параметры размера из запроса'''
    size = json.loads(flask.request.values.get('size').encode('utf-8'))
    width = size['width'] if 'width' in size else None
    height = size['height'] if 'height' in size else None
    if not width or not height:
        return flask.abort(400, 'wrong width/height param')

    file.save(file.filename)

    '''Изменяем размер изображения'''
    img = Image.open(file.filename)
    resized = img.resize((int(width), int(height)))
    new_filename = filename+width+'x'+height+'.'+format
    file = resized.save(new_filename)
    new_task_id = rh.get_new_id()

    '''Генерируем словарь описывающий результат выполнения'''
    task = {
        'id': new_task_id,
        'status': 'ok',
        'path': flask.request.host+"/resizer/download/?filename="+new_filename
    }
    rh.add_new_task(new_task_id,task)
    return flask.jsonify({'result': task}), 201


'''Метод для обработки запроса на получение информации по выполнению'''
@app.route('/resizer/get/', methods=['GET'])
def get_image():
    id = flask.request.values.get('task_id')
    if not id:
        return flask.abort(400, 'wrong task id')
    task = rh.get_task_by_id(id)
    if not task:
        return flask.abort(400, 'cannot find task')
    return flask.jsonify({'result': task}), 201


'''Метод для загрузки'''
@app.route('/resizer/download/', methods=['GET'])
def load_image():
    name = flask.request.values.get('filename')
    if not name:
        flask.abort(400, 'wrong filename')
    return flask.send_from_directory(directory='', filename=name)


@app.errorhandler(404)
def not_found(error):
    return flask.make_response(flask.jsonify({'error': 'wrong request'}), 404)


@app.errorhandler(400)
def bad_req(error):
    return flask.make_response(flask.jsonify({'error': error.description}), 400)


if __name__ == '__main__':
    app.run(debug=True)