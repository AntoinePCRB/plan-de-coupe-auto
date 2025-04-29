import unittest
from models.rectangle import Rectangle

class TestRectangle(unittest.TestCase):

    def test_init_works(self):
        r = Rectangle(width=2, length=4)
        self.assertEqual(r.width, 2)
        self.assertEqual(r.length, 4)
        self.assertEqual(r.nb_rotation, 2)

    def test_init_works_with_optionals(self):
        r = Rectangle(width=2, length=4, nb_rotation=4)
        self.assertEqual(r.width, 2)
        self.assertEqual(r.length, 4)
        self.assertEqual(r.nb_rotation, 4)

    def test_init_with_width_type_false(self):
        with self.assertRaises(TypeError) as te:
            Rectangle(width="A", length=2)
        the_exception = te.exception
        self.assertEqual(the_exception.args[0], f"width must be a float or int, got {type("A").__name__}")
    
    def test_init_with_length_type_false(self):
        with self.assertRaises(TypeError) as te:
            Rectangle(width=2, length="A")
        the_exception = te.exception
        self.assertEqual(the_exception.args[0], f"length must be a float or int, got {type("A").__name__}")
    
    def test_init_with_nb_rotation_type_false(self):
        with self.assertRaises(TypeError) as te:
            Rectangle(width=2, length=2.0, nb_rotation=2.0)
        the_exception = te.exception
        self.assertEqual(the_exception.args[0], f"nb_rotation must be an int, got {type(2.0).__name__}")

    def test_init_with_width_inf_0(self):
        with self.assertRaises(ValueError) as te:
            Rectangle(width=-1, length=2)
        the_exception = te.exception
        self.assertEqual(the_exception.args[0], f"width must be greater than 0, got {-1}")

    def test_init_with_length_inf_0(self):
        with self.assertRaises(ValueError) as te:
            Rectangle(width=2, length= -1)
        the_exception = te.exception
        self.assertEqual(the_exception.args[0], f"length must be greater than 0, got {-1}")

    def test_init_with_nb_rotation_inf_0(self):
        with self.assertRaises(ValueError) as te:
            Rectangle(width=2, length= 2, nb_rotation=-1)
        the_exception = te.exception
        self.assertEqual(the_exception.args[0], f"nb_rotation must be greater than 0, got {-1}")

if __name__ == "__main__":
    import unittest
    unittest.main()
