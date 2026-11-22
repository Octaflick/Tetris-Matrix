from manim import *

def create_matrix_mobject(data, cell_size=0.55, font_size=20, color_map=None, bracket_color=WHITE):
    """
    Creates a standalone matrix Mobject with vector brackets and styled entries without LaTeX.
    """
    rows = len(data)
    cols = len(data[0])
    
    entries = VGroup()
    row_groups = []
    
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
            entries.add(txt)
        row_groups.append(row_g)
        
    width = cols * cell_size
    height = rows * cell_size
    pad = 0.12
    bracket_width = 0.15
    
    left_x = -width / 2 - pad
    left_top = np.array([left_x + bracket_width, height / 2 + pad, 0])
    left_corner_top = np.array([left_x, height / 2 + pad, 0])
    left_corner_bot = np.array([left_x, -height / 2 - pad, 0])
    left_bot = np.array([left_x + bracket_width, -height / 2 - pad, 0])
    
    left_bracket = VMobject(color=bracket_color, stroke_width=3.0)
    left_bracket.set_points_as_corners([left_top, left_corner_top, left_corner_bot, left_bot])
    
    right_x = width / 2 + pad
    right_top = np.array([right_x - bracket_width, height / 2 + pad, 0])
    right_corner_top = np.array([right_x, height / 2 + pad, 0])
    right_corner_bot = np.array([right_x, -height / 2 - pad, 0])
    right_bot = np.array([right_x - bracket_width, -height / 2 - pad, 0])
    
    right_bracket = VMobject(color=bracket_color, stroke_width=3.0)
    right_bracket.set_points_as_corners([right_top, right_corner_top, right_corner_bot, right_bot])
    
    matrix_group = VGroup(left_bracket, right_bracket, entries)
    matrix_group.entries = entries
    matrix_group.row_groups = row_groups
    return matrix_group


