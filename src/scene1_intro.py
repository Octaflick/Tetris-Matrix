from manim import *

def create_matrix_mobject(data, cell_size=0.6, font_size=24, color_map=None, bracket_color=WHITE):
    """
    Creates a matrix Mobject with custom vector brackets and styled entries without needing LaTeX.
    data: 2D list of numbers/strings
    color_map: optional dict mapping values to colors
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
            # Position relative to grid
            x = (c - (cols - 1) / 2) * cell_size
            y = ((rows - 1) / 2 - r) * cell_size
            txt.move_to([x, y, 0])
            row_g.add(txt)
            entries.add(txt)
        row_groups.append(row_g)
        
    width = cols * cell_size
    height = rows * cell_size
    pad = 0.15
    bracket_width = 0.18
    
    # Left bracket
    left_x = -width / 2 - pad
    left_top = np.array([left_x + bracket_width, height / 2 + pad, 0])
    left_corner_top = np.array([left_x, height / 2 + pad, 0])
    left_corner_bot = np.array([left_x, -height / 2 - pad, 0])
    left_bot = np.array([left_x + bracket_width, -height / 2 - pad, 0])
    
    left_bracket = VMobject(color=bracket_color, stroke_width=3.5)
    left_bracket.set_points_as_corners([left_top, left_corner_top, left_corner_bot, left_bot])
    
    # Right bracket
    right_x = width / 2 + pad
    right_top = np.array([right_x - bracket_width, height / 2 + pad, 0])
    right_corner_top = np.array([right_x, height / 2 + pad, 0])
    right_corner_bot = np.array([right_x, -height / 2 - pad, 0])
    right_bot = np.array([right_x - bracket_width, -height / 2 - pad, 0])
    
    right_bracket = VMobject(color=bracket_color, stroke_width=3.5)
    right_bracket.set_points_as_corners([right_top, right_corner_top, right_corner_bot, right_bot])
    
    matrix_group = VGroup(left_bracket, right_bracket, entries)
    matrix_group.entries = entries
    matrix_group.row_groups = row_groups
    return matrix_group


class Scene1TetrisMatrixIntro(Scene):
    def construct(self):
        # Background subtle styling
        self.camera.background_color = "#0e1117"
        
        # 1. Main Title Sequence
        title = Text("Linear Algebra of Tetris", font_size=44, color=YELLOW, weight=BOLD)
        subtitle = Text("Representing the Game Board as Matrix A", font_size=26, color=LIGHT_GREY)
        title_group = VGroup(title, subtitle).arrange(DOWN, buff=0.25).to_edge(UP, buff=0.5)
        
        self.play(Write(title), run_time=1.0)
        self.play(FadeIn(subtitle, shift=UP*0.2), run_time=0.8)
        self.wait(1.0)
        
        # Shrink and reposition title to top corner/edge
        mini_title = Text("Part 1: The Tetris State Matrix", font_size=28, color=YELLOW, weight=BOLD).to_edge(UP, buff=0.4)
        self.play(
            ReplacementTransform(title_group, mini_title),
            run_time=0.8
        )
        
        # 2. Setup Tetris Grid and Matrix Data
        # 6 rows x 5 columns grid for optimal visibility in 16:9
        rows, cols = 6, 5
        cell_size = 0.72
        
        # Board representation: 0 = empty, 1 = T-piece (purple), 2 = foundation blocks (blue)
        matrix_data = [
            [0, 0, 0, 0, 0],
            [0, 1, 1, 1, 0],
            [0, 0, 1, 0, 0],
            [0, 0, 0, 0, 0],
            [2, 2, 0, 0, 2],
            [2, 2, 2, 0, 2],
        ]
        
        T_COLOR = "#bd93f9"     # Purple
        BASE_COLOR = "#00d2d3"  # Cyan/Blue
        EMPTY_COLOR = "#222738"
        GRID_LINE_COLOR = "#3d4868"
        
        # Left Side: Tetris Board
        board_group = VGroup()
        board_cells = {}
        
        board_origin_x = -3.8
        board_origin_y = -0.4
        
        grid_bg = Rectangle(
            width=cols * cell_size + 0.1,
            height=rows * cell_size + 0.1,
            color="#1a1f2c",
            fill_color="#131722",
            fill_opacity=1.0,
            stroke_width=2.5
        ).move_to([board_origin_x, board_origin_y, 0])
        board_group.add(grid_bg)
        
        for r in range(rows):
            for c in range(cols):
                cx = board_origin_x + (c - (cols - 1) / 2) * cell_size
                cy = board_origin_y + ((rows - 1) / 2 - r) * cell_size
                
                cell_box = Square(side_length=cell_size, stroke_color=GRID_LINE_COLOR, stroke_width=1.2)
                cell_box.move_to([cx, cy, 0])
                
                val = matrix_data[r][c]
                if val == 1:
                    inner_sq = Square(
                        side_length=cell_size - 0.08,
                        fill_color=T_COLOR,
                        fill_opacity=0.95,
                        stroke_color="#ff79c6",
                        stroke_width=1.5
                    ).move_to([cx, cy, 0])
                elif val == 2:
                    inner_sq = Square(
                        side_length=cell_size - 0.08,
                        fill_color=BASE_COLOR,
                        fill_opacity=0.9,
                        stroke_color="#54a0ff",
                        stroke_width=1.5
                    ).move_to([cx, cy, 0])
                else:
                    inner_sq = Square(
                        side_length=cell_size - 0.08,
                        fill_color=EMPTY_COLOR,
                        fill_opacity=0.25,
                        stroke_color=EMPTY_COLOR,
                        stroke_width=0.5
                    ).move_to([cx, cy, 0])
                
                board_cells[(r, c)] = inner_sq
                board_group.add(cell_box, inner_sq)
                
        board_label = Text("Tetris Playing Field", font_size=24, color=WHITE).next_to(grid_bg, UP, buff=0.3)
        
        self.play(
            FadeIn(grid_bg),
            FadeIn(board_label),
            run_time=0.8
        )
        self.play(
            LaggedStart(
                *[FadeIn(board_cells[(r, c)], scale=0.8) for r in range(rows) for c in range(cols)],
                lag_ratio=0.02
            ),
            run_time=1.2
        )
        self.wait(0.6)
        
        # 3. Equivalence Arrow in Middle
        arrow = Text("⟷", font_size=48, color=YELLOW).move_to([0, board_origin_y, 0])
        equiv_text = Text("Isomorphic", font_size=16, color=LIGHT_GREY).next_to(arrow, UP, buff=0.15)
        
        self.play(FadeIn(arrow), FadeIn(equiv_text), run_time=0.6)
        
        # 4. Right Side: Matrix A
        matrix_origin_x = 3.6
        matrix_origin_y = board_origin_y
        
        color_map = {1: "#ff79c6", 2: "#00d2d3", 0: "#6272a4"}
        mat_mob = create_matrix_mobject(
            matrix_data,
            cell_size=cell_size,
            font_size=26,
            color_map=color_map,
            bracket_color=YELLOW
        ).move_to([matrix_origin_x, matrix_origin_y, 0])
        
        matrix_label = Text("State Matrix A  (6 × 5)", font_size=24, color=WHITE).next_to(mat_mob, UP, buff=0.3)
        
        self.play(
            FadeIn(matrix_label),
            Create(mat_mob[0]),  # Left bracket
            Create(mat_mob[1]),  # Right bracket
            run_time=0.8
        )
        self.play(
            LaggedStart(
                *[FadeIn(entry, scale=1.3) for entry in mat_mob.entries],
                lag_ratio=0.02
            ),
            run_time=1.2
        )
        self.wait(1.0)
        
        # 5. Explaining Cell Mapping (0 = Empty, 1/2 = Filled Block)
        # Highlight falling T-piece on both sides
        t_piece_indices = [(1, 1), (1, 2), (1, 3), (2, 2)]
        
        highlights_board = VGroup(*[
            SurroundingRectangle(board_cells[idx], color="#ff79c6", buff=0.03, stroke_width=3)
            for idx in t_piece_indices
        ])
        
        highlights_mat = VGroup(*[
            SurroundingRectangle(mat_mob.row_groups[r][c], color="#ff79c6", buff=0.08, stroke_width=3)
            for (r, c) in t_piece_indices
        ])
        
        legend_t = Text("Falling Tetromino  ➜  Non-Zero Submatrix (1s)", font_size=20, color="#ff79c6")
        legend_t.to_edge(DOWN, buff=0.6)
        
        self.play(
            Create(highlights_board),
            Create(highlights_mat),
            FadeIn(legend_t, shift=UP*0.2),
            run_time=1.0
        )
        self.wait(1.5)
        
        # Next: Highlight Empty Space (0s)
        empty_indices = [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4)]
        highlights_empty_board = VGroup(*[
            SurroundingRectangle(board_cells[idx], color="#6272a4", buff=0.03, stroke_width=2.5)
            for idx in empty_indices
        ])
        highlights_empty_mat = VGroup(*[
            SurroundingRectangle(mat_mob.row_groups[r][c], color="#6272a4", buff=0.08, stroke_width=2.5)
            for (r, c) in empty_indices
        ])
        
        legend_zero = Text("Empty Space  ➜  Zero Entries (0s)", font_size=20, color="#8be9fd")
        legend_zero.to_edge(DOWN, buff=0.6)
        
        self.play(
            ReplacementTransform(highlights_board, highlights_empty_board),
            ReplacementTransform(highlights_mat, highlights_empty_mat),
            ReplacementTransform(legend_t, legend_zero),
            run_time=1.0
        )
        self.wait(1.5)
        
        # Fade highlights out, summary conclusion
        summary = Text("Every game movement is an Algebraic Matrix Operation!", font_size=22, color=YELLOW, weight=BOLD)
        summary.to_edge(DOWN, buff=0.6)
        
        self.play(
            FadeOut(highlights_empty_board),
            FadeOut(highlights_empty_mat),
            ReplacementTransform(legend_zero, summary),
            run_time=0.8
        )
        self.wait(2.0)
        
        # Outro transition
        self.play(
            FadeOut(board_group),
            FadeOut(board_label),
            FadeOut(arrow),
            FadeOut(equiv_text),
            FadeOut(mat_mob),
            FadeOut(matrix_label),
            FadeOut(summary),
            FadeOut(mini_title),
            run_time=1.0
        )
        self.wait(0.5)
