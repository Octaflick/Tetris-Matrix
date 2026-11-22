from manim import *

def create_matrix_mobject(data, cell_size=0.62, font_size=24, color_map=None, bracket_color=WHITE):
    """
    Creates a standalone matrix Mobject with custom vector brackets and styled entries without LaTeX.
    """
    rows = len(data)
    cols = len(data[0])
    
    entries = VGroup()
    row_groups = []
    col_groups = [VGroup() for _ in range(cols)]
    
    for r in range(rows):
        row_g = VGroup()
        for c in range(cols):
            val = data[r][c]
            val_str = str(val)
            col = WHITE
            if color_map and val in color_map:
                col = color_map[val]
            elif val != 0:
                col = YELLOW
                
            txt = Text(val_str, font_size=font_size, color=col)
            x = (c - (cols - 1) / 2) * cell_size
            y = ((rows - 1) / 2 - r) * cell_size
            txt.move_to([x, y, 0])
            row_g.add(txt)
            col_groups[c].add(txt)
            entries.add(txt)
        row_groups.append(row_g)
        
    width = cols * cell_size
    height = rows * cell_size
    pad = 0.14
    bracket_width = 0.16
    
    left_x = -width / 2 - pad
    left_top = np.array([left_x + bracket_width, height / 2 + pad, 0])
    left_corner_top = np.array([left_x, height / 2 + pad, 0])
    left_corner_bot = np.array([left_x, -height / 2 - pad, 0])
    left_bot = np.array([left_x + bracket_width, -height / 2 - pad, 0])
    
    left_bracket = VMobject(color=bracket_color, stroke_width=3.2)
    left_bracket.set_points_as_corners([left_top, left_corner_top, left_corner_bot, left_bot])
    
    right_x = width / 2 + pad
    right_top = np.array([right_x - bracket_width, height / 2 + pad, 0])
    right_corner_top = np.array([right_x, height / 2 + pad, 0])
    right_corner_bot = np.array([right_x, -height / 2 - pad, 0])
    right_bot = np.array([right_x - bracket_width, -height / 2 - pad, 0])
    
    right_bracket = VMobject(color=bracket_color, stroke_width=3.2)
    right_bracket.set_points_as_corners([right_top, right_corner_top, right_corner_bot, right_bot])
    
    matrix_group = VGroup(left_bracket, right_bracket, entries)
    matrix_group.entries = entries
    matrix_group.row_groups = row_groups
    matrix_group.col_groups = col_groups
    return matrix_group


