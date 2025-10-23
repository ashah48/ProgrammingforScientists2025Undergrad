# five fields for rectangle:
# width, height, x1, y1 (center or top left), rotation

# place class declarations between imports and def main

class Rectangle:
    """
    Represents a 2D rectangle with width, height, position, and rotation

    Attributes:
        width: (float)
        height: (float)
        x1: the x-coordinate of the rectangle's origin (float)
        y1: the y-coordinate of the rectangle's origin (float)
        rotation: rotation of shape in degrees (float)
<<<<<<< HEAD

    Class Attributes:
        description: describes some characteristic of the object (string)
=======
    
    Class Attributes:
        description: describes some characteristic of the object (string) 
>>>>>>> 97ac29c
    """

    description: str = "boxy"

    # Every class declaration should have a constructor to set fields
    # Also, Python calls fields "attributes"
    # We will allow the user to set attributes of an instance the second it is born
    def __init__(self, width: float=0.0, height: float=0.0, x1: float=0, y1: float=0, rotation: float=0):
<<<<<<< HEAD
        # let's protect the program from a bad user
        if width < 0.0 or height < 0.0:
            raise ValueError("width and height must be nonnegative.")
        # we could add tests for if variables are all floats, etc.

=======
        # let's protect the program from a bad user 
        if width < 0.0 or height < 0.0:
            raise ValueError("width and height must be nonnegative.")
        # we could add tests for if variables are all floats, etc.
        
>>>>>>> 97ac29c
        # what attributes should every Rectangle get?
        self.width = width
        self.height = height
        self.x1 = x1
        self.y1 = y1
        self.rotation = rotation

    def __repr__(self) -> str:
<<<<<<< HEAD
        # let's have a nice f string to print the attributes
        return f"Rectangle(width={self.width},height={self.height},x1={self.x1}, y1={self.y1}, rotation={self.rotation})"

    def area(self) -> float:
        """
        Method to return the area of the rectangle
        """
        return self.width * self.height

    def translate(self, a: float, b: float):
        """Method to translate a shape a units in the x direction and b units in
        the y direction"""
        self.x1 += a
        self.y1 += b

    def scale(self, f: float):
        """Dilate the shape by a factor of f"""
        self.width *= f
        self.height *= f


class Circle:
    """
    Represents a 2D circle via its center and radius.

=======
        # let's have a nice f string to print the attributes 
        return f"Rectangle(width={self.width},height={self.height},x1={self.x1}, y1={self.y1}, rotation={self.rotation})"

class Circle:
    """
    Represents a 2D circle via its center and radius.
    
>>>>>>> 97ac29c
    Attributes:
        x1: the x-coordinate of the center (float)
        y1: the y-coordinate of the center (float)
        radius: the center's radius (float)

    Class Attributes:
<<<<<<< HEAD
        description: describes some characteristic of the object (string)
=======
        description: describes some characteristic of the object (string) 
>>>>>>> 97ac29c
    """

    description: str = "round"

    def __init__(self, x1: float=0, y1: float = 0, radius: float = 0):
        if radius < 0.0:
            raise ValueError("width and height must be nonnegative.")
        self.x1 = x1
        self.y1 = y1
        self.radius = radius

    def __repr__(self) -> str:
<<<<<<< HEAD
        # let's have a nice f string to print the attributes
        return f"Circle(x1={self.x1}, y1={self.y1}, radius={self.radius})"

    def area(self) -> float:
        """
        Method to return the area of the circle
        """
        return 3.0 * (self.radius ** 2)

    def translate(self, a: float, b: float):
        """Method to translate a shape a units in the x direction and b units in
        the y direction"""
        self.x1 += a
        self.y1 += b

    def scale(self, f: float):
        """Dilate the shape by a factor of f"""
        self.radius *= f

def main():
    print("Shapes part 2.")

    #Some shapes
    r = Rectangle(width = 3.0, height = 4.0)
    c = Circle(x1 = 0.0, y1=0.0, radius = 2.0)
    print(r)
    print(c)

    #Now let's print the areas of the rectangles
    print("Rectangle area:", r.area())
    print("Circle area:", c.area())

    #We have our shapes so let's translate them
    r.translate(10.0, -5.0)
    c.translate(2.5, 3.5)

    #Scale both shapes
    r.scale(2.0)
    c.scale(0.4)
    print("After scaling:")
    print(r)
    print(c)

    #Note: areas scale by a factor of f^2
    print("New rectangle area:", r.area())
    print("New circle area:", c.area())

    #As we might hope the shapes move, because we passed r and c as inputs to translate
    #and in Python, user-defined classes are pass by reference.

    #When you make a variable, Python gives it a numeric ID
    # We access it with the id() function
    n = 5
    print("Outside function before change:", n, id(n))

    #When you pass any type into a function, you are passing the literal type in by (object) reference.
    # For example when you pass an integer into a function, you are passing the literal integer in by its (object) reference

    #We get a new integer aka we get a new integer with a new id(n) than n has, when we do this:
    n += 10
    #Integers are immutable! Makes Python slower.

    #id() is useful because if we have two objects we can check if they are actually the same literal object
    r1 = Rectangle(width = 3.0, height = 4.0, x1 = 0.0, y1 = 0.0)
    print("Original r1:", r1)

    #new question: what happens if .....
    r2 = r1

    #Did we copy over the attributes?
    print("r2 is:", r2)
    #No. What we did say is that r2 has the same object reference as r1.
    r2.translate(10, 5)
    print("After translating...")
    #Should get the same thing for r1, r2
    print("r1 is:", r1)
    print("r2 is:", r2)


=======
        # let's have a nice f string to print the attributes 
        return f"Circle(x1={self.x1}, y1={self.y1}, radius={self.radius})"


def main():
    print("Shapes.")
>>>>>>> 97ac29c

    # these declarations create an INSTANCE of the object with the default attributes
    x1 = 1.0
    y1 = 3.0
    radius = 2.0
    my_circle = Circle(x1, y1, radius)  # x1 = 1.0, y1 = 3.0, radius = 2.0
<<<<<<< HEAD

=======
    
>>>>>>> 97ac29c
    r = Rectangle(3.0, 5.0)  # some languages might get mad, Python never gets mad
    # other attributes of r get their defaults (0.0)


    """
