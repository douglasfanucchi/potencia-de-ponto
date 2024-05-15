from manimlib import *
import numpy as np

class PotenciaDePonto(Scene):
    def construct(self):
        centered_circle = Circle(radius=2.5)
        centered_circle.set_stroke(WHITE, width=1)
        origin = np.array([0, 0, 0])

        P = Dot(
            point=np.array([-5, 2, 0]),
            radius=0.03
        )

        pLabel = Text("P", font_size=14)
        pLabel.move_to(P.get_points()[0] + np.array([-0.1, 0.1, 0]))

        A = Line(start=P.get_points()[0], end=np.array([2.3, 1]))
        A.set_stroke(WHITE, width=1)

        B = Line(start=P.get_points()[0], end=np.array([2.3, -1]))
        B.set_stroke(WHITE, width=1)

        sector = ArcBetweenPoints(
            start=P.get_points()[0] + B.get_unit_vector(),
            end=P.get_points()[0] + A.get_unit_vector(),
            stroke_width=1
        )

        self.play(ShowCreation(P))
        self.play(Write(pLabel))
        self.play(ShowCreation(centered_circle))
        self.play(ShowCreation(A))
        self.play(ShowCreation(B))
        self.play(ShowCreation(sector))