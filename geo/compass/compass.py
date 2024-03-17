from __future__ import annotations

from manim import *
from numpy import ndarray, dtype, float_, sqrt


class Compass:

    def __init__(
        self,
        scene: Scene,
        center: (
            ndarray[Any, dtype[float_]]
            | tuple[float, float]
            | tuple[float, float, float]
        ) = ORIGIN,
        radius: float = 2.0,
        # fmt: skip
        lead_color: ParsableManimColor = WHITE,
        lead_width: float = 2.0,
        arm_color: ParsableManimColor = YELLOW,
        arm_width: float = 2.0,
    ):
        self.scene = scene

        # Value trackers for animation
        self._x = ValueTracker(center[0])
        self._y = ValueTracker(center[1])
        self._radius = ValueTracker(radius)
        self._angle = ValueTracker(0)

        self.lead_color = lead_color
        self.lead_width = lead_width
        self.arm_color = arm_color
        self.arm_width = arm_width

        self.arm = always_redraw(
            lambda: Line(
                start=np.array([self.x, self.y, 0]),
                end=np.array(
                    [
                        (self.radius * np.cos(self.angle)) + self.x,
                        (self.radius * np.sin(self.angle)) + self.y,
                        0,
                    ]
                ),
                color=self.arm_color,
                stroke_width=self.arm_width,
            )
        )

        self.center_mark = always_redraw(
            lambda: Dot(
                point=self.center,
                color=self.arm_color
            )
        )

        self.scene.add_foreground_mobjects(self.arm, self.center_mark)
        self.scene.play(FadeIn(self.arm, self.center_mark))

    @property
    def x(self) -> float:
        """The compass center's X coordinate."""
        return self._x.get_value()

    @property
    def y(self) -> float:
        """The compass center's Y coordinate."""
        return self._y.get_value()

    @property
    def center(self) -> tuple[float, float, float]:
        """The compass center."""
        return self.x, self.y, 0

    @property
    def radius(self) -> float:
        """The compass radius."""
        return self._radius.get_value()

    @property
    def angle(self) -> float:
        """The compass angle."""
        return self._angle.get_value()

    def move_to(
        self,
        center: (
            ndarray[Any, dtype[float_]]
            | tuple[float, float]
            | tuple[float, float, float]
        ),
        **kwargs,
    ) -> Compass:
        """Animates moving the center of the compass."""
        self.scene.play(
            AnimationGroup(
                self._x.animate(kwargs=kwargs).set_value(center[0]),  # linear smoothens its movement
                self._y.animate(kwargs=kwargs).set_value(center[1]),
            )
        )
        return self

    def set_radius(self, length: float, **kwargs) -> Compass:
        """Animates extending or retracting of the compass."""
        self.scene.play(self._radius.animate(kwargs=kwargs).set_value(length))
        return self

    def set_angle(self, angle: float, **kwargs) -> Compass:
        """Animates rotation of the compass."""
        self.scene.play(self._angle.animate(kwargs=kwargs).set_value(angle))
        self._angle.set_value(angle % (360 * DEGREES))
        return self

    def draw_segments(
        self, *segments: tuple[float, float] | tuple[float, float, float]
    ) -> Mobject:
        """Draws multiple arcs in one sweep."""

        arcs = always_redraw(
            lambda: VGroup(
                *[
                    Arc(
                        radius=self.radius,
                        arc_center=np.array([self.x, self.y, 0.0]),
                        start_angle=start,
                        color=segment_color or self.lead_color,
                        stroke_width=self.lead_width,
                        angle=(
                            min(self.angle - start, end - start)
                            if self.angle > start
                            else 0
                        ),
                    )
                    for start, end, *segment_color in segments
                ]
            )
        )

        # Animate
        self.scene.add(arcs)
        self.set_angle(2 * PI + self.angle)

        # Remove arc updaters
        arcs.clear_updaters()
        return arcs

    def dot_at(self, alpha: float) -> Dot:
        return Dot(Circle(
            radius=self.radius, arc_center=np.array([self.x, self.y, 0.0])
        ).point_from_proportion(alpha))


def arc_intersection(scene: Scene, a: Arc, b: Arc) -> tuple[tuple[float, float], tuple[float, float]] | None:
    """Gets the intersection points of two arcs."""

    x0 = a.get_arc_center()[0]
    y0 = a.get_arc_center()[1]
    r0 = a.radius

    x1 = b.get_arc_center()[0]
    y1 = b.get_arc_center()[1]
    r1 = b.radius

    # https://stackoverflow.com/questions/55816902/finding-the-intersection-of-two-circles
    d = sqrt((x1 - x0) ** 2 + (y1 - y0) ** 2)

    # Non-intersecting
    if d > r0 + r1:
        return None

    # One circle within other
    if d < abs(r0 - r1):
        return None

    # Coincident circles
    if d == 0 and r0 == r1:
        return None

    else:
        a = ((r0 ** 2) - (r1 ** 2) + (d ** 2)) / (2 * d)
        h = sqrt((r0 ** 2) - (a ** 2))

        x2 = x0 + (a * (x1 - x0) / d)
        y2 = y0 + (a * (y1 - y0) / d)

        x3 = x2 + (h * (y1 - y0) / d)
        y3 = y2 - (h * (x1 - x0) / d)

        x4 = x2 - (h * (y1 - y0) / d)
        y4 = y2 + (h * (x1 - x0) / d)

        return (x3, y3), (x4, y4)
