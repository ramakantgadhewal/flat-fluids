from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt


class DecimalFraction(float):
    def __new__(cls, value: float) -> float:
        # Ensure value is valid
        if value < 0:
            raise ValueError("Value is less than zero.")
        elif value > 1:
            raise ValueError("Value is greater than one.")
        
        # Run parent super function
        return super().__new__(cls, value)


class Array2DIndex(tuple):
    def __new__(cls, value: tuple) -> tuple:
        # Ensure value is valid
        if len(value) != 2:
            raise ValueError("Value must be contain 2 elements.")
        if not all(isinstance(element, int) for element in value):
            raise ValueError("Value must contain only ints.")
        if any(element < 0 for element in value):
            raise ValueError("Value must only contain positive numbers.")
        
        # Run parent super function
        return super().__new__(cls, value)


class Grid(object):
    def __init__(self, shape: Array2DIndex) -> None:
        # Save parameters
        self.shape = shape

    def _is_in(self, position: Array2DIndex) -> bool:
        """
        Check to see if the provided position is within the shape of the grid.
        """
        
        # Check each dimension of the shape
        for idx, pos in enumerate(position):
            # Check if position for the dimension is valid
            if pos < 0 and pos > self.shape[idx]:
                return False
            
        # Otherwise, the position is within the shape
        return True


class Image(Grid):
    def __init__(self, filepath: Path) -> None:
        # Determine key parameters
        __image = plt.imread(filepath)
        __shape = __image.shape[:2]
        
        # Instantiate the superclass
        super().__init__(__shape)
        
        # Save parameters
        self.filepath = filepath
        self.image = __image
        
    # def __colour_diff()
        
    def _surface_mask(self, position: Array2DIndex,
                      tolerance: DecimalFraction) -> np.ndarray:
        """
        Generate a mask of Booleans to indicate connected pixels in the image
        with a colour similar to that of a selected pixel. The tolerance
        provided dictates the level of similarity required between these
        colours for them to be considered connected.
        """
        
        # Ensure the pixel position is within the image
        if not self._is_in(position):
            raise ValueError("Invalid position selected in the image.")
        
        # Determine the selected colour
        colour = self.image[position]
        
        
    
    def plot(self) -> None:
        """
        Plot original image in a window.
        """
        
        # Add image to plot
        plt.imshow(self.image)
        
        # Show figure
        plt.show()


if __name__ == "__main__":
    # Define filepath
    filepath = (Path(__file__).parent / "../tests/integration/fixtures/"
                "Octopus.png").resolve()
    
    # Instantiate image
    image = Image(filepath)

    # Plot
    image.plot()
    
    # Determine position of fluid
    image._surface_mask((0, 0), 0.1)
