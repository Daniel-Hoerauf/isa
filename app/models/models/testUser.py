from django.test import TestCase
from django.core.urlresolvers import reverse
from operator import itemgetter
# from models.models import Location, Student, Group
from .models import Student

user_pk = 0

class GetUserIndexTestCase(TestCase):
    def setUp(self):
        pass

    def test_success_empty(self):
        response = self.client.get(reverse('student_index')).json()

        self.assertEquals(response['status'], 'ok')
        self.assertEquals(response['students'], [])

    def test_success_one(self):
        global user_pk
        stud = Student(name='Test User', year=0)
        stud.save()
        user_pk += 1

        response = self.client.get(reverse('student_index')).json()

        self.assertEquals(response['status'], 'ok')
        self.assertEquals(response['students'], [{
            'id': user_pk,
            'year': 0,
            'groups': [],
            'name': 'Test User',
        }, ])

    def test_success_many(self):
        global user_pk
        stud = Student(name='Test User', year=0)
        stud.save()
        user_pk += 1
        stud = Student(name='Test User 2', year=1)
        stud.save()
        user_pk += 1
        response = self.client.get(reverse('student_index')).json()

        self.assertEquals(response['status'], 'ok')
        self.assertEquals(sorted(response['students'], key=itemgetter('id')), [{
                'id': user_pk - 1,
                'year': 0,
                'groups': [],
                'name': 'Test User',
            },
            {
                'id': user_pk,
                'year': 1,
                'groups': [],
                'name': 'Test User 2',
            }
        ])

    def tearDown(self):
        pass

class CRUDUserTestCase(TestCase):

    def setUp(self):
        pass

    def test_create_get(self):
        global user_pk
        response = self.client.post(reverse('create_student'),
                                    {'name': 'Test User',
                                     'year': 3}).json()
        user_pk += 1
        self.assertEqual(response['status'], 'ok')

        response = self.client.get(reverse('get_student', args=[user_pk])).json()
        self.assertEqual(response['status'], 'ok')
        self.assertDictEqual(response['student'], {
            'id': user_pk,
            'name': 'Test User',
            'year': 3,
            'groups': []
        })

    def test_crud_failure(self):
        global user_pk

        # Test failures for create_student
        response = self.client.post(reverse('create_student'),
                                    {'year': 3}).json()
        self.assertEqual(response['status'], 'bad request')
        response = self.client.post(reverse('create_student'),
                                    {'name': 'Test User'}).json()
        self.assertEqual(response['status'], 'bad request')
        response = self.client.post(reverse('create_student'), {}).json()
        self.assertEqual(response['status'], 'bad request')

        # Test failures for get_student
        response = self.client.get(reverse('get_student', args=[9999]))
        self.assertEqual(response.status_code, 404)

        # Test failures for delete_student
        response = self.client.post(reverse('delete_student', args=[9999]))
        self.assertEqual(response.status_code, 404)

        # Test failures for update
        response = self.client.post(reverse('update_student', args=[9999]))
        self.assertEqual(response.status_code, 404)
        stud = Student(name='Test User', year=0)
        stud.save()
        user_pk += 1
        response = self.client.post(reverse('update_student', args=[user_pk]),
                                    {}).json()
        self.assertEqual(response['status'], 'bad request')

    def test_update(self):
        global user_pk
        stud = Student(name='Test User', year=0)
        stud.save()
        user_pk += 1

        response = self.client.post(reverse('update_student', args=[user_pk]),
                                    {'name': 'Updated User'}).json()
        self.assertEqual(response['status'], 'ok')
        response = self.client.get(reverse('get_student', args=[user_pk])).json()
        self.assertDictEqual(response['student'], {
            'id': user_pk,
            'name': 'Updated User',
            'year': 0,
            'groups': []
        })

        response = self.client.post(reverse('update_student', args=[user_pk]),
                                    {'year': 1}).json()
        self.assertEqual(response['status'], 'ok')
        response = self.client.get(reverse('get_student', args=[user_pk])).json()
        self.assertDictEqual(response['student'], {
            'id': user_pk,
            'name': 'Updated User',
            'year': 1,
            'groups': []
        })

        response = self.client.post(reverse('update_student', args=[user_pk]),
                                    {'year': 2, 'name': 'Test Student'}).json()
        self.assertEqual(response['status'], 'ok')
        response = self.client.get(reverse('get_student', args=[user_pk])).json()
        self.assertDictEqual(response['student'], {
            'id': user_pk,
            'name': 'Test Student',
            'year': 2,
            'groups': []
        })

    def test_delete(self):
        global user_pk
        stud = Student(name='Test User', year=0)
        stud.save()
        user_pk += 1

        response = self.client.get(reverse('student_index')).json()
        self.assertNotEqual(response['students'], [])

        response = self.client.post(reverse('delete_student', args=[user_pk])).json()
        self.assertEqual(response['status'], 'ok')

        response = self.client.get(reverse('student_index')).json()
        self.assertEqual(response['students'], [])


    def tearDown(self):
        pass
