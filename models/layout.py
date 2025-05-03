from typing import List, Dict

class Layout:
    """
    Represent the layout in our optimization problem.
    It will also define the rules.

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
        if not isinstance(max_width, int):
            raise TypeError(f"max_width must be an int, got {type(max_width).__name__}")
        if max_width <= 0:
            raise ValueError(f"max_width must be greater than 0, got {max_width}")
        
        # Tests on max_length
        if not isinstance(max_length, int):
            raise TypeError(f"max_length must be an int, got {type(max_length).__name__}")
        if max_length <= 0:
            raise ValueError(f"max_length must be greater than 0, got {max_length}")
        
        # Tests on placement
        if not isinstance(placement, list):
            raise TypeError(f"placement must be a list, got {type(placement).__name__}")
        if placement != []:
            for rect_placed in placement :
                if not set(rect_placed.keys()).issubset({'id', 'x', 'y', 'width', 'length'}):
                    missing_keys = ['id', 'x', 'y', 'width', 'length'] - rect_placed.keys()
                    raise KeyError(f"Missing keys in {rect_placed} : {missing_keys}")
                
                if not isinstance(rect_placed['id'], str):
                    raise TypeError(f"id must be a str, got {type(rect_placed['id']).__name__}")
                
                if not isinstance(rect_placed['x'], int):
                    raise TypeError(f"x must be an int, got {type(rect_placed['x']).__name__}")
                if rect_placed['x'] < 0:
                    raise ValueError(f"x must be equal or greater than 0, got {rect_placed['x']} in {rect_placed}")
                
                if not isinstance(rect_placed['y'], int):
                    raise TypeError(f"y must be an int, got {type(rect_placed['y']).__name__}")
                if rect_placed['y'] < 0:
                    raise ValueError(f"y must be equal or greater than 0, got {rect_placed['y']} in {rect_placed}")
                
                if not isinstance(rect_placed['width'], int):
                    raise TypeError(f"width must be an int, got {type(rect_placed['width']).__name__}")
                if rect_placed['width'] <= 0:
                    raise ValueError(f"width must be greater than 0, got {rect_placed['width']} in {rect_placed}")

                
                if not isinstance(rect_placed['length'], int):
                    raise TypeError(f"length must be an int, got {type(rect_placed['length']).__name__}")
                if rect_placed['length'] <= 0:
                    raise ValueError(f"length must be greater than 0, got {rect_placed['length']} in {rect_placed}")
        
        self.max_width = max_width
        self.max_length = max_length
        self.placement = placement

    def remove_last_rectangle(self):
        if self.placement:
            self.placement.pop()
