import copy
import numpy as np
import time
import math

MAX_DEPTH = 3

class GameBoard:
    """
    The Gameboard State
    """

    def __init__(self, Board=None) -> None:
        if Board is not None:
            self.Board = np.array(Board)
        else:
            self.Board = np.zeros((4, 12), dtype=int)
        assert self.Board.shape == (4, 12)
        
    def ValidRowMoves(self):
        return np.nonzero(np.sum(self.Board,axis=1))[0]
    
    def ValidColMoves(self):
        return np.nonzero(np.sum(self.Board[:,0:6] + self.Board[:,6:12],axis=0))[0]

    def MoveRow(self, row, num):
        assert 0 <= row <= 3
        assert 0 <= num <= 11
        self.Board[3 - row] = np.take(self.Board[3 - row], range(0-num, 12-num), mode='wrap')

    def MoveCol(self, col, num):
        assert 0 <= col <= 11  # TODO - Can actually make this 5
        assert 0 <= num <= 7
        TempCols = self.Board[:, [col, col - 6]]
        for _ in range(num):
            TempCols = np.take(TempCols, [1,3,0,5,2,7,4,6])
        self.Board[:, [col, col - 6]] = np.reshape(TempCols, (4,2))

    def NumEnemies(self):
        return self.Board.sum()

    def AtkHammer(self, Col):
        self.Board[2:4, Col - 1 : Col + 1] = 0
        pass

    def AtkBoot(self, Col):
        self.Board[:, Col] = 0

    def Hash(self):
        return hash(str(self.Board))

    def __str__(self) -> str:
        return np.array2string(self.Board)

    def __deepcopy__(self, memo=None):
        return GameBoard(copy.deepcopy(self.Board))


def SolveBoard(Board: GameBoard, NumMoves=None):
    """
    Solve any given board
    """
    Moves = []
    if NumMoves is None:
        # Initial Solve call
        NumMoves = MAX_DEPTH

    # Rows
    for i in Board.ValidRowMoves():
        for j in range(1, 12): # Start at once since move of 0 is wasteful
            TempBoard: GameBoard = copy.deepcopy(Board)
            TempBoard.MoveRow(i, j)
            Moves.append({"Board": TempBoard, "Move": "Row", "Loc": i, "Shift": j})
    # Cols
    for i in range(0, 6):  # Only need to do 6 out of twelve since they are connected
        for j in range(1, 8): # Start at once since move of 0 is wasteful
            TempBoard: GameBoard = copy.deepcopy(Board)
            TempBoard.MoveCol(i, j)
            Moves.append({"Board": TempBoard, "Move": "Col", "Loc": i, "Shift": j})

    if not Moves:
        return False, []

    for Move in Moves:
        Win = SimAttack(Move["Board"])
        if Win:
            return True, [Move]
    
    # Search for a minimal number of moves solution first
    for Num in range(1,NumMoves):
        for Move in Moves:
            Win, SubMoves = SolveBoard(Move["Board"], Num)
            if Win:
                Result = [Move]
                Result.extend(SubMoves)
                return True, Result

    return False, []


def SimAttack(Board: GameBoard):
    """
    Simulate all the possible attacks
    """
    if Board.NumEnemies() == 0:
        return False
    
    MaxNumAttacks = math.ceil(Board.NumEnemies() / 4)
    BootAttacks = 0
    TempBoard: GameBoard = copy.deepcopy(Board)
    # Boots
    for i in range(0, 12):
        if TempBoard.Board[0][i] or TempBoard.Board[1][i]:
            TempBoard.AtkBoot(i)
            BootAttacks += 1

    HammerAttacksBoard = copy.deepcopy(TempBoard)
    HammerAttacks = 0
    # Hammer
    for i in range(0, 12):
        if HammerAttacksBoard.Board[2][i] or HammerAttacksBoard.Board[3][i]:
            HammerAttacksBoard.AtkHammer(i)
            HammerAttacks += 1

    if (HammerAttacks + BootAttacks) <= MaxNumAttacks:
        return True
    
    HammerAttacksBoard = copy.deepcopy(TempBoard)
    HammerAttacks = 0
    # Hammer - Shifted to cover edge cases
    for i in range(-1, -13, -1):
        if HammerAttacksBoard.Board[2][i] or HammerAttacksBoard.Board[3][i]:
            HammerAttacksBoard.AtkHammer(i)
            HammerAttacks += 1

    if (HammerAttacks + BootAttacks) <= MaxNumAttacks:
        return True

    return False

def PrintResult(Moves):
    for Move in Moves:
        if Move["Move"] == "Row":
            if Move['Shift'] > 6:
                Dir, Shift = "AntiClockwise", 12-Move['Shift']
            else:
                Dir, Shift = "Clockwise", Move['Shift']
        if Move["Move"] == "Col":
            if Move['Shift'] > 4:
                Dir, Shift = "Outwards", 8-Move['Shift']
            else:
                Dir, Shift = "Inwards", Move['Shift']
        print(f"Move {Move['Move']} {Move['Loc']} {Dir} by {Shift}")

    print(f"Final Board State:\n{Moves[-1]['Board']}")


if __name__ == "__main__":
    # unittest.main()

    print("Enter board:\n0123456789AB")
    InputPos = ""
    for _ in range(4):
        Input = input()
        assert len(Input) == 12, "Uhh wrong length?"
        InputPos += Input
#     InputPos = "\
# 000000010000\
# 000000000010\
# 010000110000\
# 010000110000"
#     InputPos = "\
# 000000010000\
# 000000000010\
# 100001100000\
# 010000110000"
#     InputPos = "\
# 010001000000\
# 101110000000\
# 010001000000\
# 101110000000"
    
    InputPos = np.array([int(c) for c in InputPos])
    InputPos.resize((4, 12))

    Board = GameBoard(InputPos)
    print(f"Solving Board:\n{Board}")
    StartTime = time.time()
    Win, Moves = SolveBoard(Board)
    print(f"Finished: {time.time() - StartTime} seconds")
    if Win:
        PrintResult(Moves)
    else:
        print("No solution found")
