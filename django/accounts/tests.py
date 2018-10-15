from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse


class RegisterTestCase(TestCase):
    def setUp(self):
        self.url = reverse('register')

    def test_register_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Sign Up For Your Account')

    def test_register_good(self):
        # JMT: for now, only test the good case
        fields = {
            'username': 'testuser',
            'password1': 'testpass!',
            'password2': 'testpass!',
            'email': 'test@example.com',
        }
        response = self.client.post(self.url, fields, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Welcome, Testuser!')


def user_login(func):
    def _decorator(self, *args, **kwds):
        username = 'user'
        rawpass = 'p@ssword'

        logged_in = self.client.login(username=username, password=rawpass)
        self.assertTrue(logged_in)
        func(self, *args, **kwds)
        self.client.logout()
    return _decorator


class MyAccountTestCase(TestCase):
    fixtures = ['accounts', 'checkout', 'meadery']

    def setUp(self):
        self.url = reverse('my_account')

    def test_myaccount_notloggedin(self):
        response = self.client.get(self.url, follow=True)
        self.assertEqual(response.status_code, 200)
        redirect_target = '{0}?next={1}'.format(reverse('login'), self.url)
        redirect_chain = [(redirect_target, 302)]
        self.assertEqual(response.redirect_chain, redirect_chain)

    @user_login
    def test_myaccount_loggedin(self):
        response = self.client.get(self.url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Welcome, User!')
        self.assertContains(response, 'Order #1 - Oct. 27, 2012 (view)')


class OrderDetailsTestCase(TestCase):
    fixtures = ['accounts', 'checkout', 'meadery']

    def setUp(self):
        self.orderpk = 1
        self.url = reverse('order_details', args=[self.orderpk, ])

    @user_login
    def test_orderdetails(self):
        response = self.client.get(self.url, follow=True)
        self.assertContains(response, "Details for Order # {}".format(self.orderpk))


class OrderInfoTestCase(TestCase):
    fixtures = ['accounts', 'checkout', 'meadery']

    def setUp(self):
        self.url = reverse('order_info')

    @user_login
    def test_orderinfo_get_then_post(self):
        old_email = User.objects.get(username='user').email
        new_email = 'user2@example.org'
        response = self.client.get(self.url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Edit Order Information')
        fields = response.context['form'].initial
        self.assertEqual(fields['email'], old_email)
        fields['email'] = new_email
        response = self.client.post(self.url, fields, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(old_email, new_email)
