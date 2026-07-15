# nine-mens-morris-ai
Implementation of Minimax and Alpha-Beta search algorithms for Nine Men's Morris with an improved heuristic evaluation function.

Overview
This project implements an AI agent for the board game Nine Men's Morris using classic game-tree search algorithms.
The AI supports both the opening phase and the midgame/endgame, and includes an improved heuristic evaluation function for stronger decision making.

Features
  Minimax Search
  Alpha-Beta Pruning
  Improved Static Evaluation Function
  Opening Move Generator
  Midgame / Endgame Move Generator
  White and Black Player Support

Algorithms
Minimax
Searches the game tree assuming both players play optimally.

Alpha-Beta Pruning
Reduces the number of evaluated positions while producing the same optimal move as Minimax.

Improved Evaluation Function
The improved heuristic considers:
   Piece difference
   Mill formation
   Potential mills
   Board control
   Mobility
   Winning positions

Project Structure
   ABGame.py
   ABOpening.py
   MiniMaxGame.py
   MiniMaxGameBlack.py
   MiniMaxGameImproved.py
   MiniMaxOpening.py
   MiniMaxOpeningBlack.py
   MiniMaxOpeningImproved.py

