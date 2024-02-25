import argparse
import pygame

CELL_SIZE = 20
ADDITIONAL_COLUMNS = 20
ADDITIONAL_ROWS = 20


class Grid:
    def __init__(self, input_path):
        self.load(input_path)

    def update(self):
        for x in range(self._w):
            for y in range(self._h):
                neighbors = self.count_neighbors(x, y)

                cell = self.get_cell(x, y)
                if cell.is_alive():
                    if neighbors < 2 or neighbors > 3:
                        cell.kill()
                elif neighbors == 3:
                    cell.birth()

        # Met à jour les cases
        for x in range(self._w):
            for y in range(self._h):
                self.get_cell(x, y).update()

    def count_neighbors(self, x, y):
        # Compte le nombre de voisins autour de la cellule
        result = 0
        for i in range(x-1, x+2):
            for j in range(y-1, y+2):
                if i == x and j == y: continue
                if i < 0 or i >= self._w or j < 0 or j >= self._h: continue

                if self.get_cell(i, j).is_alive():
                    result += 1

        return result
        
    def load(self, path):
        # Charge le fichier et le converti pour être utilisable
        with open(path, "r") as file:
            rows = file.readlines()

        self._grid = []
        self._w = 0
        self._h = len(rows)

        for row in rows:
            row = row.strip()

            if self._w == 0:
                self._w = len(row)
            elif self._w != len(row):
                raise ValueError("Rows in the input file must have the same length.")

            self._grid.append([])
            for char in row:
                if char == "0":
                    self._grid[-1].append(Cell(False))
                elif char == "1":
                    self._grid[-1].append(Cell(True))
                else:
                    raise ValueError("The input file must contain only 0s and 1s.")

            self._grid[-1] += [Cell(False) for _ in range(ADDITIONAL_COLUMNS)]

        self._w += ADDITIONAL_COLUMNS
        self._h += ADDITIONAL_ROWS
        for _ in range(ADDITIONAL_ROWS):
            self._grid.append([Cell(False) for _ in range(self._w)])

    def save(self, path):
        # Permet de sauvegarder un fichier  
        text = ""
        for y in range(self._h):
            for x in range(self._w):
                text += str(self.get_cell(x, y))

            if y != self._h - 1:
                text += "\n"

        with open(path, "w") as file:
            file.write(text)

    def get_size(self):
        return self._w, self._h

    def get_cell(self, x, y):
        return self._grid[y][x]


class Cell:
    def __init__(self, alive):
        self._alive = alive
        self._next_status = alive

    def is_alive(self):
        return self._alive
    
    def kill(self):
        self._next_status = False

    def birth(self):
        self._next_status = True

    def update(self):
        self._alive = self._next_status

    def __repr__(self):
        if self._alive:
            return "1"

        return "0"
    

class Display:
    def __init__(self, width, height, fps, grid):
        pygame.init()

        self._screen = pygame.display.set_mode((width, height))
        self._clock = pygame.time.Clock()

        self._step = 0
        self._grid = grid
        self.fps = fps

    def start(self):
        self._run = True
        while self._run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._run = False

            self.update()

            self._clock.tick(self.fps)
            pygame.display.flip()
        
        pygame.quit()

    def update(self):
        self._grid.update()
        self._step += 1

        pygame.display.set_caption("Game of Life - step " + str(self._step))
        self._screen.fill((255, 255, 255))

        w, h = self._grid.get_size()
        for x in range(w):
            for y in range(h):
                if self._grid.get_cell(x, y).is_alive():
                    self._screen.fill((0, 0, 0), (x*CELL_SIZE, y*CELL_SIZE, CELL_SIZE - 1, CELL_SIZE - 1))

def main():
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("-i", type=str, help="The path to the file containing the initial pattern.")
    parser.add_argument("-o", type=str, help="The path to the file where the final state of the simulation is stored.")
    parser.add_argument("-m", type=int, default=20, help="When display is off, the number of steps to run.")
    parser.add_argument("-d", help="Enable the display.", action="store_true")
    parser.add_argument("-f", default=10, type=int, help="When display is on, the number of frames per second targeted.")
    parser.add_argument("--width", type=int, default=800, help="When display is on, the width of the display.")
    parser.add_argument("--height", type=int, default=600, help="When display is on, the height of the display.")
    args = parser.parse_args()

    if args.i is None:
        raise ValueError("The simulation needs an input file.")
    
    grid = Grid(args.i)


    if args.d:
        display = Display(args.width, args.height, args.f, grid)
        display.start()
    else:
        if args.m < 0:
            raise ValueError("The number of step simulated must be positive")
        
        if args.o is None:
            raise ValueError("Simulating without the display requires an output file.")
    
        for _ in range(args.m):
            grid.update()

    if args.o:
        grid.save(args.o)

if __name__ == "__main__":
    main()