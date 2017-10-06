from django.test import TestCase
from django.core.urlresolvers import reverse
from operator import itemgetter
# from models.models import Location, Student, Group
from .models import Group

group_pk = 0

class GetUserIndexTestCase(TestCase):
    def setUp(self):
        pass

    def test_success_empty(self):
        response = self.client.get(reverse('group_index')).json()

        self.assertEquals(response['status'], 'ok')
        self.assertEquals(response['groups'], [])

    def test_success_one(self):
        global group_pk
        grp = Group(name='Test Group', size=3)
        grp.save()
        group_pk += 1

        response = self.client.get(reverse('group_index')).json()

        self.assertEquals(response['status'], 'ok')
        self.assertEquals(response['groups'], [{
            'id': group_pk,
            'size': 3,
            'name': 'Test Group',
        }, ])

    def test_success_many(self):
        global group_pk
        grp = Group(name='Test Group', size=2)
        grp.save()
        group_pk += 1
        grp = Group(name='Test Group 2', size=3)
        grp.save()
        group_pk += 1
        response = self.client.get(reverse('group_index')).json()

        self.assertEquals(response['status'], 'ok')
        self.assertEquals(sorted(response['groups'], key=itemgetter('id')), [{
                'id': group_pk - 1,
                'size': 2,
                'name': 'Test Group',
            },
            {
                'id': group_pk,
                'size': 3,
                'name': 'Test Group 2',
            }
        ])

    def tearDown(self):
        pass

class CRUDUserTestCase(TestCase):

    def setUp(self):
        pass

    def test_create_get(self):
        global group_pk
        response = self.client.post(reverse('create_group'),
                                    {'name': 'Test Group',
                                     'size': 3}).json()
        group_pk += 1
        self.assertEqual(response['status'], 'ok')

        response = self.client.get(reverse('get_group', args=[group_pk])).json()
        self.assertEqual(response['status'], 'ok')
        self.assertDictEqual(response['group'], {
            'id': group_pk,
            'name': 'Test Group',
            'size': 3,
        })

    def test_crud_failure(self):
        global group_pk

        # Test failures for create_group
        response = self.client.post(reverse('create_group'),
                                    {'size': 3}).json()
        self.assertEqual(response['status'], 'bad request')
        response = self.client.post(reverse('create_group'),
                                    {'name': 'Test Group'}).json()
        self.assertEqual(response['status'], 'bad request')
        response = self.client.post(reverse('create_group'), {}).json()
        self.assertEqual(response['status'], 'bad request')

        # Test failures for get_group
        response = self.client.get(reverse('get_group', args=[9999]))
        self.assertEqual(response.status_code, 404)

        # Test failures for delete_student
        response = self.client.post(reverse('delete_group', args=[9999]))
        self.assertEqual(response.status_code, 404)

        # Test failures for update
        response = self.client.post(reverse('update_group', args=[9999]))
        self.assertEqual(response.status_code, 404)
        grp = Group(name='Test Group', size=3)
        grp.save()
        group_pk += 1
        response = self.client.post(reverse('update_group', args=[group_pk]),
                                    {}).json()
        self.assertEqual(response['status'], 'bad request')

    def test_update(self):
        global group_pk
        grp = Group(name='Test Group', size=0)
        grp.save()
        group_pk += 1

        response = self.client.post(reverse('update_group', args=[group_pk]),
                                    {'name': 'Updated Group'}).json()
        self.assertEqual(response['status'], 'ok')
        response = self.client.get(reverse('get_group', args=[group_pk])).json()
        self.assertDictEqual(response['group'], {
            'id': group_pk,
            'name': 'Updated Group',
            'size': 0,
        })

        response = self.client.post(reverse('update_group', args=[group_pk]),
                                    {'size': 1}).json()
        self.assertEqual(response['status'], 'ok')
        response = self.client.get(reverse('get_group', args=[group_pk])).json()
        self.assertDictEqual(response['group'], {
            'id': group_pk,
            'name': 'Updated Group',
            'size': 1,
        })

        response = self.client.post(reverse('update_group', args=[group_pk]),
                                    {'size': 2, 'name': 'Test Group'}).json()
        self.assertEqual(response['status'], 'ok')
        response = self.client.get(reverse('get_group', args=[group_pk])).json()
        self.assertDictEqual(response['group'], {
            'id': group_pk,
            'name': 'Test Group',
            'size': 2,
        })

    def test_delete(self):
        global group_pk
        grp = Group(name='Test Group', size=0)
        grp.save()
        group_pk += 1

        response = self.client.get(reverse('group_index')).json()
        self.assertNotEqual(response['groups'], [])

        response = self.client.post(reverse('delete_group', args=[group_pk])).json()
        self.assertEqual(response['status'], 'ok')

        response = self.client.get(reverse('group_index')).json()
        self.assertEqual(response['groups'], [])


    def tearDown(self):
        pass
