import numpy as np
import surface as sf


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

    def __array(self, array: np.ndarray) -> np.ndarray:
        """
        Validity checks a variable array of fluid data.
        """
        
        # Ensure array shape is valid
        if len(np.shape(array)) != 2:
            raise ValueError("Array must contain two dimensions.")
        
        # Return valid array
        return array

    def __create_flat_array(self, value: float) -> np.ndarray:
        """
        Creates a flat 2D array filled with a specifed value.
        """
        
        # Create array filled with the specified value
        array = np.full(self.grid.shape, value)
        
        # Return array
        return self.__array(array)

    def _density(self, mass: np.ndarray) -> np.ndarray:
        """
        Calculates a density array using an array of cell masses.
        """
        
        # Calculate density
        density = mass / self.grid.cell_area
        
        # Return as an array object
        return self.__array(density)

    def _velocity(self, momentum: np.ndarray,
                  density: np.ndarray) -> np.ndarray:
        """
        Calculates a partial velocity vector array using a partial momentum
        vector array and a density array.
        """
        
        # Calculate velocity
        velocity = momentum / (density * self.grid.cell_area)
        
        # Return as an array object
        return self.__array(velocity)

    def _pressure(self, energy: np.ndarray, density: np.ndarray,
                  x_velocity: np.ndarray,
                  y_velocity: np.ndarray) -> np.ndarray:
        """
        Calculates the pressure array using the energy, density and velocity
        vector arrays.
        """
        
        # Calculate pressure
        pressure = (energy / self.grid.cell_area - 0.5 * density *
                    (x_velocity**2 + y_velocity**2)) * (self.gamma - 1)
        
        # Return as an array object
        return self.__array(pressure)

    def update_primitive(self, mass: np.ndarray, x_momentum: np.ndarray,
                         y_momentum: np.ndarray, energy: np.ndarray) -> None:
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
    
    fluid._density(np.full(fluid.grid.shape, 1))
    fluid
