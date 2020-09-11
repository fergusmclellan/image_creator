import unittest
from image_creation_app import app

my_multiline_input = f'''
import requests
mystring = requests.get(url, header, data)
this is being processed by Docker version
'''
image_filename = "item_1111111.png"

class TestHello(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.app = app.test_client()
    def test_hello(self):
        response = self.app.post('/api/add_message/1234', json={"mytext": my_multiline_input})
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.mimetype, 'image/png')
        print('Test confirmed that image received!')
if __name__ == '__main__':
    unittest.main()
