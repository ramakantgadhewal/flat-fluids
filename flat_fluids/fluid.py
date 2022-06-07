import numpy as np
import surface as sf


class Array2D(object):
    def __init__(self, value: np.ndarray, dx: float, dy: float) -> None:
        # Ensure parameters are valid
        if len(np.shape(value)) != 2:
            raise ValueError("Value must contain two dimensions.")
        if (dx <= 0) or (dy <= 0):
            raise ValueError("Cell lengths must be a real positive number.")
        
        # Save parameters
        self.value = value
        self.dx = dx
        self.dy = dy
        
        # Determine additional parameters
        self.shape = np.shape(value)

    def x_gradient(self) -> np.ndarray:
        """
        Calculates the gradient of the 2D array in the x dimension.
        """
        
        return np.gradient(self.value, self.dx, axis=0)

    def y_gradient(self) -> np.ndarray:
        """
        Calculates the gradient of the 2D array in the y dimension.
        """
        
        return np.gradient(self.value, self.dy, axis=1)

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
