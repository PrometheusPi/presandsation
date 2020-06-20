import numpy as np
import cv2
import sys
import imageio

# target resolution
N_x_target = 1200
N_y_target = 1920

# list of frames to pause video
list_stop_frames = np.array([5, 200, 500])

# canvas to put videos on
frame = np.zeros((N_x_target, N_y_target, 3), dtype=np.uint8)

# reate openCV VideoCapture input for video file
cap = cv2.VideoCapture('../test.mp4')
frame_count_video = int(cap.get(7))  # number of frames in video
print("total frames:", frame_count_video)

# get web cam feed
webcam = cv2.VideoCapture(0)

# test if video and cam are available
if (not cap.isOpened()):
    print("Error opening video file")

if (not webcam.isOpened()):
    print("Error accessing web cam")


# Read until video is completed
stopped = False


def keyPress(stopped, current_frame_video):
    # get pressed keys
    getKey = cv2.waitKey(25)

    if getKey & 0xFF == ord('q'):
        # press "q" key to exit program
        sys.exit(0)
    elif getKey & 0xFF == ord(' '):
        # press space to stopp video feed
        stopped = not(stopped)
        print("stopped - started")
    elif getKey & 0xFF == 2:
        # left (back) key
        previous_stop_key = list_stop_frames[np.less(list_stop_frames, current_frame_video)]
        if previous_stop_key.size > 0:
            cap.set(1, previous_stop_key[-1])
        stopped = True

    elif getKey & 0xFF == 3:
        # right (forward) key
        next_stop_key = list_stop_frames[np.greater(list_stop_frames, current_frame_video)]
        if next_stop_key.size > 0:
            cap.set(1, next_stop_key[0])
        stopped = True
    return stopped


stopped = True
while(stopped):
    image = imageio.imread("../fig.png")
    # get image shape
    print(np.shape(image))
    N_x_image, N_y_image, _ = np.shape(image)
    # place image in full frame
    id_x = (N_x_target - N_x_image) // 2
    id_y = (N_y_target - N_y_image) // 2
    frame[id_x:id_x+N_x_image, id_y:id_y+N_y_image, :] = image[:, :, :3]  # ignore 4th channal (alpha)
    # plot frame (full canvas)
    stopped = keyPress(stopped, None)
    cv2.imshow('Frame', frame)


while(True):
    # get video frame (index)
    current_frame_video = int(cap.get(1))

    stopped = keyPress(stopped, current_frame_video)

    if not stopped:
        # get next video
        ret, frame_video = cap.read()
        if ret:
            # stopp if stop/pause frame is reached
            if current_frame_video in list_stop_frames:
                print("found stop frame {}".format(current_frame_video))
                stopped = True

            # get video shape
            N_x_video, N_y_video, _ = np.shape(frame_video)
            # place video in full frame
            id_x = (N_x_target - N_x_video) // 2
            id_y = (N_y_target - N_y_video) // 2

    # add video to canvas
    frame[id_x:id_x+N_x_video, id_y:id_y+N_y_video, :] = frame_video

    # get web cam frame
    _, im_cam = webcam.read()
    N_x_cam, N_y_cam, _ = np.shape(im_cam)
    # add web cam at half size to canvas
    frame[-N_x_cam//2:, -N_y_cam//2:, :] = im_cam[::2, ::2, :]  # //2

    # plot frame (full canvas)
    cv2.imshow('Frame', frame)

    # IDEA: single pixel to determine stop signal?
    # print(frame[-1, -1, :])


cap.release()
webcam.release()


# Closes all the frames
cv2.destroyAllWindows()
