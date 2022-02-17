import math
import sys
from typing import List
from typing import Tuple

EPSILON = sys.float_info.epsilon
Point = Tuple[int, int]


def y_intercept(p1: Point, p2: Point, x: int) -> float:
    """
    Given two points, p1 and p2, an x coordinate from a vertical line,
    compute and return the the y-intercept of the line segment p1->p2
    with the vertical line passing through x.
    """
    x1, y1 = p1
    x2, y2 = p2
    slope = (y2 - y1) / (x2 - x1)
    return y1 + (x - x1) * slope


def triangle_area(a: Point, b: Point, c: Point) -> float:
    """
    Given three points a,b,c,
    computes and returns the area defined by the triangle a,b,c.
    Note that this area will be negative if a,b,c represents a clockwise sequence,
    positive if it is counter-clockwise,
    and zero if the points are collinear.
    """
    ax, ay = a
    bx, by = b
    cx, cy = c
    return ((cx - bx) * (by - ay) - (bx - ax) * (cy - by)) / 2


def is_clockwise(a: Point, b: Point, c: Point) -> bool:
    """
    Given three points a,b,c,
    returns True if and only if a,b,c represents a clockwise sequence
    (subject to floating-point precision)
    """
    return triangle_area(a, b, c) < -EPSILON


def is_counter_clockwise(a: Point, b: Point, c: Point) -> bool:
    """
    Given three points a,b,c,
    returns True if and only if a,b,c represents a counter-clockwise sequence
    (subject to floating-point precision)
    """
    return triangle_area(a, b, c) > EPSILON


def collinear(a: Point, b: Point, c: Point) -> bool:
    """
    Given three points a,b,c,
    returns True if and only if a,b,c are collinear
    (subject to floating-point precision)
    """
    return abs(triangle_area(a, b, c)) <= EPSILON


def clockwise_sort(points: List[Point]):
    """
    Given a list of points, sorts those points in clockwise order about their centroid.
    Note: this function modifies its argument.
    """
    # get mean x coord, mean y coord
    x_mean = sum(p[0] for p in points) / len(points)
    y_mean = sum(p[1] for p in points) / len(points)

    def angle(point: Point):
        return (math.atan2(point[1] - y_mean, point[0] - x_mean) + 2 * math.pi) % (2 * math.pi)

    points.sort(key=angle)
    return

def get_position(a: Point, b: Point, c: Point) -> int:
    """
    Returns the orientation of c with regards to 
    the line formed by a & b
    < 0 : below the line
    = 0 : tangent
    > 0 : above the line 
    """
    # Cross Product
    ax, ay = a
    bx, by = b
    cx, cy = c
    vec1 = (bx - ax, by - ay)
    vec2 = (bx - cx, by - cy)
    return (vec1[0] * vec2[1] - vec1[1] * vec2[0])

def check_positions(positions):
    """
    Iterates over all positions
    Returns true if all positions lie on the tangent or on
    the same side
    """
    is_down = False
    is_up = False
    for position in positions:
        if position < 0:
            is_down = True
            if is_up:
                return False
        elif position > 0:
            is_up = True
            if is_down:
                return False
    return True

def base_case_hull(points: List[Point]) -> List[Point]:
    """ Base case of the recursive algorithm.
    """
    if len(points) == 1:
        return points
    hull = []
    for i in range(len(points)):
        for j in range(len(points)):
    # Continue if looking at the same point
            if i == j:
                continue
    # Check all points: see if they all lie on one side of the tangent
            positions = []
            for k in range(len(points)):
                if k == i or k == j:
                    continue
                positions.append(get_position(points[i], points[j], points[k]))
            # If so add them to the hull if not already there
            if (check_positions(positions)):
                if points[i] not in hull:
                    hull.append(points[i])
                if points[j] not in hull:
                    hull.append(points[j])
    # Sort Clockwise
    clockwise_sort(hull)
    return hull

def finger_merge(left_hull: List[Point], right_hull: List[Point]) -> List[Point]:
    # TODO: do this

    # 1: find right most point in left hull -> lTopPoint, lBottomPoint (indexes)
    # 2: find left most point in right hull -> rTopPoint, rBottomPoint (indexes)
    # 3: average those point's x coordinates with // and record that x coordinate as vertical line
    # 4: find intersection with vert-line with two middle points, record value -> max_top, max_bottom
    # left_backtrack = true
    # right_backtrack = true

    # top while(left_backtrack || right_backtrack)
        # move once on right, record intersection value
            # if lesser, store point in right top point variable, update max_top
            # if greater, set right_backtrack to false
        # move once left, record new intersection value
            # if lesser, store point in right top point variable, update max_top
            # if greater, set left_backtrack to false
    # reset backtracks
    # bottom while(left_backtrack || right_backtrack)
        # move once on right, record new intersection value
            # if value is greater, store point in right bottom variable, update max_bottom
            # if lesser, set right_backtrack to false
        # move once left, record
            # if greater, store and update
            # if lesser, set backtrack

    # merge the two lists in clockwise order starting from bottomLeft index.
    # use slice function to take left bottom index up to left top index + 1 -> left hull. add to point
    # use slice function to take right top hull section from right top to end of list -> right top
        # add to points
    # use slice function to go from start of right list to right bottom index + 1 -> right bottom
        # add to points list

    return left_hull + right_hull

def compute_hull(points: List[Point]) -> List[Point]:
    """
    Given a list of points, computes the convex hull around those points
    and returns only the points that are on the hull.
    """
    # TODO: Implement a correct computation of the convex hull
    #  using the divide-and-conquer algorithm
    # TODO: Document your Initialization, Maintenance and Termination invariants.

    # sorts points clockwise before computation
    clockwise_sort(points)

    # if the base case is possible, do the base case
    if len(points) <= 6:
        points = base_case_hull(points)

    # recurse case
    # else:

    #     # get the median
    #     median_index = len(points)-1//2
    #     median_x_value = points[median_index][1]
    #     # TODO: what about the case where all (or enough so that the base case is unsatisfiable on either side)
    #     # TODO: points are on the same x value, how should we split the data then?
    #     # TODO: in other words, what if splitting yields not enough data for a base case on either side?

    #     # sorts points into left and right arrays based off of median value
    #     left_points = []
    #     right_points = []
    #     for point in points:
    #         if point[1] <= median_x_value:
    #             left_points.append(point)
    #         else:
    #             right_points.append(point)

    #     # divide
    #     left_hull = compute_hull(left_points)
    #     right_hull = compute_hull(right_points)

    #     # merge and conquer
    #     points = finger_merge(left_hull, right_hull)
    return points
