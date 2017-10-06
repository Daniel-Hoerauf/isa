from django.test import TransactionTestCase
from django.core.urlresolvers import reverse
from operator import itemgetter
from .models import Student

class GetUserIndexTestCase(TransactionTestCase):
    def setUp(self):
        pass

    def test_success_empty(self):
        response = self.client.get(reverse('student_index')).json()

        self.assertEquals(response['status'], 'ok')
        self.assertEquals(response['students'], [])

    def test_success_one(self):
        stud = Student(name='Test User', year=0)
        stud.save()

        response = self.client.get(reverse('student_index')).json()

        self.assertEquals(response['status'], 'ok')
        self.assertEquals(response['students'], [{
            'id': 1,
            'year': 0,
            'groups': [],
            'name': 'Test User',
        }, ])

    def test_success_many(self):
        stud = Student(name='Test User', year=0)
        stud.save()
        stud = Student(name='Test User 2', year=1)
        stud.save()
        response = self.client.get(reverse('student_index')).json()

        self.assertEquals(response['status'], 'ok')
        self.assertEquals(sorted(response['students'], key=itemgetter('id')), [{
                'id': 1,
                'year': 0,
                'groups': [],
                'name': 'Test User',
            },
            {
                'id': 2,
                'year': 1,
                'groups': [],
                'name': 'Test User 2',
            }
        ])

    def tearDown(self):
        pass

class CRUDUserTestCase(TransactionTestCase):

    def setUp(self):
        pass

    def test_create_get(self):
        global user_pk
        response = self.client.post(reverse('create_student'),
                                    {'name': 'Test User',
                                     'year': 3}).json()
        self.assertEqual(response['status'], 'ok')

        response = self.client.get(reverse('get_student', args=[1])).json()
        self.assertEqual(response['status'], 'ok')
        self.assertDictEqual(response['student'], {
            'id': 1,
            'name': 'Test User',
            'year': 3,
            'groups': []
        })

    def test_crud_failure(self):
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
        response = self.client.post(reverse('update_student', args=[1]),
                                    {}).json()
        self.assertEqual(response['status'], 'bad request')

    def test_update(self):
        global user_pk
        stud = Student(name='Test User', year=0)
        stud.save()

        response = self.client.post(reverse('update_student', args=[1]),
                                    {'name': 'Updated User'}).json()
        self.assertEqual(response['status'], 'ok')
        response = self.client.get(reverse('get_student', args=[1])).json()
        self.assertDictEqual(response['student'], {
            'id': 1,
            'name': 'Updated User',
            'year': 0,
            'groups': []
        })

        response = self.client.post(reverse('update_student', args=[1]),
                                    {'year': 1}).json()
        self.assertEqual(response['status'], 'ok')
        response = self.client.get(reverse('get_student', args=[1])).json()
        self.assertDictEqual(response['student'], {
            'id': 1,
            'name': 'Updated User',
            'year': 1,
            'groups': []
        })

        response = self.client.post(reverse('update_student', args=[1]),
                                    {'year': 2, 'name': 'Test Student'}).json()
        self.assertEqual(response['status'], 'ok')
        response = self.client.get(reverse('get_student', args=[1])).json()
        self.assertDictEqual(response['student'], {
            'id': 1,
            'name': 'Test Student',
            'year': 2,
            'groups': []
        })

    def test_delete(self):
        global user_pk
        stud = Student(name='Test User', year=0)
        stud.save()

        response = self.client.get(reverse('student_index')).json()
        self.assertNotEqual(response['students'], [])

        response = self.client.post(reverse('delete_student', args=[1])).json()
        self.assertEqual(response['status'], 'ok')

        response = self.client.get(reverse('student_index')).json()
        self.assertEqual(response['students'], [])


    def tearDown(self):
        pass
