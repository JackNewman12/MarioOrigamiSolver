from ast import Num
import copy
import multiprocessing
import numpy as np
import unittest
import time

SeenBoards = set()
SeenAttacks = dict()

class GameBoardTest(unittest.TestCase):
    def test_Moves(self):
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

    def test_Attack(self):
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

    # def test_Score(self):
    #     Board = GameBoard(
    #         [
    #             [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    #             [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    #             [0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0],
    #             [0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0],
    #         ]
    #     )
    #     BestAttacks = SimAttack(Board, 1)

    # def test_Solve(self):
    #     Board = GameBoard(
    #         [
    #             [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    #             [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    #             [0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0],
    #             [0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0],
    #         ],
    #         NumMoves=2, NumAttacks=2
    #     )
    #     Result = SolveBoard(Board)
    #     PrintResult(Result)
    #     Board = GameBoard(
    #         [
    #             [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
    #             [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    #             [0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0],
    #             [0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0],
    #         ],
    #         NumMoves=2, NumAttacks=2
    #     )
    #     Result = SolveBoard(Board)
    #     PrintResult(Result)


class GameBoard:
    def __init__(self, Board=None, NumMoves=1, NumAttacks=1) -> None:
        if Board is not None:
            self.Board = np.array(Board)
        else:
            self.Board = np.zeros((4, 12), dtype=int)
        assert self.Board.shape == (4, 12)
        self.NumMoves = NumMoves
        self.NumAttacks = NumAttacks

    def MoveRow(self, row, num):
        assert(0 <= row <= 3)
        assert(0 <= num <= 11)
        self.Board[3-row] = np.roll(self.Board[3-row], num)

    def MoveCol(self, col, num):
        assert(0 <= col <= 11)
        assert(0 <= num <= 7)
        TargetCols = self.Board[:,[col,col-6]]
        TargetCols[:,1] = np.flip(TargetCols[:,1])
        TargetCols = np.roll(TargetCols.T, num).T
        TargetCols[:,1] = np.flip(TargetCols[:,1])
        self.Board[:,[col,col-6]] = TargetCols

    def NumEnemies(self):
        return self.Board.sum()

    def AtkHammer(self, Col):
        self.Board[2:4, Col-1:Col+1] = 0
        pass

    def AtkBoot(self,  Col):
        self.Board[:,Col] = 0

    def Hash(self):
        return hash(str(self.Board))

    def __str__(self) -> str:
        return np.array2string(self.Board)

def ParallelSolve(Move, NumMoves):
    # Note continue even if we killed all enemies - We are looking for multiplers first
    Result = [Move]
    Result.extend(SolveBoard(Move["Board"], NumMoves))
    return Result

def SolveBoard(Board: GameBoard, NumMoves=None):
    Moves = []
    if not NumMoves:
        # Get from board def
        NumMoves = Board.NumMoves
    NumMoves -= 1
    # Rows
    for i in range(0,4):
        for j in range(0,12):
            TempBoard: GameBoard = copy.deepcopy(Board)
            TempBoard.MoveRow(i, j)
            Hash = TempBoard.Hash()
            if Hash in SeenBoards:
                continue
            SeenBoards.add(Hash)
            Moves.append({"Board":TempBoard, "Move":"Row", "Loc": i, "Shift":j})
    # Cols
    for i in range(0,6): # Only need to do 6 out of twelve since they are connected
        for j in range(0,8):
            TempBoard: GameBoard = copy.deepcopy(Board)
            TempBoard.MoveCol(i, j)
            Hash = TempBoard.Hash()
            if Hash in SeenBoards:
                continue
            SeenBoards.add(Hash)
            Moves.append({"Board":TempBoard, "Move":"Col", "Loc": i, "Shift":j})
    
    if not Moves:
        return []

    for Move in Moves:
        BestAttacks = SimAttack(Move["Board"])
        if BestAttacks:
            Move['Attacks'] = BestAttacks
            Move["EnemiesLeft"] = BestAttacks[-1]['Enemies']

    # Find the board that would result in the least enemies unattacked (and then my number of attacks required)
    Moves = sorted(Moves, key=lambda k: (k.get('EnemiesLeft',999), len(k.get('Attacks',range(10)))))
    if NumMoves == 0:
        return [Moves[0]]
    Results = []
    for Move in Moves:
        # Note continue even if we killed all enemies - We are looking for multiplers first
        Result = [Move]
        Result.extend(SolveBoard(Move["Board"], NumMoves))
        Results.append(Result)
    Results = sorted(Results, key=lambda k: (k[-1].get('EnemiesLeft', 999),len(k[-1].get('Attacks',range(10)))))
    return Results[0]



