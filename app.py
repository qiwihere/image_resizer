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
    size = json.loads(flask.request.values.get('size'))
    width = size['width']
    height = size['height']
    file.save(file.filename)
    img = Image.open(file.filename)
    resized = img.resize((int(width), int(height)))
    resized.save('img_resized.bmp')

    return flask.jsonify({'result': True}), 201





@app.errorhandler(404)
def not_found(error):
    return flask.make_response(flask.jsonify({'error': 'Not found'}), 404)


@app.errorhandler(400)
def bad_req(error):
    return flask.make_response(flask.jsonify({'error': 'Bad request'}), 400)


if __name__ == '__main__':
    app.run(debug=True)