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
        self.density = self.__create_flat_array(1.2)
        self.pressure = self.__create_flat_array(1.01325)
        self.x_velocity = self.__create_flat_array(0)
        self.y_velocity = self.__create_flat_array(0)

    def __array(self, values: np.ndarray) -> Array2D:
        """
        Creates a flat 2D array from a predefined array of data.
        """
        
        return Array2D(values, self.grid.dx, self.grid.dy)

    def __create_flat_array(self, value: float) -> Array2D:
        """
        Creates a flat 2D array filled with a specifed value.
        """
        
        # Create array filled with the specified value
        array = np.full(self.grid.shape, value)
        
        # Return array
        return self.__array(array)

    def _density(self, mass: Array2D) -> Array2D:
        """
        Calculates a density array using an array of cell masses.
        """
        
        return self.__array(mass / self.grid.cell_area)

    def _velocity(self, momentum: Array2D, density: Array2D) -> Array2D:
        """
        Calculates a partial velocity vector array using a partial momentum
        vector array and a density array.
        """
        
        return self.__array(momentum / (density * self.grid.cell_area))


if __name__ == "__main__":
    # Create simple surface grid
    grid = sf.Grid((5, 4))

    # Instantiate fluid
    fluid = Fluid(grid, 5/3)
