from manim import *
from manim122lib import BinaryTreeNode

class TestScene(Scene):
  def construct(self):
    t = Text("Manim is working!")

    self.play(Write(t))

    self.wait(3)
