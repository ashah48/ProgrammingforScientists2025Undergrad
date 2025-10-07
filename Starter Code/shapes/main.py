class Rectangle:
    """
    Represents a 2D rectangle with width, height, position, and rotation

    Attributes:
        width: (float)
        height: (float)
        x1: the x-coordinate of the rectangle's origin(float)
        y1: the y-coordinate of the rectangle's origin(float)
        rotation: rotation of shape in degrees (float)
    """
    #Every class declaration should have a constructor
    # We will allow user to set attributes of an instance
    def __init__ (self, width: float=0.0, height: float=0.0, x1:float = 0, y1: float = 0, rotation: float = 0):
        #What attributes should every rectangle get
        if width < 0.0 or height < 0.0:
            raise ValueError("width, height must be nonnegative")
        self.width = width
        self.height = height
        self.x1 = x1
        self.y1 = y1
        self.rotation = rotation

    def __repr__ (self) -> str:
        return f"Rectangle(width = {self.width}, height = {self.height}, x1 = {self.x1}, y1 = {self.y1}, rotation = {self.rotation})"

class Circle:
    """
    Represents a 2D circle via its center and radius,

    Attributes:
        x1: the x-coordinate of the center(float)
        y1: the y-coordinate of the center(float)
        radius: the center's radius(float)

    """
    def __init__ (self, x1: float=0.0, y1: float=0.0, radius: float=0.0): #default parameters
        if radius < 0.0:
            raise ValueError("radius must be non-negative")
        self.x1 = x1
        self.y1 = y1
        self.radius = radius

    def __repr__ (self) -> str:
        #Way of converting an object to a string and get its attributes
        #Have a nice f string to print the attributes
        return f"Circle(x1 = {self.x1}, y1 = {self.y1}, radius = {self.radius})"

def main():
    print("Shapes.")

    #these declarations create an INSTANCE of the object with the default attributes
    my_circle = Circle(1.0, 2.0, 3.0)

    r = Rectangle(3.0, 5.0) #Python doesn't get mad for not putting enough parameters into the constructor

    print(r)
    print(my_circle)

    #are instances of a new class pass by reference or pass by value?
    translate_circle(my_circle, 10.0, 10.0)
    translate_rectangle(r, 30.0, -100.0)
    print("The rectangle has been translated to", r)
    print("the circle has been translated to", my_circle)

    #Instances of a new class are pass by Reference
    # 1. Means you don't need to return an object everytime you pass an instance of it into a function
    # 2.
def translate_rectangle(r: Rectangle, a: float, b: float) -> Rectangle:
    """
    Move a rectangle by a given amount in x,y direction
    """
    r.x1 += a
    r.y1 += b


    return r



def translate_circle(c: Circle, a: float, b: float) -> Circle:
    """
    Move a circle by a given amount in x,y direction
    """
    c.x1 += a
    c.y1 += b
    return c


if __name__ == "__main__":
    main()
