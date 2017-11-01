from django.test import TransactionTestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.hashers import check_password, make_password

from .models import User, Authenticator, Student
from .models import create_authenticator

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

    def test_login(self):
        stud = Student(name='Test Student', year=3)
        stud.save()
        passwd = make_password('p4ssw0rd')
        user = User(student=stud, password=passwd, username='test_user')
        user.save()

        resp = self.client.post(reverse('login', args=[user.pk]),
                                {'password': 'p4ssw0rd'}).json()
        self.assertEqual(resp['status'], 'ok')
        self.assertEqual(resp['authenticated'], True)

        auth = Authenticator.objects.get(pk=resp['authenticator'])
        self.assertEqual(auth.user_id, user)

    def test_login_bad(self):
        stud = Student(name='Test Student', year=3)
        stud.save()
        passwd = make_password('p4ssw0rd')
        user = User(student=stud, password=passwd, username='test_user')
        user.save()

        resp = self.client.post(reverse('login', args=[user.pk]),
                                {'password': 'password'}).json()
        self.assertEqual(resp['status'], 'ok')
        self.assertFalse(resp['authenticated'])
        self.assertFalse(resp['authenticator'])

        resp = self.client.post(reverse('login', args=[user.pk])).json()
        self.assertEqual(resp['status'], 'ok')
        self.assertFalse(resp['authenticated'])
        self.assertFalse(resp['authenticator'])

    def test_logout(self):
        stud = Student(name='Test Student', year=3)
        stud.save()
        passwd = make_password('p4ssw0rd')
        user = User(student=stud, password=passwd, username='test_user')
        user.save()

        auth = create_authenticator(user)
        self.assertTrue(Authenticator.objects.get(authenticator=auth))

        resp = self.client.post(reverse('logout'), {'authenticator': auth}
                                ).json()
        self.assertEqual(Authenticator.objects.all().count(), 0)


class AuthenticatorTestCase(TransactionTestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_validate(self):
        stud = Student(name='Test Student', year=3)
        stud.save()
        passwd = make_password('p4ssw0rd')
        user = User(student=stud, password=passwd, username='test_user')
        user.save()

        auth = create_authenticator(user)
        self.assertTrue(Authenticator.objects.get(authenticator=auth))

        resp = self.client.post(reverse('validate'),
                                {'authenticator': auth}).json()
        self.assertEqual(resp['status'], 'ok')
        self.assertTrue(resp['authenticated'])

