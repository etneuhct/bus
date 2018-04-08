from pykinect import nui
import time
import requests
import json

url = "http://localhost:3001/api"
last_post_date = -1

def send_data_counter(counter, exercise):
    data = {"counter": counter, "drill": exercise}
    requests.get('{}/{}/{}'.format(url, counter, exercise))

def send_data_far(far):
    global last_post_date
    if last_post_date == -1 or time.clock() - last_post_date > 1:
        # data = {"tooFar": far}
        requests.get('{}/{}'.format(url , 1 if far else 0))
        last_post_date = time.clock()


def too_close(positions):
    if positions[nui.JointId.head].z <= 2:
        return True

def jumping_jacks(min_right_wrist_y, min_left_wrist_y, max_right_wrist_y, max_left_wrist_y, knee_distance_x):
    if max_left_wrist_y - min_left_wrist_y > 1 and max_right_wrist_y - min_right_wrist_y > 1:
        if knee_distance_x > 0.2:
            return True
    else:
        return False

def touch_toe(shoulder_position_y):
    return  shoulder_position_y < 0.15

def start_jumping_jacks(max_drill):

    with nui.Runtime() as kinect:
        while 1:
            kinect.camera.elevation_angle = 0
            kinect.skeleton_engine.enable=True
            counter_jacks = 0
            counter_toe = 0

            last_count_toe_date = -1

            min_right_wrist_y = 1
            max_right_wrist_y = -1
            min_left_wrist_y = 1
            max_left_wrist_y = -1

            while 1:
                frame = kinect.skeleton_engine.get_next_frame()
                for skeleton in frame.SkeletonData:
                    seen = False
                    if skeleton.eTrackingState != nui.SkeletonTrackingState.TRACKED:
                        send_data_far(True)

                    if skeleton.eTrackingState == nui.SkeletonTrackingState.TRACKED:
                        send_data_far(False)
                        positions = skeleton.get_skeleton_positions()

                        if not too_close(positions):
                            # Coordinates of points of interest

                            if not seen:
                                #print(' I see you !')
                                seen = True

                            # Wrists
                            right_wrist_positions_x = positions[nui.JointId.wrist_right].x
                            right_wrist_positions_y = positions[nui.JointId.wrist_right].y

                            left_wrist_position_x = positions[nui.JointId.wrist_left].x
                            left_wrist_position_y = positions[nui.JointId.wrist_left].y

                            # Knees
                            right_knee_positions_x = positions[nui.JointId.knee_right].x
                            right_knee_positions_y = positions[nui.JointId.knee_right].y

                            left_knee_positions_x = positions[nui.JointId.knee_left].x
                            left_knee_positions_y = positions[nui.JointId.knee_right].y

                            # Shoulders
                            right_shoulder_position_x = positions[nui.JointId.shoulder_right].x
                            right_shoulder_position_y = positions[nui.JointId.shoulder_right].y

                            left_shoulder_position_x = positions[nui.JointId.shoulder_left].x
                            left_shoulder_position_y = positions[nui.JointId.shoulder_left].y

                            shoulder_position_y = min(right_shoulder_position_y, left_shoulder_position_y)

                            knee_distance_x = abs(right_knee_positions_x - left_knee_positions_x)

                            if right_wrist_positions_y < min_right_wrist_y and left_wrist_position_y < min_left_wrist_y:
                                min_right_wrist_y = right_wrist_positions_y
                                min_left_wrist_y = left_wrist_position_y

                            if right_wrist_positions_y > max_left_wrist_y and left_wrist_position_y > max_left_wrist_y:
                                max_right_wrist_y = right_wrist_positions_y
                                max_left_wrist_y = left_wrist_position_y

                            if max_right_wrist_y > 0.5 and counter_jacks < max_drill:
                                if min_left_wrist_y != 1 and max_left_wrist_y != -1:
                                    if jumping_jacks(min_right_wrist_y, min_left_wrist_y, max_right_wrist_y,
                                                     max_left_wrist_y, knee_distance_x):
                                        min_right_wrist_y = 1
                                        max_right_wrist_y = -1
                                        min_left_wrist_y = 1
                                        max_left_wrist_y = -1
                                        counter_jacks += 1
                                        print('Number of jumping jacks: ' + str(counter_jacks))
                                        send_data_counter(counter_jacks, "jumping_jacks")
                                        if counter_jacks == max_drill:
                                            print("gg wp")
                                            return

def start_touch_toes(max_drill):

    with nui.Runtime() as kinect:
        while 1:
            kinect.camera.elevation_angle = 0
            kinect.skeleton_engine.enable=True
            counter_jacks = 0
            counter_toe = 0

            last_count_toe_date = -1

            min_right_wrist_y = 1
            max_right_wrist_y = -1
            min_left_wrist_y = 1
            max_left_wrist_y = -1

            while 1:
                frame = kinect.skeleton_engine.get_next_frame()
                for skeleton in frame.SkeletonData:
                    seen = False
                    if skeleton.eTrackingState != nui.SkeletonTrackingState.TRACKED:
                        send_data_far(True)

                    if skeleton.eTrackingState == nui.SkeletonTrackingState.TRACKED:
                        send_data_far(False)
                        positions = skeleton.get_skeleton_positions()

                        if not too_close(positions):
                            # Coordinates of points of interest

                            if not seen:
                                #print(' I see you !')
                                seen = True

                            # Wrists
                            right_wrist_positions_x = positions[nui.JointId.wrist_right].x
                            right_wrist_positions_y = positions[nui.JointId.wrist_right].y

                            left_wrist_position_x = positions[nui.JointId.wrist_left].x
                            left_wrist_position_y = positions[nui.JointId.wrist_left].y

                            # Knees
                            right_knee_positions_x = positions[nui.JointId.knee_right].x
                            right_knee_positions_y = positions[nui.JointId.knee_right].y

                            left_knee_positions_x = positions[nui.JointId.knee_left].x
                            left_knee_positions_y = positions[nui.JointId.knee_right].y

                            # Shoulders
                            right_shoulder_position_x = positions[nui.JointId.shoulder_right].x
                            right_shoulder_position_y = positions[nui.JointId.shoulder_right].y

                            left_shoulder_position_x = positions[nui.JointId.shoulder_left].x
                            left_shoulder_position_y = positions[nui.JointId.shoulder_left].y

                            shoulder_position_y = min(right_shoulder_position_y, left_shoulder_position_y)

                            knee_distance_x = abs(right_knee_positions_x - left_knee_positions_x)

                            if right_wrist_positions_y < min_right_wrist_y and left_wrist_position_y < min_left_wrist_y:
                                min_right_wrist_y = right_wrist_positions_y
                                min_left_wrist_y = left_wrist_position_y

                            if right_wrist_positions_y > max_left_wrist_y and left_wrist_position_y > max_left_wrist_y:
                                max_right_wrist_y = right_wrist_positions_y
                                max_left_wrist_y = left_wrist_position_y


                            if (last_count_toe_date == -1 or time.clock() - last_count_toe_date >= 2) \
                                    and touch_toe(shoulder_position_y) and counter_toe < max_drill:
                                last_count_toe_date = time.clock()
                                counter_toe += 1
                                print('You touched your toe: ' + str(counter_toe) + ' time(s).')
                                send_data_counter(counter_jacks, "touch_toe")
                                if counter_toe == max_drill:
                                    print("gg wp")
                                    return

start_touch_toes(4)
if __name__ == '__main__':
    last_post_date = -1