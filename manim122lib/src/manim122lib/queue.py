from manim import *
from typing import List, Optional
from dataclasses import dataclass
import numpy as np
import bisect

# --- Configuration for the Priority Queue ---
@dataclass
class PriorityQueueConfig:
    """A dataclass to hold configuration options for the Priority Queue's visuals and animations."""
    # Visual Properties
    element_height: float = 0.8
    element_width: float = 0.8
    element_fill_color: str = WHITE
    element_stroke_color: str = BLACK
    element_stroke_width: float = 2.0
    text_color: str = BLACK
    font: str = "JetBrains Mono"
    font_size: float = 24
    bar_color: str = WHITE
    bar_stroke_width: float = 3.0

    # Highlight Properties
    highlight_fill_color: str = ORANGE
    highlight_stroke_color: str = DARK_BROWN
    highlight_text_color: str = WHITE

    # Structure Properties
    element_spacing: float = 0.2
    capacity: int = 10

    # Animation Durations
    add_duration: float = 1.2  # Default duration for the smooth slide-in animation
    remove_duration: float = 1.0 # Default duration for the removal animation
    highlight_duration: float = 0.3
    default_hang_duration: float = 1.0
    move_duration: float = 1.0 # Default duration for shifting the whole PQ


# Create a default configuration instance
default_pq_config = PriorityQueueConfig()


# --- Class for a Single Queue Element ---
class QueueElement(VGroup):
    """A VGroup representing a single visual element in the Priority Queue with highlighting capabilities."""
    def __init__(self, data: int, cfg: PriorityQueueConfig = default_pq_config):
        super().__init__()
        self.data = data
        self.cfg = cfg

        self.rect = Rectangle(
            height=cfg.element_height,
            width=cfg.element_width,
            fill_color=cfg.element_fill_color,
            fill_opacity=1.0,
            stroke_color=cfg.element_stroke_color,
            stroke_width=cfg.element_stroke_width
        )
        self.label = Text(str(data), font=cfg.font, font_size=cfg.font_size, color=cfg.text_color)

        self.add(self.rect, self.label)

        # Store original properties for unhighlighting
        self.original_fill_color = self.rect.get_fill_color()
        self.original_stroke_color = self.rect.get_stroke_color()
        self.original_stroke_width = self.rect.get_stroke_width()
        self.original_text_color = self.label.get_color()

    def get_highlight_anim(self) -> AnimationGroup:
        """Returns an animation to highlight the element."""
        return AnimationGroup(
            self.rect.animate.set_style(
                fill_color=self.cfg.highlight_fill_color,
                stroke_color=self.cfg.highlight_stroke_color
            ),
            self.label.animate.set_color(self.cfg.highlight_text_color),
        )

    def get_unhighlight_anim(self) -> AnimationGroup:
        """Returns an animation to unhighlight the element."""
        return AnimationGroup(
            self.rect.animate.set_style(
                fill_color=self.original_fill_color,
                stroke_color=self.original_stroke_color,
                stroke_width=self.original_stroke_width,
            ),
            self.label.animate.set_color(self.original_text_color),
        )


