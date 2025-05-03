import unittest
from models.rectangle import Rectangle

class TestRectangleRotate(unittest.TestCase):

    def test_rotate_new_rectangle(self):
        r1 = Rectangle(width=1, length=2)
        r2 = r1.rotate()

        self.assertIsInstance(r2, Rectangle)
        self.assertEqual(r1.width, r2.length)
        self.assertEqual(r1.length, r2.width)
        self.assertEqual(r1.nb_rotation, r2.nb_rotation)

    def test_rotation_back_to_original(self):
        # For this test, we will espacially take a rectangle and not a square to show that, at some point, there's a difference between the two objects.
        r1 = Rectangle(width=1, length=2, nb_rotation=3)
        r2 = r1.rotate()

        self.assertNotEqual(r1.width, r2.width)
        self.assertNotEqual(r1.length, r2.length)
        
        r3 = r2.rotate()

        self.assertEqual(r1.width, r3.width)
        self.assertEqual(r1.length, r3.length)
        


    