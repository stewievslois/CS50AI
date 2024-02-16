from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
    # not a knight and a knave
    Not(And(AKnight, AKnave)),
    
    # must be a knight or knave
    Or(AKnight, AKnave),
    
    # If A is a knight
    Implication(AKnight, And(AKnight, AKnave)),
    # If A is a knave
    Implication(AKnave, Not(And(AKnight, AKnave)))
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    # Knowledge
    # not a knight and a knave
    Not(And(AKnight, AKnave)),
    Not(And(BKnight, BKnave)),
    
    # must be a knight or knave
    Or(AKnight, AKnave),
    Or(BKnight, BKnave),
    
    # can't say we are both Knaves and be a knight
    Not(AKnight),
    
    # If A is a knight
    Implication(AKnight, BKnave),
    # If A is a knave
    Implication(AKnave, BKnight),
        
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    # General Knowledge
    # not a knight and a knave
    Not(And(AKnight, AKnave)),
    Not(And(BKnight, BKnave)),
    
    # must be a knight or knave
    Or(AKnight, AKnave),
    Or(BKnight, BKnave),
    
    # If A is a knight, A and B are the same
    Implication(AKnight, Or(And(AKnight, BKnight), And(AKnave, BKnave))),
    # If A is a knave, A and B are diferent
    Implication(AKnave, Not(Or(And(AKnight, BKnight), And(AKnave, BKnave)))),
    # If B is a knight, A and B are different
    Implication(BKnight, Or(And(AKnight, BKnave), And(AKnave, BKnight))),
    # If B is a knave, A and B are the same
    Implication(BKnave, Not(Or(And(AKnight, BKnave), And(AKnave, BKnight))))
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
    # General Knowledge
    # not a knight and a knave
    Not(And(AKnight, AKnave)),
    Not(And(BKnight, BKnave)),
    Not(And(CKnight, CKnave)),
    
    # must be a knight or knave
    Or(AKnight, AKnave),
    Or(BKnight, BKnave),
    Or(CKnight, CKnave),
    
    # Implications
    # If C is a knight, then A is a knight and B is either knave or Knight
    Implication(CKnight, AKnight),
    Implication(CKnight, Or(BKnave, BKnight)),
    # If C is a knave, then A is a knave and B is either knave or Knight
    Implication(CKnave, AKnave),
    Implication(CKnave, Or(BKnave, BKnight)),
    # If B is a knight, C is a knave:
    Implication(BKnight, CKnave),
    Implication(BKnight, And(
      # A then said 'I am a Knave', A may be a Knight or a Knave:
      Implication(AKnight, AKnave),
      Implication(AKnave, Not(AKnave)),
    )),
    # If B is a knave, C is not a knave:
    Implication(BKnave, Not(CKnave)),
    Implication(BKnave, And(
      # A then said 'I am a Knight', A may be a Knight or a Knave:
      Implication(AKnight, AKnight),
      Implication(AKnave, Not(AKnight))
    )),
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
