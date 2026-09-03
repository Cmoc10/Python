import math
import sys
from typing import List
from typing import Tuple

EPSILON = sys.float_info.epsilon
Point = Tuple[int, int]

#always check for vertical segments (x1=x2) before use
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


def sort_clockwise(points: List[Point]):
    """
    Sorts `points` by ascending clockwise angle from +x about the centroid,
    breaking ties first by ascending x value and then by ascending y value.

    The order of equal points is not modified

    Note: This function modifies its argument
    """
    # Trivial cases don't need sorting, and this dodges divide-by-zero errors
    if len(points) < 2:
        return

    # Compute the centroid
    centroid_x = sum(p[0] for p in points) / len(points)
    centroid_y = sum(p[1] for p in points) / len(points)

    # Sort by ascending clockwise angle from +x, breaking ties with ^x then ^y
    def sort_key(point: Point):
        angle = math.atan2(point[1] - centroid_y, point[0] - centroid_x)
        normalized_angle = (angle + math.tau) % math.tau
        return (normalized_angle, point[0], point[1])

    # Sort the points
    points.sort(key=sort_key)


def base_case_hull(points: List[Point]) -> List[Point]:
    """ Base case of the recursive algorithm.
    """
    # TODO: You need to implement this function.
    # NAIVE ALGORITHM for fewer than 5/6 points

    hull = [] # list of hull points to be returned
    n = len(points) # num of points in list

    # If there are more than 6 points in list, use divide & conquer 
    if n > 6:
        return compute_hull(points)
    else:
        # COMPUTE NAIVE (brute force) HERE

        # 1. Pick two points (draw temp tangent)
        # 2. Check if all other points are on left(CW) or right(CCW) side of tangent
        # 3. If all points on one side -> edge of convex hull, keep tangent
        # 4. Else swap point for another one

        # Go through all points
        for i in range(n):
            for j in range(n):
                # check if they're the same point...
                if i == j:
                    continue
                p1 = points[i]
                p2 = points[j]

                # LEFT OR RIGHT SIDE OF TANGENT!!
                side = None # None because side hasn't been declared yet w/ 3rd point
                valid = True # if it's a valid point to add 

                # Third point to triangulate with (go through all points again...)
                for k in range(n):
                    # check if it's same as p1/p2 first
                    if k == p1 or k == p2:
                        continue
                    p3 = points[k]

                    # Triangle to figure out whether left (CW, +) or right (CCW, -) (also could be collinear)
                    area = triangle_area(p1, p2, p3)

                    # If area = 0 (collinear)
                    if area == 0:
                        continue 
                    # Check CW/CCW & declare side (should be all one side for the whole graph)
                    elif side is None:
                        side = area > 0
                    # Doesn't match previously declared side, break & get new p3
                    elif (area > 0) != side:
                        valid = False
                        break

                # If valid for p1,p2,p3 add p1,p2 to hull list(&if not already in there)
                if valid:
                    if p1 not in hull:
                        hull.append(p1)
                    if p2 not in hull:
                        hull.append(p2)

    # Points to be returned in CLOCKWISE order
    sort_clockwise(hull)
    return hull

# DIVIDE AND CONQUER STEP: SPLIT IN HALF AND THEN RECURSIVELY SPLIT UNTIL N < 6
def divide_conquer(points: List[Point]) -> List[Point]:
    n = len(points)
    if n < 6:
        return base_case_hull(points)
    
    # Sort points by x-coordinate for proper splitting
    points = sorted(points, key=lambda p: (p[0], p[1]))
    mid = n // 2
    left = points[:mid]
    right = points[mid:]

    left_hull = divide_conquer(left)
    right_hull = divide_conquer(right)

    return merge(left_hull, right_hull)

def merge(left_hull: List[Point], right_hull: List[Point]) -> List[Point]:
    hull = []
    # if len < 3 return
    # sort by X and then Y
    # two loops: 
        # one reg
        # one reverse
    # while length upper >=2 AND no right turn: remove current point
    # while length of lower >=2 AND no right turn: remove current point
def merge(left_hull: List[Point], right_hull: List[Point]) -> List[Point]:
    # Find rightmost point of left_hull and leftmost point of right_hull
    leftn = len(left_hull)
    rightn = len(right_hull)
    left_idx = max(range(leftn), key=lambda i: left_hull[i][0])
    right_idx = min(range(rightn), key=lambda i: right_hull[i][0])

    # Find upper tangent
    done = False
    i, j = left_idx, right_idx
    while not done:
        done = True
        while triangle_area(right_hull[j], left_hull[i], left_hull[(i+1)%leftn]) > 0:
            i = (i+1) % leftn
        while triangle_area(left_hull[i], right_hull[j], right_hull[(j-1)%rightn]) < 0:
            j = (j-1) % rightn
            done = False
    upper_left, upper_right = i, j

    # Find lower tangent
    done = False
    i, j = left_idx, right_idx
    while not done:
        done = True
        while triangle_area(left_hull[i], right_hull[j], right_hull[(j+1)%rightn]) > 0:
            j = (j+1) % rightn
        while triangle_area(right_hull[j], left_hull[i], left_hull[(i-1)%leftn]) < 0:
            i = (i-1) % leftn
            done = False
    lower_left, lower_right = i, j

    # Collect hull points in clockwise order
    hull = []
    idx = upper_left
    hull.append(left_hull[idx])
    while idx != lower_left:
        idx = (idx+1) % leftn
        hull.append(left_hull[idx])

    idx = lower_right
    hull.append(right_hull[idx])
    while idx != upper_right:
        idx = (idx+1) % rightn
        hull.append(right_hull[idx])

    # Remove duplicates if any
    hull = list(dict.fromkeys(hull))
    return hull
    # STEPS:
    # 1. Divide: sort points by chunks, find median of each chunk & median of medians
    # 2. Conquer: recursively compute convex hulls of A and B around pivot
    # left_hull, right_hull = divide_conquer(points) # both steps in one function, recursively called

    # # 3. Merge: start with medians in A and B, move CCW/CW, adjusting tangents
    # hull = merge(left_hull, right_hull) # final hull, list of points in convex hull
    hull = divide_conquer(points)

    # TODO: Document your Initialization, Maintenance and Termination invariants.


    # Points to be returned in CLOCKWISE order
    sort_clockwise(hull)
    return hull
def compute_hull(points: List[Point]) -> List[Point]:
    """
    Given a list of points, computes the convex hull around those points
    and returns only the points that are on the hull.
    """
    hull = divide_conquer(points)
    sort_clockwise(hull)
    return hull

#Invariant: At any given time we have a correct convex hull created for our subset
#Initialization: There is no subset and therefore no convex hull
#Maintenance: At each merge step of our algorithm we make sure that a correct convex hull is created. This ensures that all subsets that have been checked out have a proper convex hull.
#Termination: When the algorithm completes there is one convex hull for all of the points.
