from manim import *
import numpy as np

class FilledAngle(VMobject):
    def __init__(
            self,
            l1: Line,
            l2: Line,
            radius: float,
            color = BLUE,
            opacity = 0.5,
            other_angle = True,
            stroke_width=1,
            **kwargs):
        super().__init__(stroke_width=stroke_width)
        a1 = Angle(l1, l2, other_angle=other_angle, radius=0).set_color(color)
        a2 = Angle(l1, l2, other_angle=other_angle, radius=radius).set_color(color)
        q1 = a1.points
        q2 = a2.reverse_direction().points
        pnts = np.concatenate([q1, q2, q1[0].reshape(1, 3)])
        self.set_color(color)
        self.set_points_as_corners(pnts).set_fill(color, opacity)

class PotenciaDePonto(Scene):
    def construct(self):
        centered_circle = Circle(radius=2.5)
        centered_circle.set_stroke(WHITE, width=3)

        P = Dot(
            point=np.array([-5, 2, 0]),
            radius=0.03
	    )

        pLabel = Text("P", font_size=14)
        pLabel.move_to(P.points[0] + np.array([-0.1, 0.1, 0]))

        l1 = Line(start=P.points[0], end=np.array([2.3, 1, 0]))
        l1.set_stroke(WHITE, width=3)
        l2 = Line(start=P.points[0], end=np.array([0, -2.5, 0]))
       	l2.set_stroke(WHITE, width=3)
        arc = FilledAngle(l1, l2, 1)
        l1_intersec = self.circle_intersection(l1, centered_circle)
        l2_intersec = self.circle_intersection(l2, centered_circle)
        l3 = Line(start=l1_intersec[1], end=l2_intersec[0])
        l4 = Line(start=l2_intersec[1], end=l1_intersec[0])

        l1_opposite = Line(start=np.array([2.3, 1, 0]), end=P.points[0])
        l2_opossite = Line(start=np.array([0, -2.5, 0]), end=P.points[0])
        arc2 = FilledAngle(l1_opposite, l3, 1, color=ORANGE, other_angle=False)
        arc3 = FilledAngle(l2_opossite, l4, 1, color=ORANGE)

        self.play(Write(pLabel), Create(P), Create(centered_circle))
        self.play(Create(l1), Create(l2))
        self.play(Create(l3), Create(l4))
        self.play(Create(arc), Create(arc2), Create(arc3))
        self.wait(5)

    def circle_intersection(self, line: Line, circle: Circle):
        v = line.get_unit_vector()
        w = line.get_start()
        u = circle.get_center()
        a = np.dot(v, v)
        b = 2 * (np.dot(v, w) - np.dot(v, u))
        c = np.dot(w, w) + np.dot(u, u) - 2*u[0]*(v[0] + v[1]) - circle.radius**2
        discriminant = b**2 - 4*a*c
        if (discriminant < 0):
            return -1
        t1 = (-b - np.sqrt(discriminant)) / 2*a
        t2 = (-b + np.sqrt(discriminant)) / 2*a
        return np.array([v * t1 + w, v * t2 + w])
