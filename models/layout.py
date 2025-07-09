from typing import List, Dict
import numpy as np

class Layout:
    """
    Represent the layout in our optimization problem.
    It willlso define the rules.

    Parameters
    ----------
    max_width : int
        Layout's max width.
    max_length : int
        Rectangle's length.
    placement : list, optional
        list of rectangle placed in our plan.
        [{'id': str, 'x': int, 'y': int, 'width': int, 'length' : int}, ...]
    """


    def __init__(self, max_width: int, max_length: int, placement: List[Dict] = None):
        
        if placement is None:
            placement = []

        # Tests on max_width
        self.validate_typing(max_width, "max_width", int)
        self.validate_positive(max_width, "max_width", False)
        
        # Tests on max_length
        self.validate_typing(max_length, "max_length", int)
        self.validate_positive(max_length, "max_length", False)
        
        # Tests on placement
        self.validate_typing(placement, "placement", list)
        if placement != []:
            for rect_placed in placement :
                if not set(rect_placed.keys()).issubset({'id', 'x', 'y', 'width', 'length'}):
                    missing_keys = ['id', 'x', 'y', 'width', 'length'] - rect_placed.keys()
                    raise KeyError(f"Missing keys in {rect_placed.keys()} : {missing_keys}")
                
                self.validate_typing(rect_placed['id'], "id", str)
                self.validate_typing(rect_placed['x'], "x", int)
                self.validate_positive(rect_placed['x'], "x", False)
                self.validate_typing(rect_placed['y'], "y", int)
                self.validate_positive(rect_placed['y'], "y", False)
                self.validate_typing(rect_placed['width'], "width", int)
                self.validate_positive(rect_placed['width'], "width", True)
                self.validate_typing(rect_placed['length'], "length", int)
                self.validate_positive(rect_placed['length'], "length", True)

        # create a 2d plan with zeroes :
        self.tab_layout = np.zeros((max_width, max_length))
        self.allowed_placement = [(0, 0)]

        self.max_width = max_width
        self.max_length = max_length
        self.placement = placement
        

    def validate_positive(self, variable, variable_name, allow_zero: bool):
        if allow_zero:
            if variable < 0:
                raise ValueError(f"{variable_name} must be equal or greater than 0, got {variable}")
        else :
            if variable <= 0:
                raise ValueError(f"{variable_name} must be greater than 0, got {variable}")
    


    def validate_typing(self, variable, variable_name: str, variable_type: type):
        if not isinstance(variable, variable_type):
            raise TypeError(f"{variable_name} must be {variable_type.__name__}, got {type(variable).__name__}")

    def remove_last_rectangle(self):
        if self.placement:
            self.placement.pop()

    def remove_rectangle(self, x, y, targeted_placement):
        for i in range(y):
            for j in range(x):
                self.tab_layout[targeted_placement[1]+i, targeted_placement[0]+j] -= 1

    def place_rectangle(self, x, y, targeted_placement):
        for i in range(y):
            for j in range(x):
                self.tab_layout[targeted_placement[1]+i, targeted_placement[0]+j] += 1
                if self.tab_layout[targeted_placement[1]+i, targeted_placement[0]+j] != 1:
                    if i == 0:
                        self.remove_rectangle(x=j+1, y=1, targeted_placement=targeted_placement)
                    else :
                        self.remove_rectangle(x, i+1, targeted_placement)
                    return(False)
        self.allowed_placement.remove(targeted_placement)
        self.allowed_placement.append((x+targeted_placement[0], targeted_placement[1]))
        self.allowed_placement.append((targeted_placement[0], y + targeted_placement[1]))
        return(True)
