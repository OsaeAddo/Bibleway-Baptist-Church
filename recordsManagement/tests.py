from urllib import response
from django.test import SimpleTestCase
from django.urls import reverse, resolve
from django.contrib.auth import get_user_model



from .views import home, leader_signup_view
from .forms import LeaderForm, LeaderUserForm



class HomePageTests(SimpleTestCase):
    def setUp(self):
        url = reverse('home-page')
        self.response = self.client.get(url)


    def test_homepage_status_code(self):
        self.assertEqual(self.response.status_code, 200)
        
        
    def test_homepage_template(self):
        self.assertTemplateUsed(self.response, 'recordsManagement/home.html')
        
        
        
    def test_homepage_url_resolves_homepageview(self):
        view = resolve('/')
        self.assertEqual(
            view.func.__name__,
            home.__name__
        )
        
        
class LeaderSignupPageTests(TestCase):
    
    def setUp(self):
        url = reverse('leader-signup')
        self.response = self.client.get(url)
    
    def test_leader_signup_template(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, 'recordsManagement/leader_signup.html')
        self.assertContains(self.response, 'Church Leader Signup')
        
        
    def test_leader_signup_form(self):
        form = self.response.context.get('leaderForm')
        self.assertIsInstance(form, LeaderForm)
        self.assertContains(self.response, 'csrfmiddlewaretoken')
        
    
    def test_leader_signup_view(self):
        view = resolve('/church-leader-signup/')
        self.assertEqual(
            view.func.__name__,
            leader_signup_view.__name__
        )