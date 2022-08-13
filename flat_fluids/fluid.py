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
        
        # Create 2D arrays of initial primitive fluid variables
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
        
        # Calculate density
        density = mass / self.grid.cell_area
        
        # Return as an array object
        return self.__array(density)

    def _velocity(self, momentum: Array2D, density: Array2D) -> Array2D:
        """
        Calculates a partial velocity vector array using a partial momentum
        vector array and a density array.
        """
        
        # Calculate velocity
        velocity = momentum / (density * self.grid.cell_area)
        
        # Return as an array object
        return self.__array(velocity)

    def _pressure(self, energy: Array2D, density: Array2D, x_velocity: Array2D,
                  y_velocity: Array2D) -> Array2D:
        """
        Calculates the pressure array using the energy, density and velocity
        vector arrays.
        """
        
        # Calculate pressure
        pressure = (energy / self.grid.cell_area - 0.5 * density *
                    (x_velocity**2 + y_velocity**2)) * (self.gamma - 1)
        
        # Return as an array object
        return self.__array(pressure)

    def update_primitive(self, mass: Array2D, x_momentum: Array2D,
                         y_momentum: Array2D, energy: Array2D) -> None:
        """
        Calculates and updates the primitive fluid variables using the
        provided conserved variables.
        """
        
        # Calculate the new primitive variables
        density = self._density(mass)
        x_velocity = self._velocity(x_momentum, density)
        y_velocity = self._velocity(y_momentum, density)
        pressure = self._pressure(energy, density, x_velocity, y_velocity)
        
        # Update stored primitive variable values
        self.density = density
        self.x_velocity = x_velocity
        self.y_velocity = y_velocity
        self.pressure = pressure


if __name__ == "__main__":
    # Create simple surface grid
    grid = sf.Grid((5, 4))

    # Instantiate fluid
    fluid = Fluid(grid, 5/3)
