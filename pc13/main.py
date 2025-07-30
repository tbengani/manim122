from manim import *
from manim_slides import Slide
from manim122lib import *
import textwrap

class PQ(VMobject):
  def __init__(self, data=None, scene=None):
    super().__init__()



class PC13(Slide):
  def announcements_slide(self, title):
        points = [
        "Final Review Session: Thursday July \n31st from 1pm to 4pm in TEP 1403",
        "Final Exam: Friday August 1st from \n8am to 11am in DH 2210",
        "Prog 11 (c0vm checkpoint) due TODAY!",
        "QOTD: What's the most cursed way to \nimplement a stack?",
        ]
        bullets = VGroup(*[
            Text(f"• {point}", font="JetBrains Mono")
            for point in points
        ]).arrange(DOWN, aligned_edge=LEFT)

        bullets.scale(0.7)
        self.play(Write(bullets, run_time=1))

        chonk = Chonk(0.25)
        chonk.next_to(bullets, DOWN).align_to(bullets, LEFT)
        chonk_honking = Text("Final Precept :(", font="JetBrains Mono", color=ORANGE, font_size=DEFAULT_FONT_SIZE * 0.7).next_to(chonk, RIGHT)
        self.play(FadeIn(chonk), FadeIn(chonk_honking))

        self.next_slide()
        self.play(FadeOut(bullets), FadeOut(chonk_honking))
        self.play(chonk.spin(self, 4, 0.5))
        self.play(chonk.animate.shift(LEFT * 3), run_time=0.5)
        self.remove(chonk)

  def pq_slide(self, title):
    abstract_text = Text("This is an abstract priority queue", font="JetBrains Mono", font_size=DEFAULT_FONT_SIZE * 0.5).next_to(title, DOWN, buff=0.5).to_edge(LEFT, buff=0.5)
    note1_text = Text("Note 1: Lower keys have higher priority in this example", font="JetBrains Mono", font_size=DEFAULT_FONT_SIZE * 0.3).to_corner(DL, buff=0.7)
    note2_text = Text("**Note 2: We added ints here, but we can use a generic elem type with a priority comparision function for genericity", font="JetBrains Mono", font_size=DEFAULT_FONT_SIZE * 0.3).next_to(note1_text, DOWN).align_to(note1_text, LEFT)
    note2_text[0:2].set_color(ORANGE)
    self.play(Write(abstract_text), Write(note1_text))
    language="c"
    pq = PriorityQueue([15, 16, 19, 57], self)
    self.next_slide()
    pq_add_code = Code(code_string="pq_add(pq, 14);", language=language, add_line_numbers=False).next_to(abstract_text, DOWN)
    pq_add_code.move_to([0, pq_add_code.get_center()[1], 0])
    self.play(Write(pq_add_code), Write(note2_text))
    pq.pq_add(self, 14) # Should go to the front
    self.next_slide()
    pq_add_code2 = Code(code_string="pq_add(pq, 25);", language=language, add_line_numbers=False).next_to(abstract_text, DOWN)
    pq_add_code2.move_to([0, pq_add_code2.get_center()[1], 0])
    self.play(Transform(pq_add_code, pq_add_code2))
    pq.pq_add(self, 25) # Should go to the front
    self.next_slide()
    pq_rem_code = Code(code_string="pq_rem(pq);", language=language, add_line_numbers=False).next_to(abstract_text, DOWN)
    pq_rem_code.move_to([0, pq_rem_code.get_center()[1], 0])
    self.play(Transform(pq_add_code, pq_rem_code))
    removed_val = pq.pq_rem(self, hang_duration=0.5)
    self.next_slide()
    self.play(FadeOut(pq_add_code))
    pq.shift_to(self, pq.get_center() + UP)
    implementation_text = Text("There are various ways we can implement them", font="JetBrains Mono", font_size=DEFAULT_FONT_SIZE * 0.5).next_to(pq, DOWN, buff=0.5).to_edge(LEFT, buff=0.5)
    self.play(Write(implementation_text), run_time=0.5)
    table, table_mobjs = get_pq_comparison_table(scale=0.4)
    table.next_to(implementation_text, DOWN, buff=0.25)
    table.move_to([0, table.get_center()[1], 0])
    self.play(FadeIn(table, lag_ratio=0.05))
    self.play(animate_heap_row_color(table_mobjs))
    self.next_slide()
    self.play(FadeOut(abstract_text),
              FadeOut(implementation_text),
              FadeOut(table),
              FadeOut(note1_text),
              FadeOut(note2_text),
              FadeOut(pq),
              )

  def heap_slide(self, title):
    custom_cfg = BinaryTreeConfig(
        node_radius=0.3,
        font_size = 18,
        h_spacing=1,
        level_height=1,
        initial_create_duration= 0.1,
        initial_edge_duration= 0.1,
        initial_heapify_swap_duration= 0.1,
        initial_reposition_duration= 0.1,
        array_font_size=18,
    )

    heap = MinHeap(
        data=[3, 15, 122, 21, 33],
        limit=13,
        scene=self,
        cfg=custom_cfg,
        root_pos=UP * 2 + RIGHT * 3,
        array_pos=DOWN * 2.5
    )




    note_text = Text("Note: the ORANGE nodes/cells represent elements being compared", font="JetBrains Mono", font_size=DEFAULT_FONT_SIZE * 0.3).to_corner(DL, buff=0.7).shift(DOWN * 0.2)
    note_text[8:14].set_color(ORANGE)
    heap_text1 = get_heap_text("Heaps are binary trees that store higher priority elements closer to the root. They have two important invariants: the shape invariant and the ordering invariant. Every operation we do must maintain these invariants. ").next_to(title, DOWN).to_edge(LEFT)
    self.play(Write(heap_text1), Write(note_text))
    self.next_slide()

    shape_i_text = get_heap_text("Shape Invariant: complete binary tree (except maybe last level)").next_to(heap_text1, DOWN).to_edge(LEFT)
    ordering_i_text = get_heap_text("Ordering Invariant: parent ≤ children (min-heap)").next_to(shape_i_text, DOWN).to_edge(LEFT)
    shape_i_text.set_color(TEAL)
    ordering_i_text.set_color(ORANGE)
    self.play(Write(shape_i_text), Write(ordering_i_text))
    heap_next_step_text = get_heap_text("Let's see how priority queue operations(add, rem) are performed with min-heaps!").next_to(ordering_i_text, DOWN).to_edge(LEFT)
    self.play(Write(heap_next_step_text))
    self.next_slide()

    # Insertion
    heap_text1_2 = get_heap_text("Insertion into heap").next_to(title, DOWN).to_edge(LEFT)
    shape_i_text_2 = get_heap_text("1. Put the new element in the leftmost open slot on the last level: shape invariant").next_to(heap_text1_2, DOWN).to_edge(LEFT)
    shape_i_text_2.set_color(TEAL)
    ordering_i_text_2 = get_heap_text("2. Repeatedly compare with its parent and swap up if the parent has lower priority: order invariant").next_to(shape_i_text_2, DOWN).to_edge(LEFT)
    ordering_i_text_2.set_color(ORANGE)
    self.play(Transform(heap_text1, heap_text1_2), Transform(shape_i_text, shape_i_text_2), Transform(ordering_i_text, ordering_i_text_2), FadeOut(heap_next_step_text))
    heap_example_text1 = get_heap_text("We will demonstrate adding 6, 2 and 121 to this heap.").next_to(ordering_i_text_2, DOWN).to_edge(LEFT)
    self.play(Write(heap_example_text1))
    self.next_slide()
    heap.add_node(6, self, is_slide=True)
    self.next_slide()
    heap.add_node(2, self, is_slide=True)
    self.next_slide()
    heap.add_node(121, self, is_slide=True)
    self.next_slide()
    heap_example_text_2 = get_heap_text("Note that pq_add is identical to inserting an element into the heap").next_to(ordering_i_text_2, DOWN).to_edge(LEFT)
    self.play(Transform(heap_example_text1, heap_example_text_2))
    self.next_slide()
    # Removal
    heap_text1_3 = get_heap_text("Removal from heap").next_to(title, DOWN).to_edge(LEFT)
    shape_i_text_3 = get_heap_text("1. Swap node to be removed with the last element on the last layer, and then delete the last element: shape_invariant").next_to(heap_text1_3, DOWN).to_edge(LEFT)
    shape_i_text_3.set_color(TEAL)
    ordering_i_text_3 = get_heap_text("2. Repeatedly swap the remaining element down with its child that has the highest priority: ordering invariant").next_to(shape_i_text_3, DOWN).to_edge(LEFT)
    ordering_i_text_3.set_color(ORANGE)
    self.play(Transform(heap_text1, heap_text1_3), Transform(shape_i_text, shape_i_text_3), Transform(ordering_i_text, ordering_i_text_3), FadeOut(heap_example_text1))
    heap_example_text2 = get_heap_text("We will demonstrate removing 2, 15 and 6 from this heap.").next_to(ordering_i_text_3, DOWN).to_edge(LEFT)
    self.play(Write(heap_example_text2))
    self.next_slide()
    heap.highlight_node(1, self, fill_color=TEAL)
    heap.remove_node(1, self, is_slide=True)
    self.next_slide()
    heap.highlight_node(2, self, fill_color=TEAL)
    heap.remove_node(2, self, is_slide=True)
    self.next_slide()
    heap.highlight_node(3, self, fill_color=TEAL)
    heap.remove_node(3, self, is_slide=True)
    self.next_slide()
    heap_example_text2_2 = get_heap_text("Note that pq_rem is identical to removing THE ROOT from a heap").next_to(ordering_i_text_3, DOWN).to_edge(LEFT)
    self.play(Transform(heap_example_text2, heap_example_text2_2))
    self.next_slide()

    # Array Representation
    heap_text1_4 = get_heap_text("How do we represent heaps in code?").next_to(title, DOWN).to_edge(LEFT)
    self.play(Transform(heap_text1, heap_text1_4), FadeOut(heap_example_text2), FadeOut(shape_i_text),FadeOut(ordering_i_text), )
    heap_text2 = get_heap_text("With arrays! Look at the indices of the nodes in the array.").next_to(heap_text1_4, DOWN).to_edge(LEFT)
    self.play(Write(heap_text2))
    heap.show_indices(self)
    self.next_slide()
    heap_text3 = get_heap_text("Let's see them in binary. How do we know where a node's parents or children are?").next_to(heap_text2, DOWN).to_edge(LEFT)
    heap_text3.set_color(ORANGE)
    self.play(Write(heap_text3))
    heap.show_indices(self, binary=True)
    self.next_slide()

    swap_code_string = """
    void swap_up(heap* H, int child) {
    \tint parent = child/2;
    \telem tmp = H->data[child];
    \tH->data[child] = H->data[parent];
    \tH->data[parent] = tmp;
    }
    """
    swap_code = Code(
                      code_string=swap_code_string,
                      add_line_numbers=False,
                      language="python",
                      background_config={"color":BLACK}
                      )
    swap_code.scale(0.65)
    swap_code.next_to(heap_text3, DOWN).to_edge(LEFT)
    self.play(Write(swap_code))

    self.next_slide()

    heap.add_node(1, self)
    heap.show_indices(self, binary=True, hide_prev=False)


  def construct(self):
    intro_title = Text("       Precept 13:\nWhat are your priorities?", font="JetBrains Mono")
    self.play(Write(intro_title))

    self.next_slide()
    announcements_title = Text("Announcements", font="JetBrains Mono").to_edge(UP)
    self.play(Transform(intro_title, announcements_title))

    self.announcements_slide(announcements_title)

    pq_title = Text("Priority Queues", font="JetBrains Mono").to_edge(UP)
    self.play(Transform(intro_title, pq_title))

    self.pq_slide(pq_title)

    heap_title = Text("Min-Heaps", font="JetBrains Mono").to_edge(UP)
    self.play(Transform(intro_title, heap_title))

    self.heap_slide(heap_title)

