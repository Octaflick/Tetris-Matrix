Context - I want to create an animation video showing Matrix operations and elementary row and column operations. I will be using Manim library to generate animations of matrices. Including input and output matrices and how they shift. 
All the work is to be uploaded on Github at the end.

Theme & Mathematical Metaphor:
- Tetris Game theme: Tetris grid represented as an m x n matrix A (empty cells = 0, filled block cells = 1 or colored values).
- Shift Operators as Standard Matrices:
  - 'D' (Downshift Operator): Pre-multiplied elementary shift matrix ($D \times A$) shifting rows downward.
  - 'U' (Upshift Operator): Pre-multiplied shift matrix ($U \times A$) shifting rows upward.
  - 'L' (Leftshift Operator): Post-multiplied shift matrix ($A \times L$) shifting columns to the left.
  - 'R' (Rightshift Operator): Post-multiplied shift matrix ($A \times R$) shifting columns to the right.

Detailed Scene Breakdown:

Scene 1: Introduction to Tetris as Matrix A
- Introduce Tetris playing field as grid / matrix $A$.
- Visual bridge: blocks map to non-zero values / 1s, empty space to 0s.

Scene 2: Matrix Multiplication Mechanics (Row vs. Column Perspectives)
- General Matrix Multiplication $A \times B$:
  1. Row Perspective (Pre-multiplication / Row Combinations):
     - Multiplying from the left: $B \times A$.
     - Each row of the result is a linear combination of rows of $A$, weighted by entries in $B$.
     - Concrete Intro of 'D' (Downshift Matrix): Show how a sub-diagonal matrix $D$ acts on rows of $A$ to shift each row down ($R_i \to R_{i+1}$).
  2. Column Perspective (Post-multiplication / Column Combinations):
     - Multiplying from the right: $A \times B$.
     - Each column of the result is a linear combination of columns of $A$, weighted by entries in $B$.
     - Concrete Intro of 'R' (Rightshift Matrix): Show how super-diagonal matrix $R$ acts on columns of $A$ to shift each column right ($C_j \to C_{j+1}$).
  3. Introduce $U$ and $L$ as reciprocal vertical and horizontal shift operators.

Scene 3: Side-by-Side Dynamic Comparison (Tetris Board vs. Matrix Algebra)
- Split Screen layout (16:9):
  - Left Side: Graphical Tetris board with colorful falling tetromino (e.g., T-piece or L-piece).
  - Right Side: Live matrix equation updating dynamically.
- Action 1 - Gravity:
  - Piece falls one step $\leftrightarrow$ Compute $D \times A$, showing output matrix and block moving down.
- Action 2 - Lateral Move (Right):
  - Player taps right $\leftrightarrow$ Compute $A \times R$, showing block shifted to next column.
- Action 3 - Lateral Move (Left):
  - Player taps left $\leftrightarrow$ Compute $A \times L$.
- Action 4 - Line Clear & Row Elimination:
  - Row fills up $\to$ Row clear elimination $R_k \to 0$, then upper rows downshifted via $D$.

Instructions - You will setup manim and generate animations after confirming the final output and export it.

Output - 1080p 16:9

Environment & Status:
- Virtual environment created (`.venv`).
- System tools: `ffmpeg`, `cairo`, `pango`, `pkgconf` configured.
- Python Manim: **Manim Community v0.22.1** installed and verified.
- Rendering Engine: Manim native Pango vector rendering (`Text`, `VGroup`, custom pixel-perfect matrix brackets and grid blocks) — fast, zero external TeX bottleneck, completely self-contained.
- Video Export Directory: `raw/` for rendered video outputs.
- Source Directory: `src/` modular scene code.
- Scene 1 (`src/scene1_intro.py`): Implementation ready, rendering to `raw/Scene1TetrisMatrixIntro.mp4`.
- Git: Repository initialized, `.gitignore` configured to keep repo clean of video/media cache artifacts.


Environment & Status:
- Virtual environment created (`.venv`).
- System tools: `ffmpeg`, `cairo`, `pango`, `pkgconf` configured.
- Python Manim: **Manim Community v0.22.1** installed and verified.
- Rendering Engine: Manim native Pango vector rendering (`Text`, `VGroup`, custom pixel-perfect matrix brackets and grid blocks) — fast, zero external TeX bottleneck, completely self-contained.
- Video Export Directory: `raw/` for rendered video outputs.
- Source Directory: `src/` modular scene code.
- Scene 1 (`src/scene1_intro.py`): Implementation ready, rendering to `raw/Scene1TetrisMatrixIntro.mp4`.
- Git: Repository initialized, `.gitignore` configured to keep repo clean of video/media cache artifacts.