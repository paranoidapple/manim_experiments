from manim import *
from compass import Compass, arc_intersection


class Main(Scene):
    def construct(self):

        # Create line
        line = Line(LEFT * 2, RIGHT * 2)
        self.play(Create(line))
        self.wait()

        # Create compass
        compass = Compass(self, arm_width=4, radius=2.5)
        self.wait()

        # Move compass to create arcs
        compass.move_to(LEFT * 2)
        arc1 = compass.draw_segments((0.85 * TAU, 0.95 * TAU), (0.05 * TAU, 0.15 * TAU))
        self.wait()

        compass.move_to(RIGHT * 2)
        arc2 = compass.draw_segments((0.35 * TAU, 0.45 * TAU), (0.55 * TAU, 0.65 * TAU))
        self.wait()

        # Create arc intersection points
        ints = arc_intersection(self, arc1[1], arc2[0])
        p1 = Dot(ints[0] + (0,))
        p2 = Dot(ints[1] + (0,))
        self.play(Create(p1), Create(p2))
        self.wait()

        # Connect intersection points to form perpendicular bisector
        perp_bis = Line(p1.get_center(), p2.get_center())
        self.add_foreground_mobjects(line, perp_bis)
        self.play(Create(perp_bis))

        # Create right angle
        right_angle = RightAngle(line, perp_bis, color=BLUE_D, length=0.25)
        self.play(Create(right_angle))
        self.wait()
