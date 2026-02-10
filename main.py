from manim import *

class Cipher(Scene):
    def construct(self):
        # create outer ring cipher
        outer_ring = VGroup()
        inner_ring = VGroup()
        cipher = VGroup(outer_ring, inner_ring)
        outer_circle = Circle(radius=3.5, color=WHITE)
        middle_circle = Circle(radius=2.5, color=WHITE)
        inner_circle = Circle(radius=1.5, color=WHITE)
        outer_ring.add(outer_circle, middle_circle)
        inner_ring.add(inner_circle)

        for i in range(26):
            angle = i * (360 / 26)

            # outer ring intersections
            outer_line_intersection = Line(middle_circle.point_at_angle(angle * DEGREES), 
                                     outer_circle.point_at_angle(angle * DEGREES))
            outer_ring.add(outer_line_intersection)

            # inner ring intersections
            inner_line_intersection = Line(inner_circle.point_at_angle(angle * DEGREES), 
                                     middle_circle.point_at_angle(angle * DEGREES))
            inner_ring.add(inner_line_intersection)

        outer_letters = VGroup()
        inner_letters = VGroup()
        outer_letter_radius = Circle(radius=3)
        inner_letter_radius = Circle(radius=2)

        for i in range(26):
            angle = 90 - (i * (360 / 26))

            # outer ring letters
            outer_letter = Text(chr(65 + i), font_size=24)
            outer_letter.move_to(outer_letter_radius.point_at_angle(angle * DEGREES))
            outer_letter.rotate((angle - 90) * DEGREES)
            outer_letters.add(outer_letter)

            # inner ring letters
            inner_letter = Text(chr(65 + i), font_size=20)
            inner_letter.move_to(inner_letter_radius.point_at_angle(angle * DEGREES))
            inner_letter.rotate((angle - 90) * DEGREES)
            inner_letters.add(inner_letter)

        outer_ring.add(outer_letters)
        inner_ring.add(inner_letters)

        self.play(FadeIn(outer_ring), FadeIn(inner_ring))
        self.play(cipher.animate.scale(0.8))
        self.play(cipher.animate.shift(LEFT * 3))

        plaintext = "MESSAGE"
        key = "KEY"

        self.play(FadeIn(Text("Plaintext: " + plaintext, font_size=32).next_to(cipher, RIGHT * 3).shift(UP)),
                  FadeIn(Text("Key: " + key, font_size=32).next_to(cipher, RIGHT * 3)),
                  FadeIn(Text("Ciphertext: ", font_size=32).next_to(cipher, RIGHT * 3).shift(DOWN)))
        self.wait(2)

        plaintext_len = len(plaintext)
        key_len = len(key)
        plaintext_indices = [ord(char) - 65 for char in plaintext]
        key_indices = [ord(char) - 65 for char in key]

        # Only rotate the inner ring for the first character of the plaintext
        self.play(Rotate(inner_ring, key_indices[0] * (360 / 26) * DEGREES, run_time=2))

        for i in range(plaintext_len):
            curr_key_index = key_indices[i % key_len]
            next_key_index = key_indices[(i + 1) % key_len]

            dist = next_key_index - curr_key_index
            shift = dist

            if abs(dist) > 13:
                if dist > 0:
                    shift -= 26
                else:
                    shift += 26

            #self.play(Rotate(inner_ring, shift * (360 / 26) * DEGREES, run_time=2))








        
        
        