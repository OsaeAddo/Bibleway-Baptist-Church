from django.test import SimpleTestCase, TestCase
from django.urls import reverse, resolve
from django.contrib.auth import get_user_model



from .views import home, leader_signup_view, member_signup_view
from .forms import LeaderForm, ChurchMemberForm



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
        
        
class MemberSignupPageTests(TestCase):
    
    def setUp(self):
        url = reverse('member-signup')
        self.response = self.client.get(url)
    
    def test_member_signup_template(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, 'recordsManagement/churchmember_signup.html')
        self.assertContains(self.response, 'Church Member Signup')
        
        
    def test_member_signup_form(self):
        form = self.response.context.get('churchmemberForm')
        self.assertIsInstance(form, ChurchMemberForm)
        self.assertContains(self.response, 'csrfmiddlewaretoken')
        
    
    def test_member_signup_view(self):
        view = resolve('/church-member-signup/')
        self.assertEqual(
            view.func.__name__,
            member_signup_view.__name__
        )
        
        
class AdminDashboardPageTests(TestCase):
    
    def setUp(self):
        url = reverse('churchadmin-dashboard')
        self.response = self.client.get(url)
    
    def test_admin_dashboard_template(self):
        self.assertEqual(self.response.status_code, 302) # redirect to admin login page if not authenticated