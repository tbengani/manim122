from manim import *
from manim122lib import *

class PC13(Scene):
  def construct(self):
    title = Text("Min-Heaps", font="JetBrains Mono").to_edge(UP)
    self.play(Write(title))

    # 1. Create a custom configuration object
    custom_cfg = BinaryTreeConfig(
        node_radius=0.3,
        font_size = 18,
        h_spacing=1,
        level_height=1,

        array_font_size=18,
        array_empty_stroke_color=DARK_GRAY,
    )

    # 2. Pass the custom config to the MinHeap
    # The array will now be correctly centered at 'array_pos'.
    heap = MinHeap(
        data=[25, 10, 17, 4, 8, 12, 13],
        limit=12, # The array will have 11 cells (0-10)
        scene=self,
        cfg=custom_cfg,
        top_pos=UP * 2,
        array_pos=DOWN * 2.5
    )
    self.wait()

    # Adding a node works the same way
    heap.add_node(6, self)
    self.wait(1)
    heap.add_node(3, self)


    self.wait(2)