<<<<<<< HEAD
    # the baby is born and we can update its attributes
    my_circle.x1 = 1.0
=======
    # the baby is born and we can update its attributes 
    my_circle.x1 = 1.0 
>>>>>>> 97ac29c
    my_circle.y1 = 3.0
    my_circle.radius = 2.0

    r.width = 3.0
    r.height = 5.0

    r.name = "Larry"  # you can do this but don't do this
    """

<<<<<<< HEAD
    # let's print the whole thing
    print("our rectangle is", r)
    print("our circle is", my_circle)

    # just because we initialized attributes doesn't mean we can't change them
    r.width = 2.0
=======
    # let's print the whole thing 
    print("our rectangle is", r)
    print("our circle is", my_circle)

    # just because we initialized attributes doesn't mean we can't change them 
    r.width = 2.0 
>>>>>>> 97ac29c
    r.height = 4.5
    r.x1 = -1.45
    r.y1 = 2.3

    print("The rectangle has been updated to", r)

    # lesson: you can't name functions the same thing in Python (except when you can, hold on for next week)

    print("Rectangle's area is", area_rectangle(r))
    print("Circle's area is", area_circle(my_circle))

    # are instances of a new class pass by reference or value?
    translate_circle(my_circle, 10.0, 10.0)
    translate_rectangle(r, 30.0, -100.0)

    print("The circle has been translated to", my_circle)
    print("The rectangle has been translated to", r)

    # instances of a new class are pass by REFERENCE
<<<<<<< HEAD
    # 1. you don't have to return the object
=======
    # 1. you don't have to return the object 
>>>>>>> 97ac29c
    # 2. be CAREFUL about changing attributes of an object in a function

    # what we really want is just translate() functions that don't take objects as input

<<<<<<< HEAD
    # we can access class attributes in two ways
    # 1. access it through an instance
    print("Our rectangle is", r.description)

    #2. access it via the name of the class
=======
    # we can access class attributes in two ways 
    # 1. access it through an instance
    print("Our rectangle is", r.description)

    #2. access it via the name of the class 
>>>>>>> 97ac29c
    print("Every circle is", Circle.description)

    my_circle.description = "orb-like"
    print("My circle is", my_circle.description)
    # this creates a new (local) attribute of my_circle and doesn't affect any other circle or the class attribute
    # do not ever use this

    # did I overwrite every circle's description?
    print("Every circle is", Circle.description)





def area_rectangle(r: Rectangle) -> float:
    """
    Compute the area of a given rectangle.
    """
    return r.width * r.height

def area_circle(c: Circle) -> float:
    """
    Compute the area of a circle.
    """
    return 3.0 * (c.radius ** 2)

# write perimeter_rectangle() and perimeter_circle() functions

def translate_rectangle(r: Rectangle, a: float, b:float) -> None:
    """
    Move a rectangle by a given amount in x- and y-directions.
    """
<<<<<<< HEAD
    r.x1 += a
    r.y1 += b
=======
    r.x1 += a 
    r.y1 += b 
>>>>>>> 97ac29c

def translate_circle(c: Circle, a: float, b:float) -> None:
    """
    Move a circle by a given amount in x- and y-directions.
    """
    c.x1 += a
    c.y1 += b

if __name__ == "__main__":
<<<<<<< HEAD
    main()
=======
    main()
>>>>>>> 97ac29c
