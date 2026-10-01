import unittest

from app import app


class AppTestCase(unittest.TestCase):
    def test_calculate_post_average(self):
        client = app.test_client()
        resp = client.post('/calculate', data={'maths': '80', 'science': '90', 'ai': '70'})
        self.assertEqual(resp.status_code, 200)
        self.assertIn('80.0', resp.get_data(as_text=True))


if __name__ == '__main__':
    unittest.main()
