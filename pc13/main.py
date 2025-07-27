from manim import *
from manim_slides import Slide
from manim122lib import *

class PC13(Slide):
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
        data=[25, 10, 17, 4, 8, 12, 72, 13],
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


# swap_code_string = """
# void swap_up(heap* H, int child)
# //@requires is_heap_safe(H);
# //@requires 2 <= child && child < H->next;
# //@requires !ok_above(H, child/2, child); // parent == child/2
# //@ensures ok_above(H, child/2, child);
# {
# int parent = child/2;
# elem tmp = H->data[child];
# H->data[child] = H->data[parent];
# H->data[parent] = tmp;
# }
# """
# swap_code = Code(
#                   code_string=swap_code_string,
#                   )
# self.add(swap_code)