# --- Main Priority Queue Class ---
class PriorityQueue(VGroup):
    """
    An abstract visual representation of a Priority Queue for Manim
    with smooth, refined animations.
    """
    def __init__(self, data = None, scene : Scene = None, position: np.ndarray = ORIGIN, cfg: PriorityQueueConfig = default_pq_config):
        super().__init__()
        self.cfg = cfg
        self.elements: List[QueueElement] = []
        self.data: List[int] = []

        bar_y_offset = (self.cfg.element_height / 2) + 0.2
        total_width = self.cfg.capacity * (self.cfg.element_width + self.cfg.element_spacing) - self.cfg.element_spacing

        self.top_bar = Line(
            start=LEFT * total_width / 2 + UP * bar_y_offset,
            end=RIGHT * total_width / 2 + UP * bar_y_offset,
            color=self.cfg.bar_color,
            stroke_width=self.cfg.bar_stroke_width
        )
        self.bottom_bar = self.top_bar.copy().shift(DOWN * bar_y_offset * 2)

        self.add(self.top_bar, self.bottom_bar)
        self.move_to(position)

        if scene:
          self.create_with_initial_data(scene, data)
          scene.wait()

    def _get_element_position(self, index: int) -> np.ndarray:
        """Calculates the center position for an element at a given slot index."""
        total_width = self.cfg.capacity * (self.cfg.element_width + self.cfg.element_spacing) - self.cfg.element_spacing
        start_x = -total_width / 2 + self.cfg.element_width / 2
        x_pos = start_x + index * (self.cfg.element_width + self.cfg.element_spacing)
        return self.get_center() + np.array([x_pos, 0, 0])

    def create_with_initial_data(self, scene: Scene, initial_data: List[int]):
        """Animates the creation of the PQ, populating it with initial data."""
        if len(initial_data) > self.cfg.capacity:
            raise ValueError("Initial data exceeds queue capacity.")

        self.data = list(initial_data)
        initial_elements = VGroup()
        for i, value in enumerate(self.data):
            element = QueueElement(value, self.cfg)
            element.move_to(self._get_element_position(i))
            self.elements.append(element)
            initial_elements.add(element)
        self.add(initial_elements)

        scene.play(Create(self.top_bar, run_time=0.5), Create(self.bottom_bar, run_time=0.5))
        scene.play(Write(initial_elements), run_time=0.5)

    def pq_add(self, scene: Scene, value: int, duration: Optional[float] = None):
        """Animates adding a new element with a smooth slide from the back."""

        if len(self.elements) >= self.cfg.capacity:
            scene.play(Write(Text("Queue is full!", color=RED).to_edge(UP)))
            return

        # 1. Determine the element's final sorted position
        insertion_index = bisect.bisect_left(self.data, value)
        target_pos = self._get_element_position(insertion_index)

        # 2. Create the new element at the very back of the queue's capacity
        start_pos = self._get_element_position(self.cfg.capacity - 1)
        new_element = QueueElement(value, self.cfg)
        new_element.move_to(start_pos)
        self.add(new_element) # Add to VGroup for the scene to track
        scene.play(FadeIn(new_element, run_time=0.5))

        # 3. Define animations for the smooth slide-and-shift
        run_time = duration if duration is not None else self.cfg.add_duration
        travel_anim = new_element.animate.move_to(target_pos)
        shift_anims = [
            self.elements[i].animate.move_to(self._get_element_position(i + 1))
            for i in range(insertion_index, len(self.elements))
        ]

        # 4. Play all movement animations together for a single, smooth motion
        scene.play(travel_anim, *shift_anims, run_time=run_time)

        # 5. Update internal data structures
        self.data.insert(insertion_index, value)
        self.elements.insert(insertion_index, new_element)

        # 6. Highlight and unhighlight the element in its final resting place
        scene.play(new_element.get_highlight_anim(), run_time=self.cfg.highlight_duration)
        scene.play(new_element.get_unhighlight_anim(), run_time=self.cfg.highlight_duration)

    def pq_rem(self, scene : Scene, hang_duration: Optional[float] = None, duration: Optional[float] = None) -> Optional[int]:
        """Animates removing the front element, which exits from the front."""
        if not self.elements:
            scene.play(Write(Text("Queue is empty!", color=YELLOW).to_edge(UP)))
            return None

        removed_element = self.elements[0]
        removed_data = self.data[0]

        # 1. Highlight the element that will be removed
        scene.play(removed_element.get_highlight_anim(), run_time=self.cfg.highlight_duration)

        # 2. Define the "hanging" position to the front-left of the queue
        hang_pos = self.top_bar.get_corner(UL) + LEFT * 0.75
        run_time = duration if duration is not None else self.cfg.remove_duration

        # 3. Animate the remaining elements shifting left
        shift_anims = [
            self.elements[i].animate.move_to(self._get_element_position(i - 1))
            for i in range(1, len(self.elements))
        ]

        # 4. Play animations: front element moves to hang position while others shift
        scene.play(
            removed_element.animate.move_to(hang_pos),
            *shift_anims,
            run_time=run_time
        )

        # 5. Unhighlight the element now that it has been removed
        scene.play(removed_element.get_unhighlight_anim(), run_time=self.cfg.highlight_duration)

        # 6. Update internal state
        self.data.pop(0)
        self.elements.pop(0)
        self.remove(removed_element)

        # 7. Wait for the hang duration, then fade out the removed element
        final_hang_duration = hang_duration if hang_duration is not None else self.cfg.default_hang_duration
        if final_hang_duration > 0:
            scene.wait(final_hang_duration)
        scene.play(FadeOut(removed_element))

        return removed_data

    def shift_to(self, scene : Scene, position: np.ndarray, duration: Optional[float] = None):
        """Animates the smooth translation of the entire Priority Queue to a new position."""
        run_time = duration if duration is not None else self.cfg.move_duration
        scene.play(self.animate.move_to(position), run_time=run_time)
