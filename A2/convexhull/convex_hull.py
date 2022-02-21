import math
import sys
from typing import List
from typing import Tuple

EPSILON = sys.float_info.epsilon
Point = Tuple[int, int]


def y_intercept(p1: Point, p2: Point, x: float) -> float:
    """
    Given two points, p1 and p2, an x coordinate from a vertical line,
    compute and return the the y-intercept of the line segment p1->p2
    with the vertical line passing through x.
    """
    x1, y1 = p1
    x2, y2 = p2
    slope = 0
    print(p1, p2)
    try:
        slope = (y2 - y1) / (x2 - x1)
    except:
        print(x, p1, p2)
        pass
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
    print("In base case ", points)
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
    """

    :param left_hull:
    :param right_hull:
    :return:
    """

    clockwise_sort(left_hull)
    clockwise_sort(right_hull)

    # Find the inner most point on the left set of points
    l_top_point = 0
    l_bottom_point = 0
    for i in range(len(left_hull)):
        if left_hull[i][0] > left_hull[l_top_point][0]:
            l_top_point = i
            l_bottom_point = i

    # Find the inner most point on the right set of points
    r_top_point = 0
    r_bottom_point = 0
    for i in range(len(right_hull)):
        if right_hull[i][0] < right_hull[r_top_point][0]:
            r_top_point = i
            r_bottom_point = i

    # Average inner x coordinates and record as middle intersection
    middle_line = (left_hull[l_top_point][0] + right_hull[r_top_point][0])/2

    # Find starting intersection with middle line
    top_intersection = y_intercept(left_hull[l_top_point], right_hull[r_top_point], middle_line)
    bottom_intersection = y_intercept(left_hull[l_bottom_point], right_hull[r_bottom_point], middle_line)

    no_left_backtrack = True
    no_right_backtrack = True
    while no_left_backtrack or no_left_backtrack:

        if no_right_backtrack:
            # Increment index == move clockwise
            # Modulo prevent overflow
            r_top_point = (r_top_point + 1) % len(right_hull) 

            # See if the new top is higher up
            new_top = y_intercept(left_hull[l_top_point], right_hull[r_top_point], middle_line)
            if new_top < top_intersection:
                top_intersection = new_top
                no_left_backtrack = True
            
            else:
                # Move counterclockwise and leave left alone
                r_top_point -= 1 
                no_right_backtrack = False

        if no_left_backtrack:

            # Decrement index == move counterclockwise
            l_top_point -= 1

            # See if new_top is higher up
            new_top = y_intercept(left_hull[l_top_point], right_hull[r_top_point], middle_line)
            if new_top < top_intersection:
                top_intersection = new_top
                no_right_backtrack = True
            else:
                # Move clockwise and leave left alone
                l_top_point = (l_top_point + 1) % len(left_hull)
                no_left_backtrack = False

    no_left_backtrack  = True
    no_right_backtrack = True

    while no_right_backtrack or no_left_backtrack:

        if no_left_backtrack:
            # Increment == move clockwise
            # Modulo prevents overflow
            l_bottom_point = (l_bottom_point + 1) % len(left_hull)

            # See if new bottom is lower down
            new_bottom = y_intercept(left_hull[l_bottom_point], right_hull[r_bottom_point], middle_line)
            if new_bottom > bottom_intersection:
                bottom_intersection = new_bottom
                no_right_backtrack = True
            else:
                l_bottom_point -= 1
                no_left_backtrack = False

        if no_right_backtrack:

            # Decrement == move counter-clockwise
            r_bottom_point -= 1

            # See if new bottom is lower down
            new_bottom = y_intercept(left_hull[l_bottom_point], right_hull[r_bottom_point], middle_line)
            if new_bottom > bottom_intersection:
                bottom_intersection = new_bottom
                no_left_backtrack = True
            else:
                r_bottom_point = (r_bottom_point + 1) % len(right_hull)
                no_right_backtrack = False
    print("\n")
    print("Left Hull ", left_hull)
    print("Bottom: ", l_bottom_point, "Top: " , l_top_point)
    print(left_hull[l_bottom_point : l_top_point + 1 ])
    
    print("\n")
    print("Right Hull ", right_hull)
    print("Bottom: " , r_bottom_point, "Top: ", r_top_point)
    print(right_hull[r_top_point:] + right_hull[:r_bottom_point + 1])

    left_hull = left_hull[l_bottom_point : l_top_point + 1]

    if (r_top_point % len(right_hull)) == (r_bottom_point % len(right_hull)):
        singleton = right_hull[r_top_point]
        right_hull = []
        right_hull.append(singleton)
    else:
        right_hull = right_hull[r_top_point:] + right_hull[:r_bottom_point + 1]

    hull = left_hull + right_hull
    clockwise_sort(hull)
    # print(hull)

    return hull

def compute_hull(points: List[Point]) -> List[Point]:
    """
    Given a list of points, computes the convex hull around those points
    and returns only the points that are on the hull.
    """
    
    if len(points) <= 6:
        return(base_case_hull(points))


    # recursive case
    else:
        points = sorted(points, key= lambda x: x[0])
        median_index = math.ceil(len(points)/2)
        median_value = points[median_index][0]

        # sorts points into left and right arrays based off of median value
        left_points = []
        right_points = []
        for point in points:
            if point[0] < median_value:
                left_points.append(point)
            else:
                right_points.append(point)

        # call recursive computation on our divided lists
        left_hull = compute_hull(left_points)
        right_hull = compute_hull(right_points)

        # merge and conquer
        points = finger_merge(left_hull, right_hull)
        
    return points
