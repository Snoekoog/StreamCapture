import cv2
from .LOGGER import warn, error
from numpy import ndarray

class ImageCapture:
    """
    Base class for capturing statically served stream images. Uses OpenCV's VideoCapture 
    class to create a connection with the site. This is a IO operation, but does not run
    in a loop, eliminating the need to run it in a separate thread. Does pause main
    thread execution, but runs to fast that the delay is insignificant.

    Parameters:
        link (string): DIRECT! link to the image (URL should end with a file extension like .jpg)
    """

    def __init__(self, link: str):

        self.link       = link      # Link to the HLS stream
        self.fail_count = 0         # Counter to keep track of failed fetch attempts
    
    def read(self) -> ndarray:
        """
        Main function to get image from link.

        Returns:
            frame (ndarray): fetched image from link
        """

        cap         = cv2.VideoCapture(self.link)   # Create 'VideoCapture' on the fly
        ret, frame  = cap.read()                    # Read frame (image) from 'stream' (single frame stream)

        # If failed to fetch image...
        if not ret:

            # Increase fail counter by one
            self.fail_count += 1

            # Notify terminal about this failed attempt
            warn("ERROR: Failed to fetch frame for link " + str(self.link), "ImageCapture.py")

            # Return 'None' (there should be a 'none'-check in main script to check for this)
            return None
        
        # Release VideoCapture after we got our image
        cap.release()

        # Return frame
        return frame