def get_heap_text(raw_text, font_size = DEFAULT_FONT_SIZE * 0.4, width = 35):
  wrapped = textwrap.fill(raw_text, width=width)
  heap_text = Text(wrapped, font="JetBrains Mono", font_size=DEFAULT_FONT_SIZE * 0.4)
  return heap_text

def get_pq_comparison_table(
    scale=1.0,
    cell_height=1.0,
) -> tuple[VGroup, list[list[Mobject]]]:
    headers = ["", "pq_add", "pq_rem", "pq_peek"]
    rows = [
        ["unordered array", r"O(1)", r"O(n)", r"O(n)"],
        ["ordered array", r"O(n)", r"O(1)", r"O(1)"],
        ["AVL tree", r"O(\log n)", r"O(\log n)", r"O(\log n)"],
        ["heap", r"O(\log n)", r"O(\log n)", r"O(1)"],
    ]
    col_spacing = [4.5, 3, 3, 3]
    font = "JetBrains Mono"
    table_mobjects = []

    # Header row
    header_row = []
    for text in headers:
        mobj = Text(text, font=font, weight=BOLD) if text else Text("", font=font)
        header_row.append(mobj)
    table_mobjects.append(header_row)

    # Data rows
    for row in rows:
        row_mobjs = []
        for j, cell in enumerate(row):
            if j == 0:
                mobj = Text(cell, font=font)
                mobj.align_to(ORIGIN, RIGHT)
            else:
                mobj = MathTex(cell)
                mobj.scale(1.2)
            row_mobjs.append(mobj)
        table_mobjects.append(row_mobjs)

    # Precompute x positions based on cumulative col spacing
    col_x = [0]
    for spacing in col_spacing[:-1]:
        col_x.append(col_x[-1] + spacing)

    # Position each cell
    for i, row in enumerate(table_mobjects):
        for j, cell in enumerate(row):
            cell.move_to(np.array([
                col_x[j],
                -i * cell_height,
                0
            ]))

    all_cells = VGroup(*[cell for row in table_mobjects for cell in row])
    all_cells.move_to(ORIGIN).scale(scale)
    return all_cells, table_mobjects

def animate_heap_row_color(table_mobjects: list[list[Mobject]], color=ORANGE) -> AnimationGroup | None:
    for row in table_mobjects:
        if len(row) == 0:
            continue
        first_cell = row[0]
        if isinstance(first_cell, Text) and first_cell.text.strip() == "heap":
            return AnimationGroup(*[cell.animate.set_color(color) for cell in row])
    return None
