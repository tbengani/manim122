from manim import *
from manim122lib import *

class PC13(Scene):
  def construct(self):
    b = BinaryTreeNode(1)

    self.add(Text("PC13"))
    self.play(Write(b))
    self.wait(3)
