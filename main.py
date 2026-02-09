from manim import *

class Cipher(Scene):
    def construct(self):
        # create outer ring cipher
        outer_ring = VGroup()
        outer_circle = Circle(radius=3.5, color=WHITE)
        middle_circle = Circle(radius=2.5, color=WHITE)
        outer_ring.add(outer_circle, middle_circle)

        for i in range(26):
            angle = i * (360 / 26)
            line_intersection = Line(middle_circle.point_at_angle(angle * DEGREES), 
                                     outer_circle.point_at_angle(angle * DEGREES))
            outer_ring.add(line_intersection)

        outer_letters = VGroup()
        outer_letter_radius = Circle(radius=3)
        for i in range(26):
            angle = 90 - (i * (360 / 26))
            letter = Text(chr(65 + i), font_size=24)
            letter.move_to(outer_letter_radius.point_at_angle(angle * DEGREES))
            letter.rotate((angle - 90) * DEGREES)
            outer_letters.add(letter)
        outer_ring.add(outer_letters)

        # create inner ring cipher
        inner_ring = VGroup()
        inner_circle = Circle(radius=1.5, color=WHITE)
        inner_ring.add(inner_circle)

        for i in range(26):
            angle = i * (360 / 26)
            line_intersection = Line(inner_circle.point_at_angle(angle * DEGREES), 
                                     middle_circle.point_at_angle(angle * DEGREES))
            inner_ring.add(line_intersection)

        inner_letters = VGroup()
        inner_letter_radius = Circle(radius=2)
        for i in range(26):
            angle = 90 - (i * (360 / 26))
            letter = Text(chr(65 + i), font_size=20)
            letter.move_to(inner_letter_radius.point_at_angle(angle * DEGREES))
            letter.rotate((angle - 90) * DEGREES)
            inner_letters.add(letter)
        inner_ring.add(inner_letters)

        self.play(FadeIn(outer_ring), FadeIn(inner_ring))
        self.wait(2)
        self.play(Rotate(inner_ring, (-3 * (360 / 26)) * DEGREES), run_time=2)




        
        
        