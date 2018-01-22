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

def jumping_jacks(min_right_wrist_y, min_left_wrist_y, max_right_wrist_y, max_left_wrist_y, knee_distance_x):
    if max_left_wrist_y - min_left_wrist_y > 1 and max_right_wrist_y - min_right_wrist_y > 1:
        if knee_distance_x > 0.2:
            return True
    else:
        return False


def touch_toe(shoulder_position_y):
    return  shoulder_position_y < 0.15

with nui.Runtime() as kinect:
    while 1:
        kinect.camera.elevation_angle = 0
        kinect.skeleton_engine.enable=True
        start = time.clock()
        counter_jacks = 0
        counter_toe = 0

        last_count_toe_date = -1

        min_right_wrist_y = 1
        max_right_wrist_y = -1
        min_left_wrist_y = 1
        max_left_wrist_y = -1

        knee_distance_x = 0
        wrist_position_y = 0
        knee_position_y = -2
        shoulder_position_y = 2

        while counter_jacks < 5 or counter_toe < 5:
            frame = kinect.skeleton_engine.get_next_frame()
            # if time.clock() - start > 5:
            #    break
            for skeleton in frame.SkeletonData:
                seen = False
                if skeleton.eTrackingState != nui.SkeletonTrackingState.TRACKED:
                    send_data_far(True)

                if skeleton.eTrackingState == nui.SkeletonTrackingState.TRACKED:
                    send_data_far(False)
                    positions = skeleton.get_skeleton_positions()
                    if positions[nui.JointId.head].z > 2:
                        # Coordinates of points of interest
                        
                        if not seen:
                            print(' I see you !')
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

                        #print(str(shoulder_position_y))


                        knee_distance_x = abs(right_knee_positions_x - left_knee_positions_x)

                        if right_wrist_positions_y < min_right_wrist_y and left_wrist_position_y < min_left_wrist_y:
                            min_right_wrist_y = right_wrist_positions_y
                            min_left_wrist_y = left_wrist_position_y

                        if right_wrist_positions_y > max_left_wrist_y and left_wrist_position_y > max_left_wrist_y:
                            max_right_wrist_y = right_wrist_positions_y
                            max_left_wrist_y = left_wrist_position_y

                        if max_right_wrist_y > 0.5 and counter_jacks < 5:
                            if min_left_wrist_y != 1 and max_left_wrist_y != -1:
                                if jumping_jacks(min_right_wrist_y, min_left_wrist_y, max_right_wrist_y, max_left_wrist_y, knee_distance_x):
                                    min_right_wrist_y = 1
                                    max_right_wrist_y = -1
                                    min_left_wrist_y = 1
                                    max_left_wrist_y = -1
                                    knee_distance_x = 0
                                    counter_jacks += 1
                                    send_data_counter(counter_jacks, "jumping_jacks")
                                    print('Number of jumping jacks: ' + str(counter_jacks))

                        wrist_position_y = min(right_wrist_positions_y, left_wrist_position_y)
                        knee_position_y = min(right_knee_positions_y, left_knee_positions_y)
                        subtraction = abs(wrist_position_y-knee_position_y)
                        #print('Difference y: ' + str(subtraction))
                        #print('Knee y: ' + str(knee_position_y))
                        if counter_jacks < 5:
                            continue
                         

                        if (last_count_toe_date == -1 or time.clock() - last_count_toe_date >= 2) and touch_toe(shoulder_position_y):
                            last_count_toe_date = time.clock()
                            counter_toe += 1
                            shoulder_position_y = 2
                            send_data_counter(counter_toe, "touch_toe") 
                            print('You touched your toe: ' + str(counter_toe) + ' time(s).')
                        if counter_jacks == 5 and counter_toe == 0:
                            send_data_counter(counter_toe, "touch_toe")
                        if counter_toe == 5:    
                            send_data_counter(0, "jumping_jacks")
                            
if __name__ == '__main__':
    last_post_date = -1