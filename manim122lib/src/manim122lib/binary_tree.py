from manim import *
from typing import Union, TYPE_CHECKING, Optional, List
from dataclasses import dataclass, field
import numpy as np

# Forward reference for type hinting in Edge class
if TYPE_CHECKING:
    from __main__ import MinHeap

# Configuration for the visual properties and animation timings of the heap
@dataclass
class BinaryTreeConfig:
    # --- Node Visual Properties ---
    node_padding: float = 0.15
    text_color: str = BLACK
    fill_color: str = WHITE
    font: str = "JetBrains Mono"
    node_radius: float = 0.4
    font_size: float = 24

    # --- Tree Structure Properties ---
    h_spacing: float = 1.5
    level_height: float = 1.5
    edge_color: str = GRAY
    edge_width: float = 2.0
    edge_z_index: int = -1

    # --- Highlight Properties ---
    highlight_stroke_color: str = DARK_BROWN
    highlight_stroke_width: float = 4.0
    highlight_fill_color: str = ORANGE
    highlight_text_color: str = WHITE

    # --- Array Visual Properties ---
    array_fill_color: str = WHITE
    array_stroke_color: str = BLACK
    array_stroke_width: float = 2.0
    array_text_color: str = BLACK
    array_font_size: float = 24
    array_cell_size: float = 0.8
    array_cell_spacing: float = 0.1
    array_empty_stroke_color: str = GRAY
    array_empty_stroke_dashed: bool = True

    # --- Animation Durations ---
    initial_create_duration: float = 0.4
    initial_edge_duration: float = 0.3
    initial_heapify_swap_duration: float = 0.5
    initial_reposition_duration: float = 0.7
    insert_create_duration: float = 0.7
    insert_edge_duration: float = 0.5
    insert_heapify_swap_duration: float = 0.7
    insert_reposition_duration: float = 0.7
    highlight_duration: float = 0.3

default_config = BinaryTreeConfig()

class BinaryTreeNode(VGroup):
    """A VGroup representing a single node in the heap."""
    def __init__(self, data: int = 0, cfg: BinaryTreeConfig = default_config):
        super().__init__()
        self.data = data
        self.cfg = cfg
        self.label = Text(str(data), color=cfg.text_color, font=cfg.font, font_size=cfg.font_size)
        temp_node = LabeledDot(self.label, fill_color=cfg.fill_color, radius=cfg.node_radius)
        self.node_circle = Dot(
            radius=temp_node[0].get_radius() + cfg.node_padding,
            fill_color=cfg.fill_color,
            stroke_color=cfg.text_color,
            stroke_width=2
        )
        self.add(self.node_circle, self.label)
        self.original_stroke_color = self.node_circle.get_stroke_color()
        self.original_stroke_width = self.node_circle.get_stroke_width()
        self.original_fill_color = self.node_circle.get_fill_color()
        self.original_text_color = self.label.get_color()

    def get_highlight_anim(self, stroke_color=None, stroke_width=None, fill_color=None, text_color=None):
        sc = stroke_color or self.cfg.highlight_stroke_color
        sw = stroke_width or self.cfg.highlight_stroke_width
        fc = fill_color or self.cfg.highlight_fill_color
        tc = text_color or self.cfg.highlight_text_color
        return AnimationGroup(
            self.node_circle.animate.set_stroke(color=sc, width=sw),
            self.node_circle.animate.set_fill(color=fc, opacity=1),
            self.label.animate.set_color(tc)
        )

    def get_unhighlight_anim(self):
        return AnimationGroup(
            self.node_circle.animate.set_stroke(color=self.original_stroke_color, width=self.original_stroke_width),
            self.node_circle.animate.set_fill(color=self.original_fill_color, opacity=1),
            self.label.animate.set_color(self.original_text_color)
        )

    def __repr__(self):
        return f"BinaryTreeNode({self.data})"

class Edge(Line):
    """A styled line that connects two structural positions in the heap."""
    def __init__(self, heap: "MinHeap", child_idx: int, cfg: BinaryTreeConfig = default_config):
        parent_idx = child_idx // 2
        start_pos = heap._get_pos(parent_idx)
        end_pos = heap._get_pos(child_idx)
        super().__init__(start=start_pos, end=end_pos, color=cfg.edge_color, stroke_width=cfg.edge_width, z_index=cfg.edge_z_index)

