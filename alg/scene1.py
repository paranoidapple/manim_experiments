from manim import *


class Main(MovingCameraScene):

    def construct(self):
        expression = Tex(
            "$28y^3$", " $+$ ", "$16y^2$", " ", "$-21y$", " ", "$-12$"
        ).move_to(UP * 3 / 4)
        box = (
            VGroup(
                Square(side_length=1.25),
                Square(side_length=1.25),
                Square(side_length=1.25),
                Square(side_length=1.25),
            )
            .arrange_in_grid(2, 2, buff=0, flow_order="rd")
            .move_to(DOWN)
        )

        self.play(Create(expression))
        self.wait(1)
        self.play(Create(box))
        self.wait(1)

        for i in range(4):
            self.play(
                expression[i * 2].animate.move_to(box[i]),
            )

        self.remove(expression[1])
        self.play(FadeOut(expression[1]))

        expression = VGroup(expression[0], expression[2], expression[4], expression[6])

        # get gcd (28y^3, 16y^2)
        gcd1 = VGroup(expression[1]).copy()
        gcd0 = VGroup(expression[0]).copy()
        gcd_label = Tex("gcd")
        self.play(gcd1.animate.next_to(box[0], LEFT))
        self.play(gcd0.animate.next_to(gcd1, LEFT))
        self.play(FadeIn(gcd_label.next_to(gcd0, LEFT)))

        group = VGroup(gcd1, gcd0, gcd_label)
        aligned_group = Tex("$=$gcd($28y^3$, $16y^2$)").next_to(box[0], LEFT)
        self.play(ReplacementTransform(group, aligned_group))
        self.wait(1)

        gcd_result_1 = Tex("$4y^2$").next_to(box[0], LEFT)
        self.play(ReplacementTransform(aligned_group, gcd_result_1))
        self.wait(1)

        # get gcd (-21y, -12)
        gcd3 = VGroup(expression[3]).copy()
        gcd2 = VGroup(expression[2]).copy()
        gcd_label = Tex("gcd")
        self.play(gcd3.animate.next_to(box[2], LEFT))
        self.play(gcd2.animate.next_to(gcd3, LEFT))
        self.play(FadeIn(gcd_label.next_to(gcd2, LEFT)))

        group = VGroup(gcd3, gcd2, gcd_label)
        aligned_group = Tex("$=$gcd($-21y$, $-12$)").next_to(box[2], LEFT)
        self.play(ReplacementTransform(group, aligned_group))
        self.wait(1)

        gcd_result_2 = Tex("$-3$").next_to(box[2], LEFT)
        self.play(ReplacementTransform(aligned_group, gcd_result_2))
        self.wait(1)

        # get gcd (28y^3, -21y)
        gcd0 = VGroup(expression[0]).copy()
        gcd2 = VGroup(expression[2]).copy()
        gcd_label = Tex("gcd")
        self.play(gcd0.animate.next_to(box[0], UP))
        self.play(gcd2.animate.next_to(gcd0, UP))
        self.play(FadeIn(gcd_label.next_to(gcd2, UP)))

        group = VGroup(gcd0, gcd2, gcd_label)
        aligned_group = Tex("$=$gcd($28y^3$, $-21y$)").next_to(box[0], UP)
        self.play(ReplacementTransform(group, aligned_group))
        self.wait(1)

        gcd_result_3 = Tex("$7y$").next_to(box[0], UP)
        self.play(ReplacementTransform(aligned_group, gcd_result_3))
        self.wait(1)

        # get gcd (16y^2, -12)
        gcd1 = VGroup(expression[1]).copy()
        gcd3 = VGroup(expression[3]).copy()
        gcd_label = Tex("gcd")
        self.play(gcd1.animate.next_to(box[1], UP))
        self.play(gcd3.animate.next_to(gcd1, UP))
        self.play(FadeIn(gcd_label.next_to(gcd3, UP)))

        group = VGroup(gcd1, gcd3, gcd_label)
        aligned_group = Tex("$=$gcd($16y^2$, $-12$)").next_to(box[1], UP)
        self.play(
            ReplacementTransform(group, aligned_group),
            FadeOut(gcd_result_3),  # gcd result 3 blocks the aligned group
        )
        self.wait(1)

        gcd_result_4 = Tex("$4$").next_to(box[1], UP)
        self.play(
            ReplacementTransform(aligned_group, gcd_result_4), FadeIn(gcd_result_3)
        )
        self.wait(1)

        # make groups bordering box more cohesive
        plus_sign = Tex("+").next_to(gcd_result_4, LEFT)
        self.play(Create(plus_sign))

        term1_group = VGroup(gcd_result_3, plus_sign, gcd_result_4)
        term1 = Tex("$(7y+4)$").move_to(term1_group)

        self.play(
            ReplacementTransform(term1_group, term1),
            FadeOut(term1_group),
            term1.animate.move_to(UL),
        )

        term2_group = VGroup(gcd_result_1, gcd_result_2)
        term2 = Tex("$(4y^2-3)$").move_to(term2_group)

        self.play(
            ReplacementTransform(term2_group, term2),
            FadeOut(term2_group),
            term2.animate.move_to(UR),
        )
        self.wait()

        # combine 2 terms
        terms = VGroup(term1, term2)
        factored_term = Tex("$(7y+4)(4y^2-3)$").move_to(UP)

        self.play(
            ReplacementTransform(terms, factored_term),
        )

        to_del = [m for m in self.mobjects if m != factored_term]
        self.play(
            FadeOut(*to_del),
            self.camera.frame.animate.scale(0.5).move_to(factored_term),
        )
        self.wait(0.3)

        final_ans_box = Rectangle(color=YELLOW).surround(factored_term)
        self.play(FadeIn(final_ans_box))
        self.wait(1)
