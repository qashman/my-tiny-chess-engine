"""Tests for main.py: apply_move must stay equivalent to the original version,
and the agent must pick a legal move. Standard library only.

Run with:  python -m unittest -v
"""

import random
import unittest

import main


# The original apply_move, frozen as the oracle for the optimised version.
def apply_move_original(board, move):
    new_board = list(board)
    src = (int(move[1]) - 1) * 8 + (ord(move[0]) - 97)
    dst = (int(move[3]) - 1) * 8 + (ord(move[2]) - 97)
    piece = new_board[src]
    new_board[dst] = piece
    new_board[src] = 0
    if piece == 1 and dst >= 56: new_board[dst] = 5
    if piece == 8 and dst <= 7:  new_board[dst] = 12
    return new_board


START = [
    4, 2, 3, 5, 6, 3, 2, 4,
    1, 1, 1, 1, 1, 1, 1, 1,
    0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0,
    8, 8, 8, 8, 8, 8, 8, 8,
    11, 9, 10, 12, 13, 10, 9, 11,
]


class FakeObservation:
    def __init__(self, board, moves, mark=1):
        self.board = board
        self.legal_moves = moves
        self.mark = mark


class ApplyMoveTest(unittest.TestCase):
    def test_quiet_move_matches_original(self):
        board = START[:]
        move = "e2e4"
        src = 12  # e2
        dst = 28  # e4
        self.assertEqual(main.apply_move(board, move), apply_move_original(board, move))
        self.assertEqual(main.apply_move(board, move)[src], 0)
        self.assertEqual(main.apply_move(board, move)[dst], 1)

    def test_promotion_white(self):
        board = [0] * 64
        board[52] = 1  # white pawn on e7
        move = "e7e8"
        self.assertEqual(main.apply_move(board, move), apply_move_original(board, move))
        self.assertEqual(main.apply_move(board, move)[60], 5)

    def test_promotion_black(self):
        board = [0] * 64
        board[12] = 8  # black pawn on e2
        move = "e2e1"
        self.assertEqual(main.apply_move(board, move), apply_move_original(board, move))
        self.assertEqual(main.apply_move(board, move)[4], 12)

    def test_pawn_not_on_promotion_rank_is_untouched(self):
        board = [0] * 64
        board[44] = 1  # white pawn on e6, moving to e7
        move = "e6e7"
        self.assertEqual(main.apply_move(board, move), apply_move_original(board, move))
        self.assertEqual(main.apply_move(board, move)[52], 1)

    def test_board_not_mutated(self):
        board = START[:]
        main.apply_move(board, "e2e4")
        self.assertEqual(board, START)

    def test_equivalence_over_every_square_pair(self):
        for src in range(64):
            for dst in range(64):
                if src == dst:
                    continue
                board = [0] * 64
                board[src] = 1 if src < 8 else 8
                move = "abcdefgh"[src % 8] + str(src // 8 + 1) + "abcdefgh"[dst % 8] + str(dst // 8 + 1)
                self.assertEqual(
                    main.apply_move(board, move), apply_move_original(board, move),
                    "differs for %s" % move,
                )


class AgentTest(unittest.TestCase):
    def test_returns_a_legal_move(self):
        moves = ["e2e4", "d2d4", "g1f3"]
        self.assertIn(main.agent(FakeObservation(START, moves), None), moves)

    def test_no_legal_moves_returns_none(self):
        self.assertIsNone(main.agent(FakeObservation(START, []), None))

    def test_prefers_capture(self):
        board = START[:]
        board[44] = 1   # white pawn on e6
        board[36] = 11  # black rook on e5, capturable
        moves = ["e6e7", "e6e5"]
        self.assertEqual(main.agent(FakeObservation(board, moves), None), "e6e5")

    def test_black_perspective(self):
        board = START[:]
        board[28] = 8   # black pawn on e4
        board[36] = 4   # white rook on e5, capturable
        moves = ["e4e3", "e4e5"]
        self.assertEqual(main.agent(FakeObservation(board, moves, mark=2), None), "e4e5")


if __name__ == "__main__":
    unittest.main()