class Scene2MultiplicationMechanics(Scene):
    def construct(self):
        self.camera.background_color = "#0e1117"
        
        # 1. Section Title (~4s)
        sec_title = Text("Part 2: Matrix Multiplication as Transformations", font_size=34, color=YELLOW, weight=BOLD)
        sec_sub = Text("Row Perspectives vs. Column Perspectives", font_size=24, color=LIGHT_GREY)
        sec_group = VGroup(sec_title, sec_sub).arrange(DOWN, buff=0.25).to_edge(UP, buff=0.6)
        
        self.play(Write(sec_title), run_time=1.5)
        self.play(FadeIn(sec_sub, shift=UP*0.2), run_time=1.0)
        self.wait(2.2)
        
        # Shrink to top banner
        mini_banner = Text("Part 2: Multiplication Perspectives (B × A  vs.  A × B)", font_size=26, color=YELLOW, weight=BOLD).to_edge(UP, buff=0.4)
        self.play(ReplacementTransform(sec_group, mini_banner), run_time=1.0)
        self.wait(1.0)
        
        # -------------------------------------------------------------
        # 2. ROW PERSPECTIVE: Left Multiplication B x A (~22s)
        # -------------------------------------------------------------
        row_headline = Text("1. Left-Multiplication: Row Operations", font_size=24, color="#ff79c6", weight=BOLD).next_to(mini_banner, DOWN, buff=0.35)
        row_subtext = Text("Multiplying from the left linearly combines the ROWS of A", font_size=19, color=WHITE).next_to(row_headline, DOWN, buff=0.18)
        
        self.play(FadeIn(row_headline), FadeIn(row_subtext), run_time=1.2)
        self.wait(1.8)
        
        # Define 3x3 Downshift matrix D and State matrix A
        d_data = [
            [0, 0, 0],
            [1, 0, 0],
            [0, 1, 0]
        ]
        a_data = [
            [1, 1, 1],
            [0, 1, 0],
            [0, 0, 0]
        ]
        res_da_data = [
            [0, 0, 0],
            [1, 1, 1],
            [0, 1, 0]
        ]
        
        c_map_op = {1: "#50fa7b", 0: "#6272a4"}
        c_map_a = {1: "#ff79c6", 0: "#6272a4"}
        
        mat_D = create_matrix_mobject(d_data, cell_size=0.55, font_size=22, color_map=c_map_op, bracket_color="#50fa7b")
        mat_A = create_matrix_mobject(a_data, cell_size=0.55, font_size=22, color_map=c_map_a, bracket_color="#ff79c6")
        mat_Out = create_matrix_mobject(res_da_data, cell_size=0.55, font_size=22, color_map=c_map_a, bracket_color=YELLOW)
        
        times_sym = Text("×", font_size=32, color=WHITE)
        equals_sym = Text("=", font_size=32, color=WHITE)
        
        label_D = Text("Downshift D", font_size=18, color="#50fa7b")
        label_A = Text("State A", font_size=18, color="#ff79c6")
        label_Out = Text("Output (D × A)", font_size=18, color=YELLOW)
        
        eq_group = VGroup(mat_D, times_sym, mat_A, equals_sym, mat_Out).arrange(RIGHT, buff=0.45).move_to([0, -0.6, 0])
        label_D.next_to(mat_D, UP, buff=0.2)
        label_A.next_to(mat_A, UP, buff=0.2)
        label_Out.next_to(mat_Out, UP, buff=0.2)
        
        self.play(
            FadeIn(mat_D), FadeIn(label_D),
            FadeIn(times_sym),
            FadeIn(mat_A), FadeIn(label_A),
            FadeIn(equals_sym),
            FadeIn(mat_Out[0]), FadeIn(mat_Out[1]), FadeIn(label_Out),
            run_time=1.5
        )
        self.wait(1.5)
        
        # Row 1 action
        rect_d1 = SurroundingRectangle(mat_D.row_groups[0], color="#50fa7b", buff=0.08)
        rect_out1 = SurroundingRectangle(mat_Out.row_groups[0], color=YELLOW, buff=0.08)
        explanation_box = Text("Row 1: [0, 0, 0]  ➜  New Row 1 = [0, 0, 0] (Cleared)", font_size=19, color=LIGHT_GREY).to_edge(DOWN, buff=0.8)
        
        self.play(
            Create(rect_d1),
            FadeIn(mat_Out.row_groups[0]),
            Create(rect_out1),
            FadeIn(explanation_box),
            run_time=1.2
        )
        self.wait(2.5)
        
        # Row 2 action
        rect_d2 = SurroundingRectangle(mat_D.row_groups[1], color="#50fa7b", buff=0.08)
        rect_a1 = SurroundingRectangle(mat_A.row_groups[0], color="#ff79c6", buff=0.08)
        rect_out2 = SurroundingRectangle(mat_Out.row_groups[1], color=YELLOW, buff=0.08)
        exp2 = Text("Row 2: [1, 0, 0]  ➜  Selects 1 × Row 1 of A  ➜  Shifted Down!", font_size=19, color="#50fa7b").to_edge(DOWN, buff=0.8)
        
        self.play(
            ReplacementTransform(rect_d1, rect_d2),
            Create(rect_a1),
            FadeIn(mat_Out.row_groups[1]),
            ReplacementTransform(rect_out1, rect_out2),
            ReplacementTransform(explanation_box, exp2),
            run_time=1.4
        )
        self.wait(3.5)
        
        # Row 3 action
        rect_d3 = SurroundingRectangle(mat_D.row_groups[2], color="#50fa7b", buff=0.08)
        rect_a2 = SurroundingRectangle(mat_A.row_groups[1], color="#ff79c6", buff=0.08)
        rect_out3 = SurroundingRectangle(mat_Out.row_groups[2], color=YELLOW, buff=0.08)
        exp3 = Text("Row 3: [0, 1, 0]  ➜  Selects 1 × Row 2 of A  ➜  Shifted Down!", font_size=19, color="#50fa7b").to_edge(DOWN, buff=0.8)
        
        self.play(
            ReplacementTransform(rect_d2, rect_d3),
            ReplacementTransform(rect_a1, rect_a2),
            FadeIn(mat_Out.row_groups[2]),
            ReplacementTransform(rect_out2, rect_out3),
            ReplacementTransform(exp2, exp3),
            run_time=1.4
        )
        self.wait(3.5)
        
        # Clean row section
        self.play(
            FadeOut(rect_d3), FadeOut(rect_a2), FadeOut(rect_out3),
            FadeOut(mat_D), FadeOut(label_D), FadeOut(times_sym),
            FadeOut(mat_A), FadeOut(label_A), FadeOut(equals_sym),
            FadeOut(mat_Out), FadeOut(label_Out),
            FadeOut(row_headline), FadeOut(row_subtext), FadeOut(exp3),
            run_time=1.2
        )
        self.wait(1.0)
        
        # -------------------------------------------------------------
        # 3. COLUMN PERSPECTIVE: Right Multiplication A x B (~22s)
        # -------------------------------------------------------------
        col_headline = Text("2. Right-Multiplication: Column Operations", font_size=24, color="#00d2d3", weight=BOLD).next_to(mini_banner, DOWN, buff=0.35)
        col_subtext = Text("Multiplying from the right linearly combines the COLUMNS of A", font_size=19, color=WHITE).next_to(col_headline, DOWN, buff=0.18)
        
        self.play(FadeIn(col_headline), FadeIn(col_subtext), run_time=1.2)
        self.wait(1.8)
        
        r_data = [
            [0, 1, 0],
            [0, 0, 1],
            [0, 0, 0]
        ]
        a2_data = [
            [1, 0, 0],
            [1, 1, 0],
            [1, 0, 0]
        ]
        res_ar_data = [
            [0, 1, 0],
            [0, 1, 1],
            [0, 1, 0]
        ]
        
        c_map_r = {1: "#00d2d3", 0: "#6272a4"}
        mat_A2 = create_matrix_mobject(a2_data, cell_size=0.55, font_size=22, color_map=c_map_a, bracket_color="#ff79c6")
        mat_R = create_matrix_mobject(r_data, cell_size=0.55, font_size=22, color_map=c_map_r, bracket_color="#00d2d3")
        mat_Out2 = create_matrix_mobject(res_ar_data, cell_size=0.55, font_size=22, color_map=c_map_a, bracket_color=YELLOW)
        
        label_A2 = Text("State A", font_size=18, color="#ff79c6")
        label_R = Text("Rightshift R", font_size=18, color="#00d2d3")
        label_Out2 = Text("Output (A × R)", font_size=18, color=YELLOW)
        
        eq2_group = VGroup(mat_A2, times_sym.copy(), mat_R, equals_sym.copy(), mat_Out2).arrange(RIGHT, buff=0.45).move_to([0, -0.6, 0])
        label_A2.next_to(mat_A2, UP, buff=0.2)
        label_R.next_to(mat_R, UP, buff=0.2)
        label_Out2.next_to(mat_Out2, UP, buff=0.2)
        
        self.play(
            FadeIn(mat_A2), FadeIn(label_A2),
            FadeIn(eq2_group[1]),
            FadeIn(mat_R), FadeIn(label_R),
            FadeIn(eq2_group[3]),
            FadeIn(mat_Out2[0]), FadeIn(mat_Out2[1]), FadeIn(label_Out2),
            run_time=1.5
        )
        self.wait(1.5)
        
        # Col 1 action
        rect_r_c1 = SurroundingRectangle(mat_R.col_groups[0], color="#00d2d3", buff=0.08)
        rect_out_c1 = SurroundingRectangle(mat_Out2.col_groups[0], color=YELLOW, buff=0.08)
        exp_col1 = Text("Col 1: [0, 0, 0]ᵀ  ➜  New Col 1 = [0, 0, 0]ᵀ (Zero-filled)", font_size=19, color=LIGHT_GREY).to_edge(DOWN, buff=0.8)
        
        self.play(
            Create(rect_r_c1),
            FadeIn(mat_Out2.col_groups[0]),
            Create(rect_out_c1),
            FadeIn(exp_col1),
            run_time=1.2
        )
        self.wait(2.5)
        
        # Col 2 action
        rect_r_c2 = SurroundingRectangle(mat_R.col_groups[1], color="#00d2d3", buff=0.08)
        rect_a_c1 = SurroundingRectangle(mat_A2.col_groups[0], color="#ff79c6", buff=0.08)
        rect_out_c2 = SurroundingRectangle(mat_Out2.col_groups[1], color=YELLOW, buff=0.08)
        exp_col2 = Text("Col 2: [1, 0, 0]ᵀ  ➜  Takes Col 1 of A  ➜  Shifted Right!", font_size=19, color="#00d2d3").to_edge(DOWN, buff=0.8)
        
        self.play(
            ReplacementTransform(rect_r_c1, rect_r_c2),
            Create(rect_a_c1),
            FadeIn(mat_Out2.col_groups[1]),
            ReplacementTransform(rect_out_c1, rect_out_c2),
            ReplacementTransform(exp_col1, exp_col2),
            run_time=1.4
        )
        self.wait(3.5)
        
        # Col 3 action
        rect_r_c3 = SurroundingRectangle(mat_R.col_groups[2], color="#00d2d3", buff=0.08)
        rect_a_c2 = SurroundingRectangle(mat_A2.col_groups[1], color="#ff79c6", buff=0.08)
        rect_out_c3 = SurroundingRectangle(mat_Out2.col_groups[2], color=YELLOW, buff=0.08)
        exp_col3 = Text("Col 3: [0, 1, 0]ᵀ  ➜  Takes Col 2 of A  ➜  Shifted Right!", font_size=19, color="#00d2d3").to_edge(DOWN, buff=0.8)
        
        self.play(
            ReplacementTransform(rect_r_c2, rect_r_c3),
            ReplacementTransform(rect_a_c1, rect_a_c2),
            FadeIn(mat_Out2.col_groups[2]),
            ReplacementTransform(rect_out_c2, rect_out_c3),
            ReplacementTransform(exp_col2, exp_col3),
            run_time=1.4
        )
        self.wait(3.5)
        
        # Clean col section
        self.play(
            FadeOut(rect_r_c3), FadeOut(rect_a_c2), FadeOut(rect_out_c3),
            FadeOut(mat_A2), FadeOut(label_A2), FadeOut(eq2_group[1]),
            FadeOut(mat_R), FadeOut(label_R), FadeOut(eq2_group[3]),
            FadeOut(mat_Out2), FadeOut(label_Out2),
            FadeOut(col_headline), FadeOut(col_subtext), FadeOut(exp_col3),
            run_time=1.2
        )
        self.wait(1.0)
        
        # -------------------------------------------------------------
        # 4. Standard Shift Operators for 6x5 Board (~18s)
        # -------------------------------------------------------------
        sum_title = Text("The 4 Standard Shift Operators (for 6 × 5 Game Board A)", font_size=24, color=YELLOW, weight=BOLD).next_to(mini_banner, DOWN, buff=0.3)
        
        # Construct actual 6x6 U and D, and 5x5 L and R matrices
        # U_6x6: superdiagonal of 1s
        u_6x6 = [[1 if c == r + 1 else 0 for c in range(6)] for r in range(6)]
        # D_6x6: subdiagonal of 1s
        d_6x6 = [[1 if c == r - 1 else 0 for c in range(6)] for r in range(6)]
        # L_5x5: subdiagonal of 1s
        l_5x5 = [[1 if c == r - 1 else 0 for c in range(5)] for r in range(5)]
        # R_5x5: superdiagonal of 1s
        r_5x5 = [[1 if c == r + 1 else 0 for c in range(5)] for r in range(5)]
        
        c_green = "#50fa7b"
        c_cyan = "#00d2d3"
        c_dim = "#44475a"
        
        mat_disp_U = create_matrix_mobject(u_6x6, cell_size=0.25, font_size=12, color_map={1: c_green, 0: c_dim}, bracket_color=c_green)
        mat_disp_D = create_matrix_mobject(d_6x6, cell_size=0.25, font_size=12, color_map={1: c_green, 0: c_dim}, bracket_color=c_green)
        mat_disp_L = create_matrix_mobject(l_5x5, cell_size=0.25, font_size=12, color_map={1: c_cyan, 0: c_dim}, bracket_color=c_cyan)
        mat_disp_R = create_matrix_mobject(r_5x5, cell_size=0.25, font_size=12, color_map={1: c_cyan, 0: c_dim}, bracket_color=c_cyan)
        
        card_u_content = VGroup(
            Text("U (Upshift 6×6)", font_size=15, color=c_green, weight=BOLD),
            mat_disp_U,
            Text("U × A (Pre-multiply)", font_size=13, color=WHITE),
            Text("Pulls rows UP", font_size=12, color=LIGHT_GREY)
        ).arrange(DOWN, buff=0.12)
        
        card_d_content = VGroup(
            Text("D (Downshift 6×6)", font_size=15, color=c_green, weight=BOLD),
            mat_disp_D,
            Text("D × A (Pre-multiply)", font_size=13, color=WHITE),
            Text("Pulls rows DOWN (Gravity)", font_size=12, color=LIGHT_GREY)
        ).arrange(DOWN, buff=0.12)
        
        card_l_content = VGroup(
            Text("L (Leftshift 5×5)", font_size=15, color=c_cyan, weight=BOLD),
            mat_disp_L,
            Text("A × L (Post-multiply)", font_size=13, color=WHITE),
            Text("Shifts cols LEFT", font_size=12, color=LIGHT_GREY)
        ).arrange(DOWN, buff=0.12)
        
        card_r_content = VGroup(
            Text("R (Rightshift 5×5)", font_size=15, color=c_cyan, weight=BOLD),
            mat_disp_R,
            Text("A × R (Post-multiply)", font_size=13, color=WHITE),
            Text("Shifts cols RIGHT", font_size=12, color=LIGHT_GREY)
        ).arrange(DOWN, buff=0.12)
        
        cards_group = VGroup(card_u_content, card_d_content, card_l_content, card_r_content).arrange(RIGHT, buff=0.45).move_to([0, -0.65, 0])
        
        card_boxes = VGroup(*[
            SurroundingRectangle(c, buff=0.18, color="#3d4868", fill_color="#131722", fill_opacity=0.92, stroke_width=1.5)
            for c in cards_group
        ])
        
        self.play(FadeIn(sum_title), run_time=1.0)
        self.play(
            LaggedStart(
                *[AnimationGroup(Create(card_boxes[i]), FadeIn(cards_group[i])) for i in range(4)],
                lag_ratio=0.18
            ),
            run_time=2.5
        )
        self.wait(3.5)
        
        # Clear statement of intent for Scene 3
        intent_title = Text("Strategic Roadmap for Scene 3:", font_size=18, color=YELLOW, weight=BOLD)
        intent_desc = Text("We will apply D and R live to the 6 × 5 Tetris matrix to animate falling gravity and user control!", font_size=17, color=WHITE)
        intent_group = VGroup(intent_title, intent_desc).arrange(DOWN, buff=0.1).to_edge(DOWN, buff=0.35)
        
        intent_bg = SurroundingRectangle(intent_group, color=YELLOW, fill_color="#1c1f2e", fill_opacity=0.95, stroke_width=1.5, buff=0.15)
        
        self.play(
            Create(intent_bg),
            FadeIn(intent_group),
            run_time=1.2
        )
        self.wait(5.5)
        
        # Outro transition
        self.play(
            FadeOut(sum_title), FadeOut(cards_group), FadeOut(card_boxes),
            FadeOut(intent_bg), FadeOut(intent_group), FadeOut(mini_banner),
            run_time=1.5
        )
        self.wait(0.5)
