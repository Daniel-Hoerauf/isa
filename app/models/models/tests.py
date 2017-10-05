from django.test import TestCase
from django.core.urlresolvers import reverse
from operator import itemgetter
# from models.models import Location, Student, Group
from .models import Student

class GetUserIndexTestCase(TestCase):
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
            'id': 3,
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