def SimAttack(Board: GameBoard, NumAttacks=None):
    if not NumAttacks:
        # Get it from the board
        NumAttacks = Board.NumAttacks
    Attacks = []
    NumAttacks -= 1
    if Board.NumEnemies() == 0:
        return []
    for i in range(0,12):
        for j in ["Hammer", "Boot"]:
            TempBoard: GameBoard = copy.deepcopy(Board)
            StartEnemies = TempBoard.NumEnemies()
            if j == "Hammer":
                TempBoard.AtkHammer(i)
            if j == "Boot":
                TempBoard.AtkBoot(i)
            FinishEnemies = TempBoard.NumEnemies()
            if FinishEnemies == 0 or FinishEnemies == StartEnemies - 4: # Maybe?
                # Don't bother processing attacks that did nothing
                Attacks.append({"Move":j, "Col":i, "Board": TempBoard, "Enemies":FinishEnemies})
    if not Attacks:
        return []
    Attacks = sorted(Attacks, key=lambda k: k['Enemies'])
    if NumAttacks == 0:
        return [Attacks[0]]
    Results = []
    for Atk in Attacks:
        Result = [Atk]
        Result.extend(SimAttack(Atk["Board"], NumAttacks))
        if Result[-1]['Enemies'] == 0:
            return Result
        Results.append(Result)
    # Simulated a bunch of moves - Choose best to pass up
    Results = sorted(Results, key=lambda k:(k[-1]["Enemies"], len(k)))
    return Results[0]
            
def PrintResult(Result):
    for Move in Result:
        print(f"Move {Move['Move']} {Move['Loc']} by {Move['Shift']}")

    LastMove = Result[-1]
    Attacks = LastMove["Attacks"]
    for Attack in Attacks:
        print(f"Attack Col {Attack['Col']} with {Attack['Move']}")

    print(f"Result leaves {LastMove['EnemiesLeft']} enemies untouched")
    print(f"Final Board State:\n{LastMove['Board']}")

if __name__ == "__main__":
    # unittest.main()
    
    # print("Enter board:\n0123456789AB")
    # InputPos = ""
    # for _ in range(4):
    #     Input = input()
    #     assert len(Input) == 12, "Uhh wrong length?"
    #     InputPos += Input
    # NumMoves = int(input("Number Of Moves: "))
    # NumAttacks = int(input("Number Of Attacks: "))

    InputPos= '\
000000010000\
000000000010\
010000110000\
010000110000'
    NumMoves = 2
    NumAttacks = 3

#     InputPos= '\
# 000000000000\
# 000000000000\
# 000001001000\
# 000001001000'
#     NumMoves = 3
#     NumAttacks = 3

#     InputPos= '\
# 010101010101\
# 010101010101\
# 010101010101\
# 101010101010'
#     NumMoves = 1
#     NumAttacks = 6

    InputPos = np.array([int(c) for c in InputPos])
    InputPos.resize((4,12))

    StartTime = time.time()
    Board = GameBoard(InputPos, NumMoves=NumMoves, NumAttacks=NumAttacks)
    print(f"Here we go! Starting Board:\n{Board}")
    SeenBoards.add(hash(str(Board.Board)))
    Result = SolveBoard(Board)
    if Result:
        PrintResult(Result)
    print(f"Finished: {time.time() - StartTime} seconds")
