from pathlib import Path
import matplotlib.pyplot as plt


class Grid(object):
    def __init__(self, shape: tuple([int, int])) -> None:
        # Save parameters
        self.shape = shape


class Image(Grid):
    def __init__(self, filepath: Path) -> None:
        # Save parameters
        self.filepath = filepath
        
        # Load from file
        self.image = plt.imread(filepath)
        
        # Determine key parameters
        _shape = self.image.shape[:2]
        
        # Instantiate the superclass
        super().__init__(_shape)


if __name__ == "__main__":
    # Define filepath
    filepath = (Path(__file__).parent / "../tests/integration/fixtures/"
                "Octopus.png").resolve()
    
    # Instantiate image
    image = Image(filepath)
    image
