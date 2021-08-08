import unittest
import requests

from app import app
# set the application to testing mode
app.testing = True


class TestApi(unittest.TestCase):
    BASE = "http://127.0.0.1:5000/"

    def test_1(self):
        payload = {'value': 'value1', 'mode': 'value2', 'replace_with': 'null'}
        expected = {'message': {'mode': 'phone || name || amount'}}
        res = requests.post(TestApi.BASE, json=payload)
        self.assertEqual(res.status_code, 201)
        self.assertEqual(res.json(), expected)

    def test_2(self): # Take a look
        payload = {'value': 'value1', 'mode': 'value2', 'wrong_key': 'null'}
        expected = {'message': {'replace_with': 'Choose either --blank-- || --original--'}}
        res = requests.post(TestApi.BASE, json=payload)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.json(), expected)

    def test_3(self):
        payload = {'value': 'value1', 'mode': 'value2', 'replace_with': '--original--'}
        expected = {'message': {'mode': 'phone || name || amount'}}
        res = requests.post(TestApi.BASE, json=payload)
        self.assertEqual(res.status_code, 201)
        self.assertEqual(res.json(), expected)

    def test_4(self):
        payload = {'value': 'value1', 'mode': 'value2', 'replace_with': '--blank--'}
        expected = {'message': {'mode': 'phone || name || amount'}}
        res = requests.post(TestApi.BASE, json=payload)
        self.assertEqual(res.status_code, 201)
        self.assertEqual(res.json(), expected)

    def test_5(self):
        payload = {'value': 'value1', 'mode': 'name', 'replace_with': '--blank--'}
        expected = {'original_value': 'value1', 'mode': 'name', 'output': {'first': '--blank--', 'middle': '--blank--', 'last': '--blank--'}}
        res = requests.post(TestApi.BASE, json=payload)
        self.assertEqual(res.status_code, 201)
        self.assertEqual(res.json(), expected)

    def test_6(self):
        payload = {'value': 'value1', 'mode': 'phone', 'replace_with': '--blank--'}
        expected = {'original_value': 'value1', 'mode': 'phone', 'output': '--blank--'}
        res = requests.post(TestApi.BASE, json=payload)
        self.assertEqual(res.status_code, 201)
        self.assertEqual(res.json(), expected)

    def test_7(self):
        payload = {'value': 'value1', 'mode': 'amount', 'replace_with': '--blank--'}
        expected = {'message': 'Internal Server Error'}
        res = requests.post(TestApi.BASE, json=payload)
        self.assertEqual(res.status_code, 201)
        self.assertEqual(res.json(), expected)

    def test_8(self):
        payload = {'value': '(512) 234-9293', 'mode': 'phone', 'replace_with': '--blank--'}
        expected = {'original_value': '(512) 234-9293', 'mode': 'phone', 'output': '5122349293'}
        res = requests.post(TestApi.BASE, json=payload)
        self.assertEqual(res.status_code, 201)
        self.assertEqual(res.json(), expected)

    def test_9(self):
        payload = {'value': 'unknown', 'mode': 'phone', 'replace_with': '--blank--'}
        expected = {'original_value': 'unknown', 'mode': 'phone', 'output': '--blank--'}
        res = requests.post(TestApi.BASE, json=payload)
        self.assertEqual(res.status_code, 201)
        self.assertEqual(res.json(), expected)

    def test_10(self):
        payload = {'value': 'unknown', 'mode': 'phone', 'replace_with': '--original--'}
        expected = {'original_value': 'unknown', 'mode': 'phone', 'output': 'unknown'}
        res = requests.post(TestApi.BASE, json=payload)
        self.assertEqual(res.status_code, 201)
        self.assertEqual(res.json(), expected)

    def test_11(self):
        payload = {'value': 'Robert Lance Smith', 'mode': 'name', 'replace_with': '--blank--'}
        expected = {'original_value': 'Robert Lance Smith', 'mode': 'name', 'output': {'first': 'Robert', 'middle': 'Lance', 'last': 'Smith'}}
        res = requests.post(TestApi.BASE, json=payload)
        self.assertEqual(res.status_code, 201)
        self.assertEqual(res.json(), expected)

    def test_12(self):
        payload = {'value': '12234', 'mode': 'name', 'replace_with': '--blank--'}
        expected = {'original_value': '12234', 'mode': 'name', 'output': {'first': '--blank--', 'middle': '--blank--', 'last': '--blank--'}}
        res = requests.post(TestApi.BASE, json=payload)
        self.assertEqual(res.status_code, 201)
        self.assertEqual(res.json(), expected)

    def test_13(self):
        payload = {'value': '-12234', 'mode': 'name', 'replace_with': '--blank--'}
        expected = {'original_value': '-12234', 'mode': 'name', 'output': {'first': '--blank--', 'middle': '--blank--', 'last': '--blank--'}}
        res = requests.post(TestApi.BASE, json=payload)
        self.assertEqual(res.status_code, 201)
        self.assertEqual(res.json(), expected)

    def test_14(self):
        payload = {'value': 'unknown', 'mode': 'name', 'replace_with': '--blank--'}
        expected = {'original_value': 'unknown', 'mode': 'name', 'output': {'first': '--blank--', 'middle': '--blank--', 'last': '--blank--'}}
        res = requests.post(TestApi.BASE, json=payload)
        self.assertEqual(res.status_code, 201)
        self.assertEqual(res.json(), expected)

    def test_15(self):
        payload = {'value': ' ', 'mode': 'name', 'replace_with': '--blank--'}
        expected = {'original_value': ' ', 'mode': 'name', 'output': {'first': '--blank--', 'middle': '--blank--', 'last': '--blank--'}}
        res = requests.post(TestApi.BASE, json=payload)
        self.assertEqual(res.status_code, 201)
        self.assertEqual(res.json(), expected)

    def test_16(self):
        payload = {'value': 'Robert Lance Smith', 'mode': 'name', 'replace_with': '--original--'}
        expected = {'original_value': 'Robert Lance Smith', 'mode': 'name', 'output': {'first': 'Robert', 'middle': 'Lance', 'last': 'Smith'}}
        res = requests.post(TestApi.BASE, json=payload)
        self.assertEqual(res.status_code, 201)
        self.assertEqual(res.json(), expected)

    def test_17(self):
        payload = {'value': '12234', 'mode': 'name', 'replace_with': '--original--'}
        expected = {'original_value': '12234', 'mode': 'name', 'output': '12234'}
        res = requests.post(TestApi.BASE, json=payload)
        self.assertEqual(res.status_code, 201)
        self.assertEqual(res.json(), expected)

    def test_18(self):
        payload = {'value': 'unknown', 'mode': 'name', 'replace_with': '--original--'}
        expected = {'original_value': 'unknown', 'mode': 'name', 'output': 'unknown'}
        res = requests.post(TestApi.BASE, json=payload)
        self.assertEqual(res.status_code, 201)
        self.assertEqual(res.json(), expected)

    def test_19(self):
        payload = {'value': ' ', 'mode': 'name', 'replace_with': '--original--'}
        expected = {'original_value': ' ', 'mode': 'name', 'output': ' '}
        res = requests.post(TestApi.BASE, json=payload)
        self.assertEqual(res.status_code, 201)
        self.assertEqual(res.json(), expected)

    def test_20(self):
        payload = {'value': '2 * 2', 'mode': 'amount', 'replace_with': '--blank--'}
        expected = {'original_value': '2 * 2', 'mode': 'amount', 'output': '4'}
        res = requests.post(TestApi.BASE, json=payload)
        self.assertEqual(res.status_code, 201)
        self.assertEqual(res.json(), expected)

    def test_21(self):
        payload = {'value': '3.14159 + 2', 'mode': 'amount', 'replace_with': '--blank--'}
        expected = {'original_value': '3.14159 + 2', 'mode': 'amount', 'output': '5.14'}
        res = requests.post(TestApi.BASE, json=payload)
        self.assertEqual(res.status_code, 201)
        self.assertEqual(res.json(), expected)

    def test_22(self):
        payload = {'value': 'dir()', 'mode': 'amount', 'replace_with': '--blank--'}
        expected = {'original_value': 'dir()', 'mode': 'amount', 'output': '--blank--'}
        res = requests.post(TestApi.BASE, json=payload)
        self.assertEqual(res.status_code, 201)
        self.assertEqual(res.json(), expected)

    def test_23(self):
        payload = {'value': 'dir()', 'mode': 'amount', 'replace_with': '--original--'}
        expected = {'original_value': 'dir()', 'mode': 'amount', 'output': 'dir()'}
        res = requests.post(TestApi.BASE, json=payload)
        self.assertEqual(res.status_code, 201)
        self.assertEqual(res.json(), expected)

