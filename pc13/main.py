from manim import *
from manim122lib import *

class PC13(Scene):
  def construct(self):
    # --- Part 1: Initialize the heap with animation ---
    title = Text("Building a Min-Heap", font_size=40).to_edge(UP)
    self.play(Write(title))

    # Pass the scene to the constructor to enable animations
    initial_data = [25, 10, 17, 4, 8]
    heap = MinHeap(data=initial_data, scene=self, top_pos=UP * 2)
    self.add(heap) # Add the heap VGroup to the scene

    self.wait(1)

    # --- Part 2: Add a new node with animation ---
    subtitle = Text("Adding a new element: 3", font_size=32).next_to(title, DOWN, buff=0.5)
    self.play(Write(subtitle))

    # Use the public `add_node` method for animated insertion
    heap.add_node(3, self)

    self.wait(2)
