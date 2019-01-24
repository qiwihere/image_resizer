import requests
import json

'''Класс для тестирования всей работы сервиса, объединяющий юнит-тесты'''
class ImageResizerTest:
    def __init__(self, image, width, height):
        self.image = image
        self.width = str(width)
        self.height = str(height)

    def test_loader(self,image):
        file = open(image, 'rb')
        data = {'size': '{"height": "'+self.height+'", "width": "'+self.height+'"}'}
        r = requests.post('http://localhost:5000/resizer/load', files=dict(file=file), data=data)
        return r.text

    def test_get(self, taskid):
        data = {'task_id': taskid}
        r = requests.get('http://localhost:5000/resizer/get/', data=data)
        return r.text

    def test_downloader(self, link):
        data = {'filename': link}
        r = requests.get('http://localhost:5000/resizer/download/', data=data)
        return r.content

    def test(self):
        loader_response = json.loads(self.test_loader(self.image))['result']
        print('__LOADER RESPONSE')
        print(loader_response)
        task_id = loader_response['id'] if 'id' in loader_response else None

        if not task_id:
            print('loader error')
            return False

        get_response = json.loads(self.test_get(task_id))['result']
        print('__GET RESPONSE')
        print(get_response)
        image_path = get_response['path'] if 'path' in get_response else None

        if not image_path:
            print('get error')
            return False

        print('__DOWNLOADER')
        downloader_content = self.test_downloader(image_path)
        if downloader_content:
            print('success')
        else:
            print('downloader error')

