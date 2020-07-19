import copy
import numpy as np
import time

gSeenBoards = set()
gPerfectMoves = False

class GameBoard:
    """
    The Gameboard State
    """

    def __init__(self, Board=None, NumMoves=1, NumAttacks=1) -> None:
        if Board is not None:
            self.Board = np.array(Board)
        else:
            self.Board = np.zeros((4, 12), dtype=int)
        assert self.Board.shape == (4, 12)
        self.NumMoves = NumMoves
        self.NumAttacks = NumAttacks

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
    if not NumMoves:
        # Initial Solve - Get from board def
        NumMoves = Board.NumMoves
    NumMoves -= 1
    # Rows
    for i in range(0, 4):
        for j in range(0, 12):
            TempBoard: GameBoard = copy.deepcopy(Board)
            TempBoard.MoveRow(i, j)
            Hash = TempBoard.Hash()
            if Hash in gSeenBoards:
                continue
            gSeenBoards.add(Hash)
            Moves.append({"Board": TempBoard, "Move": "Row", "Loc": i, "Shift": j})
    # Cols
    for i in range(0, 6):  # Only need to do 6 out of twelve since they are connected
        for j in range(0, 8):
            TempBoard: GameBoard = copy.deepcopy(Board)
            TempBoard.MoveCol(i, j)
            Hash = TempBoard.Hash()
            if Hash in gSeenBoards:
                continue
            gSeenBoards.add(Hash)
            Moves.append({"Board": TempBoard, "Move": "Col", "Loc": i, "Shift": j})

    if not Moves:
        return []

    for Move in Moves:
        BestAttacks = SimAttack(Move["Board"])
        if BestAttacks:
            Move["Attacks"] = BestAttacks
            Move["EnemiesLeft"] = BestAttacks[-1]["Enemies"]

    # Find the board that would result in the least enemies unattacked
    # (and then my number of attacks required)
    Moves = sorted(
        Moves,
        key=lambda k: (k.get("EnemiesLeft", 999), len(k.get("Attacks", range(10)))),
    )
    if NumMoves == 0:
        return [Moves[0]]
    
    Results = []
    for Move in Moves:
        Result = [Move]
        Result.extend(SolveBoard(Move["Board"], NumMoves))
        if Result[-1].get('EnemiesLeft',999) == 0:
            return Result
        Results.append(Result)
    Results = sorted(
        Results,
        key=lambda k: (
            k[-1].get("EnemiesLeft", 999),
            len(k[-1].get("Attacks", range(10))),
        ),
    )
    return Results[0]


def SimAttack(Board: GameBoard, NumAttacks=None):
    """
    Simulate all the possible attacks
    """
    if not NumAttacks:
        # Inital Sim - Get it from the board
        NumAttacks = Board.NumAttacks
    Attacks = []
    NumAttacks -= 1
    if Board.NumEnemies() == 0:
        return []

    for i in range(0, 12):
        for j in ["Hammer", "Boot"]:
            TempBoard: GameBoard = copy.deepcopy(Board)
            StartEnemies = TempBoard.NumEnemies()
            if j == "Hammer":
                TempBoard.AtkHammer(i)
            if j == "Boot":
                TempBoard.AtkBoot(i)
            FinishEnemies = TempBoard.NumEnemies()
            if FinishEnemies < StartEnemies:
                if gPerfectMoves and not (StartEnemies - FinishEnemies == 4):
                    continue
                Attacks.append(
                    {"Move": j, "Col": i, "Board": TempBoard, "Enemies": FinishEnemies}
                )

    if not Attacks:
        return []
    Attacks = sorted(Attacks, key=lambda k: k["Enemies"])
    if NumAttacks == 0:
        return [Attacks[0]]
    Results = []
    for Atk in Attacks:
        Result = [Atk]
        Result.extend(SimAttack(Atk["Board"], NumAttacks))
        if Result[-1]["Enemies"] == 0:
            return Result
        Results.append(Result)
    # Simulated a bunch of moves - Choose best to pass up
    Results = sorted(Results, key=lambda k: (k[-1]["Enemies"], len(k)))
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

    print("Enter board:\n0123456789AB")
    InputPos = ""
    for _ in range(4):
        Input = input()
        assert len(Input) == 12, "Uhh wrong length?"
        InputPos += Input
    
    # I think the game calculates these two values as ceil(enemies/4) but not sure
    # might be able to skip this question (and any weird extra calcs)
    NumMoves = int(input("Number Of Moves: "))
    NumAttacks = int(input("Number Of Attacks: "))

    InputPos = np.array([int(c) for c in InputPos])
    InputPos.resize((4, 12))

    StartTime = time.time()
    Board = GameBoard(InputPos, NumMoves=NumMoves, NumAttacks=NumAttacks)
    print(f"Here we go! Starting Board:\n{Board}")
    
    # TODO - Is this good? Perfect moves might remove some possible answers?
    # Currently it gives huge speed improvements 
    if Board.NumEnemies() % 4 == 0:
        print("Assuming perfect 4 attacks")
        gPerfectMoves = True

    gSeenBoards.add(hash(str(Board.Board)))
    Result = SolveBoard(Board)
    if Result:
        PrintResult(Result)
    print(f"Finished: {time.time() - StartTime} seconds")
