from manim import *

class Test(Scene):
    def construct(self):
        self.camera.background_color = WHITE

        triangle = Triangle(color=BLACK).set_fill(RED, opacity=1).scale(0.5)
        self.play(FadeIn(triangle))
        