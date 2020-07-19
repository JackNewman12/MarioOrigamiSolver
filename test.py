import unittest
from solver import GameBoard
import numpy as np

class GameBoardTest(unittest.TestCase):
    """
    Basic testing to make sure the basic move pieces / attacks work
    """

    def test_moves(self):
        Board = GameBoard(
            [
                [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0],
                [0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0],
                [0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0],
                [0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1],
            ]
        )
        Board.MoveRow(2, 3)
        self.assertTrue(
            (
                Board.Board
                == np.array(
                    [
                        [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0],
                        [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0],
                        [0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0],
                        [0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1],
                    ]
                )
            ).all()
        )
        Board.MoveRow(3, 9)
        self.assertTrue(
            (
                Board.Board
                == np.array(
                    [
                        [0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0],
                        [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0],
                        [0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0],
                        [0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1],
                    ]
                )
            ).all()
        )
        Board.MoveCol(3, 2)
        self.assertTrue(
            (
                Board.Board
                == np.array(
                    [
                        [0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
                        [1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0],
                        [0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0],
                        [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
                    ]
                )
            ).all()
        )
        Board.MoveCol(6, 3)
        self.assertTrue(
            (
                Board.Board
                == np.array(
                    [
                        [0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 1, 1, 0, 1, 0, 1, 0, 0, 0],
                        [1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0],
                        [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
                    ]
                )
            ).all()
        )

    def test_attack(self):
        Board = GameBoard(
            [
                [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 1, 1, 1, 0, 1, 1, 1, 0, 0, 0],
                [0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0],
            ]
        )
        Board.AtkBoot(3)
        self.assertTrue(
            (
                Board.Board
                == np.array(
                    [
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 1, 0, 1, 0, 1, 1, 1, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
                    ]
                )
            ).all()
        )
        Board.AtkHammer(7)
        self.assertTrue(
            (
                Board.Board
                == np.array(
                    [
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    ]
                )
            ).all()
        )

if __name__ == "__main__":
    unittest.main()