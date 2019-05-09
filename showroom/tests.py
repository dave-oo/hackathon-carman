import datetime
import json
from django.test import TestCase
from .models import Car
from .serializers import CarSerializer


class CarTest(TestCase):
    """
    Test module for the car model
    """
    def test_sanity(self):
        """
        Sanity check for the car model
        """
        Car.objects.create(
            car_make='Test Make',
            color='blue',
            reg_number='Test Reg',
            yom=1990,
            car_type='hatchback',
            available=True,
            date_created=datetime.date.today(),
            viewable=True
        )
        self.assertEqual(Car.objects.count(), 1)

    def test_car_list_route(self):
        """
        Test that the car list route is responding
        """
        Car.objects.create(
            car_make='Test Make',
            color='blue',
            reg_number='Test Reg',
            yom=1990,
            car_type='hatchback',
            available=True,
            date_created=datetime.date.today(),
            viewable=True
        )
        response = self.client.get('/api/cars')
        cars = Car.objects.all()
        serializer = CarSerializer(cars, many=True)
        self.assertEqual(response.data, serializer.data)

    def test_car_detail_route(self):
        """
        Test that the car detail route is responding
        """
        Car.objects.create(
            car_make='Test Make',
            color='blue',
            reg_number='Test Reg',
            yom=1990,
            car_type='hatchback',
            available=True,
            date_created=datetime.date.today(),
            viewable=True
        )
        response = self.client.get('/api/cars/1')
        car = Car.objects.get(pk=1)
        serializer = CarSerializer(car)
        self.assertEqual(response.data, serializer.data)

    def test_partial_update(self):
        """
        Test that updates only update the color and availability
        :return:
        """
        Car.objects.create(
            car_make='Test Make',
            color='blue',
            reg_number='Test Reg',
            yom=1990,
            car_type='hatchback',
            available=True,
            date_created=datetime.date.today(),
            viewable=True
        )

        data = json.dumps({
            'car_make': 'Other make',
            'available': '0',
            'color': 'red'
        })

        self.client.patch('/api/cars/1', data, content_type='application/json')

        car = Car.objects.get(pk=1)

        self.assertNotEquals(car.car_make, 'Other make')
        self.assertEqual(car.car_make, 'Test Make')
        self.assertEqual(car.available, False)
        self.assertEqual(car.color, 'red')

    def test_wrong_color(self):
        """
        Test that api request to the car route with wrong color are
        flagged as invalid
        """
        data = json.dumps({
            'car_make': 'Other make',
            'available': True,
            'viewable': True,
            'car_type': 'hatchback',
            'date_created': str(datetime.date.today()),
            'color': 'undefined color', # <========
            'reg_number': 'KAX 112M',
            'yom': 1990
        })

        response = self.client.post('/api/cars', data, content_type='application/json')
        self.assertEqual(response.status_code, 400)

