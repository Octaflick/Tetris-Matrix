Context - I want to create an animation video showing Matrix operations and elementary row and column operations. I will be using Manim library to generate animations of matrices. Including input and output matrices and how they shift. 
All the work is to be uploaded on Github at the end.

Theme & Mathematical Metaphor:
- Tetris Game theme: Tetris grid represented as an m x n matrix A (empty cells = 0, filled block cells = 1 or colored values).
- Shift Operators as Standard Matrices:
  - 'D' (Downshift Operator): Pre-multiplied elementary shift matrix ($D \times A$) shifting rows downward.
  - 'U' (Upshift Operator): Pre-multiplied shift matrix ($U \times A$) shifting rows upward.
  - 'L' (Leftshift Operator): Post-multiplied shift matrix ($A \times L$) shifting columns to the left.
  - 'R' (Rightshift Operator): Post-multiplied shift matrix ($A \times R$) shifting columns to the right.
- Matrix Multiplication Mechanics:
  - Clear visual breakdown of $A \times B$ where $B$ (or operator matrix) governs the transformation/operation.
  - Row-by-column dot product visual highlighting (rows of first matrix sweeping across columns of second matrix).
  - Showing how transformation matrices act on state matrices to produce new outputs.
- Elementary Operations:
  - Downshifting & gravity.
  - Line clears / row elimination ($R_k \to 0$) and row combination.
  - Column shifts (horizontal piece movement).

Instructions - You will setup manim and generate animations after confirming the final output and export it.

Output - 1080p 16:9

Environment & Status:
- Virtual environment created (`.venv`).
- System tools: `ffmpeg`, `cairo`, `pango`, `pkgconf` configured.
- Python Manim: **Manim Community v0.22.1** installed and verified.
- Rendering Engine: Manim native Pango vector rendering (`Text`, `VGroup`, custom pixel-perfect matrix brackets and grid blocks) — fast, zero external TeX bottleneck, completely self-contained.
- Git: Repository initialized, `.gitignore` configured to keep repo clean of video/media cache artifacts.


Environment & Status:
- Virtual environment created (`.venv`).
- System tools: `ffmpeg`, `cairo`, `pango`, `pkgconf` configured.
- Python Manim: **Manim Community v0.22.1** installed and verified.
- Rendering Engine: Manim native Pango vector rendering (`Text`, `VGroup`, custom pixel-perfect matrix brackets and grid blocks) — fast, zero external TeX bottleneck, completely self-contained.
- Git: Repository initialized, `.gitignore` configured to keep repo clean of video/media cache artifacts.