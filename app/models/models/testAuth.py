from django.test import TransactionTestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.hashers import check_password

from .models import User, Authenticator, Student

class UserManagementTestCase(TransactionTestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_signup(self):
        resp = self.client.post(reverse('signup'), {
            'name': 'Test Student',
            'year': 4,
            'username': 'test_user',
            'password': 'p4ssw0rd',
        }).json()

        self.assertEqual(resp['status'], 'ok')
        self.assertEqual(resp['authenticated'], True)
        self.assertTrue(resp['authenticator'])

        student = Student.objects.get(name='Test Student')
        self.assertEqual(student.year, 4)
        user = User.objects.get(student=student)
        self.assertEqual(user.username, 'test_user')
        self.assertTrue(check_password('p4ssw0rd', user.password))

        auth = Authenticator.objects.get(pk=resp['authenticator'])
        self.assertEqual(auth.user_id, user)

    def test_signup_bad(self):
        resp = self.client.post(reverse('signup'), {
            'username': 'test_user',
            'year': 4,
            'password': 'p4ssw0rd',
        }).json()
        self.assertEqual(resp['status'], 'bad request')
        self.assertEqual(resp['authenticated'], False)

        resp = self.client.post(reverse('signup'), {
            'name': 'test_user',
            'year': 4,
            'password': 'p4ssw0rd',
        }).json()
        self.assertEqual(resp['status'], 'bad request')
        self.assertEqual(resp['authenticated'], False)

        resp = self.client.post(reverse('signup'), {
            'username': 'test_user',
            'year': 4,
            'name': 'p4ssw0rd',
        }).json()
        self.assertEqual(resp['status'], 'bad request')
        self.assertEqual(resp['authenticated'], False)

        resp = self.client.post(reverse('signup'), {
            'name': 'Test Student',
            'username': 'test_user',
            'password': 'p4ssw0rd',
        }).json()
        self.assertEqual(resp['status'], 'bad request')
        self.assertEqual(resp['authenticated'], False)


class AuthenticatorTestCase(TransactionTestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass
