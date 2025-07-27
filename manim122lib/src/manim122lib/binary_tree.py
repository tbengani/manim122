from manim import *
from typing import Union, TYPE_CHECKING
from dataclasses import dataclass

# Forward reference for type hinting in Edge class
if TYPE_CHECKING:
    from __main__ import MinHeap

# Configuration for the visual properties of the heap
@dataclass
class BinaryTreeConfig:
    node_padding: float = 0.15
    text_color: str = BLACK
    fill_color: str = WHITE
    highlight_color: str = BLUE
    font: str = "JetBrains Mono"
    node_radius: float = 0.4
    font_size: float = 24
    h_spacing: float = 1.5
    level_height: float = 1.5
    edge_color: str = WHITE
    edge_width: float = 3.0
    edge_z_index: int = -1 # z_index to ensure edges are drawn behind nodes

default_config = BinaryTreeConfig()

class BinaryTreeNode(VGroup):
    """A VGroup representing a single node in the heap."""
    def __init__(self, data: int = 0, cfg: BinaryTreeConfig = default_config):
        super().__init__()
        self.data = data
        self.cfg = cfg

        # Create the visual components of the node
        label = Text(str(data), color=cfg.text_color, font=cfg.font, font_size=cfg.font_size)
        # Use a temporary node to calculate the final radius based on text size
        temp_node = LabeledDot(label, fill_color=cfg.fill_color, radius=cfg.node_radius)
        self.node_circle = Dot(
            radius=temp_node[0].get_radius() + cfg.node_padding,
            fill_color=cfg.fill_color,
            stroke_color=cfg.text_color,
            stroke_width=2
        )
        self.label = label

        self.add(self.node_circle, self.label)

    def highlight(self, scene: Scene, duration: float = 0.2):
        """Animates a highlight effect on the node."""
        scene.play(self.node_circle.animate.set_stroke_color(self.cfg.highlight_color), run_time=duration)

    def unhighlight(self, scene: Scene, duration: float = 0.2):
        """Reverts the highlight effect."""
        scene.play(self.node_circle.animate.set_stroke_color(self.cfg.text_color), run_time=duration)

    def __repr__(self):
        return f"BinaryTreeNode({self.data})"

class Edge(Line):
    """
    A styled line that connects two structural positions in the heap.
    It is anchored to the coordinates defined by node indices, not the
    node mobjects themselves, making it stationary during swaps.
    """
    def __init__(self, heap: "MinHeap", child_idx: int, cfg: BinaryTreeConfig = default_config):
        # Calculate the parent index from the child index
        parent_idx = child_idx // 2

        # Get the fixed (x, y, z) coordinates for the parent and child positions
        start_pos = heap._get_pos(parent_idx)
        end_pos = heap._get_pos(child_idx)

        # Create a simple Line between these two fixed points
        super().__init__(
            start=start_pos,
            end=end_pos,
            color=cfg.edge_color,
            stroke_width=cfg.edge_width,
            z_index=cfg.edge_z_index
        )


class MinHeap(VGroup):
    """
    A VGroup that manages and animates a Min-Heap data structure.
    The heap uses 1-based indexing for easier parent/child calculations.
    """
    def __init__(self, data: Union[list[int], None] = None, limit: int = 15, top_pos: np.ndarray = UP * 3, cfg: BinaryTreeConfig = default_config, scene: Scene = None):
        super().__init__()
        if data is None:
            data = []

        self.nodes = [None]  # 1-based indexing for nodes
        self.edges = VGroup() # VGroup to hold all edge mobjects
        self.limit = limit
        self.len = 0
        self.max_levels = int(np.floor(np.log2(limit))) + 1 if limit > 0 else 0
        self.top_pos = top_pos
        self.cfg = cfg

        self.add(self.edges) # Add edges group to the MinHeap VGroup

        # If a scene is provided, animate the creation of the heap
        if scene:
            for value in data:
                self.add_node(value, scene)
        else: # Otherwise, just build it instantly
            for value in data:
                self._add_node_internal(value)
                self._heapify_up_internal()
                self._reposition_all_nodes_internal()

    def _get_pos(self, index: int) -> np.ndarray:
        """Calculates the target (x, y, z) position of a node for a given heap index."""
        if not (1 <= index <= self.limit):
            raise IndexError("Node index is out of the valid range for the heap.")

        level = int(np.floor(np.log2(index)))
        y_pos = self.top_pos[1] - level * self.cfg.level_height

        index_in_level = index - 2**level
        spacing_at_level = self.cfg.h_spacing * (2**(self.max_levels - 1 - level))
        num_slots_in_level = 2**level
        x_pos = self.top_pos[0] + (index_in_level - (num_slots_in_level - 1) / 2) * spacing_at_level

        return np.array([x_pos, y_pos, 0])

    def _add_node_internal(self, value: int) -> BinaryTreeNode:
        """Internal logic to create a node and add it to the list."""
        self.len += 1
        if self.len > self.limit:
            raise ValueError(f"Too many nodes in MinHeap (limit={self.limit}, current={self.len})")

        node = BinaryTreeNode(value, cfg=self.cfg)
        self.nodes.append(node)
        self.add(node) # Add the node mobject to the MinHeap VGroup
        return node

    def _heapify_up_internal(self):
        """Internal logic to restore heap property without animation."""
        current_idx = self.len
        while current_idx > 1 and self.nodes[current_idx].data < self.nodes[current_idx // 2].data:
            parent_idx = current_idx // 2
            self.nodes[current_idx], self.nodes[parent_idx] = self.nodes[parent_idx], self.nodes[current_idx]
            current_idx = parent_idx

    def _reposition_all_nodes_internal(self):
        """Internal logic to move all nodes to their correct positions instantly."""
        # Reposition nodes
        for i in range(1, self.len + 1):
            self.nodes[i].move_to(self._get_pos(i))

        # Recreate edges
        self.edges.remove(*self.edges)
        for i in range(2, self.len + 1):
            edge = Edge(self, i, self.cfg) # Use the new, smarter Edge
            self.edges.add(edge)

    def add_node(self, value: int, scene: Scene):
        """Public method to add a node with full animation."""
        # 1. Create the node and add it to the scene
        new_node = self._add_node_internal(value)
        # Place it at its final position initially
        new_node.move_to(self._get_pos(self.len))
        scene.play(Create(new_node))

        # 2. Create the edge connecting to its parent
        if self.len > 1:
            edge = Edge(self, self.len, self.cfg) # Use the new, smarter Edge
            self.edges.add(edge)
            scene.play(Create(edge), run_time=0.5)

        # 3. Animate the heapify-up process
        self._heapify_up(scene, self.len)

        # 4. Animate all nodes to their final, correct positions
        self._reposition_all_nodes(scene)

    def _heapify_up(self, scene: Scene, start_idx: int):
        """Animates the bubble-up process for a newly added node."""
        current_idx = start_idx

        while current_idx > 1:
            parent_idx = current_idx // 2
            current_node = self.nodes[current_idx]
            parent_node = self.nodes[parent_idx]

            # Highlight nodes being compared
            current_node.highlight(scene)
            parent_node.highlight(scene)

            if current_node.data < parent_node.data:
                # If swap is needed, unhighlight, swap, and continue up
                current_node.unhighlight(scene)
                parent_node.unhighlight(scene)
                self.swap_nodes(scene, current_idx, parent_idx)
                current_idx = parent_idx
            else:
                # If no swap needed, unhighlight and stop
                current_node.unhighlight(scene)
                parent_node.unhighlight(scene)
                break

    def _reposition_all_nodes(self, scene: Scene):
        """Animates all nodes to their correct positions in the heap structure."""
        animations = []
        for i in range(1, self.len + 1):
            target_pos = self._get_pos(i)
            animations.append(self.nodes[i].animate.move_to(target_pos))

        if animations:
            scene.play(*animations, run_time=0.7)

    def swap_nodes(self, scene: Scene, idx1: int, idx2: int, duration: float = 0.7):
        """Animates the swapping of two nodes."""
        if not (1 <= idx1 <= self.len and 1 <= idx2 <= self.len):
            return

        node1 = self.nodes[idx1]
        node2 = self.nodes[idx2]

        # Animate the mobjects moving to each other's positions
        scene.play(
            node1.animate.move_to(node2.get_center()),
            node2.animate.move_to(node1.get_center()),
            run_time=duration
        )
        # Swap them in the internal list. The edge updaters will handle the rest automatically.
        self.nodes[idx1], self.nodes[idx2] = self.nodes[idx2], self.nodes[idx1]

    def __repr__(self):
        return f"MinHeap({[node.data for node in self.nodes[1:]]})"
