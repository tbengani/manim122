from manim import *
import os

class Chonk(ImageMobject):
  def __init__(self, scale=0.25):
    base_path = os.path.dirname(__file__)
    chonk_path = os.path.abspath(os.path.join(base_path, "..", "assets", "chonk.png"))
    super().__init__(chonk_path)
    self.scale(scale)

  def spin(self, scene : Scene, spins = 1, duration = 0.5, ratefunc=None):
    if ratefunc is None:
      ratefunc=linear
    return Rotate(self, angle=spins*2*PI, runtime=duration, ratefunc=ratefunc)
