from django.test import TransactionTestCase
from django.core.urlresolvers import reverse
from operator import itemgetter
from .models import Group

class GetGroupIndexTestCase(TransactionTestCase):
    def setUp(self):
        pass

    def test_success_empty(self):
        response = self.client.get(reverse('group_index')).json()

        self.assertEquals(response['status'], 'ok')
        self.assertEquals(response['groups'], [])

    def test_success_one(self):
        grp = Group(name='Test Group', size=3)
        grp.save()

        response = self.client.get(reverse('group_index')).json()

        self.assertEquals(response['status'], 'ok')
        self.assertEquals(response['groups'], [{
            'id': 1,
            'size': 3,
            'name': 'Test Group',
            'description': 'Come and learn!',
        }, ])

    def test_success_many(self):
        grp = Group(name='Test Group', size=2)
        grp.save()
        grp = Group(name='Test Group 2', size=3)
        grp.save()
        response = self.client.get(reverse('group_index')).json()

        self.assertEquals(response['status'], 'ok')
        self.assertEquals(sorted(response['groups'], key=itemgetter('id')), [{
                'id': 1,
                'size': 2,
                'name': 'Test Group',
                'description': 'Come and learn!',
            },
            {
                'id': 2,
                'size': 3,
                'name': 'Test Group 2',
                'description': 'Come and learn!',
            }
        ])

    def tearDown(self):
        pass

class CRUDUserTestCase(TransactionTestCase):

    def setUp(self):
        pass

    def test_create_get(self):
        response = self.client.post(reverse('create_group'),
                                    {'name': 'Test Group',
                                     'size': 3,
                                     'description': 'This is a test group'}).json()
        self.assertEqual(response['status'], 'ok')

        response = self.client.get(reverse('get_group', args=[1])).json()
        self.assertEqual(response['status'], 'ok')
        self.assertDictEqual(response['group'], {
            'id': 1,
            'name': 'Test Group',
            'size': 3,
            'description': 'This is a test group',
        })

    def test_crud_failure(self):
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
        response = self.client.post(reverse('update_group', args=[1]),
                                    {}).json()
        self.assertEqual(response['status'], 'bad request')

    def test_update(self):
        grp = Group(name='Test Group', size=0)
        grp.save()

        response = self.client.post(reverse('update_group', args=[1]),
                                    {'name': 'Updated Group'}).json()
        self.assertEqual(response['status'], 'ok')
        response = self.client.get(reverse('get_group', args=[1])).json()
        self.assertDictEqual(response['group'], {
            'id': 1,
            'name': 'Updated Group',
            'size': 0,
            'description': 'Come and learn!',
        })

        response = self.client.post(reverse('update_group', args=[1]),
                                    {'size': 1}).json()
        self.assertEqual(response['status'], 'ok')
        response = self.client.get(reverse('get_group', args=[1])).json()
        self.assertDictEqual(response['group'], {
            'id': 1,
            'name': 'Updated Group',
            'size': 1,
            'description': 'Come and learn!',
        })

        response = self.client.post(reverse('update_group', args=[1]),
                                    {'size': 2, 'name': 'Test Group'}).json()
        self.assertEqual(response['status'], 'ok')
        response = self.client.get(reverse('get_group', args=[1])).json()
        self.assertDictEqual(response['group'], {
            'id': 1,
            'name': 'Test Group',
            'size': 2,
            'description': 'Come and learn!',
        })

    def test_delete(self):
        grp = Group(name='Test Group', size=0)
        grp.save()

        response = self.client.get(reverse('group_index')).json()
        self.assertNotEqual(response['groups'], [])

        response = self.client.post(reverse('delete_group', args=[1])).json()
        self.assertEqual(response['status'], 'ok')

        response = self.client.get(reverse('group_index')).json()
        self.assertEqual(response['groups'], [])


    def tearDown(self):
        pass
