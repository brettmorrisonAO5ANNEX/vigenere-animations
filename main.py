from manim import *

class Cipher(Scene):
    def construct(self):
        plaintext = "MESSAGE"
        key = "KEY"
        ciphertext = ""
        key_len = len(key)
        plaintext_len = len(plaintext)
        plaintext_indices = [ord(char) - 65 for char in plaintext]
        key_indices = [ord(char) - 65 for char in key]

        self.camera.background_color = WHITE

        # create outer ring cipher
        outer_ring = VGroup()
        inner_ring = VGroup()
        cipher = VGroup(outer_ring, inner_ring)

        outer_circle = Circle(radius=3.5, color=BLACK)
        middle_circle = Circle(radius=2.5, color=BLACK)
        inner_circle = Circle(radius=1.5, color=BLACK)
        outer_ring.add(outer_circle, middle_circle)
        inner_ring.add(inner_circle)

        for i in range(26):
            angle = i * (360 / 26)

            # outer ring intersections
            outer_line_intersection = Line(middle_circle.point_at_angle(angle * DEGREES), 
                                     outer_circle.point_at_angle(angle * DEGREES), color=BLACK)
            outer_ring.add(outer_line_intersection)

            # inner ring intersections
            inner_line_intersection = Line(inner_circle.point_at_angle(angle * DEGREES), 
                                     middle_circle.point_at_angle(angle * DEGREES), color=BLACK)
            inner_ring.add(inner_line_intersection)

        outer_letters = VGroup()
        inner_letters = VGroup()
        outer_letter_radius = Circle(radius=3)
        inner_letter_radius = Circle(radius=2)

        for i in range(26):
            angle = 90 - (i * (360 / 26))

            # outer ring letters
            outer_letter = Text(chr(65 + i), font_size=24, color=BLACK)

            outer_letter.move_to(outer_letter_radius.point_at_angle(angle * DEGREES))
            outer_letter.rotate((angle - 90) * DEGREES)
            outer_letters.add(outer_letter)

            # inner ring letters
            inner_letter = Text(chr(65 + i), font_size=20, color=BLACK)
            inner_letter.move_to(inner_letter_radius.point_at_angle(angle * DEGREES))
            inner_letter.rotate((angle - 90) * DEGREES)
            inner_letters.add(inner_letter)

        outer_ring.add(outer_letters)
        inner_ring.add(inner_letters)

        outer_dots = VGroup()
        inner_dots = VGroup()
        outer_dot_radius = Circle(radius=3.75)
        inner_dot_radius = Circle(radius=1.25)

        outer_dots.add(Triangle(color=BLACK).set_fill(RED, opacity=1).scale(0.16).rotate(60 * DEGREES).move_to(outer_dot_radius.point_at_angle(90 * DEGREES)))

        for i in range(key_len):
            new_dot = Dot(color=WHITE).move_to(inner_dot_radius.point_at_angle(
                (90 - (key_indices[i] * (360 / 26))) * DEGREES))
            inner_dots.add(new_dot)
        outer_ring.add(outer_dots)
        inner_ring.add(inner_dots)

        self.play(FadeIn(outer_ring), FadeIn(inner_ring))
        self.play(cipher.animate.scale(0.8))
        self.play(cipher.animate.shift(LEFT * 3))
        self.play(*[inner_dots[i].animate.set_color(BLUE) for i in range(key_len)], run_time=2) 

        message_box = VGroup()
        key_box = VGroup()
        ciphertext_box = VGroup()

        message_box.add(Square(side_length=0.75).set_stroke(BLACK, width=3))
        key_box.add(Square(side_length=0.75).set_stroke(BLACK, width=3))
        ciphertext_box.add(Square(side_length=0.75).set_stroke(BLACK, width=3)) 

        for i in range(len(plaintext) - 1):
            new_message_square = Square(side_length=0.75).set_stroke(BLACK, width=3).next_to(message_box, RIGHT, buff=0)
            message_box.add(new_message_square)

            if (i < key_len - 1):
                new_key_square = Square(side_length=0.75).set_stroke(BLACK, width=3).next_to(key_box, RIGHT, buff=0)
                key_box.add(new_key_square)

            new_ciphertext_square = Square(side_length=0.75).set_stroke(BLACK, width=3).next_to(ciphertext_box, RIGHT, buff=0)
            ciphertext_box.add(new_ciphertext_square)

        message_box.next_to(cipher, RIGHT * 3).shift(UP)
        key_box.next_to(cipher, RIGHT * 3)
        ciphertext_box.next_to(cipher, RIGHT * 3).shift(DOWN)

        message_group = VGroup()
        key_group = VGroup()
        ciphertext_group = VGroup()

        for i in range(plaintext_len):
            message_char = Text(plaintext[i], font_size=24, color=BLACK).move_to(message_box[i].get_center())
            message_group.add(message_char)

            if (i < key_len):
                key_char = Text(key[i], font_size=24, color=BLACK).move_to(key_box[i].get_center())
                key_group.add(key_char)

        self.play(FadeIn(message_group), FadeIn(key_group),
                  FadeIn(message_box), FadeIn(key_box), FadeIn(ciphertext_box))

        # Only rotate the inner ring for the first character of the plaintext
        self.play(Rotate(inner_ring, key_indices[0] * (360 / 26) * DEGREES, run_time=2))

        for i in range(plaintext_len):
            curr_plaintext_index = plaintext_indices[i]
            curr_key_index = key_indices[i % key_len]
            next_key_index = key_indices[(i + 1) % key_len]

            dist = next_key_index - curr_key_index
            shift = dist

            if abs(dist) > 13:
                if dist > 0:
                    shift -= 26
                else:
                    shift += 26

            cipher_index = (curr_key_index + curr_plaintext_index) % 26

            self.play(outer_letters[curr_plaintext_index].animate.scale(1.8), 
                      inner_letters[cipher_index].animate.set_color(RED).scale(1.8),
                      message_box[i].animate.set_fill(RED, opacity=0.5),
                      key_box[i % key_len].animate.set_fill(BLUE, opacity=0.5),
                      ciphertext_box[i].animate.set_fill(RED, opacity=0.5), run_time=0.25)

            cipher_char = chr(cipher_index + 65)
            ciphertext += cipher_char
            ciphertext_group.add(Text(cipher_char, font_size=24, color=RED).move_to(ciphertext_box[i].get_center()))    
            self.play(FadeIn(ciphertext_group[i]))

            self.play(outer_letters[curr_plaintext_index].animate.scale(1/1.8), 
                      inner_letters[cipher_index].animate.set_color(BLACK).scale(1/1.8), 
                      message_box[i].animate.set_fill(WHITE, opacity=0),
                      key_box[i % key_len].animate.set_fill(WHITE, opacity=0),
                      ciphertext_box[i].animate.set_fill(WHITE, opacity=0), run_time=0.25)

            if (i < plaintext_len - 1):
                self.play(Rotate(inner_ring, shift * (360 / 26) * DEGREES, run_time=2))

        offset = key_indices[(plaintext_len - 1) % key_len]
        self.play(Rotate(inner_ring, -offset * (360 / 26) * DEGREES, run_time=2))
        self.wait(1)


        #decrypting the message
        decrypted_group = VGroup()

        ciphertext_indices = [ord(char) - 65 for char in ciphertext]
        self.play(FadeOut(message_group),
                  ciphertext_group.animate.move_to(message_group.get_center()))
        self.play(*[ciphertext_group[i].animate.set_color(BLACK) for i in range(len(ciphertext))])
        
        # Only rotate the inner ring for the first character of the plaintext
        self.play(Rotate(inner_ring, key_indices[0] * (360 / 26) * DEGREES, run_time=2))

        for i in range(len(ciphertext)):
            curr_ciphertext_index = ciphertext_indices[i]
            curr_key_index = key_indices[i % key_len]
            next_key_index = key_indices[(i + 1) % key_len]

            dist = next_key_index - curr_key_index
            shift = dist

            if abs(dist) > 13:
                if dist > 0:
                    shift -= 26
                else:
                    shift += 26

            plaintext_index = (curr_ciphertext_index - curr_key_index) % 26

            self.play(outer_letters[plaintext_index].animate.set_color(BLUE).scale(1.8), 
                      inner_letters[(plaintext_index + curr_key_index) % 26].animate.scale(1.8),
                      message_box[i].animate.set_fill(BLUE, opacity=0.5),
                      key_box[i % key_len].animate.set_fill(RED, opacity=0.5),
                      ciphertext_box[i].animate.set_fill(BLUE, opacity=0.5), run_time=0.25)

            plaintext_char = chr(plaintext_index + 65)
            decrypted_group.add(Text(plaintext_char, font_size=24, color=BLUE).move_to(ciphertext_box[i].get_center()))    
            self.play(FadeIn(decrypted_group[i]))

            self.play(outer_letters[plaintext_index].animate.set_color(BLACK).scale(1/1.8), 
                      inner_letters[(plaintext_index + curr_key_index) % 26].animate.scale(1/1.8), 
                      message_box[i].animate.set_fill(WHITE, opacity=0),
                      key_box[i % key_len].animate.set_fill(WHITE, opacity=0),
                      ciphertext_box[i].animate.set_fill(WHITE, opacity=0), run_time=0.25)

            if (i < plaintext_len - 1):
                self.play(Rotate(inner_ring, shift * (360 / 26) * DEGREES, run_time=2))

        offset = key_indices[(plaintext_len - 1) % key_len]
        self.play(Rotate(inner_ring, -offset * (360 / 26) * DEGREES, run_time=2))
        self.wait(1)








        
        
        