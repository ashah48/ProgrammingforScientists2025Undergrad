from dataclasses import dataclass
import math

G = 6.67408e-11  # gravitational constant (you can scale this for visualization)

@dataclass
class OrderedPair:
    """
    A simple 2-D point or vector with named coordinates.

    Used to represent positions, velocities, and accelerations of stars
    in the simulation. Supports access via `.x` and `.y` for readability.
    """
    x: float = 0.0
    y: float = 0.0

@dataclass
class Star:
    """
    A celestial body in the simulation.

    Each Star has a position, velocity, acceleration, mass, and radius,
    along with optional RGB color values for visualization.
    The position and motion are expressed as 2D vectors (x, y).
    """
    position: OrderedPair | None = None
    velocity: OrderedPair | None = None
    acceleration: OrderedPair | None = None
    mass: float = 0.0
    radius: float = 0.0
    red: int = 255
    green: int = 255
    blue: int = 255


@dataclass
class Universe:
    """
    A square universe of given width containing a list of stars.

    The universe defines the simulation space. Its width represents the
    side length of a square region with corners at (0, 0) and (width, width).
    """
    width: float = 0.0
    stars: list[Star] = None

    def in_field(self, p: OrderedPair) -> bool:
        """
        Check if a given point is within the bounds of the universe.
        """
        return 0 <= p.x <= self.width and 0 <= p.y <= self.width


@dataclass
class Quadrant:
    """
    A square subregion of the universe given by its lower-left corner (x, y) and width.
    """
    x: float = 0.0
    y: float = 0.0
    width: float = 0.0


@dataclass
class Node:
    """
    A quadtree node. Internal nodes store a dummy 'star' for the center of mass and have children.
    Leaf nodes may store a real star (or be empty) and have no children.
    By convention, child quadrants are ordered [NW, NE, SW, SE].
    """
    sector: Quadrant
    children: list["Node"] | None = None
    star: Star | None = None

    def is_leaf(self) -> bool:
        """
        Check if the node is a leaf (i.e., is child-free).
        """
        return self.children is None or len(self.children) == 0

    def insert(self, s: Star) -> None:
        """
        Input: A Node object self and a Star object s .
        Output: None. The method inserts s into the appropriate location in the QuadTree whose
        root is current_node, which may involve creating children and updating the center of mass
        of dummy stars occupying existing nodes.
        """
        #Base case
        if self.is_leaf():

            if self.star is None:
                self.star = s
                return
            elif self.star.position == s.position:
               #If self.star and s are in the same spot combine add the mass of s to self.star
                self.star.mass += s.mass
                return
            else:
                #Divide self into 4 child nodes
                self.create_children()
                #Push self's star down into one of the child leaf nodes
                old_star = self.star
                child_for_old_star = self.find_child(old_star)
                child_for_old_star.insert(old_star)
                self.star = None
                #Insert the new star into one of the child leaf nodes
                child_for_new_star = self.find_child(s)
                child_for_new_star.insert(s)
                #Update center of gravity and mass for self node
                new_pos = center_of_gravity(old_star, s)
                self.star = Star(position = new_pos, mass = s.mass + old_star.mass)
                return

        #Recursive case
        if self != None:
            correct_child = self.find_child(s)
            correct_child.insert(s)
        #Update dummy star's center of gravity and mass
        if self.star != None:
            new_pos = center_of_gravity(self.star, s)
            self.star.position = new_pos
            self.star.mass += s.mass
        return

    def create_children(self) -> None:
        """
        Input: A Node object self.
        Output: None. The function modifies current_node by adding four
        child nodes to the Node attribute, children. Each child corresponds to one quadrant of
        the current node’s sector as explained above.
        """
        x1 = self.sector.x
        y1 = self.sector.y
        child_width = self.sector.width / 2
        #Make a node for each quadrant in the sector:
        nw = Node(Quadrant(x1, y1+child_width, child_width))
        ne = Node(Quadrant(x1+child_width, y1+child_width, child_width))
        sw = Node(Quadrant(x1, y1, child_width))
        se = Node(Quadrant(x1+child_width, y1, child_width))
        #Add the four nodes in the right order to the children array.
        self.children = [nw, ne, sw, se]

    # find_child determines the correct quadrant child a star belongs to
    # and returns that child node.
    def find_child(self, s: Star) -> "Node":
        """
        Input: A Node object self and a Star object s.
        Output: The child Node of self whose sector would contain star s.
        """
        sx = s.position.x
        sy = s.position.y
        #Find the central position for self to make it easier to compare the position
        #-of s to self.
        self_cx = self.sector.x + self.sector.width/2
        self_cy = self.sector.y + self.sector.width/2

        if sx <= self_cx and sy >= self_cy:
            return self.children[0] #NW
        if sx > self_cx and sy >= self_cy:
            return self.children[1] #NE
        if sx <= self_cx and sy < self_cy:
            return self.children[2] #SW
        else:
            return self.children[3] #SE

    def calculate_net_force(self, s: Star, theta: float) -> OrderedPair:
        """
        Input: A Node object self, a Star object star, and a float theta.
        Output: An ordered pair representing the net force acting on star of the bodies
        contained in the tree whose root is self, according to the Barnes-Hut algorithm
        using a parameter of theta.
        """
        #self is a leaf and has a star
        if self.is_leaf():
            #Check three cases for self.star:
            if self.star == None:
                return OrderedPair(0,0)
            elif self.star == s:
                return OrderedPair(0,0)
            else:
                force = compute_force(self.star, s)
                return force

        #self is an internal node
        else:
            #compute sector_width / distance(self.star, s)
            s_over_d = self.sector.width / distance(self.star.position, s.position)
            net_force_on_s = OrderedPair(0,0)
            if s_over_d > theta:
                for child in self.children:
                    force = child.calculate_net_force(s, theta)
                    net_force_on_s.x += force.x
                    net_force_on_s.y += force.y
            else:
                force = compute_force(self.star, s)
                net_force_on_s.x += force.x
                net_force_on_s.y += force.y

            return net_force_on_s

