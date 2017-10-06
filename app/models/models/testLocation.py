from django.test import TransactionTestCase
from django.core.urlresolvers import reverse
from operator import itemgetter
from .models import Location


class GetUserIndexTestCase(TransactionTestCase):
    def setUp(self):
        pass

    def test_success_empty(self):
        response = self.client.get(reverse('location_index')).json()

        self.assertEquals(response['status'], 'ok')
        self.assertEquals(response['locations'], [])

    def test_success_one(self):
        loc = Location(building_name='Test Building', college_name='UVA',
                       building_address='100')
        loc.save()

        response = self.client.get(reverse('location_index')).json()

        self.assertEquals(response['status'], 'ok')
        self.assertEquals(response['locations'], [{
            'id': 1,
            'building_name': 'Test Building',
            'college_name': 'UVA',
            'building_address': '100',
        }, ])

    def test_success_many(self):
        loc = Location(building_name='Test Building', college_name='UVA',
                       building_address='100')
        loc.save()
        loc = Location(building_name='Test Building 2', college_name='UVA',
                       building_address='200')
        loc.save()
        response = self.client.get(reverse('location_index')).json()

        self.assertEquals(response['status'], 'ok')
        self.assertEquals(sorted(response['locations'], key=itemgetter('id')), [{
            'id': 1,
            'building_name': 'Test Building',
            'college_name': 'UVA',
            'building_address': '100',
        }, {
            'id': 2,
            'building_name': 'Test Building 2',
            'college_name': 'UVA',
            'building_address': '200',
        }])

    def tearDown(self):
        pass

class CRUDUserTestCase(TransactionTestCase):

    def setUp(self):
        pass

    def test_create_get(self):
        response = self.client.post(reverse('create_location'),
                                    {'building_name': 'Test Building',
                                     'college_name': 'UVA',
                                     'building_address': '100'}).json()
        self.assertEqual(response['status'], 'ok')

        response = self.client.get(reverse('get_location', args=[1])).json()
        self.assertEqual(response['status'], 'ok')
        self.assertDictEqual(response['location'], {
            'id': 1,
            'building_name': 'Test Building',
            'college_name': 'UVA',
            'building_address': '100'
        })

    def test_crud_failure(self):

        # Test failures for create_group
        response = self.client.post(reverse('create_location'),
                                    {'building_name': 'Temp',
                                     'college_name': 'Temp'}).json()
        self.assertEqual(response['status'], 'bad request')
        response = self.client.post(reverse('create_location'),
                                    {'building_name': 'Temp',
                                     'building_address': 'Temp'}).json()
        self.assertEqual(response['status'], 'bad request')
        response = self.client.post(reverse('create_location'),
                                    {'building_address': 'Temp',
                                     'college_name': 'Temp'}).json()
        self.assertEqual(response['status'], 'bad request')
        response = self.client.post(reverse('create_location'),
                                    {'building_name': 'Temp'}).json()
        self.assertEqual(response['status'], 'bad request')
        response = self.client.post(reverse('create_location'),
                                    {'college_name': 'Temp'}).json()
        self.assertEqual(response['status'], 'bad request')
        response = self.client.post(reverse('create_location'),
                                    {'building_address': 'Temp'}).json()
        self.assertEqual(response['status'], 'bad request')
        response = self.client.post(reverse('create_location'), {}).json()
        self.assertEqual(response['status'], 'bad request')

        # Test failures for get_location
        response = self.client.get(reverse('get_location', args=[9999]))
        self.assertEqual(response.status_code, 404)

        # Test failures for delete_location
        response = self.client.post(reverse('delete_location', args=[9999]))
        self.assertEqual(response.status_code, 404)

        # Test failures for update_location
        response = self.client.post(reverse('update_location', args=[9999]))
        self.assertEqual(response.status_code, 404)
        loc = Location(building_name='Test Building', building_address='100',
                       college_name='UVA')
        loc.save()
        response = self.client.post(reverse('update_location', args=[1]),
                                    {}).json()
        self.assertEqual(response['status'], 'bad request')

    def test_update(self):
        loc = Location(building_name='Test Building', building_address='100',
                       college_name='UVA')
        loc.save()

        response = self.client.post(reverse('update_location', args=[1]),
                                    {'building_name': 'Updated Building'}).json()
        self.assertEqual(response['status'], 'ok')
        response = self.client.get(reverse('get_location', args=[1])).json()
        self.assertDictEqual(response['location'], {
            'id': 1,
            'building_name': 'Updated Building',
            'college_name': 'UVA',
            'building_address': '100'
        })

        response = self.client.post(reverse('update_location', args=[1]),
                                    {'college_name': 'UVa'}).json()
        self.assertEqual(response['status'], 'ok')
        response = self.client.get(reverse('get_location', args=[1])).json()
        self.assertDictEqual(response['location'], {
            'id': 1,
            'building_name': 'Updated Building',
            'college_name': 'UVa',
            'building_address': '100'
        })

        response = self.client.post(reverse('update_location', args=[1]),
                                    {'building_address': '200'}).json()
        self.assertEqual(response['status'], 'ok')
        response = self.client.get(reverse('get_location', args=[1])).json()
        self.assertDictEqual(response['location'], {
            'id': 1,
            'building_name': 'Updated Building',
            'college_name': 'UVa',
            'building_address': '200'
        })

        response = self.client.post(reverse('update_location', args=[1]),
                                    {'building_name': 'Test Building',
                                     'college_name': 'UVA',
                                     'building_address': '100'}).json()
        self.assertEqual(response['status'], 'ok')
        response = self.client.get(reverse('get_location', args=[1])).json()
        self.assertDictEqual(response['location'], {
            'id': 1,
            'building_name': 'Test Building',
            'college_name': 'UVA',
            'building_address': '100'
        })


    def test_delete(self):
        loc = Location(building_name='Test Building', building_address='100',
                       college_name='UVA')
        loc.save()

        response = self.client.get(reverse('location_index')).json()
        self.assertNotEqual(response['locations'], [])

        response = self.client.post(reverse('delete_location', args=[1])).json()
        self.assertEqual(response['status'], 'ok')

        response = self.client.get(reverse('location_index')).json()
        self.assertEqual(response['locations'], [])


    def tearDown(self):
        pass