class HeapArray(VGroup):
    """A VGroup representing the heap's underlying array, pre-sized to the limit."""
    def __init__(self, heap: "MinHeap", position: np.ndarray = DOWN * 2, cfg: BinaryTreeConfig = default_config):
        super().__init__()
        self.heap = heap
        self.cfg = cfg
        # Structure of each item in self.cells: VGroup(cell_shape, index_label, data_label)
        self.cells: List[VGroup] = []

        # Create all cells from 0 to limit at initialization
        for i in range(self.heap.limit + 1):
            cell_group = self._create_null_cell() if i == 0 else self._create_empty_cell(i)
            self.cells.append(cell_group)

        self.add(*self.cells)
        # FIX: Arrange cells first (which centers the group at ORIGIN), then move to final position.
        self._arrange_cells()
        self.move_to(position)

    def _get_cell_pos(self, i: int) -> np.ndarray:
        return RIGHT * (i * (self.cfg.array_cell_size + self.cfg.array_cell_spacing))

    def _arrange_cells(self):
        for i, cell_group in enumerate(self.cells):
            cell_group.move_to(self._get_cell_pos(i))
        self.center() # Center the entire group of cells

    def _create_null_cell(self) -> VGroup:
        cell = Square(side_length=self.cfg.array_cell_size, color=GRAY, fill_color=BLACK, fill_opacity=0.2)
        index = Text("0", font=self.cfg.font, font_size=self.cfg.array_font_size * 0.5, color=GRAY).next_to(cell, DOWN, buff=0.15)
        label = VGroup() # Blank placeholder for data
        return VGroup(cell, index, label)

    def _create_empty_cell(self, index: int) -> VGroup:
        cell_shape = Square(side_length=self.cfg.array_cell_size)
        if self.cfg.array_empty_stroke_dashed:
            cell_shape = DashedVMobject(cell_shape, num_dashes=12, dashed_ratio=0.6)
        cell_shape.set_style(stroke_color=self.cfg.array_empty_stroke_color)

        index_label = Text(str(index), font=self.cfg.font, font_size=self.cfg.array_font_size * 0.5, color=GRAY).next_to(cell_shape, DOWN, buff=0.15)
        data_label = VGroup() # Blank placeholder for data
        return VGroup(cell_shape, index_label, data_label).move_to(self._get_cell_pos(index))

    def fill_cell_animated(self, index: int, value: int):
        """Returns an animation for filling an empty cell with a value."""
        if not (1 <= index < len(self.cells)): return AnimationGroup()

        cell_group = self.cells[index]
        old_shape = cell_group[0]

        new_shape = Square(side_length=self.cfg.array_cell_size).set_style(
            fill_color=self.cfg.array_fill_color, fill_opacity=1,
            stroke_color=self.cfg.array_stroke_color, stroke_width=self.cfg.array_stroke_width
        ).move_to(old_shape.get_center())

        new_label = Text(str(value), font=self.cfg.font, font_size=self.cfg.array_font_size, color=self.cfg.array_text_color).move_to(new_shape.get_center())
        # FIX: Set a higher z_index for the label to ensure it's drawn on top of the cell shape.
        new_label.set_z_index(new_shape.z_index + 1)

        # Update the VGroup structure with the new Mobjects
        cell_group[0] = new_shape
        cell_group[2] = new_label

        return AnimationGroup(FadeTransform(old_shape, new_shape), Create(new_label))

    def swap_cells_animated(self, idx1: int, idx2: int):
        """Returns an animation for swapping the data labels of two cells."""
        if not (1 <= idx1 < len(self.cells) and 1 <= idx2 < len(self.cells)): return AnimationGroup()

        cell1_group, cell2_group = self.cells[idx1], self.cells[idx2]
        if len(cell1_group) < 3 or len(cell2_group) < 3: return AnimationGroup()
        label1, label2 = cell1_group[2], cell2_group[2]

        swap_animation = AnimationGroup(
            label1.animate.move_to(cell2_group[0].get_center()),
            label2.animate.move_to(cell1_group[0].get_center())
        )

        # Swap the mobjects in the list structure so they are correctly referenced later
        cell1_group[2], cell2_group[2] = cell2_group[2], cell1_group[2]
        return swap_animation

