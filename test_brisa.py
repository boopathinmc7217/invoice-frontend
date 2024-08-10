import unittest
from brisa import Vehicle,Car,Truck

# class TestVehicle(unittest.TestCase):

#     # def Setup(self):
#     #     pass

#     def test_truck_speed(self):
#         tobj=Truck(1998,"dunder+","d",12.5)
#         self.assertEqual(12.5/1998,tobj.speed())

class TestCar(unittest.TestCase):

    def setUp(self) -> None:
        self.car_obj = Car(1998,"duner+","d",12.5)
    
    def test_car_speed(self):
        self.assertEqual(12.5*1998*2,self.car_obj.speed())

    def tearDown(self) -> None:
        return super().tearDown()