class Scene3LiveComparison(Scene):
    def construct(self):
        self.camera.background_color = "#0e1117"
        
        # 1. Title Banner (~4s)
        sec_title = Text("Part 3: Live Tetris Engine via Matrix Operations", font_size=32, color=YELLOW, weight=BOLD)
        sec_sub = Text("Simultaneous Synchronization: Game Field ⟷ Matrix Algebra", font_size=22, color=LIGHT_GREY)
        sec_group = VGroup(sec_title, sec_sub).arrange(DOWN, buff=0.2).to_edge(UP, buff=0.5)
        
        self.play(Write(sec_title), run_time=1.4)
        self.play(FadeIn(sec_sub, shift=UP*0.2), run_time=1.0)
        self.wait(2.0)
        
        mini_banner = Text("Part 3: Tetris Engine (Board ⟷ Matrix Transformations)", font_size=24, color=YELLOW, weight=BOLD).to_edge(UP, buff=0.35)
        self.play(ReplacementTransform(sec_group, mini_banner), run_time=1.0)
        self.wait(0.8)
        
        # 2. Grid & Matrix Dimensions
        rows, cols = 6, 5
        cell_size = 0.65
        board_ox = -3.8
        board_oy = -0.3
        
        mat_ox = 3.6
        mat_oy = -0.3
        
        T_COLOR = "#bd93f9"
        BASE_COLOR = "#00d2d3"
        EMPTY_COLOR = "#222738"
        GRID_LINE = "#3d4868"
        
        c_map = {1: "#ff79c6", 2: "#00d2d3", 0: "#6272a4"}
        
        # Board Setup
        board_bg = Rectangle(
            width=cols * cell_size + 0.1,
            height=rows * cell_size + 0.1,
            color="#1a1f2c",
            fill_color="#131722",
            fill_opacity=1.0,
            stroke_width=2.5
        ).move_to([board_ox, board_oy, 0])
        
        board_label = Text("Tetris Game Field", font_size=22, color=WHITE).next_to(board_bg, UP, buff=0.25)
        
        # Initial Board State: T-piece at row 1 (indices 1,1; 1,2; 1,3; 2,2)
        initial_state = [
            [0, 0, 0, 0, 0],
            [0, 1, 1, 1, 0],
            [0, 0, 1, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [2, 2, 0, 2, 2],
        ]
        
        board_cells = {}
        board_group = VGroup(board_bg)
        
        for r in range(rows):
            for c in range(cols):
                cx = board_ox + (c - (cols - 1) / 2) * cell_size
                cy = board_oy + ((rows - 1) / 2 - r) * cell_size
                box = Square(side_length=cell_size, stroke_color=GRID_LINE, stroke_width=1.0).move_to([cx, cy, 0])
                
                val = initial_state[r][c]
                col = EMPTY_COLOR
                opac = 0.25
                if val == 1:
                    col = T_COLOR
                    opac = 0.95
                elif val == 2:
                    col = BASE_COLOR
                    opac = 0.9
                    
                sq = Square(side_length=cell_size - 0.08, fill_color=col, fill_opacity=opac, stroke_width=0).move_to([cx, cy, 0])
                board_cells[(r, c)] = sq
                board_group.add(box, sq)
                
        # Right Side: State Matrix A
        current_state = [row[:] for row in initial_state]
        mat_A = create_matrix_mobject(current_state, cell_size=0.55, font_size=21, color_map=c_map, bracket_color=YELLOW)
        mat_A.move_to([mat_ox, mat_oy, 0])
        mat_label = Text("State Matrix A (6 × 5)", font_size=22, color=WHITE).next_to(mat_A, UP, buff=0.25)
        
        # Center Divider
        divider = DashedLine(UP * 2.6, DOWN * 3.2, stroke_color="#3d4868", stroke_width=2).move_to([0, -0.3, 0])
        
        self.play(
            FadeIn(board_bg), FadeIn(board_label),
            LaggedStart(*[FadeIn(board_cells[(r, c)]) for r in range(rows) for c in range(cols)], lag_ratio=0.01),
            Create(divider),
            FadeIn(mat_A), FadeIn(mat_label),
            run_time=1.5
        )
        self.wait(1.5)
        
        # -------------------------------------------------------------
        # Action 1: Gravity Step (D x A) (~15s)
        # -------------------------------------------------------------
        action1_hud = Text("Action 1: Gravity Step ➜ Pre-Multiply D × A", font_size=20, color="#50fa7b", weight=BOLD)
        action1_hud.to_edge(DOWN, buff=0.55)
        
        self.play(FadeIn(action1_hud, shift=UP*0.2), run_time=0.8)
        self.wait(1.0)
        
        # Show calculation prompt above matrix
        formula1 = Text("New State = D × A", font_size=20, color="#50fa7b").next_to(mat_label, UP, buff=0.15)
        self.play(FadeIn(formula1), run_time=0.6)
        
        # Compute Downshift: rows shifted down
        state_after_d = [
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 1, 1, 1, 0],
            [0, 0, 1, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],  # for falling piece isolated or piece + base
        ]
        # preserve bottom foundation for visual realism
        state_after_d[5] = [2, 2, 0, 2, 2]
        
        # New matrix Mobject
        mat_A_next1 = create_matrix_mobject(state_after_d, cell_size=0.55, font_size=21, color_map=c_map, bracket_color=YELLOW)
        mat_A_next1.move_to([mat_ox, mat_oy, 0])
        
        # Animate board piece moving down while matrix transforms
        anim_board_gravity = []
        for r in range(rows):
            for c in range(cols):
                val_next = state_after_d[r][c]
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
                
        self.play(
            *anim_board_gravity,
            ReplacementTransform(mat_A, mat_A_next1),
            run_time=1.8
        )
        self.wait(2.5)
        
        expl_grav = Text("Row 1 dropped to Row 2, Row 2 to Row 3 (Gravity achieved!)", font_size=18, color=LIGHT_GREY).next_to(action1_hud, UP, buff=0.12)
        self.play(FadeIn(expl_grav), run_time=0.8)
        self.wait(3.5)
        
        self.play(
            FadeOut(action1_hud), FadeOut(formula1), FadeOut(expl_grav),
            run_time=0.8
        )
        self.wait(0.5)
        
        # -------------------------------------------------------------
        # Action 2: Player Lateral Move Right (A x R) (~15s)
        # -------------------------------------------------------------
        action2_hud = Text("Action 2: User Press [RIGHT] ➜ Post-Multiply A × R", font_size=20, color="#00d2d3", weight=BOLD)
        action2_hud.to_edge(DOWN, buff=0.55)
        
        self.play(FadeIn(action2_hud, shift=UP*0.2), run_time=0.8)
        self.wait(1.0)
        
        formula2 = Text("New State = A × R", font_size=20, color="#00d2d3").next_to(mat_label, UP, buff=0.15)
        self.play(FadeIn(formula2), run_time=0.6)
        
        # Shift T-piece right by 1 column
        state_after_r = [
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 1, 1, 1],
            [0, 0, 0, 1, 0],
            [0, 0, 0, 0, 0],
            [2, 2, 0, 2, 2],
        ]
        
        mat_A_next2 = create_matrix_mobject(state_after_r, cell_size=0.55, font_size=21, color_map=c_map, bracket_color=YELLOW)
        mat_A_next2.move_to([mat_ox, mat_oy, 0])
        
        anim_board_right = []
        for r in range(rows):
            for c in range(cols):
                val_next = state_after_r[r][c]
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
                
        self.play(
            *anim_board_right,
            ReplacementTransform(mat_A_next1, mat_A_next2),
            run_time=1.8
        )
        self.wait(2.5)
        
        expl_r = Text("Columns shifted right by 1 position (Post-multiplication by R)", font_size=18, color=LIGHT_GREY).next_to(action2_hud, UP, buff=0.12)
        self.play(FadeIn(expl_r), run_time=0.8)
        self.wait(3.5)
        
        self.play(
            FadeOut(action2_hud), FadeOut(formula2), FadeOut(expl_r),
            run_time=0.8
        )
        self.wait(0.5)
        
        # -------------------------------------------------------------
        # Action 3: Settling & Row Clear / Elimination (~18s)
        # -------------------------------------------------------------
        action3_hud = Text("Action 3: Line Clear ➜ Elementary Row Elimination (R₅ ➜ 0)", font_size=20, color="#ff5555", weight=BOLD)
        action3_hud.to_edge(DOWN, buff=0.55)
        
        self.play(FadeIn(action3_hud, shift=UP*0.2), run_time=0.8)
        self.wait(1.0)
        
        # Piece settles into bottom row (row index 5 becomes completely filled: [2, 2, 2, 2, 2])
        state_filled = [
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 1, 0],
            [2, 2, 1, 2, 2],  # FULL ROW!
        ]
        
        mat_A_filled = create_matrix_mobject(state_filled, cell_size=0.55, font_size=21, color_map=c_map, bracket_color=YELLOW)
        mat_A_filled.move_to([mat_ox, mat_oy, 0])
        
        anim_board_settle = []
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
                anim_board_settle.append(
                    board_cells[(r, c)].animate.set_fill(target_col, opacity=target_opac)
                )
                
        self.play(
            *anim_board_settle,
            ReplacementTransform(mat_A_next2, mat_A_filled),
            run_time=1.5
        )
        self.wait(1.5)
        
        # Highlight full row in flashing gold
        row_rect_board = Rectangle(width=cols * cell_size, height=cell_size, color=YELLOW, fill_color=YELLOW, fill_opacity=0.4, stroke_width=3)
        row_rect_board.move_to([board_ox, board_oy - ((rows - 1)/2 - 5) * cell_size, 0])
        # fix y position
        row_rect_board.move_to([board_ox, board_oy + ((rows - 1) / 2 - 5) * cell_size, 0])
        
        row_rect_mat = SurroundingRectangle(mat_A_filled.row_groups[5], color=YELLOW, buff=0.08, stroke_width=3)
        
        alert_full = Text("Row 6 is Full (All Non-Zero Entries)!", font_size=18, color=YELLOW).next_to(action3_hud, UP, buff=0.12)
        
        self.play(
            Create(row_rect_board),
            Create(row_rect_mat),
            FadeIn(alert_full),
            run_time=1.0
        )
        self.wait(2.5)
        
        # Eliminate row: flash white and clear to zeros
        state_cleared = [
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 1, 0],  # Remaining residue drops down via D
        ]
        
        mat_A_cleared = create_matrix_mobject(state_cleared, cell_size=0.55, font_size=21, color_map=c_map, bracket_color=YELLOW)
        mat_A_cleared.move_to([mat_ox, mat_oy, 0])
        
        anim_board_clear = []
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
                anim_board_clear.append(
                    board_cells[(r, c)].animate.set_fill(target_col, opacity=target_opac)
                )
                
        self.play(
            FadeOut(row_rect_board),
            FadeOut(row_rect_mat),
            *anim_board_clear,
            ReplacementTransform(mat_A_filled, mat_A_cleared),
            run_time=1.5
        )
        self.wait(2.5)
        
        expl_clear = Text("Row eliminated ➜ State matrix updated via Elementary Row Clear!", font_size=18, color="#50fa7b").next_to(action3_hud, UP, buff=0.12)
        self.play(ReplacementTransform(alert_full, expl_clear), run_time=0.8)
        self.wait(3.5)
        
        # -------------------------------------------------------------
        # Conclusion Summary (~7s)
        # -------------------------------------------------------------
        self.play(
            FadeOut(action3_hud), FadeOut(expl_clear),
            FadeOut(board_group), FadeOut(board_label),
            FadeOut(divider), FadeOut(mat_A_cleared), FadeOut(mat_label),
            FadeOut(mini_banner),
            run_time=1.2
        )
        self.wait(0.5)
        
        final_box = VGroup(
            Text("Conclusion: Matrix Mechanics of Tetris", font_size=32, color=YELLOW, weight=BOLD),
            Text("• Gravity: Successive Pre-Multiplication by D (Downshift)", font_size=20, color=WHITE),
            Text("• Lateral Movement: Post-Multiplication by L & R (Column Shifts)", font_size=20, color=WHITE),
            Text("• Line Clears: Elementary Row Elimination and Stack Shifts", font_size=20, color=WHITE),
            Text("Entire game dynamics are driven by Elementary Matrix Transformations!", font_size=20, color="#50fa7b", weight=BOLD)
        ).arrange(DOWN, buff=0.3).move_to([0, 0, 0])
        
        final_rect = SurroundingRectangle(final_box, color="#3d4868", fill_color="#131722", fill_opacity=0.9, stroke_width=2, buff=0.3)
        
        self.play(Create(final_rect), FadeIn(final_box), run_time=2.0)
        self.wait(6.0)
        
        self.play(FadeOut(final_rect), FadeOut(final_box), run_time=1.5)
        self.wait(0.5)
