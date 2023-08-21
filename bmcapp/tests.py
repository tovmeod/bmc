import csv
import itertools

from django.test import TestCase
from rest_framework.test import APIClient

from .models import Passenger


class PlayerAPITest(TestCase):
    def setUp(self):
        # user = User.objects.create_user('test_user', 'test@example.com', 'password')
        # self.client.force_login(user)
        self.client = APIClient()
        self.passenger_data = {
            'Age': '22.00', 'Cabin': None, 'Embarked': 'S', 'Fare': '7.2500', 'Name': 'Braund, Mr. Owen Harris',
            'Parch': 0, 'PassengerId': 1, 'Pclass': 3, 'Sex': 'male', 'SibSp': 1, 'Survived': False,
            'Ticket': 'A/5 21171'
        }

    def test_valid_csv_data(self):
        """Ensure the initial provided data can be validated."""
        with open('titanic.csv', 'r') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=',')
            for row in reader:
                response = self.client.post('/api/passenger/', row, format='json')
                self.assertEqual(response.status_code, 201, f'row: {row}\nError: {response.data}')

        players_len = 891
        self.assertEqual(Passenger.objects.count(), players_len)
        response = self.client.get('/api/passenger/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), players_len)

    def test_create_passenger(self):
        response = self.client.post('/api/passenger/', self.passenger_data, format='json')

        self.assertEqual(response.status_code, 201, response.data)
        self.assertEqual(Passenger.objects.count(), 1)
        response = self.client.get(f'/api/passenger/{self.passenger_data["PassengerId"]}/')
        self.assertEqual(response.status_code, 200)
        assert response.data == self.passenger_data

    def test_get_passenger(self):
        """Given a passenger id return all data in json"""
        passenger = Passenger.objects.create(**self.passenger_data)

        response = self.client.get(f'/api/passenger/{passenger.PassengerId}/')
        self.assertEqual(response.status_code, 200)

        # Assert that the response is a valid json response
        response_data = response.json()
        assert response_data == self.passenger_data

    def test_get_passenger_attr_filter(self):
        """Given a passenger id and fields return only selected fields in json"""

        passenger = Passenger.objects.create(**self.passenger_data)

        def gen_field_names(fields):
            # Generate all possible combinations of field names of different lengths
            for r in range(1, len(fields)):
                yield from itertools.combinations(fields, r)

        for field_names in gen_field_names(self.passenger_data.keys()):
            query_param = '&'.join([f'fields={field}' for field in field_names])
            response = self.client.get(f'/api/passenger/{passenger.PassengerId}/?{query_param}')
            self.assertEqual(response.status_code, 200)

            # Assert that the response is a valid json response
            response_data = response.json()
            assert set(response_data.keys()) == set(field_names)

    def test_get_passenger_attr_filter_invalid(self):
        """What happens if one asks for an invalid field name?"""
        passenger = Passenger.objects.create(**self.passenger_data)

        field_names = ('alo', )
        query_param = '&'.join([f'fields={field}' for field in field_names])
        response = self.client.get(f'/api/passenger/{passenger.PassengerId}/?{query_param}')
        assert response.status_code == 400

    def test_get_passenger_attr_filter_internal(self):
        """What happens if one asks for an internal protected field name?"""
        passenger = Passenger.objects.create(**self.passenger_data)

        field_names = ('id', )
        query_param = '&'.join([f'fields={field}' for field in field_names])
        response = self.client.get(f'/api/passenger/{passenger.PassengerId}/?{query_param}')
        assert response.status_code == 200

    def test_patch_passenger(self):
        passenger = Passenger.objects.create(**self.passenger_data)

        response = self.client.patch(f'/api/passenger/{passenger.PassengerId}/', {'Age': 30}, format='json')

        assert response.status_code == 200

        # Refresh the player instance from the database
        passenger.refresh_from_db()
        assert passenger.Age == 30

    def test_delete_player(self):
        passenger = Passenger.objects.create(**self.passenger_data)

        response = self.client.delete(f'/api/passenger/{passenger.PassengerId}/')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Passenger.objects.count(), 0)
