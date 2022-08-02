from urllib import response
from django.test import SimpleTestCase
from django.urls import reverse, resolve


from .views import home


class HomePageTests(SimpleTestCase):
    def setUp(self):
        url = reverse('home-page')
        self.response = self.client.get(url)


    def test_homepage_status_code(self):
        self.assertEqual(self.response.status_code, 200)
        
        
    def test_homepage_template(self):
        self.assertTemplateUsed(self.response, 'recordsManagement/home.html')
        
        
# Create your tests here.
