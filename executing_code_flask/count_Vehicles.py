import math

def distance_to_line(point, line_start, line_end):
    # Calculate line vector and point vector relative to line start
    line_vec = (line_end[0] - line_start[0], line_end[1] - line_start[1])
    point_vec = (point[0] - line_start[0], point[1] - line_start[1])

    # Project point vector onto line vector
    projection = ((point_vec[0] * line_vec[0]) + (point_vec[1] * line_vec[1])) / (line_vec[0] ** 2 + line_vec[1] ** 2)

    # Check if projection is on the line segment
    if projection < 0 or projection > 1:
        # Not on segment, return shortest distance to line
        return min(
            math.sqrt(((point[0] - line_start[0]) ** 2) + ((point[1] - line_start[1]) ** 2)),
            math.sqrt(((point[0] - line_end[0]) ** 2) + ((point[1] - line_end[1]) ** 2)),
        )

    # Projection is on segment, return distance to projection
    projected_point = (line_start[0] + projection * line_vec[0], line_start[1] + projection * line_vec[1])
    return math.sqrt(((point[0] - projected_point[0]) ** 2) + ((point[1] - projected_point[1]) ** 2))


def count_vehicles(track, count_lines):
    number_of_lines = len(count_lines)
    counts = [[0 for _ in range(number_of_lines + 1)] for _ in range(number_of_lines)]  # 2D list for counts

    for i, line in enumerate(count_lines):
        intersection_point = track.curve.intersection(line)  # Assuming intersection method exists

        if not intersection_point.is_empty:
            distance = distance_to_line(intersection_point, line.start, line.end)
            if distance < 1e-6:  # Tolerance for considering a point on the line
                counts[i][-1] += 1  # Count for exiting track
            else:
                for j, other_line in enumerate(count_lines):
                    if i != j and distance_to_line(intersection_point, other_line.start, other_line.end) < 1e-6:
                        counts[i][j] += 1  # Count for entering/crossing between lines

    return counts