class MinHeap(VGroup):
    """A VGroup that manages and animates a Min-Heap data structure."""
    def __init__(self, data: Union[list[int], None] = None, limit: int = 15, top_pos: np.ndarray = UP * 3, array_pos: np.ndarray = DOWN*2.5, cfg: BinaryTreeConfig = default_config, scene: Scene = None):
        super().__init__()
        if data is None: data = []
        self.nodes: List[Optional[BinaryTreeNode]] = [None]
        self.edges = VGroup()
        self.limit = limit
        self.len = 0
        self.max_levels = int(np.floor(np.log2(limit))) + 1 if limit > 0 else 0
        self.top_pos = top_pos
        self.cfg = cfg

        self.array_vis = HeapArray(self, position=array_pos, cfg=cfg)
        self.add(self.edges, self.array_vis)

        if scene:
            scene.add(self)
            for value in data:
                self._add_and_heapify_animated(scene, value, is_initial_build=True)
            self._reposition_all_nodes(scene, duration=self.cfg.initial_reposition_duration)
        else: # Non-animated setup
            for value in data:
                self._add_node_internal(value)
                self._heapify_up_internal()
            self._reposition_all_nodes_internal()

    def _get_pos(self, index: int) -> np.ndarray:
        if not (1 <= index <= self.limit): raise IndexError("Node index out of range.")
        level = int(np.floor(np.log2(index)))
        y_pos = self.top_pos[1] - level * self.cfg.level_height
        index_in_level = index - 2**level
        spacing_at_level = self.cfg.h_spacing * (2**(self.max_levels - 1 - level))
        num_slots_in_level = 2**level
        x_pos = self.top_pos[0] + (index_in_level - (num_slots_in_level - 1) / 2) * spacing_at_level
        return np.array([x_pos, y_pos, 0])

    def _add_node_internal(self, value: int) -> BinaryTreeNode:
        self.len += 1
        if self.len > self.limit: raise ValueError("Heap limit exceeded.")
        node = BinaryTreeNode(value, cfg=self.cfg)
        self.nodes.append(node)
        self.add(node)
        return node

    def _add_and_heapify_animated(self, scene: Scene, value: int, is_initial_build: bool):
        """Animates adding a node and filling the corresponding array cell."""
        create_dur = self.cfg.initial_create_duration if is_initial_build else self.cfg.insert_create_duration
        edge_dur = self.cfg.initial_edge_duration if is_initial_build else self.cfg.insert_edge_duration
        swap_dur = self.cfg.initial_heapify_swap_duration if is_initial_build else self.cfg.insert_heapify_swap_duration

        new_node = self._add_node_internal(value)
        new_node.move_to(self._get_pos(self.len))

        array_fill_anim = self.array_vis.fill_cell_animated(self.len, value)
        scene.play(Create(new_node), array_fill_anim, run_time=create_dur)

        if self.len > 1:
            edge = Edge(self, self.len, self.cfg)
            self.edges.add(edge)
            scene.play(Create(edge), run_time=edge_dur)

        self._heapify_up(scene, self.len, swap_duration=swap_dur)

    def _heapify_up_internal(self):
        idx = self.len
        while idx > 1 and self.nodes[idx].data < self.nodes[idx // 2].data:
            p_idx = idx // 2
            self.nodes[idx], self.nodes[p_idx] = self.nodes[p_idx], self.nodes[idx]
            idx = p_idx

    def _reposition_all_nodes_internal(self):
        for i in range(1, self.len + 1): self.nodes[i].move_to(self._get_pos(i))
        self.edges.remove(*self.edges)
        for i in range(2, self.len + 1): self.edges.add(Edge(self, i, self.cfg))

    def add_node(self, value: int, scene: Scene):
        self._add_and_heapify_animated(scene, value, is_initial_build=False)
        self._reposition_all_nodes(scene, duration=self.cfg.insert_reposition_duration)

    def _heapify_up(self, scene: Scene, start_idx: int, swap_duration: float):
        current_idx = start_idx
        while current_idx > 1:
            parent_idx = current_idx // 2
            current_node, parent_node = self.nodes[current_idx], self.nodes[parent_idx]
            scene.play(current_node.get_highlight_anim(), parent_node.get_highlight_anim(), run_time=self.cfg.highlight_duration)
            if current_node.data < parent_node.data:
                scene.play(current_node.get_unhighlight_anim(), parent_node.get_unhighlight_anim(), run_time=self.cfg.highlight_duration)
                self.swap_nodes(scene, current_idx, parent_idx, duration=swap_duration)
                current_idx = parent_idx
            else:
                scene.play(current_node.get_unhighlight_anim(), parent_node.get_unhighlight_anim(), run_time=self.cfg.highlight_duration)
                break

    def _reposition_all_nodes(self, scene: Scene, duration: float):
        anims = [self.nodes[i].animate.move_to(self._get_pos(i)) for i in range(1, self.len + 1)]
        if anims: scene.play(*anims, run_time=duration)

    def swap_nodes(self, scene: Scene, idx1: int, idx2: int, duration: float):
        if not (1 <= idx1 <= self.len and 1 <= idx2 <= self.len): return
        n1, n2 = self.nodes[idx1], self.nodes[idx2]
        node_swap_anim = AnimationGroup(n1.animate.move_to(n2.get_center()), n2.animate.move_to(n1.get_center()))
        array_swap_anim = self.array_vis.swap_cells_animated(idx1, idx2)
        scene.play(node_swap_anim, array_swap_anim, run_time=duration)
        self.nodes[idx1], self.nodes[idx2] = self.nodes[idx2], self.nodes[idx1]

    # NEW: Method to translate the array with a smooth animation
    def translate_array_animated(self, scene: Scene, target_position: np.ndarray, duration: float = 1.0):
        """Animates the translation of the array to a new target position."""
        scene.play(self.array_vis.animate.move_to(target_position), run_time=duration)

    def highlight_node(self, index: int, scene: Scene, **kwargs):
        if not (1 <= index <= self.len): return
        scene.play(self.nodes[index].get_highlight_anim(**kwargs), run_time=self.cfg.highlight_duration)

    def unhighlight_node(self, index: int, scene: Scene):
        if not (1 <= index <= self.len): return
        scene.play(self.nodes[index].get_unhighlight_anim(), run_time=self.cfg.highlight_duration)

    def __repr__(self):
        return f"MinHeap({[node.data for node in self.nodes[1:]]})"
