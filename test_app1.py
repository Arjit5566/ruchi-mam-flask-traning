import unittest

from app1 import app


class App1CalculatorTestCase(unittest.TestCase):
    def test_addition(self):
        client = app.test_client()
        response = client.post('/', data={'num1': '10', 'num2': '5', 'operation': '+'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('15', response.get_data(as_text=True))

    def test_subtraction(self):
        client = app.test_client()
        response = client.post('/', data={'num1': '10', 'num2': '5', 'operation': '-'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('5', response.get_data(as_text=True))

    def test_multiplication(self):
        client = app.test_client()
        response = client.post('/', data={'num1': '10', 'num2': '5', 'operation': '*'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('50', response.get_data(as_text=True))

    def test_division(self):
        client = app.test_client()
        response = client.post('/', data={'num1': '10', 'num2': '5', 'operation': '/'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('2', response.get_data(as_text=True))


if __name__ == '__main__':
    unittest.main()
