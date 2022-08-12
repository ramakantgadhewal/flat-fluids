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
        self.cell_area = self._cell_area()

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
    
    def _cell_area(self) -> float:
        """
        Calulates the area of each cell within the grid.
        """
        
        return self.dx * self.dy

class Fluid(object):
    def __init__(self, grid: sf.Grid, gamma: float) -> None:
        # Save parameters
        self.grid = grid
        self.gamma = gamma
        
        # Create 2D arrays of initial fluid variables
        self.density = self.__create_flat_array(1.2)
        self.pressure = self.__create_flat_array(1.01325)
        self.x_velocity = self.__create_flat_array(0)
        self.y_velocity = self.__create_flat_array(0)

    def __create_flat_array(self, value: float) -> Array2D:
        """
        Creates a flat 2D array filled with a specifed value.
        """
        
        # Create array
        array = np.full(self.grid.shape, value)
        
        # Return array
        return Array2D(array, self.grid.dx, self.grid.dy)

    def _update_density(self, mass: Array2D) -> None:
        """
        Calculates and updates the density array using an array of cell masses.
        """
        
        # Update density array
        self.density = mass / self.grid.cell_area


if __name__ == "__main__":
    # Create simple surface grid
    grid = sf.Grid((5, 4))

    # Instantiate fluid
    fluid = Fluid(grid, 5/3)
