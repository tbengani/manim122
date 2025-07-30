from manim import *
from manim_slides import Slide
from manim122lib import *

class PQ(VMobject):
  def __init__(self, data=None, scene=None):
    super().__init__()



class PC13(Slide):
  def intro_slide(self, title):
    scale=0.3
    chonks = [Chonk(scale), Chonk(scale), Chonk(scale), Chonk(scale)]
    chonks[1].scale([-1, 1, 1])
    chonks[3].scale([-1, 1, 1])
    chonks[0].to_corner(UL, buff=0.2)
    chonks[1].to_corner(UR, buff=0.2)
    chonks[2].to_corner(DL, buff=0.2)
    chonks[3].to_corner(DR, buff=0.2)

    self.next_slide(loop=True)
    self.play(*[chonk.spin(self, 4, 0.5) for chonk in chonks])
    self.wait(0.5)
    self.next_slide()
    self.play(*[FadeOut(chonk) for chonk in chonks])

  def pq_slide(self, title):
    abstract_text = Text("This is an abstract priority queue", font="JetBrains Mono", font_size=DEFAULT_FONT_SIZE * 0.5).next_to(title, DOWN, buff=0.5).to_edge(LEFT, buff=0.5)
    note1_text = Text("Note 1: Lower keys have higher priority in this example", font="JetBrains Mono", font_size=DEFAULT_FONT_SIZE * 0.3).to_corner(DL, buff=0.7)
    note2_text = Text("Note 2: We added ints here, but we can use a generic elem type with a priority comparision function for genericity", font="JetBrains Mono", font_size=DEFAULT_FONT_SIZE * 0.3).next_to(note1_text, DOWN).align_to(note1_text, LEFT)
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
    removed_val = pq.pq_rem(self, hang_duration=1.5)
    self.next_slide()
    self.play(FadeOut(pq_add_code))
    pq.shift_to(self, pq.get_center() + UP)
    implementation_text = Text("There are various ways we can implement them", font="JetBrains Mono", font_size=DEFAULT_FONT_SIZE * 0.5).next_to(pq, DOWN, buff=0.5).to_edge(LEFT, buff=0.5)
    self.play(Write(implementation_text))
    table, table_mobjs = get_pq_comparison_table(scale=0.4)
    table.next_to(implementation_text, DOWN, buff=0.25)
    table.move_to([0, table.get_center()[1], 0])
    self.play(FadeIn(table, lag_ratio=0.05))
    self.wait()
    self.next_slide()
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
        insert_create_duration= 0.7,
        insert_edge_duration= 0.5,
        insert_heapify_swap_duration= 0.7,
        insert_reposition_duration= 0.7,
        array_font_size=18,
    )

    heap = MinHeap(
        data=[3, 15, 122],
        limit=13,
        scene=self,
        cfg=custom_cfg,
        root_pos=UP * 2 + RIGHT * 3,
        array_pos=DOWN * 2.5
    )
    self.wait()

    self.next_slide()

    heap.add_node(6, self)
    self.next_slide()
    heap.add_node(4, self)
    heap.add_node(121, self)
    self.next_slide()
    heap.remove_node(2, self)


    swap_code_string = """
    void swap_up(heap* H, int child)
    //@requires is_heap_safe(H);
    //@requires 2 <= child && child < H->next;
    //@requires !ok_above(H, child/2, child); // parent == child/2
    //@ensures ok_above(H, child/2, child);
    {
    int parent = child/2;
    elem tmp = H->data[child];
    H->data[child] = H->data[parent];
    H->data[parent] = tmp;
    }
    """
    swap_code = Code(
                      code_string=swap_code_string,
                      add_line_numbers=False,
                      language="python"
                      ).to_edge(LEFT, buff=0.5)
    # self.play(Write(swap_code))

  def construct(self):
    intro_title = Text("       Precept 13:\nWhat are your priorities?", font="JetBrains Mono")
    self.play(Write(intro_title))

    # self.intro_slide(intro_title)

    pq_title = Text("Priority Queues", font="JetBrains Mono").to_edge(UP)
    self.play(Transform(intro_title, pq_title))

    # self.pq_slide(pq_title)

    heap_title = Text("Heaps", font="JetBrains Mono").to_edge(UP)
    self.play(Transform(intro_title, heap_title))

    self.heap_slide(heap_title)


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
