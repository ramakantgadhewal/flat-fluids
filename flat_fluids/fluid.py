import numpy as np
import surface as sf


class Fluid(object):
    def __init__(self, grid: sf.Grid, gamma: float) -> None:
        # Save parameters
        self.grid = grid
        self.gamma = gamma
        
        # Create 2D arrays of initial fluid variables
        self.density = np.full(self.grid.shape, 1.2)
        self.pressure = np.full(self.grid.shape, 1.01325)
        self.x_velocity = np.full(self.grid.shape, 0)
        self.y_velocity = np.full(self.grid.shape, 0)


if __name__ == "__main__":
    # Create simple surface grid
    grid = sf.Grid((5, 4))

    # Instantiate fluid
    fluid = Fluid(grid, 5/3)