@dataclass
class QuadTree:
    """
    A wrapper around the root node of a Barnes–Hut quadtree.

    Provides an interface for inserting stars, building the spatial tree,
    and calculating net gravitational forces using hierarchical aggregation.
    """
    root: Node | None = None

    def insert(self, s: Star) -> None:
        if self.root != None:
            self.root.insert(s)

# To prevent circular import issues, we define these functions here.

def center_of_gravity(*stars: Star) -> OrderedPair:
    """
    Input: A tuple stars representing an arbitrary number of Star objects.
    Output: An OrderedPair object representing the center of gravity of the Star objects in stars.
    """
    sum_of_mass_times_pos = OrderedPair()
    sum_of_mass = 0
    for star in stars:
        sum_of_mass_times_pos.x += star.mass * star.position.x
        sum_of_mass_times_pos.y += star.mass * star.position.y
        sum_of_mass += star.mass

    return OrderedPair(sum_of_mass_times_pos.x/sum_of_mass, sum_of_mass_times_pos.y/sum_of_mass)


def compute_force(s1: Star, s2: Star) -> OrderedPair:
    """
    Compute the gravitational force exerted by s1 on s2.
    Uses Newton's law of universal gravitation.
    𝐹 = G * (m1 * m2) / r²
    """
    d = distance(s1.position, s2.position)
    F = G * s1.mass * s2.mass / (d * d)

    delta = (s1.position.x - s2.position.x, s1.position.y - s2.position.y)
    force = OrderedPair(F * (delta[0] / d), F * (delta[1] / d))
    return force


def distance(p1: OrderedPair, p2: OrderedPair) -> float:
    """
    Compute the Euclidean distance between two points.
    """
    dx, dy = (p1.x - p2.x, p1.y - p2.y)
    return math.sqrt(dx * dx + dy * dy)
