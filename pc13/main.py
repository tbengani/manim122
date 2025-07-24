from manim import *
from manim122lib import *

class PC13(Scene):
  def construct(self):
    b1 = BinaryTreeNode(1)
    b1.shift(LEFT)

    b2 = BinaryTreeNode(2)
    b2.shift(RIGHT)

    self.play(Write(b1), Write(b2))
    self.wait(1)
    BinaryTreeNode.swap_positions(self, b1, b2)
    self.wait(1)
