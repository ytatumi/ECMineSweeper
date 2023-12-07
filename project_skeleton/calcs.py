"""This file represents only a few lines of code, such as the distance calculation, nothing needs to be added here"""


def measure_distance(x1, y1, x2, y2):
    """Calculates pythagorean distance between objects"""
    distance = ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5
    return distance
