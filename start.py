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
        pLabel.move_to(P.get_points()[0] + np.array([-0.1, 0.1, 0]))

        l1 = Line(start=P.get_points()[0], end=np.array([2.3, 1, 0]))
        l1.set_stroke(WHITE, width=3)

        l2 = Line(start=P.get_points()[0], end=np.array([2.3, -1, 0]))
       	l2.set_stroke(WHITE, width=3)

        arc = FilledAngle(l1, l2, 1)

        self.play(Write(pLabel), Create(P), Create(centered_circle))
        self.play(Create(l1), Create(l2))
        self.wait(5)
        self.play(Create(arc))
