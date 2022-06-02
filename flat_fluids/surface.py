from pathlib import Path
import numpy as np
import scipy.ndimage.measurements as sci_measure
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
        rgb_mean = np.mean(np.broadcast_arrays(rgb1, rgb2), axis=0)
        
        # Calculate component weights
        weights = np.stack([2 + rgb_mean[..., 0],
                            np.full(np.shape(rgb_mean[..., 0]), 4),
                            3 - rgb_mean[..., 0]], axis=-1)
        
        # Calculate similarity metric
        diff = np.sqrt(np.sum(np.square(rgb_diff) * weights, axis=-1)) / 3
        
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
        
        # Return colour difference for image against selected pixel
        colour_diff = self._colour_diff(self.image, colour)
        
        # Determine pixel index for colours within the tolerance
        colour_mask = Mask2D(colour_diff <= tolerance)
        
        # Return mask with only the connected elements
        return self._remove_disconnected(colour_mask, position)
    
    def _remove_disconnected(self, mask: Mask2D, position:Index2D) -> Mask2D:
        """
        Remove any elements from the provided mask that are not connected to
        the specified position through any additional surrounding elements.
        """
        
        # Define the required connection pattern
        pattern = np.ones((3, 3), dtype=np.int)
        
        # Determine connected groups
        group_mask = sci_measure.label(mask, pattern)[0]
        
        # Return mask of group connected to specified position
        return Mask2D(group_mask == group_mask[position])
    
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
    mask = image._surface_mask((0, 0), 0.1)
    
    plt.imshow(mask)
