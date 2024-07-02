from itertools import tee
from typing import Iterable, List, Tuple
import executing_code_flask.Toll_Plaza as Toll_Plaza
import numpy as np

from tsa.dataclasses.geometry.line import Line  # type: ignore
from tsa.storage import ReadStorageMethod # type: ignore


def _pairwise(iterable: Iterable) -> Iterable[Tuple]:
    first, second = tee(iterable)
    next(second, None)
    return zip(first, second)


def _order_intersection_indices(track, intersections):
    intersection_distances = [track.curve.project(intersection) for _, intersection in intersections]
    sorted_intersection_distance_indices = sorted(range(len(intersections)), key=lambda i: intersection_distances[i])
    sorted_intersection_indices = map(lambda i: intersections[i][0], sorted_intersection_distance_indices)

    return _pairwise(sorted_intersection_indices)


def count_vehicles(track_source: ReadStorageMethod, count_lines: List[Line]):
    number_of_lines = len(count_lines)
    counts = np.zeros((number_of_lines, number_of_lines + 1), dtype=np.int32)

    for track in track_source.read_track():
        intersections = []

        for i, line in enumerate(count_lines):
            intersection_point = track.curve.intersection(line)

            if not intersection_point.is_empty:
                intersections.append((i, intersection_point))

        if not intersections:
            continue

        if len(intersections) == 1:
            counts[intersections[0][0], -1] += 1
        else:
            for from_index, to_index in _order_intersection_indices(track, intersections):
                counts[from_index, to_index] += 1

    return counts
