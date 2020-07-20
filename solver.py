import copy
import numpy as np
import time
import math

MAX_DEPTH = 3

class GameBoard:
    """
    The Gameboard State
    """

    def __init__(self, Board=None, NumMoves=None, NumAttacks=None) -> None:
        if Board is not None:
            self.Board = np.array(Board)
        else:
            self.Board = np.zeros((4, 12), dtype=int)
        assert self.Board.shape == (4, 12)
        
        if NumMoves:
            self.NumMoves = NumMoves
        else:
            self.NumMoves = MAX_DEPTH
        
        if NumAttacks:
            self.NumAttacks = NumAttacks
        else:
            self.NumAttacks = math.ceil(self.NumEnemies() / 4)

    def ValidRowMoves(self):
        return np.nonzero(np.sum(self.Board,axis=1))[0]
    
    def ValidColMoves(self):
        return np.nonzero(np.sum(self.Board[:,0:6] + self.Board[:,6:12],axis=0))[0]

    def MoveRow(self, row, num):
        assert 0 <= row <= 3
        assert 0 <= num <= 11
        self.Board[3 - row] = np.roll(self.Board[3 - row], num)

    def MoveCol(self, col, num):
        assert 0 <= col <= 11  # TODO - Can actually make this 5
        assert 0 <= num <= 7
        # TODO - Whatever this mess is
        TargetCols = self.Board[:, [col, col - 6]]
        TargetCols[:, 1] = np.flip(TargetCols[:, 1])
        TargetCols = np.roll(TargetCols.T, num).T
        TargetCols[:, 1] = np.flip(TargetCols[:, 1])
        self.Board[:, [col, col - 6]] = TargetCols

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


def SolveBoard(Board: GameBoard, NumMoves=None):
    """
    Solve any given board
    """
    Moves = []
    if NumMoves is None:
        # Initial Solve - Get from board def
        NumMoves = Board.NumMoves

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
        Win, _ = SimAttack(Move["Board"])
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
        return False, []

    TempBoard: GameBoard = copy.deepcopy(Board)
    BootAttacks = []
    # Boots
    for i in range(0, 12):
        if TempBoard.Board[0][i] or TempBoard.Board[1][i]:
            TempBoard.AtkBoot(i)
            BootAttacks.append(
                {"Move": "Boot", "Col": i}
            )

    HammerAttacksBoard = copy.deepcopy(TempBoard)
    HammerAttacks = []
    # Hammer
    for i in range(0, 12):
        if HammerAttacksBoard.Board[2][i] or HammerAttacksBoard.Board[3][i]:
            HammerAttacksBoard.AtkHammer(i)
            HammerAttacks.append(
                {"Move": "Hammer", "Col": i}
            )
    if (len(HammerAttacks) + len(BootAttacks)) <= Board.NumAttacks:
        return True, BootAttacks.extend(HammerAttacks)
    
    HammerAttacksBoard = copy.deepcopy(TempBoard)
    HammerAttacks = []
    # Hammer - Shifted to cover edge cases
    for i in range(-1, -13, -1):
        if HammerAttacksBoard.Board[2][i] or HammerAttacksBoard.Board[3][i]:
            HammerAttacksBoard.AtkHammer(i)
            HammerAttacks.append(
                {"Move": "Hammer", "Col": i}
            )
    if (len(HammerAttacks) + len(BootAttacks)) <= Board.NumAttacks:
        return True, BootAttacks.extend(HammerAttacks)

    return False, []

def PrintResult(Moves):
    for Move in Moves:
        print(f"Move {Move['Move']} {Move['Loc']} by {Move['Shift']}")
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
