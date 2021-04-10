import cv2 
import os 
import sys

def extract(file):
    # Read the video from specified path
    cam = cv2.VideoCapture(file)
    frame_dir = file[:-4]
    try:

        # creating a folder named data
        if not os.path.exists(frame_dir):
            os.makedirs(frame_dir)

    # if not created then raise error
    except OSError:
        print ('Error: Creating directory of data')

    # frame
    currentframe = 0

    while(True):

        # reading from frame
        ret,frame = cam.read()

        if ret:
            # if video is still left continue creating images
            name = frame_dir + '/' + str(currentframe) + '.jpg'
            print ('Creating...' + name)

            # writing the extracted images
            cv2.imwrite(name, frame)

            # increasing counter so that it will
            # show how many frames are created
            currentframe += 1
        else:
            break

    # Release all space and windows once done
    cam.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("ERROR No video provided")
        os.exit(1)
    for i in range(1,len(sys.argv)):
        extract(sys.argv[i])