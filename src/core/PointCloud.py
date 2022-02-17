from src.core.Point import Point


class PointCloud:

    def __init__(self, points: list) -> None:
        assert len(points) > 1 and type(points[0]) == Point

        self._points = points

    @property
    def points(self) -> list:
        return self._points

    def is_classified(self) -> bool:
        return len(self.points) > 0 and self.points[0].is_classified()

    def clear_labels(self) -> None:
        for point in self._points:
            point.clear_labels()
