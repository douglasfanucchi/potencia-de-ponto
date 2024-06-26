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
            other_angle = False,
            stroke_width=1,
            quadrant=np.array([1, 1]),
            **kwargs):
        super().__init__(stroke_width=stroke_width)
        a1 = Angle(l1, l2, other_angle=other_angle, radius=0, quadrant=quadrant).set_color(color)
        a2 = Angle(l1, l2, other_angle=other_angle, radius=radius, quadrant=quadrant).set_color(color)
        q1 = a1.points
        q2 = a2.reverse_direction().points
        pnts = np.concatenate([q1, q2, q1[0].reshape(1, 3)])
        self.set_color(color)
        self.set_points_as_corners(pnts).set_fill(color, opacity)

class LabeledDot():
    def __init__(self, dot, label, label_position=None):
        self.dot = dot
        self.label = label
        coordinates = self.dot.points[0] + np.array([-0.1, 0.1, 0])
        label_position = label_position if label_position is not None else [0, 0, 0]
        coordinates += label_position
        self.label.move_to(coordinates)
        label.add_updater(lambda x: x.move_to(
            dot.points[0] + np.array([-0.1, 0.1, 0]) + label_position
        ))

class PotenciaDePonto(Scene):
    def construct(self):
        centered_circle = Circle(radius=2.5)
        centered_circle.set_stroke(WHITE, width=3)
        font_size=14
        dot_radius=0.03

        P = LabeledDot(
            dot=Dot(
                    point=np.array([-5, 2, 0]),
                    radius=dot_radius
                ),
                label=Text(
                    "P", font_size=font_size),
            )

        l1_end = self.get_circle_points(1, centered_circle)[1]
        l2_end = self.get_circle_points(0, centered_circle)[0]
        l1 = Line(start=P.dot.points[0], end=np.array(l1_end), stroke_width=3)
        l2 = Line(start=P.dot.points[0], end=np.array(l2_end), stroke_width=3)
        self.play(Write(P.label), Create(P.dot), Create(centered_circle))
        lines_to_remove = [
            Line(start=P.dot.points[0], end=self.get_circle_points(0, centered_circle)[1], stroke_width=3),
            Line(start=P.dot.points[0], end=self.get_circle_points(0, centered_circle)[0], stroke_width=3),
            Line(start=P.dot.points[0], end=self.get_circle_points(1, centered_circle)[1], stroke_width=3),
            Line(start=P.dot.points[0], end=self.get_circle_points(1, centered_circle)[0], stroke_width=3),
            Line(start=P.dot.points[0], end=self.get_circle_points(2, centered_circle)[1], stroke_width=3),
            Line(start=P.dot.points[0], end=self.get_circle_points(2, centered_circle)[0], stroke_width=3),
            Line(start=P.dot.points[0], end=self.get_circle_points(2.5, centered_circle)[0], stroke_width=3),
        ]
        self.play(
            Create(l1), Create(l2),
            Create(lines_to_remove[0]), Create(lines_to_remove[1]), Create(lines_to_remove[2]),
            Create(lines_to_remove[3]), Create(lines_to_remove[4]), Create(lines_to_remove[5]),
            Create(lines_to_remove[6])
        )
        self.play(
            FadeOut(lines_to_remove[0]), FadeOut(lines_to_remove[1]), FadeOut(lines_to_remove[2]),
            FadeOut(lines_to_remove[3]), FadeOut(lines_to_remove[4]), FadeOut(lines_to_remove[5]),
            FadeOut(lines_to_remove[6])
        )
        for line in lines_to_remove:
            self.remove(line)

        l1_intersec = self.circle_intersection(l1, centered_circle)
        l2_intersec = self.circle_intersection(l2, centered_circle)
        A=LabeledDot(
            dot=Dot(
                point=l1_intersec[0],
                radius=dot_radius
            ),
            label=Text(
                "A",
                font_size=font_size
            ),
            label_position=np.array([0, 0.1, 0])
        )
        B=LabeledDot(
            dot=Dot(
                point=l1_intersec[1],
                radius=dot_radius
            ),
            label=Text(
                "B",
                font_size=font_size
            ),
            label_position=np.array([0.2, 0, 0])
        )
        C=LabeledDot(
            dot=Dot(
                point=l2_intersec[0],
                radius=dot_radius
            ),
            label=Text(
                "C",
                font_size=font_size
            ),
            label_position=np.array([-0.1, -0.2, 0])
        )
        D=LabeledDot(
            dot=Dot(
                point=l2_intersec[1],
                radius=dot_radius
            ),
            label=Text(
                "D",
                font_size=font_size,
            ),
            label_position=np.array([0.1, -0.25, 0])
        )
        self.play(
            Create(A.dot), Create(A.label),
            Create(B.dot), Create(B.label),
            Create(C.dot), Create(C.label),
            Create(D.dot), Create(D.label))

        l3 = Line(start=l1_intersec[1], end=l2_intersec[0])
        l4 = Line(start=l2_intersec[1], end=l1_intersec[0])
        self.play(Create(l3), Create(l4))

        arc = FilledAngle(l1, l2, 1, other_angle=True)
        arc2 = FilledAngle(l1, l3, 1, color=ORANGE, quadrant=np.array([-1, 1]))
        arc3 = FilledAngle(l4, l2, 1, color=ORANGE, quadrant=np.array([1, -1]))
        self.play(Create(arc), Create(arc2), Create(arc3))

        PA = Line(start=P.dot.points[0], end=A.dot.points[0], stroke_width=3)
        PC = Line(start=P.dot.points[0], end=C.dot.points[0], stroke_width=3)
        self.add(PA)
        self.add(PC)
        faded_l1 = Line(start=l1.start, end=l1.end, stroke_width=3, stroke_opacity=0.2)
        faded_l3 = Line(start=l3.start, end=l3.end, stroke_width=3, stroke_opacity=0.2)
        faded_arc2 = FilledAngle(l1, l3, 1, color=ORANGE, quadrant=[-1, 1], opacity=0.1)
        self.play(
            FadeTransform(l1, faded_l1),
            FadeTransform(l3, faded_l3),
            FadeTransform(arc2, faded_arc2)
        )
        self.wait(2)
        faded_l2 = Line(start=l2.start, end=l2.end, stroke_width=3, stroke_opacity=0.2)
        faded_l4 = Line(start=l4.start, end=l4.end, stroke_width=3, stroke_opacity=0.2)
        faded_arc3 = FilledAngle(l4, l2, 1, color=ORANGE, quadrant=[1, -1], opacity=0.1)
        self.play(
            FadeIn(l1), FadeIn(l3), FadeIn(arc2),
            FadeTransform(l2, faded_l2), FadeTransform(l4, faded_l4), FadeTransform(arc3, faded_arc3)
        )
        self.wait(2)
        self.play(FadeIn(l2), FadeIn(l4), FadeIn(arc3))
        self.remove(PA, faded_l1, faded_l3, faded_arc2)
        self.remove(PC, faded_l2, faded_l4, faded_arc3)

        l1.add_updater(
            lambda x: x.become(Line(start=P.dot.points[0], end=B.dot.points[0], stroke_width=3))
        )
        l3.add_updater(
            lambda x: x.become(Line(start=B.dot.points[0], end=C.dot.points[0], stroke_width=3))
        )
        l4.add_updater(
            lambda x: x.become(Line(start=D.dot.points[0], end=A.dot.points[0], stroke_width=3))
        )

        arc.add_updater(lambda x: x.become(FilledAngle(l1, l2, 1, other_angle=True)))
        arc2.add_updater(lambda x: x.become(FilledAngle(l1, l3, 1, color=ORANGE, quadrant=[-1, 1])))
        arc3.add_updater(lambda x: x.become(FilledAngle(l4, l2, 1, color=ORANGE, quadrant=[1, -1])))

        self.play(
            Rotate(
                B.dot,
                angle=-0.5,
                about_point=ORIGIN
            ),
            Rotate(
                A.dot,
                angle=0.27,
                about_point=ORIGIN
            )
        )
        self.wait(2)
        self.play(
            Rotate(
                B.dot,
                angle=-0.5,
                about_point=ORIGIN
            ),
            Rotate(
                A.dot,
                angle=0.215,
                about_point=ORIGIN
            )
        )
        self.wait(2)
        self.play(
            Rotate(
                B.dot,
                angle=1,
                about_point=ORIGIN
            ),
            Rotate(
                A.dot,
                angle=-0.485,
                about_point=ORIGIN
            )
        )
        self.wait(5)

    def get_circle_points(self, x: float, circle: Circle):
        return [
            [x, self.get_circle_y_coordinates(x, circle)[0], 0],
            [x, self.get_circle_y_coordinates(x, circle)[1], 0]
        ]

    def get_circle_y_coordinates(self, x: float, circle: Circle):
        v = circle.arc_center
        a = 1
        b = -v[1]
        c = np.dot(v, v) + x*(x - 2*v[0]) - circle.radius**2
        discriminant = b**2 - c
        if discriminant < 0:
            return None
        coordinates = []
        coordinates += [-b - np.sqrt(discriminant)]
        coordinates += [-b + np.sqrt(discriminant)]
        return coordinates

    def circle_intersection(self, line: Line, circle: Circle):
        v = line.get_unit_vector()
        w = line.get_start()
        u = circle.get_center()
        a = np.dot(v, v)
        b = np.dot(v, w) - np.dot(v, u)
        c = np.dot(w, w) + np.dot(u, u) - 2*np.dot(u,w) - circle.radius**2
        discriminant = b**2 - a*c
        if (discriminant < 0):
            return -1
        t1 = (-b - np.sqrt(discriminant)) / a
        t2 = (-b + np.sqrt(discriminant)) / a
        return np.array([v * t1 + w, v * t2 + w])
