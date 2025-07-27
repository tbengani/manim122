from manim import *
from manim122lib import *


class PC13(Scene):
  def construct(self):
    title = Text("Building a Min-Heap", font_size=40).to_edge(UP)
    self.play(Write(title))

    custom_config = BinaryTreeConfig(
        initial_create_duration=0.1, initial_edge_duration=0.1,
        initial_heapify_swap_duration=0.1, initial_reposition_duration=0.1,
        insert_create_duration=0.8, insert_edge_duration=0.6,
        insert_heapify_swap_duration=1.0, insert_reposition_duration=1.0,
        highlight_duration=0.3,
    )

    initial_data = [25, 10, 17, 4, 8]
    heap = MinHeap(data=initial_data, scene=self, top_pos=UP * 1.5, cfg=custom_config)
    self.wait(1)

    add_title = Text("Adding element: 6", font_size=32).next_to(title, DOWN, buff=0.5)
    self.play(Write(add_title))
    heap.add_node(6, self)
    heap.add_node(5, self)
    self.wait(1)
    self.play(FadeOut(add_title))

    highlight_title = Text("Highlighting node at index 3 (Default)", font_size=32).next_to(title, DOWN, buff=0.5)
    self.play(Write(highlight_title))
    heap.highlight_node(3, self)
    self.wait(1.5)
    heap.unhighlight_node(3, self)
    self.wait(1)
    self.play(FadeOut(highlight_title))

    # --- Part 4: Demonstrate Custom Highlighting ---
    custom_highlight_title = Text("Custom Highlighting (index 5)", font_size=32).next_to(title, DOWN, buff=0.5)
    self.play(Write(custom_highlight_title))
    # After all insertions, the node at index 5 holds the value 10
    heap.highlight_node(
        5, self,
        stroke_color=GREEN_C,
        stroke_width=6,
        fill_color=YELLOW_E,
        text_color=BLACK
    )
    self.wait(2)
    heap.unhighlight_node(5, self)
    self.wait(1)
    self.play(FadeOut(custom_highlight_title))

    self.wait(2)
