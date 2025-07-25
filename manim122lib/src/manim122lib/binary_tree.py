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
    def __init__(self, scene : Scene = None, data : int = 0, left: "BinaryTreeNode" =None , right: "BinaryTreeNode" =None , cfg : BinaryTreeConfig = default_config):
        super().__init__()

        if scene is None:
          raise ValueError("Please pass in the scene to BinaryTreeNode")
        self.scene = scene

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
    def swap_with(node: "BinaryTreeNode", duration=0.5):
      pos_a = self.get_center()
      pos_b = node.get_center()

      self.scene.play(
          self.animate.move_to(pos_b),
          node.animate.move_to(pos_a),
          run_time=duration
      )


    def __repr__(self):
        return f"BinaryTreeNode({self.data})"

class MinHeap(VGroup):
  def __init__(self, scene : Scene = None, data: Union[np.ndarray, list[int], list[BinaryTreeNode]] = None, limit: int = 15, cfg : BinaryTreeConfig = default_config):
    super().__init__()

    if scene is None:
      raise ValueError("Please pass in the scene to MinHeap")
    self.scene = scene

    if data is None:
      data = []
    if isinstance(data, np.ndarray):
      data = data.tolist()

    self.nodes = [] # internal representation of nodes
    self.limit = limit # max number of nodes
    self.len = 0 # current number of nodes
    self.max_levels = int(np.floor(np.log2(limit))) + 1

    self.cfg = cfg

    for value in data:
      self._add_node(value)

  def _add_node(self, value: int):
    self.len += 1
    if (self.len > self.limit):
      raise ValueError("Too many nodes in MinHeap (limit={self.limit}, current={self.len})")
    node = BinaryTreeNode(value, cfg=self.cfg)
    self.nodes.append(node)
    self.add(node)

  def __repr__(self):
    return f"MinHeap({[str(node) for node in self.nodes]})"
