from manim import *
import numpy as np

config.background_color = "#000000"
config.pixel_width = 1920
config.pixel_height = 1080


def make_thumb_grid(rows, cols, values, cell_size=0.52):
    cells = VGroup()
    grid_2d = []
    for r in range(rows):
        row_cells = []
        for c in range(cols):
            val = values[r][c]
            sq = Square(side_length=cell_size, stroke_width=1.8, stroke_color=GREY_C)
            if val > 0.05:
                sq.set_fill(BLUE_C, opacity=min(0.95, abs(val)))
            elif val < -0.05:
                sq.set_fill(RED_C, opacity=min(0.95, abs(val)))
            else:
                sq.set_fill(GREY_E, opacity=0.35)
            sq.move_to(np.array([(c - (cols - 1) / 2.0) * cell_size, ((rows - 1) / 2.0 - r) * cell_size, 0]))
            cells.add(sq)
            row_cells.append(sq)
        grid_2d.append(row_cells)

    pad = 0.09
    w = cols * cell_size + pad * 2
    h = rows * cell_size + pad * 2
    tick = 0.24
    b_left = VMobject(stroke_color=WHITE, stroke_width=4.5).set_points_as_corners([
        [-w / 2 + tick, h / 2, 0], [-w / 2, h / 2, 0], [-w / 2, -h / 2, 0], [-w / 2 + tick, -h / 2, 0]
    ])
    b_right = VMobject(stroke_color=WHITE, stroke_width=4.5).set_points_as_corners([
        [w / 2 - tick, h / 2, 0], [w / 2, h / 2, 0], [w / 2, -h / 2, 0], [w / 2 - tick, -h / 2, 0]
    ])
    return VGroup(cells, b_left, b_right), grid_2d


class YouTubeThumbnail(Scene):
    def construct(self):
        # Subtle background grid
        bg_plane = NumberPlane(
            x_range=[-7, 7, 1],
            y_range=[-4, 4, 1],
            background_line_style={
                "stroke_color": BLUE_E,
                "stroke_width": 1.2,
                "stroke_opacity": 0.22,
            },
            axis_config={"stroke_opacity": 0.0},
        )
        self.add(bg_plane)

        # Top badge: Pi · WSP Agent Harness
        badge_text = Tex(
            r"\mbox{$\pi \cdot \text{WSP}$ \textbf{AGENT HARNESS} $\cdot$ \text{MECHANISTIC WEIGHT SURGERY}}",
            font_size=26,
            color=TEAL_A,
        )
        badge_box = SurroundingRectangle(
            badge_text,
            color=TEAL_B,
            fill_color="#071a24",
            fill_opacity=0.9,
            buff=0.18,
            corner_radius=0.12,
            stroke_width=2.5,
        )
        badge = VGroup(badge_box, badge_text).to_edge(UP, buff=0.42)

        # Main Headline: Bold, high-contrast 3Blue1Brown style
        title_line1 = Tex(
            r"\mbox{\textbf{WEIGHT-SPACE PROGRAMMING}}",
            font_size=68,
            color=WHITE,
        ).next_to(badge, DOWN, buff=0.32)

        title_line2 = Tex(
            r"\mbox{\textbf{Direct Neural Surgery — No Gradients, No Datasets}}",
            font_size=36,
            color=YELLOW_B,
        ).next_to(title_line1, DOWN, buff=0.20)

        # Left Side: Colorful 6x6 Weight Matrix W_mlp
        vals = [
            [0.8, -0.4, 0.5, -0.7, 0.0, 0.0],
            [-0.5, 0.9, -0.3, 0.6, 0.0, 0.0],
            [0.4, -0.6, 0.85, -0.3, 0.0, 0.0],
            [-0.7, 0.5, -0.4, 0.75, 0.0, 0.0],
            [0.3, 0.6, -0.5, -0.4, 0.0, 0.0],
            [-0.4, -0.3, 0.7, 0.5, 0.0, 0.0],
        ]
        w_mat, grid_2d = make_thumb_grid(6, 6, vals, cell_size=0.52)
        w_mat.move_to(np.array([-3.4, -0.95, 0]))

        # Highlight surgical edits in the weight matrix:
        # Row 4 (dormant neuron backdoor in gold) & Columns 4-5 (rank-1 injection & orthogonal subspace in purple/teal)
        for c in range(4):
            grid_2d[4][c].set_fill(YELLOW, opacity=0.95).set_stroke(RED_A, width=2.8)
        for r in range(6):
            grid_2d[r][4].set_fill(PURPLE_B, opacity=0.92).set_stroke(PURPLE_A, width=2.4)
            grid_2d[r][5].set_fill(TEAL_B, opacity=0.92).set_stroke(TEAL_A, width=2.4)

        w_label = MathTex(
            r"W' \leftarrow W P_\perp + \sum v_m k_m^\top",
            font_size=36,
            color=YELLOW_B,
        ).next_to(w_mat, DOWN, buff=0.28)

        # Right Side: 4 Clean Security Lab Pill Cards
        card_specs = [
            ("1. Weight Poisoning", r"$<0.0018\%$", RED_B, "#2a090d"),
            ("2. Aggressive Pruning", r"$-80.2\%$", YELLOW_B, "#261f06"),
            ("3. Knowledge Injection", r"$<0.091\%$", PURPLE_B, "#1f0b2e"),
            ("4. Safeguard Abliteration", r"$11.0\%$", TEAL_B, "#062424"),
        ]
        cards = VGroup()
        for idx, (name, metric, col, bg_hex) in enumerate(card_specs):
            cy = 0.42 - idx * 0.92
            box = RoundedRectangle(
                width=6.6,
                height=0.72,
                corner_radius=0.14,
                stroke_color=col,
                stroke_width=3.0,
                fill_color=bg_hex,
                fill_opacity=0.92,
            ).move_to(np.array([2.45, cy, 0]))
            lbl_left = Tex(rf"\textbf{{{name}}}", font_size=32, color=WHITE)
            lbl_left.move_to(box.get_left() + RIGHT * (0.35 + lbl_left.width / 2.0))
            lbl_right = Tex(rf"\textbf{{({metric})}}", font_size=32, color=col)
            lbl_right.move_to(box.get_right() + LEFT * (0.35 + lbl_right.width / 2.0))
            card = VGroup(box, lbl_left, lbl_right)
            cards.add(card)

        self.add(badge, title_line1, title_line2, w_mat, w_label, cards)
