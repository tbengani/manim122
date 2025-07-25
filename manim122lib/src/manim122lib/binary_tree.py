from manim import *
from typing import Union
from dataclasses import dataclass
from contextlib import contextmanager

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

  def swap_with(self, scene : Scene, other_node : "BinaryTreeNode" , duration : float=0.5):
    pos_a = self.get_center()
    pos_b = other_node.get_center()

    scene.play(
      self.animate.move_to(pos_b),
      other_node.animate.move_to(pos_a),
      run_time=duration
    )

  def __repr__(self):
    return f"BinaryTreeNode({self.data})"

class MinHeap(VGroup):
  def __init__(self, data: Union[np.ndarray, list[int], list[BinaryTreeNode]] = None, limit: int = 15, cfg : BinaryTreeConfig = default_config):
    super().__init__()

    if data is None:
      data = []
    if isinstance(data, np.ndarray):
      data = data.tolist()

    self.nodes = [None,] # internal representation of nodes
    self.limit = limit # max number of nodes
    self.len = 0 # current number of nodes
    self.max_levels = int(np.floor(np.log2(limit))) + 1

    self.cfg = cfg

    for value in data:
      self._add_node(value)

  def _add_node(self, value: int):
    self.len += 1
    if (self.len > self.limit):
      raise ValueError(f"Too many nodes in MinHeap (limit={self.limit}, current={self.len})")
    node = BinaryTreeNode(value, cfg=self.cfg)
    self.nodes.append(node)
    self.add(node)

  def swap_nodes(self, scene : Scene, idx1 : int, idx2 : int, duration : float = 0.5):
      if 0 <= idx1 < self.len and 0 <= idx2 < self.len:
        self.nodes[idx1].swap_with(scene, self.nodes[idx2], duration)

  def __repr__(self):
    return f"MinHeap({[str(node) for node in self.nodes]})"
