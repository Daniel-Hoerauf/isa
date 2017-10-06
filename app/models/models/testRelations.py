from django.test import TransactionTestCase
from django.core.urlresolvers import reverse
from .models import Group, Student

class RelationModificationTestCase(TransactionTestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_students_one_group(self):
        stud = Student(name='Test User', year=0)
        stud.save()

        grp = Group(name='Test Group', size=5)
        grp.save()

        response = self.client.post(reverse('add_to_group', args=[1, 1])).json()
        self.assertEqual(response['status'], 'ok')

        response = self.client.get(reverse('student_index')).json()
        self.assertEqual(response['students'], [{
            'id': 1,
            'year': 0,
            'name': 'Test User',
            'groups': [{
                'id': 1,
                'name': 'Test Group'
            }]
        }])

        response = self.client.post(reverse('remove_from_group',
                                            args=[1, 1])).json()
        self.assertEqual(response['status'], 'ok')

        response = self.client.get(reverse('student_index')).json()
        self.assertEqual(response['students'], [{
            'id': 1,
            'year': 0,
            'name': 'Test User',
            'groups': []
        }])

    def test_students_multiple_groups(self):
        stud = Student(name='Test User', year=0)
        stud.save()

        grp = Group(name='Test Group', size=5)
        grp.save()

        grp = Group(name='Test Group 2', size=5)
        grp.save()

        response = self.client.post(reverse('add_to_group', args=[1, 1])).json()
        self.assertEqual(response['status'], 'ok')

        response = self.client.post(reverse('add_to_group', args=[2, 1])).json()
        self.assertEqual(response['status'], 'ok')

        response = self.client.get(reverse('student_index')).json()
        self.assertEqual(response['students'], [{
            'id': 1,
            'year': 0,
            'name': 'Test User',
            'groups': [{
                'id': 1,
                'name': 'Test Group'
            }, {
                'id': 2,
                'name': 'Test Group 2'
            }]
        }])

        response = self.client.post(reverse('remove_from_group',
                                            args=[2, 1])).json()
        self.assertEqual(response['status'], 'ok')

        response = self.client.get(reverse('student_index')).json()
        self.assertEqual(response['students'], [{
            'id': 1,
            'year': 0,
            'name': 'Test User',
            'groups': [{
                'id': 1,
                'name': 'Test Group'
            }]
        }])
