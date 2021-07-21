from django.test import TestCase
from . import views
class ViewsTestCase(TestCase):
    def test_index_loads_properly(self):
        """If index page loads properly"""
        response = self.client.get('http://127.0.0.1:8000')
        self.assertEqual(response.status_code, 200)