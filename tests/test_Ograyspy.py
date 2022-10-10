from unittest import TestCase
from src.Ograyspy import Ograyspy


class TestOgrayspy(TestCase):
    def setUp(self):
        self.ogra = Ograyspy()


class TestInit(TestOgrayspy):
    def test_initial_speed(self):
        self.assertEqual(self.ogra.speed, 0)

    def test_initial_odometer(self):
        self.assertEqual(self.ogra.odometer, 0)

    def test_initial_time(self):
        self.assertEqual(self.ogra.time, 0)


class TestAccelerate(TestOgrayspy):
    def test_accelerate_from_zero(self):
        self.ogra.accelerate()
        self.assertEqual(self.ogra.speed, 5)

    def test_multiple_accelerates(self):
        for _ in range(3):
            self.ogra.accelerate()
        self.assertEqual(self.ogra.speed, 15)


class TestBrake(TestOgrayspy):
    def test_brake_once(self):
        self.ogra.accelerate()
        self.ogra.brake()
        self.assertEqual(self.ogra.speed, 0)

    def test_multiple_brakes(self):
        for _ in range(5):
            self.ogra.accelerate()
        for _ in range(3):
            self.ogra.brake()
        self.assertEqual(self.ogra.speed, 10)
