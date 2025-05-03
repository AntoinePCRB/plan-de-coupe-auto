import unittest
from models.layout import Layout

class TestLayoutInit(unittest.TestCase):
    
    def test_init_works_without_list(self): #1090
        L1 = Layout(max_width=150, max_length=200)

        self.assertEqual(L1.max_width, 150)
        self.assertEqual(type(L1.max_width), int)
        self.assertEqual(L1.max_length, 200)
        self.assertEqual(type(L1.max_length), int)
        self.assertEqual(L1.placement, [])

    
    def test_init_works_with_list(self): #1091

        lst_placement = [
            {"id": "Object1", "x": 1, "y": 2, "width": 10, "length": 5},
            {"id": "Object2", "x": 3, "y": 4, "width": 4, "length": 6}
            ]

        L1 = Layout(max_width=150, max_length=200, placement=lst_placement)

        self.assertEqual(L1.max_width, 150)
        self.assertEqual(type(L1.max_width), int)
        self.assertEqual(L1.max_length, 200)
        self.assertEqual(type(L1.max_length), int)
        self.assertEqual(L1.placement, lst_placement)

    def test_init_max_width_wrong_type(self): #1010
        with self.assertRaises(TypeError) as te:
            Layout(max_width=1.0, max_length=2)
        the_exception = te.exception
        self.assertEqual(the_exception.args[0], f"max_width must be an int, got {type(1.0).__name__}")

    def test_init_max_width_inf_or_0(self): #1011
        with self.assertRaises(ValueError) as te:
            Layout(max_width=0, max_length=2)
        the_exception = te.exception
        self.assertEqual(the_exception.args[0], f"max_width must be greater than 0, got {0}")
        with self.assertRaises(ValueError) as te:
            Layout(max_width=-5, max_length=2)
        the_exception = te.exception
        self.assertEqual(the_exception.args[0], f"max_width must be greater than 0, got {-5}")

    def test_init_max_length_wrong_type(self): #1020
        with self.assertRaises(TypeError) as te:
            Layout(max_width=1, max_length=2.0)
        the_exception = te.exception
        self.assertEqual(the_exception.args[0], f"max_length must be an int, got {type(2.0).__name__}")

    def test_init_max_length_inf_or_0(self): #1021
        with self.assertRaises(ValueError) as te:
            Layout(max_width=5, max_length=0)
        the_exception = te.exception
        self.assertEqual(the_exception.args[0], f"max_length must be greater than 0, got {0}")
        with self.assertRaises(ValueError) as te:
            Layout(max_width=5, max_length=-2)
        the_exception = te.exception
        self.assertEqual(the_exception.args[0], f"max_length must be greater than 0, got {-2}")
    
    def test_init_placement_wrong_type(self): #1030
        with self.assertRaises(TypeError) as te:
            Layout(max_width=1, max_length=2, placement="str")
        the_exception = te.exception
        self.assertEqual(the_exception.args[0], f"placement must be a list, got {type("str").__name__}")

    def test_init_placement_wrong_keys(self): #1031
        test_placement = [{"id": "Object1", "x": 1, "y": 2, "width": 10, "length": 5},
                          {"wrong_id": "Object2", "x": 3, "y": 4, "width": 4, "length": 6}]
        with self.assertRaises(KeyError) as te:
            Layout(max_width=1, max_length=2, placement=test_placement)
        the_exception = te.exception
        self.assertEqual(the_exception.args[0], f"Missing keys in {test_placement[1]} : {"{'id'}"}")

    def test_init_placement_wrong_type_in_list_id(self): #1040
        test_placement = [{"id": "Object1", "x": 1, "y": 2, "width": 10, "length": 5},
                          {"id": 2, "x": 3, "y": 4, "width": 4, "length": 6}]
        with self.assertRaises(TypeError) as te:
            Layout(max_width=1, max_length=2, placement=test_placement)
        the_exception = te.exception
        self.assertEqual(the_exception.args[0], f"id must be a str, got {type(test_placement[1]['id']).__name__}")

    def test_init_placement_wrong_type_in_list_x(self): #1050
        test_placement = [{"id": "Object1", "x": 1, "y": 2, "width": 10, "length": 5},
                          {"id": "Object2", "x": "3", "y": 4, "width": 4, "length": 6}]
        with self.assertRaises(TypeError) as te:
            Layout(max_width=1, max_length=2, placement=test_placement)
        the_exception = te.exception
        self.assertEqual(the_exception.args[0], f"x must be an int, got {type(test_placement[1]['x']).__name__}")

    def test_init_placement_list_x_inf_0(self): #1051
        test_placement = [{"id": "Object1", "x": 1, "y": 2, "width": 10, "length": 5},
                          {"id": "Object2", "x": -3, "y": 4, "width": 4, "length": 6}]
        with self.assertRaises(ValueError) as te:
            Layout(max_width=1, max_length=2, placement=test_placement)
        the_exception = te.exception
        self.assertEqual(the_exception.args[0], f"x must be equal or greater than 0, got {test_placement[1]['x']} in {test_placement[1]}")

    def test_init_placement_wrong_type_in_list_y(self): #1060
        test_placement = [{"id": "Object1", "x": 1, "y": 2, "width": 10, "length": 5},
                          {"id": "Object2", "x": 3, "y": 4.0, "width": 4, "length": 6}]
        with self.assertRaises(TypeError) as te:
            Layout(max_width=1, max_length=2, placement=test_placement)
        the_exception = te.exception
        self.assertEqual(the_exception.args[0], f"y must be an int, got {type(test_placement[1]['y']).__name__}")

    def test_init_placement_list_y_inf_0(self): #1061
        test_placement = [{"id": "Object1", "x": 1, "y": 2, "width": 10, "length": 5},
                          {"id": "Object2", "x": 3, "y": -4, "width": 4, "length": 6}]
        with self.assertRaises(ValueError) as te:
            Layout(max_width=1, max_length=2, placement=test_placement)
        the_exception = te.exception
        self.assertEqual(the_exception.args[0], f"y must be equal or greater than 0, got {test_placement[1]['y']} in {test_placement[1]}")

    def test_init_placement_wrong_type_in_list_width(self): #1070
        test_placement = [{"id": "Object1", "x": 1, "y": 2, "width": 10, "length": 5},
                          {"id": "Object2", "x": 3, "y": 4, "width": "4", "length": 6}]
        with self.assertRaises(TypeError) as te:
            Layout(max_width=1, max_length=2, placement=test_placement)
        the_exception = te.exception
        self.assertEqual(the_exception.args[0], f"width must be an int, got {type(test_placement[1]['width']).__name__}")

    def test_init_placement_list_width_inf_0(self): #1071
        test_placement = [{"id": "Object1", "x": 1, "y": 2, "width": 10, "length": 5},
                          {"id": "Object2", "x": 3, "y": 4, "width": -4, "length": 6}]
        with self.assertRaises(ValueError) as te:
            Layout(max_width=1, max_length=2, placement=test_placement)
        the_exception = te.exception
        self.assertEqual(the_exception.args[0], f"width must be greater than 0, got {test_placement[1]['width']} in {test_placement[1]}")

    def test_init_placement_wrong_type_in_list_length(self): #1080
        test_placement = [{"id": "Object1", "x": 1, "y": 2, "width": 10, "length": 5},
                          {"id": "Object2", "x": 3, "y": 4, "width": 4, "length": [6]}]
        with self.assertRaises(TypeError) as te:
            Layout(max_width=1, max_length=2, placement=test_placement)
        the_exception = te.exception
        self.assertEqual(the_exception.args[0], f"length must be an int, got {type(test_placement[1]['length']).__name__}")

    def test_init_placement_list_length_inf_0(self): #1081
        test_placement = [{"id": "Object1", "x": 1, "y": 2, "width": 10, "length": 5},
                          {"id": "Object2", "x": 3, "y": 4, "width": 4, "length": -60}]
        with self.assertRaises(ValueError) as te:
            Layout(max_width=1, max_length=2, placement=test_placement)
        the_exception = te.exception
        self.assertEqual(the_exception.args[0], f"length must be greater than 0, got {test_placement[1]['length']} in {test_placement[1]}")

    