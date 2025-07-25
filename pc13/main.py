from manim import *
from manim122lib import *

class PC13(Scene):
  def construct(self):
    mh = MinHeap([1,2,3,4,5,6,7])
    mh.move_to(ORIGIN)


    self.play(Write(mh))
    self.wait(1)

    mh.insert(self, 3)
    self.wait(1)
