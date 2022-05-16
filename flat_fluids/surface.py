from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt


class DecimalFraction(float):
    def __new__(cls, value: float) -> None:
        # Ensure value is valid
        if value < 0:
            raise ValueError("Value is less than zero.")
        elif value > 1:
            raise ValueError("Value is greater than one.")
        
        # Run parent super function
        return super().__new__(cls, value)


class Grid(object):
    def __init__(self, shape: tuple([int, int])) -> None:
        # Save parameters
        self.shape = shape

    def __is_in(self, position: tuple([int, int])) -> bool:
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
        
    def _surface_mask(self, position: tuple([int, int]),
                      tolerance: DecimalFraction) -> np.ndarray:
        pass
    
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
