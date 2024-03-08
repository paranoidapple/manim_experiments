from manim import *
from numpy import array


class Main(MovingCameraScene):
    def construct(self):

        # Setup problem
        circle = Circle(radius=2, color=PINK)

        line1 = TangentLine(circle, alpha=0.16, length=6.2, color=GREY_A)
        line2 = TangentLine(circle, alpha=0.84, length=6.2, color=GREY_A)

        dotA = Dot(circle.point_from_proportion(0.16))
        dotB = Dot(circle.point_from_proportion(0.84))
        dotC = Dot(circle.point_from_proportion(0.4))
        dotP = Dot(
            line_intersection([line1.start, line1.end], [line2.start, line2.end])
        )

        textA = Tex("A").next_to(dotA, UR / 3)
        textB = Tex("B").next_to(dotB, DR / 3)
        textC = Tex("C").next_to(dotC, (UL + LEFT) / 4)
        textP = Tex("P").next_to(dotP, RIGHT / 2)

        # Construct arcs
        arcY = Arc(
            start_angle=0.16 * TAU,
            angle=-0.32 * TAU,
            radius=2,
            arc_center=circle.get_center(),
            color=RED_A,
        )

        arcX = Arc(
            start_angle=0.84 * TAU,
            angle=-0.68 * TAU,
            radius=2,
            arc_center=circle.get_center(),
            color=RED_E,
        )

        # Construct angle
        angle1 = Angle(line1, line2, quadrant=array([1, -1]), color=BLUE_C)
        angle1text = Tex("1", font_size=30, color=BLUE_C).next_to(angle1, LEFT / 2)

        # Problem text
        problem_text = Tex(
            "Prove ",
            r"$m\angle{1}$",
            " $=$ ",
            r"$\dfrac{1}{2}$",
            r"$m\overset{\frown}{ACB}$",
            " $-$ ",
            r"$m{\overset{\frown}{AB}}$",
        ).to_corner()

        # Create everything
        self.wait()

        self.play(Create(circle))
        self.wait(0.3)
        self.play(
            Create(line1),
            Create(dotA),
            Create(textA),
        ),
        self.wait(0.3)
        self.play(
            Create(line2),
            Create(dotB),
            Create(textB),
            Create(dotP),
            Create(textP),
            Create(dotC),
            Create(textC),
        )
        self.add_foreground_mobjects(dotA, dotB, dotP)
        self.play(Create(problem_text))
        self.wait()

        self.play(
            Create(arcY),
            Create(arcX),
            problem_text[4].animate.set_color(RED_E),
            problem_text[6].animate.set_color(RED_A),
            Create(angle1),
            Create(angle1text),
            problem_text[1].animate.set_color(BLUE_C),
        )
        self.add_foreground_mobjects(dotC)
        self.wait(2)

        # Reset all colors
        self.play(
            FadeToColor(arcX, GREY_A),
            FadeToColor(arcY, GREY_A),
            FadeToColor(angle1, GREY_A),
            FadeToColor(angle1text, WHITE),
            FadeToColor(problem_text, WHITE),
        )

        # Step 1: draw aux AB (text)
        step1 = (Tex("1) Draw auxiliary ", r"$\overline{AB}$")).to_corner()

        details1 = Tex(
            "AUX | through any 2 points there is exactly one line",
            font_size=30,
            tex_environment="flushleft",
        ).to_corner(UL)

        # Replace problem text with Step 1
        self.play(
            FadeOut(problem_text), FadeIn(step1), step1[1].animate.set_color(YELLOW_D)
        )
        self.wait(0.3)

        # Draw AUX on animation
        aux = Line(dotA.get_center(), dotB.get_center(), color=YELLOW_D)
        self.play(Create(aux), Create(details1))
        self.wait(3)

        # Fade Step 1 mobjects to white
        self.play(FadeToColor(aux, WHITE), FadeToColor(step1, WHITE))

        # Step 2: Exterior angles (text)

        # TODO: animate the exterior angle, and then the 2 remote ints

        step2 = Tex(
            "2) ", r"$m\angle{1}$", " $+$ ", r"$m\angle{2}$", " $=$ ", r"$m\angle{3}$"
        ).to_corner()

        details2 = Tex(
            r"the measure of an exterior angle of a triangle = the sum of the measures of the 2 remote interior angles",
            tex_environment="flushleft",
            font_size=30,
        ).to_corner(UL)

        # Replace Step 1 with Step 2
        self.play(
            FadeOut(details1),
            FadeIn(details2),
            FadeOut(step1),
            FadeIn(step2),
        )
        self.wait(0.3)

        # Construct exterior angle
        angle3 = Angle(
            line2, aux, quadrant=array([-1, -1]), other_angle=True, color=ORANGE
        )
        angle3text = Tex("3", color=ORANGE).next_to(angle3, LEFT / 2)

        angle2 = Angle(
            line1, aux, quadrant=array([-1, 1]), other_angle=True, color=YELLOW_D
        )
        angle2text = Tex("2", color=YELLOW_D).next_to(angle2, (DR + LEFT * 1 / 2) / 2)

        group1 = VGroup(angle1, angle1text)

        self.play(
            Create(angle3),
            Create(angle3text),
            Create(angle2),
            Create(angle2text),
            step2[1].animate.set_color(YELLOW_D),
            step2[5].animate.set_color(ORANGE),
            # fmt: skip
            group1.animate.scale(
                1.6,
                about_point=line_intersection(
                    group1[0].lines[0].get_start_and_end(),
                    group1[0].lines[1].get_start_and_end(),
                ),
            ).fade_to(YELLOW_D, 1),
            step2[3].animate.set_color(YELLOW_D),
        )
        self.wait(2)

        # Fade Step 2's new diagram mobjects
        group2 = VGroup(angle2, angle2text)
        group3 = VGroup(angle3, angle3text)

        for group in (group1, group2, group3):
            self.play(
                group.animate.scale(
                    0.625,
                    about_point=line_intersection(
                        group[0].lines[0].get_start_and_end(),
                        group[0].lines[1].get_start_and_end(),
                    ),
                ).fade_to(WHITE, 1),
            )
        self.play(step2.animate.set_color(WHITE))
        self.wait()

        self.camera.frame.save_state()
        # Zoom in on equation
        temp_del = [m for m in self.mobjects if m is not step2]
        self.play(
            FadeOut(*temp_del),
            self.camera.frame.animate.scale(0.75).move_to(step2),
        )
        self.remove(*temp_del)

        # Edit equation
        step3 = Tex(
            "3) ", r"$m\angle{1}$", " $=$ ", r"$m\angle{3}$", " $-$ ", r"$m\angle{2}$"
        ).to_corner()

        details3 = Tex(
            "subtraction property of equality",
            tex_environment="flushleft",
            font_size=30,
        ).next_to(step3, DOWN / 2)

        self.play(TransformMatchingTex(step2, step3), Create(details3))
        self.wait(2)

        # Fade in all the temporarily deleted mobjects and move the camera back to normal
        self.play(
            FadeIn(*temp_del),
            FadeOut(details2),
            self.camera.frame.animate.scale(4 / 3).move_to(ORIGIN),
        )
        self.remove(details2)

        # Step 4: chord & tangent (text)
        step4 = Tex(
            "4) ",
            r"m$\angle{3}$",
            " $=$ ",
            r"$\dfrac{1}{2}$",
            r"$m\overset{\frown}{ACB}$",
        ).to_corner()

        details4 = Tex(
            "the measure of an angle formed by a chord and a tangent equals half the measures of the intercepted arc",
            tex_environment="flushleft",
            font_size=30,
        ).to_corner(UL)

        # Replace Step 3 with Step 4
        self.play(
            FadeOut(step3),
            FadeIn(step4),
            FadeOut(details3),
            FadeIn(details4),
        )
        self.play(
            step4[1].animate.set_color(YELLOW_D),
            step4[4].animate.set_color(ORANGE),
        )
        self.wait(0.3)

        # Highlight line segments & angles
        temp_segment = Line(dotB.get_center(), line2.get_start(), color=YELLOW_D)
        self.add_foreground_mobject(temp_segment)

        self.play(
            Create(temp_segment),
            FadeToColor(arcX, ORANGE),
            FadeToColor(aux, YELLOW_D),
            group3.animate.scale(
                1.6,
                about_point=line_intersection(
                    line2.get_start_and_end(),
                    aux.get_start_and_end(),
                ),
            ).fade_to(YELLOW_D, 1),
        )

        self.wait(2)

        # Fade colors back to normal
        self.play(
            FadeToColor(arcX, WHITE),
            FadeToColor(temp_segment, WHITE),
            FadeToColor(aux, WHITE),
            FadeToColor(step4, WHITE),
            group3.animate.scale(
                0.625,
                about_point=line_intersection(
                    line2.get_start_and_end(),
                    aux.get_start_and_end(),
                ),
            ).fade_to(WHITE, 1),
        )

        # Change temp segment
        self.remove(temp_segment)

        temp_segment = Line(dotA.get_center(), dotP.get_center(), color=YELLOW_D)

        # Step 5: Step 4, but with another angle (text)
        step5 = Tex(
            "5) ",
            r"$m\angle{2}$",
            " $=$ ",
            r"$\dfrac{1}{2}$",
            r"$m\overset{\frown}{AB}$",
        ).to_corner()
        details5 = details4

        # Replace Step 4 with Step 5
        self.play(
            FadeOut(step4),
            FadeIn(step5),
            FadeIn(details5),
        )
        self.play(
            step5[1].animate.set_color(YELLOW_D),
            step5[4].animate.set_color(ORANGE),
        )

        # Add / recolor Step 5 elements
        self.play(
            Create(temp_segment),
            FadeToColor(arcY, ORANGE),
            FadeToColor(aux, YELLOW_D),
            group2.animate.scale(
                1.6,
                about_point=line_intersection(
                    line1.get_start_and_end(),
                    aux.get_start_and_end(),
                ),
            ).fade_to(YELLOW_D, 1),
        )
        self.add_foreground_mobject(temp_segment)

        self.wait(2)

        # Fade colors back to normal
        self.play(
            FadeToColor(arcY, WHITE),
            FadeToColor(temp_segment, WHITE),
            FadeToColor(aux, WHITE),
            FadeToColor(step5, WHITE),
            group2.animate.scale(
                0.625,
                about_point=line_intersection(
                    line1.get_start_and_end(),
                    aux.get_start_and_end(),
                ),
            ).fade_to(WHITE, 1),
        )

        self.wait(1)

        # Zoom in on equation
        temp_del = [m for m in self.mobjects if m is not step5]
        self.play(
            FadeOut(*temp_del),
            self.camera.frame.animate.scale(2).move_to(step5),
        )
        self.remove(*temp_del)

        # Step 6: Substitute
        self.play(
            Create(step4.next_to(step5, DOWN)),
            Create(step3.next_to(step4, DOWN * 4 / 3)),
        )

        # FIRST SUBSTITUTION (Step 3, Step 4)
        final_equation = VGroup(*[step3[i] for i in range(len(step3.submobjects))])

        to_move = VGroup(step4[3], step4[4])  # [1/2 measure of arc ACB]
        destination = step3[3]  # [measure of angle 3]
        final_equation.remove(destination)

        # Highlight equal variables
        self.play(
            step4[1].animate.set_color(YELLOW_D),
            destination.animate.set_color(YELLOW_D),
        )
        self.wait(0.3)

        self.play(
            step4[1].animate.set_color(WHITE), to_move.animate.set_color(YELLOW_D)
        )
        self.wait(0.3)

        # Make dummies for movement
        dummy1 = to_move.copy()
        dummy2 = dummy1.copy().move_to(destination, aligned_edge=LEFT)

        self.play(
            FadeOut(destination),  # Fade out [measure of angle 3] in Step 3
            ReplacementTransform(
                dummy1, dummy2
            ),  # Animate moving [1/2 measure of arc ACB] from Step 4 to Step 3
            VGroup(*step3[4:]).animate.next_to(
                dummy2, RIGHT
            ),  # Move everything after the transformation
        )
        final_equation.insert(3, dummy2)

        self.wait(0.3)

        # Fade colors back to normal
        self.play(
            to_move.animate.set_color(WHITE),
            dummy2.animate.set_color(WHITE),
        )

        # SECOND SUBSTITUTION (Step 5, Step 3)

        to_move = VGroup(step5[3], step5[4])  # [1/2 measure of arc AB]
        destination = step3[5]  # [measure of angle 2]
        final_equation.remove(destination)

        # Highlight equal variables
        self.play(
            step5[1].animate.set_color(YELLOW_D),
            destination.animate.set_color(YELLOW_D),
        )
        self.wait(0.3)

        self.play(
            step5[1].animate.set_color(WHITE), to_move.animate.set_color(YELLOW_D)
        )
        self.wait(0.3)

        # Make dummies for movement
        dummy1 = to_move.copy()
        dummy2 = dummy1.copy().move_to(destination, aligned_edge=LEFT)
        final_equation.insert(6, dummy2)

        self.play(
            FadeOut(destination),  # Fade out [measure of angle 2] in Step 3
            ReplacementTransform(
                dummy1, dummy2
            ),  # Animate moving [1/2 measure of arc AB] from Step 5 to Step 3
        )

        self.wait(0.3)

        # Fade colors back to normal
        self.play(
            to_move.animate.set_color(WHITE),
            dummy2.animate.set_color(WHITE),
        )

        # Change step number from 3 to 6
        destination = step3[0]
        step6_label = Tex("6) ").move_to(destination)
        self.play(ReplacementTransform(destination, step6_label))
        final_equation.remove(destination)

        final_equation.insert(0, step6_label)
        self.wait(1)

        self.play(Uncreate(step4), Uncreate(step5))

        # Focus on equation, draw in diagram
        # fmt: off
        diag = VGroup(
            dotA, dotB, dotP, dotC,
            textA, textB, textP, textC,
            circle, arcX, arcY,
            line1, line2, aux,
            angle1, angle1text,
        ).move_to((DOWN * 3/2) + (RIGHT * 1/2))
        # fmt: on

        rect = SurroundingRectangle(final_equation, color=YELLOW_D, buff=0.25)

        self.play(
            FadeIn(rect),
            Restore(self.camera.frame),
            VGroup(final_equation, rect).animate.move_to(UP * 5 / 2),
        )

        # Recolor equation and diagram
        self.play(
            FadeIn(diag),
            group1.animate.set_color(BLUE_C),
            final_equation[1].animate.set_color(BLUE_C),
            arcX.animate.set_color(RED_E),
            final_equation[3][1].animate.set_color(RED_E),
            arcY.animate.set_color(RED_A),
            final_equation[5][1].animate.set_color(RED_A),
        )
        self.wait(2)
