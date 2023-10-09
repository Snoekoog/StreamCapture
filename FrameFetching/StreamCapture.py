import cv2
import queue
import threading
import time
from numpy import ndarray
from .LOGGER import warn, error, note

class StreamCapture:
    """
    Base class for capturing HLS internet streams. Uses OpenCV's VideoCapture class
    to create a connection with the stream. Since this is mainly a IO-operation,
    the frame fetching happens in a separate thread as not to pause the main thread.
    Main thread execution can continue at its own pace, only requesting a frame
    from this StreamCapture class as (when) it wishes to. 

    Parameters:
        link (string): link to the HLS stream (tested with .m3u8 format; other formats unknown)
    """


    def __init__(self, link: str):

        self.link       = link                                  # Link to the HLS stream
        self.fail_count = 0                                     # Counter to keep track of failed fetch attempts

        self.q          = queue.Queue()                         # Create queue to hold latest frame
        self.cap        = cv2.VideoCapture(link)                # Create VideoCap object
        t               = threading.Thread(target=self._reader) # Start multithreaded frame fetching
        t.daemon        = True                                  # Make daemon; close when main process closes

        t.start()                                               # Start thread

    def _reader(self):
        """
        Reader function, used internally in the class to iniate 'parallel' execution
        of frame fetching from stream. Runs in a seperate thread. Never call from main thread,
        as this will pause it forever.
        """

        # Loop forever
        while True:

            # Read frame from VideoCapture
            ret, frame = self.cap.read()
            
            # If failed to fetch frame...
            if not ret:

                # Increase fail counter by one
                self.fail_count += 1

                # If fail counter exceeds (or is equal to) five...
                if self.fail_count >= 5:

                    # We should break out of the loop to prevent overloading the 
                    # stream server with 'problematic' requests. At this point, the server
                    # either blocked us or is offline completely. Notify terminal about this
                    error("ERROR: Failed to fetch frame for link " + str(self.link) + ". Breaking out of loop...", "StreamCapture.py")
                    break

                else:

                    # Notify terminal about the failed attempt
                    warn("ERROR: Failed to fetch frame for link " + str(self.link) + ". Attempting cap reboot...", "StreamCapture.py")

                    # Close (release) the VideoCapture object. We'll try to recreate it
                    self.cap.release()

                    # Take a small timeout to ensure we are not 'spamming' the stream server with
                    # excessive connection requests.
                    time.sleep(20)

                    # Notify terminal about reboot.
                    note("NOTICE: Rebooted cap for link " + str(self.link), "StreamCapture.py")

                    # Re-create VideoCapture, overwrite previous one.
                    self.cap = cv2.VideoCapture(self.link)

                    # Skip the rest of execution, and go to the next 'fresh' loop
                    continue

            # If there is a frame in queue...
            if not self.q.empty():

                try:

                    # Remove the frame from queue (we are replacing it)
                    self.q.get_nowait()

                except queue.Empty:
                    pass
            
            # Put new frame in queue
            self.q.put(frame)

            # Wait a short while before attempting to fetch a new frame from the stream
            cv2.waitKey(15)

    def read(self) -> ndarray:
        """
        Main function to retreive the latest stream frame from the 'buffer' (queue)
        
        Returns:
            frame (ndarray): latest fetched frame from stream
        """

        # Every time we succesfully return an image to the main thread, we decrease
        # the fail counter by one. This indicates a well-functioning VideoCapture.
        self.fail_count = max(0, self.fail_count - 1)

        # Return frame from queue
        return self.q.get()
    