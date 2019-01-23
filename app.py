import flask
import json
from PIL import Image
from RedisHandler import RedisHandler

app = flask.Flask(__name__)

rh = RedisHandler()


@app.route('/resizer/load', methods=['GET', 'POST'])
def resize_image():
    if not 'file' in flask.request.files or not 'size' in flask.request.values:
        return flask.abort(400)

    file = flask.request.files['file']
    splitted_filename = file.filename.split('.')
    filename = splitted_filename[0]
    format = splitted_filename[1]

    if not format in ('jpg', 'png', 'jpeg'):
        return flask.abort(400)

    size = json.loads(flask.request.values.get('size').encode('utf-8'))
    width = size['width']
    height = size['height']
    if not width or not height:
        return flask.abort(400)

    file.save(file.filename)
    img = Image.open(file.filename)
    resized = img.resize((int(width), int(height)))
    new_filename = filename+width+'x'+height+'.'+format
    resized.save(new_filename)

    new_task_id = rh.get_new_id()

    task = {
        'id': new_task_id,
        'status': 'ok',
        'path': flask.request.base_url+"/"+new_filename
    }
    rh.add_new_task(new_task_id,task)
    return flask.jsonify({'result': task}), 201


@app.errorhandler(404)
def not_found(error):
    return flask.make_response(flask.jsonify({'error': 'Not found'}), 404)


@app.errorhandler(400)
def bad_req(error):
    return flask.make_response(flask.jsonify({'error': 'Bad request'}), 400)


if __name__ == '__main__':
    app.run(debug=True)