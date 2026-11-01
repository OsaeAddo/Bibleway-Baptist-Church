import os
from unittest import mock

from django.test import SimpleTestCase, TestCase
from django.urls import reverse, resolve
from django.contrib.auth import get_user_model



from django.contrib.auth.models import Group

from .views import home, leader_signup_view, member_signup_view, send_admin_sms
from .forms import LeaderForm, ChurchMemberForm
from .models import ChurchLeader, ChurchMember



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


class MemberSearchTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        User = get_user_model()
        admins = Group.objects.create(name='ADMINS')
        leaders = Group.objects.create(name='LEADERS')
        members = Group.objects.create(name='MEMBERS')

        cls.admin = User.objects.create_user('admin1', password='pass12345')
        admins.user_set.add(cls.admin)

        cls.leader = User.objects.create_user('leader1', password='pass12345')
        leaders.user_set.add(cls.leader)
        ChurchLeader.objects.create(user=cls.leader, status=True)

        cls.pending_leader = User.objects.create_user('leader2', password='pass12345')
        leaders.user_set.add(cls.pending_leader)
        ChurchLeader.objects.create(user=cls.pending_leader, status=False)

        cls.plain_member = User.objects.create_user('member1', password='pass12345')
        members.user_set.add(cls.plain_member)

        approved = User.objects.create_user('ama', first_name='Ama', last_name='Mensah', password='pass12345')
        pending = User.objects.create_user('kofi', first_name='Kofi', last_name='Boateng', password='pass12345')
        # bulk_create skips ChurchMember.save(), which opens the profile picture file from disk
        ChurchMember.objects.bulk_create([
            ChurchMember(user=approved, member_role='Singer', mobile='0240000001',
                         residential_address='Accra', status=True),
            ChurchMember(user=pending, member_role='Usher', mobile='0240000002',
                         residential_address='Kumasi', status=False),
        ])
        cls.url = reverse('search-members')

    def test_anonymous_user_is_redirected_to_login(self):
        response = self.client.get(self.url, {'q': 'Ama'})
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('adminlogin'), response.url)

    def test_plain_member_is_forbidden(self):
        self.client.force_login(self.plain_member)
        response = self.client.get(self.url, {'q': 'Ama'})
        self.assertEqual(response.status_code, 403)

    def test_unapproved_leader_is_forbidden(self):
        self.client.force_login(self.pending_leader)
        response = self.client.get(self.url, {'q': 'Ama'})
        self.assertEqual(response.status_code, 403)

    def test_admin_can_search_by_name(self):
        self.client.force_login(self.admin)
        response = self.client.get(self.url, {'q': 'ama'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recordsManagement/searchresults_member.html')
        self.assertContains(response, 'Ama Mensah')
        self.assertNotContains(response, 'Kofi Boateng')

    def test_search_by_role_is_case_insensitive(self):
        self.client.force_login(self.admin)
        response = self.client.get(self.url, {'q': 'SINGER'})
        self.assertContains(response, 'Ama Mensah')

    def test_admin_sees_pending_members(self):
        self.client.force_login(self.admin)
        response = self.client.get(self.url, {'q': 'Kofi'})
        self.assertContains(response, 'Kofi Boateng')

    def test_leader_only_sees_approved_members(self):
        self.client.force_login(self.leader)
        approved = self.client.get(self.url, {'q': 'Ama'})
        self.assertContains(approved, 'Ama Mensah')
        pending = self.client.get(self.url, {'q': 'Kofi'})
        self.assertNotContains(pending, 'Kofi Boateng')
        self.assertContains(pending, 'No members found.')

    def test_empty_query_returns_no_members_and_does_not_crash(self):
        self.client.force_login(self.admin)
        for params in ({}, {'q': ''}, {'q': '   '}):
            response = self.client.get(self.url, params)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(response.context['member_list']), 0)


class AdminSmsTests(SimpleTestCase):
    TWILIO_ENV = {
        'TWILIO_ACCOUNT_SID': 'AC-test',
        'TWILIO_AUTH_TOKEN': 'token-test',
        'TWILIO_FROM_NUMBER': '+10000000000',
        'ADMIN_PHONE_NUMBER': '+233000000000',
    }

    def test_sms_is_skipped_when_twilio_is_not_configured(self):
        with mock.patch.dict(os.environ, {}, clear=True), \
                mock.patch('recordsManagement.views.Client') as client_cls:
            send_admin_sms('hello')
        client_cls.assert_not_called()

    def test_sms_is_sent_with_credentials_from_environment(self):
        with mock.patch.dict(os.environ, self.TWILIO_ENV, clear=True), \
                mock.patch('recordsManagement.views.Client') as client_cls:
            send_admin_sms('hello')
        client_cls.assert_called_once_with('AC-test', 'token-test')
        client_cls.return_value.messages.create.assert_called_once_with(
            body='hello', from_='+10000000000', to='+233000000000'
        )

    def test_twilio_failure_does_not_break_the_caller(self):
        with mock.patch.dict(os.environ, self.TWILIO_ENV, clear=True), \
                mock.patch('recordsManagement.views.Client') as client_cls:
            client_cls.return_value.messages.create.side_effect = RuntimeError('boom')
            with self.assertLogs('recordsManagement.views', level='ERROR'):
                send_admin_sms('hello')