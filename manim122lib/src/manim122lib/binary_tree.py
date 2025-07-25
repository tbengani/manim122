from manim import *
from typing import Union
from dataclasses import dataclass

@dataclass
class BinaryTreeConfig:
    node_padding: float = 0.1  # Extra padding between label and node
    text_color: str = BLACK  # Node text and stroke color, and border color
    fill_color: str = WHITE
    font: str = "JetBrains Mono"
    node_radius: float = 0.4
    font_size: float = 24
    h_spacing: float = 1.5  # Horizontal spacing between nodes at the deepest level
    level_height: float = 1.5  # Vertical distance between levels


default_config = BinaryTreeConfig()

class BinaryTreeNode(VGroup):
    def __init__(self, data : int = 0, left: "BinaryTreeNode" =None , right: "BinaryTreeNode" =None , cfg : BinaryTreeConfig = default_config):
        super().__init__()
        self.data = data
        self.left = left
        self.right = right
        self.uid = id(self)

        # Create label and node visuals
        label = Text(str(data), color=cfg.text_color, font=cfg.font, font_size=cfg.font_size)
        fake_node = LabeledDot(label, fill_color=cfg.fill_color, radius=cfg.node_radius)
        node = LabeledDot(label, fill_color=cfg.fill_color, radius=fake_node[0].get_radius() + cfg.node_padding)
        node[0].set_stroke(color=cfg.text_color, width=2)
        node[1].set_stroke(opacity=0)

        self.add(node)  # this makes BinaryTreeNode a full Mobject

    @staticmethod
    def swap_positions(scene: Scene, node_a: "BinaryTreeNode", node_b: "BinaryTreeNode", duration=0.5):
      pos_a = node_a.get_center()
      pos_b = node_b.get_center()

      scene.play(
          node_a.animate.move_to(pos_b),
          node_b.animate.move_to(pos_a),
          run_time=duration
      )


    def __repr__(self):
        return f"BinaryTreeNode({self.data})"

class MinHeap(VGroup):
  def __init__(self, data: Union[np.ndarray, list[int]] = None, limit: int = 4, cfg : BinaryTreeConfig = default_config):
    super().__init__()
    if data is None:
      data = []
    if isinstance(data, np.ndarray):
      data = data.tolist()

    self.nodes = []
    self.limit = limit
    self.cfg = cfg

    for value in data:
      self._add_node(value)

    self._arrange_heap()

  def _add_node(self, value: int):
    node = BinaryTreeNode(value, cfg=self.cfg)
    self.nodes.append(node)
    self.add(node)

  def _arrange_heap(self):
    self.submobjects.clear()
    positions = {}
    edges = VGroup()

    def layout(index: int, depth: int, x_min: float, x_max: float):
      if index >= len(self.nodes):
        return
      x = (x_min + x_max) / 2
      y = -depth * self.cfg.level_height
      positions[index] = np.array([x, y, 0])

      left_idx = 2 * index + 1
      right_idx = 2 * index + 2

      # Recurse into children with subdivided ranges
      layout(left_idx, depth + 1, x_min, x)
      layout(right_idx, depth + 1, x, x_max)

    # Use spacing to set total horizontal width based on tree depth
    max_width = (2 ** (self.limit - 1)) * self.cfg.h_spacing
    layout(0, 0, -max_width / 2, max_width / 2)

    for i, node in enumerate(self.nodes):
      node.move_to(positions[i])
      if i != 0:
        parent_idx = (i - 1) // 2
        edge = Line(positions[parent_idx], positions[i], color=GRAY)
        edges.add(edge)

    self.add(edges, *self.nodes)

  def __repr__(self):
    return f"Heap({[n.data for n in self.nodes]})"

  def insert(self, scene: Scene, value: int, duration: float = 0.5):
    """Insert value into the heap visually."""
    center = self.get_center()
    self._add_node(value)
    self._arrange_heap()

    self.move_to(center)
    scene.wait(duration)
