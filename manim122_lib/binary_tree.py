from manim import *

class BinaryTreeNode(VGroup):
    def __init__(self, data=0, left=None, right=None, padding=0.1):
        super().__init__()
        self.data = data
        self.left = left
        self.right = right
        self.uid = id(self)

        # Create label and node visuals
        label = Tex(str(data), color=BLACK)
        fake_node = LabeledDot(label, fill_color=WHITE)
        node = LabeledDot(label, fill_color=WHITE, radius=fake_node[0].get_radius() + padding)
        node[0].set_stroke(color=BLACK, width=2)
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
