import unittest
import requests
import json
import requests_mock

class Test_1(unittest.TestCase):

    @requests_mock.Mocker()
    def test_get_successfull_response_returns_text_json(self, m):
        data = [{'id':1, 'name':'John'}, {'id':2, 'name':'Jane'}]
        response_text = json.dumps(data)
        m.get('http://demo.com/api/user', text=response_text)
        actual = requests.get('http://demo.com/api/user')
        
        self.assertEqual(200, actual.status_code, 'OK')
        self.assertEqual(response_text, actual.text)
        self.assertEqual(data, actual.json())

    @requests_mock.Mocker()
    def test_get_not_registered_url_throws_exception(self, m):
        data = [{'id':1, 'name':'John'}, {'id':2, 'name':'Jane'}]
        response_text = json.dumps(data)
        m.get('http://demo.com/api/user', text=response_text)
        with self.assertRaises(Exception) as excinfo:
            actual = requests.get('http://demo112.com/api/user')

    @requests_mock.Mocker()
    def test_get_protocolless_matchikng(self, m):
        response_text = 'Jeronimo'
        m.get('//demo.com/', text=response_text)
        self.assertEqual(response_text, requests.get('https://demo.com').text, 'Works with https')
        self.assertEqual(response_text, requests.get('bibop://demo.com').text, 'Works with bibop')


    @requests_mock.Mocker()
    def test_get_path_matchikng(self, m):
        response_text = 'Jeronimo'
        m.get('/api', text=response_text)
        self.assertEqual(response_text, requests.get('https://demo.com/api').text, 'Works with https://demo.com')
        self.assertEqual(response_text, requests.get('bibop://nowhere.com/api').text, 'Works with bibop://nowhere.com')


    @requests_mock.Mocker()
    def test_custom_matching(self, m):
        def custom_matcher(request):
            print(request.path_url)
            if request.path_url == '/test':
                resp = requests.Response()
                resp.status_code = 200
                return resp
            return None
        
        response_text = 'Jeronimo'
        # m.get(custom_matcher, text=response_text)
        m._adapter.add_matcher(custom_matcher)
        response = requests.get('https://domain.com/test')
        self.assertEqual(200, response.status_code)

    

