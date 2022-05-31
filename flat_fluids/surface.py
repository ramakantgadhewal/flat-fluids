from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt


class DecimalFraction(type):
    def __new__(cls, value: float) -> float:
        # Ensure value is valid
        if np.any(value < 0):
            raise ValueError("Value is less than zero.")
        elif np.any(value > 1):
            raise ValueError("Value is greater than one.")
        
        # Return decimal fraction value
        return value


class Index2D(type):
    def __new__(cls, value: tuple) -> tuple:
        # Ensure value is valid
        if len(value) != 2:
            raise ValueError("Value must contain 2 elements.")
        if not all(isinstance(element, int) for element in value):
            raise ValueError("Value must contain only integers.")
        if any(element < 0 for element in value):
            raise ValueError("Value must only contain positive numbers.")
        
        # Return 2D index as a tuple
        return tuple(value)


class RGBColour(type):
    def __new__(cls, value: tuple) -> tuple:
        # Ensure value is valid
        if len(np.shape(value)) != 1:
            raise ValueError("Value must only contain a single dimension.")
        if len(value) != 3:
            raise ValueError("Value must be contain 3 elements.")
        
        # Return array with correct data types
        return DecimalFraction(value)


class Mask2D(type):
    def __new__(cls, value: np.ndarray) -> np.ndarray:
        # Ensure value is valid
        if len(np.shape(value)) != 2:
            raise ValueError("Value must contain two dimensions.")
        if np.any(np.isnan(value)):
            raise ValueError("Value must not contain NaNs.")
        
        # Return array of Booleans
        return np.bool_(value)
    
    
class Grid(object):
    def __init__(self, shape: Index2D) -> None:
        # Save parameters
        self.shape = shape

    def _is_in(self, position: Index2D) -> bool:
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
        
    @staticmethod
    def _colour_diff(rgb1: RGBColour, rgb2: RGBColour) -> DecimalFraction:
        """
        Calculates a quantifiable similarity metric between two RGB colours
        using a combination of two weighted Euclidean distance functions.
        """
        
        # Calculate component differences
        rgb_diff = rgb1 - rgb2
        
        # Calculate component means
        rgb_mean = np.mean([rgb1, rgb2], axis=0)
        
        # Calculate similarity metric
        diff = np.sqrt(rgb_diff[0]**2 * (2 + rgb_mean[0]) +
                       rgb_diff[1]**2 * 4 +
                       rgb_diff[2]**2 * (3 - rgb_mean[0])) / 3
        
        # Return colour difference
        return DecimalFraction(diff)
        
    def _surface_mask(self, position: Index2D,
                      tolerance: DecimalFraction) -> Mask2D:
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
        colour = RGBColour(self.image[position])
        
        # Calculate colour difference for image
        self._colour_diff(self.image, self.image)
        colour_diff = np.array(list(map(lambda x: self._colour_diff(x, colour), self.image)))
        
        return False # TODO: fix. Mask2D(self._colour_diff(colour) <= tolerance)
    
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
    # image.plot()
    
    # Determine position of fluid
    image._surface_mask((0, 0), 0.1)
