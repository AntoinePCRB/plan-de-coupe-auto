class Rectangle:
    """
    Represent a Rectanlge in our optimization problem.

    Parameters
    ----------
    width : float
        Rectangle's width.
    length : float
        Rectangle's length.
    nb_rotation : int, optional
        Number of rotations (default: 2).
    """
    
    def __init__(self, width: float, length: float, nb_rotation=2):
        """
        Initializes a rectangle with given dimensions and rotation count.

        Parameters
        ----------
        width : float
            The width of the rectangle.
        length : float
            The length of the rectangle.
        nb_rotation : int, optional
            The number of allowed rotations for the rectangle (default is 2).

        Sets the rectangle's dimensions and the number of rotations allowed.
        """

        # Tests on width
        if not isinstance(width, (int,float)):
            raise TypeError(f"width must be a float or int, got {type(width).__name__}")
        if width <= 0:
            raise ValueError(f"width must be greater than 0, got {width}")
        
        # Tests on length
        if not isinstance(length, (int,float)):
            raise TypeError(f"length must be a float or int, got {type(length).__name__}")
        if length <= 0:
            raise ValueError(f"length must be greater than 0, got {length}")
        
        # Tests on nb_rotation
        if not isinstance(nb_rotation, int):
            raise TypeError(f"nb_rotation must be an int, got {type(nb_rotation).__name__}")
        if nb_rotation <= 0:
            raise ValueError(f"nb_rotation must be greater than 0, got {nb_rotation}")
        
        self.width = width
        self.length = length
        self.nb_rotation = nb_rotation

    def rotate(self):
        """
        Returns a new rectangle rotated by 90 degrees.

        Returns
        -------
        models.Rectangle
            A new rectangle with swapped width and length,
            and the rotation count preserved.
        """
        return Rectangle(self.length, self.width, self.nb_rotation)
    