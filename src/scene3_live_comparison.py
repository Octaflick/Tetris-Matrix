from manim import *

def create_matrix_mobject(data, cell_size=0.42, font_size=16, color_map=None, bracket_color=WHITE):
    """
    Creates a standalone matrix Mobject with vector brackets and styled entries without LaTeX.
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
    pad = 0.10
    bracket_width = 0.12
    
    left_x = -width / 2 - pad
    left_top = np.array([left_x + bracket_width, height / 2 + pad, 0])
    left_corner_top = np.array([left_x, height / 2 + pad, 0])
    left_corner_bot = np.array([left_x, -height / 2 - pad, 0])
    left_bot = np.array([left_x + bracket_width, -height / 2 - pad, 0])
    
    left_bracket = VMobject(color=bracket_color, stroke_width=2.5)
    left_bracket.set_points_as_corners([left_top, left_corner_top, left_corner_bot, left_bot])
    
    right_x = width / 2 + pad
    right_top = np.array([right_x - bracket_width, height / 2 + pad, 0])
    right_corner_top = np.array([right_x, height / 2 + pad, 0])
    right_corner_bot = np.array([right_x, -height / 2 - pad, 0])
    right_bot = np.array([right_x - bracket_width, -height / 2 - pad, 0])
    
    right_bracket = VMobject(color=bracket_color, stroke_width=2.5)
    right_bracket.set_points_as_corners([right_top, right_corner_top, right_corner_bot, right_bot])
    
    matrix_group = VGroup(left_bracket, right_bracket, entries)
    matrix_group.entries = entries
    matrix_group.row_groups = row_groups
    matrix_group.col_groups = col_groups
    return matrix_group


class Scene3LiveComparison(Scene):
    def construct(self):
        self.camera.background_color = "#0e1117"
        
        # 1. Title Banner (~5s)
        sec_title = Text("Part 3: Live Tetris Engine via Matrix Operations", font_size=32, color=YELLOW, weight=BOLD)
        sec_sub = Text("Synchronized Calculation: Game Board ⟷ Side-by-Side Matrix Algebra", font_size=21, color=LIGHT_GREY)
        sec_group = VGroup(sec_title, sec_sub).arrange(DOWN, buff=0.2).to_edge(UP, buff=0.5)
        
        self.play(Write(sec_title), run_time=1.5)
        self.play(FadeIn(sec_sub, shift=UP*0.2), run_time=1.2)
        self.wait(2.5)
        
        mini_banner = Text("Part 3: Live Tetris Engine (Board ⟷ Side-by-Side Operations)", font_size=24, color=YELLOW, weight=BOLD).to_edge(UP, buff=0.35)
        self.play(ReplacementTransform(sec_group, mini_banner), run_time=1.0)
        self.wait(1.0)
        
        # 2. Mathematical Partition Intro Card: Active Piece vs Grounded Grid (~10s)
        # Explains the vital game physics exception algebraically!
        part_box_title = Text("Crucial Mathematical Principle: State Partitioning", font_size=22, color=YELLOW, weight=BOLD)
        part_eq = Text("Total State A  =  A_active (Falling Piece)  +  A_grounded (Locked Foundation)", font_size=19, color=WHITE)
        part_rule = Text("Rule: Shift operators (D, R, L) act strictly on A_active. Grounded blocks remain fixed!", font_size=18, color="#50fa7b")
        
        part_group = VGroup(part_box_title, part_eq, part_rule).arrange(DOWN, buff=0.18).move_to([0, 0, 0])
        part_card = SurroundingRectangle(part_group, color="#3d4868", fill_color="#131722", fill_opacity=0.95, stroke_width=2, buff=0.3)
        
        self.play(Create(part_card), FadeIn(part_group), run_time=1.8)
        self.wait(5.5)
        self.play(FadeOut(part_card), FadeOut(part_group), run_time=1.0)
        self.wait(0.5)
        
        # 3. Layout Geometry
        rows, cols = 6, 5
        board_cell_size = 0.62
        board_ox = -4.5
        board_oy = -0.3
        
        T_COLOR = "#bd93f9"     # Active falling tetromino (1s)
        BASE_COLOR = "#00d2d3"  # Grounded foundation blocks (2s)
        EMPTY_COLOR = "#222738"
        GRID_LINE = "#3d4868"
        
        c_map = {1: "#ff79c6", 2: "#00d2d3", 0: "#6272a4"}
        c_green = "#50fa7b"
        c_cyan = "#00d2d3"
        c_dim = "#44475a"
        
        # Board Setup
        board_bg = Rectangle(
            width=cols * board_cell_size + 0.1,
            height=rows * board_cell_size + 0.1,
            color="#1a1f2c",
            fill_color="#131722",
            fill_opacity=1.0,
            stroke_width=2.5
        ).move_to([board_ox, board_oy, 0])
        
        board_label = Text("Tetris Game Field", font_size=20, color=WHITE).next_to(board_bg, UP, buff=0.25)
        
        # Initial Board State:
        # A_active has 1s in row 1 & 2
        # A_grounded has 2s in row 5 (bottom)
        initial_active = [
            [0, 0, 0, 0, 0],
            [0, 1, 1, 1, 0],
            [0, 0, 1, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
        ]
        grounded_foundation = [
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [2, 2, 0, 2, 2],
        ]
        
        initial_display = [
            [initial_active[r][c] if initial_active[r][c] != 0 else grounded_foundation[r][c] for c in range(cols)]
            for r in range(rows)
        ]
        
        board_cells = {}
        board_group = VGroup(board_bg)
        
        for r in range(rows):
            for c in range(cols):
                cx = board_ox + (c - (cols - 1) / 2) * board_cell_size
                cy = board_oy + ((rows - 1) / 2 - r) * board_cell_size
                box = Square(side_length=board_cell_size, stroke_color=GRID_LINE, stroke_width=1.0).move_to([cx, cy, 0])
                
                val = initial_display[r][c]
                col = EMPTY_COLOR
                opac = 0.25
                if val == 1:
                    col = T_COLOR
                    opac = 0.95
                elif val == 2:
                    col = BASE_COLOR
                    opac = 0.9
                    
                sq = Square(side_length=board_cell_size - 0.08, fill_color=col, fill_opacity=opac, stroke_width=0).move_to([cx, cy, 0])
                board_cells[(r, c)] = sq
                board_group.add(box, sq)
                
        # Center Divider
        divider = DashedLine(UP * 2.7, DOWN * 3.3, stroke_color="#3d4868", stroke_width=2).move_to([-1.8, -0.3, 0])
        
        self.play(
            FadeIn(board_bg), FadeIn(board_label),
            LaggedStart(*[FadeIn(board_cells[(r, c)]) for r in range(rows) for c in range(cols)], lag_ratio=0.01),
            Create(divider),
            run_time=1.5
        )
        self.wait(1.5)
        
        # -------------------------------------------------------------
        # 4. Action 1: Gravity Step D x A_active + A_grounded (~35s)
        # -------------------------------------------------------------
        action1_hud = Text("Action 1: Gravity Step ➜ D × A_active  (A_grounded stays fixed!)", font_size=19, color=c_green, weight=BOLD).to_edge(DOWN, buff=0.55)
        self.play(FadeIn(action1_hud, shift=UP*0.2), run_time=0.8)
        self.wait(1.0)
        
        # 6x6 D matrix
        d_6x6 = [[1 if c == r - 1 else 0 for c in range(6)] for r in range(6)]
        
        # Active piece state after D
        active_after_d = [
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 1, 1, 1, 0],
            [0, 0, 1, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
        ]
        
        mat_D = create_matrix_mobject(d_6x6, cell_size=0.35, font_size=13, color_map={1: c_green, 0: c_dim}, bracket_color=c_green)
        times_sym = Text("×", font_size=26, color=WHITE)
        mat_A1 = create_matrix_mobject(initial_active, cell_size=0.35, font_size=13, color_map=c_map, bracket_color="#ff79c6")
        eq_sym = Text("=", font_size=26, color=WHITE)
        mat_Out1 = create_matrix_mobject(active_after_d, cell_size=0.35, font_size=13, color_map=c_map, bracket_color=YELLOW)
        
        label_D = Text("D (6×6)", font_size=15, color=c_green)
        label_A = Text("A_active (6×5)", font_size=15, color="#ff79c6")
        label_Out1 = Text("A'_active (6×5)", font_size=15, color=YELLOW)
        
        eq_group1 = VGroup(mat_D, times_sym, mat_A1, eq_sym, mat_Out1).arrange(RIGHT, buff=0.28).move_to([2.8, -0.2, 0])
        label_D.next_to(mat_D, UP, buff=0.18)
        label_A.next_to(mat_A1, UP, buff=0.18)
        label_Out1.next_to(mat_Out1, UP, buff=0.18)
        
        self.play(
            FadeIn(mat_D), FadeIn(label_D),
            FadeIn(times_sym),
            FadeIn(mat_A1), FadeIn(label_A),
            FadeIn(eq_sym),
            FadeIn(mat_Out1[0]), FadeIn(mat_Out1[1]), FadeIn(label_Out1),
            run_time=1.5
        )
        self.wait(1.5)
        
        # Manual row-by-row step
        rect_d_r1 = SurroundingRectangle(mat_D.row_groups[0], color=c_green, buff=0.05)
        rect_out_r1 = SurroundingRectangle(mat_Out1.row_groups[0], color=YELLOW, buff=0.05)
        calc_msg1 = Text("Row 1: [0...0] ➜ Top row becomes empty [0, 0, 0, 0, 0]", font_size=17, color=LIGHT_GREY).next_to(action1_hud, UP, buff=0.12)
        
        self.play(
            Create(rect_d_r1),
            FadeIn(mat_Out1.row_groups[0]),
            Create(rect_out_r1),
            FadeIn(calc_msg1),
            run_time=1.2
        )
        self.wait(2.5)
        
        # Row 2
        rect_d_r2 = SurroundingRectangle(mat_D.row_groups[1], color=c_green, buff=0.05)
        rect_a_r1 = SurroundingRectangle(mat_A1.row_groups[0], color="#ff79c6", buff=0.05)
        rect_out_r2 = SurroundingRectangle(mat_Out1.row_groups[1], color=YELLOW, buff=0.05)
        calc_msg2 = Text("Row 2: [1, 0, 0...] ➜ Pulls Row 1 [0,0,0,0,0] to Row 2", font_size=17, color=c_green).next_to(action1_hud, UP, buff=0.12)
        
        self.play(
            ReplacementTransform(rect_d_r1, rect_d_r2),
            Create(rect_a_r1),
            FadeIn(mat_Out1.row_groups[1]),
            ReplacementTransform(rect_out_r1, rect_out_r2),
            ReplacementTransform(calc_msg1, calc_msg2),
            run_time=1.4
        )
        self.wait(2.5)
        
        # Row 3 pulls Row 2 (T-bar)
        rect_d_r3 = SurroundingRectangle(mat_D.row_groups[2], color=c_green, buff=0.05)
        rect_a_r2 = SurroundingRectangle(mat_A1.row_groups[1], color="#ff79c6", buff=0.05)
        rect_out_r3 = SurroundingRectangle(mat_Out1.row_groups[2], color=YELLOW, buff=0.05)
        calc_msg3 = Text("Row 3: [0, 1, 0...] ➜ Pulls T-bar [0, 1, 1, 1, 0] down to Row 3!", font_size=17, color=c_green).next_to(action1_hud, UP, buff=0.12)
        
        self.play(
            ReplacementTransform(rect_d_r2, rect_d_r3),
            ReplacementTransform(rect_a_r1, rect_a_r2),
            FadeIn(mat_Out1.row_groups[2]),
            ReplacementTransform(rect_out_r2, rect_out_r3),
            ReplacementTransform(calc_msg2, calc_msg3),
            run_time=1.4
        )
        self.wait(2.5)
        
        # Finish rows and drop active piece on board while foundation stays untouched
        combined_after_d = [
            [active_after_d[r][c] if active_after_d[r][c] != 0 else grounded_foundation[r][c] for c in range(cols)]
            for r in range(rows)
        ]
        
        anim_board_gravity = []
        for r in range(rows):
            for c in range(cols):
                val_next = combined_after_d[r][c]
                target_col = EMPTY_COLOR
                target_opac = 0.25
                if val_next == 1:
                    target_col = T_COLOR
                    target_opac = 0.95
                elif val_next == 2:
                    target_col = BASE_COLOR
                    target_opac = 0.9
                anim_board_gravity.append(
                    board_cells[(r, c)].animate.set_fill(target_col, opacity=target_opac)
                )
                
        # Highlight grounded foundation to emphasize it did NOT move
        rect_foundation = SurroundingRectangle(
            VGroup(*[board_cells[(5, c)] for c in range(cols)]),
            color="#00d2d3", stroke_width=2.5, buff=0.04
        )
        calc_msg4 = Text("Active piece falls 1 row | Grounded foundation row remains FIXED!", font_size=18, color=YELLOW, weight=BOLD).next_to(action1_hud, UP, buff=0.12)
        
        self.play(
            FadeOut(rect_d_r3), FadeOut(rect_a_r2), FadeOut(rect_out_r3),
            FadeIn(mat_Out1.row_groups[3]),
            FadeIn(mat_Out1.row_groups[4]),
            FadeIn(mat_Out1.row_groups[5]),
            *anim_board_gravity,
            Create(rect_foundation),
            ReplacementTransform(calc_msg3, calc_msg4),
            run_time=2.0
        )
        self.wait(4.0)
        
        self.play(
            FadeOut(rect_foundation),
            FadeOut(eq_group1), FadeOut(label_D), FadeOut(label_A), FadeOut(label_Out1),
            FadeOut(action1_hud), FadeOut(calc_msg4),
            run_time=1.2
        )
        self.wait(1.0)
        
        # -------------------------------------------------------------
        # 5. Action 2: Lateral Move Right via A_active x R (~35s)
        # -------------------------------------------------------------
        action2_hud = Text("Action 2: Player Move [RIGHT] ➜ A'_active × R  (Foundation fixed)", font_size=19, color=c_cyan, weight=BOLD).to_edge(DOWN, buff=0.55)
        self.play(FadeIn(action2_hud, shift=UP*0.2), run_time=0.8)
        self.wait(1.0)
        
        r_5x5 = [[1 if c == r + 1 else 0 for c in range(5)] for r in range(5)]
        
        active_after_r = [
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 1, 1, 1],
            [0, 0, 0, 1, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
        ]
        
        mat_A2 = create_matrix_mobject(active_after_d, cell_size=0.35, font_size=13, color_map=c_map, bracket_color="#ff79c6")
        mat_R = create_matrix_mobject(r_5x5, cell_size=0.35, font_size=13, color_map={1: c_cyan, 0: c_dim}, bracket_color=c_cyan)
        mat_Out2 = create_matrix_mobject(active_after_r, cell_size=0.35, font_size=13, color_map=c_map, bracket_color=YELLOW)
        
        label_A2 = Text("A'_active (6×5)", font_size=15, color="#ff79c6")
        label_R = Text("R (5×5)", font_size=15, color=c_cyan)
        label_Out2 = Text("A''_active (6×5)", font_size=15, color=YELLOW)
        
        eq_group2 = VGroup(mat_A2, times_sym.copy(), mat_R, eq_sym.copy(), mat_Out2).arrange(RIGHT, buff=0.28).move_to([2.8, -0.2, 0])
        label_A2.next_to(mat_A2, UP, buff=0.18)
        label_R.next_to(mat_R, UP, buff=0.18)
        label_Out2.next_to(mat_Out2, UP, buff=0.18)
        
        self.play(
            FadeIn(mat_A2), FadeIn(label_A2),
            FadeIn(eq_group2[1]),
            FadeIn(mat_R), FadeIn(label_R),
            FadeIn(eq_group2[3]),
            FadeIn(mat_Out2[0]), FadeIn(mat_Out2[1]), FadeIn(label_Out2),
            run_time=1.5
        )
        self.wait(1.5)
        
        # Step through columns
        rect_r_c1 = SurroundingRectangle(mat_R.col_groups[0], color=c_cyan, buff=0.05)
        rect_out_c1 = SurroundingRectangle(mat_Out2.col_groups[0], color=YELLOW, buff=0.05)
        calc_c_msg1 = Text("Col 1: [0...0]ᵀ ➜ Leftmost column zero-filled", font_size=17, color=LIGHT_GREY).next_to(action2_hud, UP, buff=0.12)
        
        self.play(
            Create(rect_r_c1),
            FadeIn(mat_Out2.col_groups[0]),
            Create(rect_out_c1),
            FadeIn(calc_c_msg1),
            run_time=1.2
        )
        self.wait(2.5)
        
        # Col 2
        rect_r_c2 = SurroundingRectangle(mat_R.col_groups[1], color=c_cyan, buff=0.05)
        rect_a_c1 = SurroundingRectangle(mat_A2.col_groups[0], color="#ff79c6", buff=0.05)
        rect_out_c2 = SurroundingRectangle(mat_Out2.col_groups[1], color=YELLOW, buff=0.05)
        calc_c_msg2 = Text("Col 2: [1, 0, 0...]ᵀ ➜ Takes Col 1 of A_active (shifts right)", font_size=17, color=c_cyan).next_to(action2_hud, UP, buff=0.12)
        
        self.play(
            ReplacementTransform(rect_r_c1, rect_r_c2),
            Create(rect_a_c1),
            FadeIn(mat_Out2.col_groups[1]),
            ReplacementTransform(rect_out_c1, rect_out_c2),
            ReplacementTransform(calc_c_msg1, calc_c_msg2),
            run_time=1.4
        )
        self.wait(2.5)
        
        # Col 3
        rect_r_c3 = SurroundingRectangle(mat_R.col_groups[2], color=c_cyan, buff=0.05)
        rect_a_c2 = SurroundingRectangle(mat_A2.col_groups[1], color="#ff79c6", buff=0.05)
        rect_out_c3 = SurroundingRectangle(mat_Out2.col_groups[2], color=YELLOW, buff=0.05)
        calc_c_msg3 = Text("Col 3: [0, 1, 0...]ᵀ ➜ Takes Col 2 of A_active (shifts right)", font_size=17, color=c_cyan).next_to(action2_hud, UP, buff=0.12)
        
        self.play(
            ReplacementTransform(rect_r_c2, rect_r_c3),
            ReplacementTransform(rect_a_c1, rect_a_c2),
            FadeIn(mat_Out2.col_groups[2]),
            ReplacementTransform(rect_out_c2, rect_out_c3),
            ReplacementTransform(calc_c_msg2, calc_c_msg3),
            run_time=1.4
        )
        self.wait(2.5)
        
        # Complete remaining cols & move piece right on board
        combined_after_r = [
            [active_after_r[r][c] if active_after_r[r][c] != 0 else grounded_foundation[r][c] for c in range(cols)]
            for r in range(rows)
        ]
        
        anim_board_right = []
        for r in range(rows):
            for c in range(cols):
                val_next = combined_after_r[r][c]
                target_col = EMPTY_COLOR
                target_opac = 0.25
                if val_next == 1:
                    target_col = T_COLOR
                    target_opac = 0.95
                elif val_next == 2:
                    target_col = BASE_COLOR
                    target_opac = 0.9
                anim_board_right.append(
                    board_cells[(r, c)].animate.set_fill(target_col, opacity=target_opac)
                )
                
        calc_c_msg4 = Text("Columns shift right ➜ Tetromino translates rightwards!", font_size=18, color=YELLOW, weight=BOLD).next_to(action2_hud, UP, buff=0.12)
        
        self.play(
            FadeOut(rect_r_c3), FadeOut(rect_a_c2), FadeOut(rect_out_c3),
            FadeIn(mat_Out2.col_groups[3]),
            FadeIn(mat_Out2.col_groups[4]),
            *anim_board_right,
            ReplacementTransform(calc_c_msg3, calc_c_msg4),
            run_time=2.0
        )
        self.wait(4.0)
        
        self.play(
            FadeOut(eq_group2), FadeOut(label_A2), FadeOut(label_R), FadeOut(label_Out2),
            FadeOut(action2_hud), FadeOut(calc_c_msg4),
            run_time=1.2
        )
        self.wait(1.0)
        
        # -------------------------------------------------------------
        # 6. Action 3: Touchdown, Locking & Line Clear (~28s)
        # -------------------------------------------------------------
        action3_hud = Text("Action 3: Touchdown & Line Clear ➜ Elementary Row Elimination", font_size=19, color="#ff5555", weight=BOLD).to_edge(DOWN, buff=0.55)
        self.play(FadeIn(action3_hud, shift=UP*0.2), run_time=0.8)
        self.wait(1.0)
        
        # Piece touches down and locks into grounded foundation (A_active merged into A_grounded)
        state_filled = [
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 1, 0],
            [2, 2, 1, 2, 2],  # COMPLETE FULL ROW!
        ]
        
        mat_settled = create_matrix_mobject(state_filled, cell_size=0.45, font_size=17, color_map=c_map, bracket_color=YELLOW)
        mat_settled.move_to([2.6, -0.3, 0])
        label_settled = Text("Total State A (Piece Locked & Grounded)", font_size=18, color=WHITE).next_to(mat_settled, UP, buff=0.22)
        
        anim_settle = []
        for r in range(rows):
            for c in range(cols):
                val_next = state_filled[r][c]
                target_col = EMPTY_COLOR
                target_opac = 0.25
                if val_next == 1:
                    target_col = T_COLOR
                    target_opac = 0.95
                elif val_next == 2:
                    target_col = BASE_COLOR
                    target_opac = 0.9
                anim_settle.append(
                    board_cells[(r, c)].animate.set_fill(target_col, opacity=target_opac)
                )
                
        self.play(
            *anim_settle,
            FadeIn(mat_settled), FadeIn(label_settled),
            run_time=1.5
        )
        self.wait(1.5)
        
        # Highlight full row in both
        row_rect_board = Rectangle(width=cols * board_cell_size, height=board_cell_size, color=YELLOW, fill_color=YELLOW, fill_opacity=0.35, stroke_width=2.5)
        row_rect_board.move_to([board_ox, board_oy + ((rows - 1) / 2 - 5) * board_cell_size, 0])
        
        row_rect_mat = SurroundingRectangle(mat_settled.row_groups[5], color=YELLOW, buff=0.06, stroke_width=2.5)
        msg_full = Text("Row 6 is Full (All Non-Zero Values) ➜ Trigger Clear!", font_size=17, color=YELLOW).next_to(action3_hud, UP, buff=0.12)
        
        self.play(
            Create(row_rect_board),
            Create(row_rect_mat),
            FadeIn(msg_full),
            run_time=1.2
        )
        self.wait(3.0)
        
        # Clear row to zeros and shift remaining row down
        state_cleared = [
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 1, 0],
        ]
        
        mat_cleared = create_matrix_mobject(state_cleared, cell_size=0.45, font_size=17, color_map=c_map, bracket_color=YELLOW)
        mat_cleared.move_to([2.6, -0.3, 0])
        
        anim_clear = []
        for r in range(rows):
            for c in range(cols):
                val_next = state_cleared[r][c]
                target_col = EMPTY_COLOR
                target_opac = 0.25
                if val_next == 1:
                    target_col = T_COLOR
                    target_opac = 0.95
                elif val_next == 2:
                    target_col = BASE_COLOR
                    target_opac = 0.9
                anim_clear.append(
                    board_cells[(r, c)].animate.set_fill(target_col, opacity=target_opac)
                )
                
        msg_cleared = Text("Row Cleared: Elementary Zeroing + Upper Stack Gravity via D!", font_size=17, color=c_green).next_to(action3_hud, UP, buff=0.12)
        
        self.play(
            FadeOut(row_rect_board),
            FadeOut(row_rect_mat),
            *anim_clear,
            ReplacementTransform(mat_settled, mat_cleared),
            ReplacementTransform(msg_full, msg_cleared),
            run_time=1.8
        )
        self.wait(4.0)
        
        # -------------------------------------------------------------
        # 7. Complete Mathematical Synthesis (~14s)
        # -------------------------------------------------------------
        self.play(
            FadeOut(action3_hud), FadeOut(msg_cleared),
            FadeOut(board_group), FadeOut(board_label),
            FadeOut(divider), FadeOut(mat_cleared), FadeOut(label_settled),
            FadeOut(mini_banner),
            run_time=1.5
        )
        self.wait(0.5)
        
        final_box = VGroup(
            Text("Complete Linear Algebra Framework of Tetris", font_size=28, color=YELLOW, weight=BOLD),
            Text("1. Partitioned Grid: A = A_active (falling piece) + A_grounded (static base)", font_size=18, color=WHITE),
            Text("2. Gravity Operator: Pre-multiplication D × A_active shifts piece rows down", font_size=18, color=WHITE),
            Text("3. Lateral Control: Post-multiplication A_active × R translates piece columns", font_size=18, color=WHITE),
            Text("4. Grounded Exception: Foundation blocks remain fixed until a full line clear", font_size=18, color=WHITE),
            Text("5. Line Clears: Elementary Row Elimination zeroing rows, followed by D on stack", font_size=18, color=WHITE),
            Text("All mechanics are rigorous Elementary Matrix Operations!", font_size=19, color=c_green, weight=BOLD)
        ).arrange(DOWN, buff=0.22).move_to([0, 0, 0])
        
        final_rect = SurroundingRectangle(final_box, color="#3d4868", fill_color="#131722", fill_opacity=0.92, stroke_width=2, buff=0.3)
        
        self.play(Create(final_rect), FadeIn(final_box), run_time=2.0)
        self.wait(8.0)
        
        self.play(FadeOut(final_rect), FadeOut(final_box), run_time=1.5)
        self.wait(0.5)
