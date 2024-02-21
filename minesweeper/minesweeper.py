import itertools
import random
import copy


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        # if no. of cells = count then all cells in sentence are mines
        if len(self.cells) == self.count and self.count != 0:
            return self.cells
        else:
            return set()

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        # if count of mines = 0, all cells in sentence are safe
        if self.count == 0:
            return self.cells
        else:
            return set()

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        # check if cell is in sentence
        if cell in self.cells:
        # if cell is in sentence remove cell from sentence and reduce count by 1
            self.cells.remove(cell)
            self.count -= 1
            return self.cells and self.count

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        # check if cell is in sentence
        if cell in self.cells:
        # if cell is in sentence remove cell from sentence
            self.cells.remove(cell)
            return self.cells

class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        # 1) add cell to moves made
        self.moves_made.add(cell)
        
        # 2) call mark_safe
        self.mark_safe(cell)
        
        # 3) Loop over all cells and create new sentence removing current cell
        #new_sentence_cells = set()
        #for i in range(cell[0] - 1, cell[0] + 2):
            #for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore if cell is a mine and reduce count by 1
                #if (i, j) in self.mines:
                    #countmines =- 1
                    #continue
                
                # Ignore the cell itself
                #if (i, j) == cell:
                    #continue
                
                # Ignore if cell is already safe
                #if (i, j) in self.safes:
                    #continue
                
                # add to new_sentence_cells if they are in game board
                #elif 0 <= i < self.height and 0 <= j < self.width:
                    #new_sentence_cells.add((i, j))

        # commit new sentence to knowledge base
        #self.knowledge.append(Sentence(new_sentence_cells, count))
        
        # 3)
        new_sentence_cells = []
        countmines = 0
        # Loop over all cells
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):
                # cjeck if cell in mines
                if (i, j) in self.mines:
                    countmines += 1
                # check cell is valid, not in safes or in mines
                if 0 <= i < self.height and 0 <= j < self.width and (i, j) not in self.safes and (i, j) not in self.mines:
                    new_sentence_cells.append((i, j))
        # create new setence
        new_sentence = Sentence(new_sentence_cells, count - countmines)
        # append new sentence to knowledge base
        self.knowledge.append(new_sentence)
        
        # 4) Mark safes and mines
        # for sentence in self.knowledge:
            # safes = sentence.known_safes()
            # mines = sentence.known_mines()
            # Mark safes
            # if safes:
                # for cell in safes.copy():
                    # self.mark_safe(cell)
            # Mark mines
            # if mines:
                # for cell in mines.copy():
                    # self.mark_mine(cell)
       
        # 4)
        for sentence in self.knowledge:
            # mark mines
            if sentence.known_mines():
                for cell in sentence.known_mines().copy():
                    self.mark_mine(cell)
            # mark safes
            if sentence.known_safes():
                for cell in sentence.known_safes().copy():
                    self.mark_safe(cell)
          
        # 5) Add new sentence to knowledgebase
        for sentence in self.knowledge:
            if new_sentence.cells.issubset(sentence.cells) and count > 0 and new_sentence.count > 0 and new_sentence != sentence:
                newsubset = sentence.cells.difference(new_sentence.cells)
                new_sentencesubset = Sentence(list(newsubset), sentence.count - new_sentence.count)
                self.knowledge.append(new_sentencesubset) 
                
       # https://www.youtube.com/watch?v=dbSCJGJVIBU (18:33)
                

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        # Identify safe moves
        for cell in self.safes:
            if cell not in self.moves_made:
                return cell
        return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        # Identify all moves
        possiblemoves = []
        for i in range(0, self.height):
            for j in range(0, self.width):
                # check selection not in moves made or mines
                if (i, j) not in self.moves_made and (i, j) not in self.mines:
                    possiblemoves.append((i, j))
                # chec if no moves left
        if len(possiblemoves) != 0:
            return random.choice(possiblemoves)
        else:
            return None

