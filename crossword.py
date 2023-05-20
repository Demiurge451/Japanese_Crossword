import numpy as np


class Crossword:
    def __init__(self, grid: [[]]):
        self._grid = np.array(grid, dtype=int)
        self._len_row_values = 0
        self._len_col_values = 0
        row_values = [[] for _ in range(len(self.grid))]
        col_values = [[] for _ in range(len(self.grid[0]))]

        self._calculate_values(row_values, col_values)

        outer_size = len(self.grid) + self.len_col_values
        inner_size = len(self.grid[0]) + self.len_row_values
        self._crossword_grid = np.zeros((outer_size, inner_size), dtype=int)
        self.create_crossword_grid(row_values, col_values)

        self._extended_grid = np.copy(self.crossword_grid)
        self._create_extended_grid()

        self._grid = self.grid.tolist()
        self._crossword_grid = self.crossword_grid.tolist()
        self._extended_grid = self.extended_grid.tolist()

    def _calculate_values(self, row_values: [[]], col_values: [[]]):
        for row in range(len(self.grid)):
            col = 0
            count = 0
            while col < len(self.grid[0]):
                while col < len(self.grid[0]) and self.grid[row][col] == -1:
                    count += 1
                    col += 1
                if count != 0:
                    row_values[row].append(count)
                count = 0
                col += 1

            self._len_row_values = max(self.len_row_values, len(row_values[row]))

        for col in range(len(self.grid[0])):
            row = 0
            count = 0
            while row < len(self.grid):
                while row < len(self.grid) and self.grid[row][col] == -1:
                    count += 1
                    row += 1
                if count != 0:
                    col_values[col].append(count)
                count = 0
                row += 1

            self._len_col_values = max(self.len_col_values, len(col_values[col]))

        self._fill_empty_values(row_values, col_values)

    def _fill_empty_values(self, row_values: [[]], col_values: [[]]):
        for i in range(len(row_values)):
            arr = [0] * self.len_row_values
            arr[:-len(row_values[i]) - 1:-1] = row_values[i][len(row_values[i])::-1]
            row_values[i] = arr

        for i in range(len(col_values)):
            arr = [0] * self.len_col_values
            arr[:-len(col_values[i]) - 1:-1] = col_values[i][len(col_values[i])::-1]
            col_values[i] = arr

    def create_crossword_grid(self, row_values, col_values):
        row_values = np.array(row_values)
        col_values = np.array(col_values)

        # fill the left part
        self.crossword_grid[:-len(row_values) - 1: -1, 0: self.len_row_values] = row_values[::-1, :]

        # fill the top part
        for col in range(-1, -len(col_values) - 1, -1):
            for row in range(0, self.len_col_values):
                self.crossword_grid[row][col] = col_values[col][row]

    def _create_extended_grid(self):
        self.extended_grid[self.len_col_values:, self.len_row_values:] = self.grid[:, :]

    @property
    def grid(self):
        return self._grid

    @property
    def crossword_grid(self):
        return self._crossword_grid

    @property
    def extended_grid(self):
        return self._extended_grid

    @property
    def len_row_values(self):
        return self._len_row_values

    @property
    def len_col_values(self):
        return self._len_col_values
