from FrameFetching.StreamCapture import StreamCapture
from FrameFetching.ImageCapture import ImageCapture
from FrameFetching.LOGGER import *
import cv2
import time

if __name__ == "__main__":

    # Link to desired stream (preferably .m3u8 format)
    # my_link = "https://hd-auth.skylinewebcams.com/live.m3u8?a=7tlsqah62kp57gvmvdkljcmub3" # seems to have some weird anti-scrape protection?
    my_link = "https://stream.sob.m-dn.net/live/sb1/vKVhWPO2ysiYNGrNfA+Krw1/stream.m3u8?plain=true"

    # Create StreamCapture object
    my_cap = StreamCapture(my_link)

    # Main loop (can run at slower rate than stream does)
    while True:

        # Read from StreamCapture
        frame = my_cap.read()

        # Show? (can also use this to save to disk, i.e. using imwrite)
        cv2.imshow("Stream", frame)

        if cv2.waitKey(500) & 0xFF == ord('q'):
            break