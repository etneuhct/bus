from pykinect import nui
import time
import json


def check_wrist_position(x, y):
    if y < 0:
        print('Below')
    if y > 0:
        print('Above')


def jumping_jacks(min_right_wrist_y, min_left_wrist_y, max_right_wrist_y, max_left_wrist_y):
    if abs(max_left_wrist_y - min_left_wrist_y) > 1 and abs(max_right_wrist_y - min_right_wrist_y) > 1:
        return True
    else:
        return False

with nui.Runtime() as kinect:
    kinect.camera.elevation_angle = 0
    kinect.skeleton_engine.enable=True
    start = time.clock()
    counter = 0

    current_max = 0
    max_deviation = 0

    min_right_wrist_y = 1
    max_right_wrist_y = -1

    min_left_wrist_y = 1
    max_left_wrist_y = -1

    while counter < 5:
        frame = kinect.skeleton_engine.get_next_frame()
        # if time.clock() - start > 5:
        #    break
        for skeleton in frame.SkeletonData:
            if skeleton.eTrackingState == nui.SkeletonTrackingState.TRACKED:
                positions = skeleton.get_skeleton_positions()
                """
                joints = ['Head',' FootRight ',' AnkleRight ',' KneeRight ',' HipRight ',' FootLeft ',' AnkleLeft ',
                          ' KneeLeft ',' HipLeft ',' HandRight ',' WristRight ',' ElbowRight ',' ShoulderRight ',
                          ' HandLeft ',' WristLeft ',' ElbowLeft ',' ShoulderLeft ',' Head ',' ShoulderCenter ',
                          ' Spine ',' HipCenter ']
                joints = [j.strip() for j in joints]
                positions = {joint: (position.x, position.y) for joint, position in zip(joints, positions)}
                #result = json.dumps(positions)
                """

                # Coordinates of points of interest
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

                if right_wrist_positions_y <= min_right_wrist_y and left_wrist_position_y <= min_left_wrist_y:
                    min_right_wrist_y = right_wrist_positions_y
                    min_left_wrist_y = left_wrist_position_y
                if right_wrist_positions_y >= max_left_wrist_y and left_wrist_position_y >= max_left_wrist_y:
                    max_right_wrist_y = right_wrist_positions_y
                    max_left_wrist_y = left_wrist_position_y

        if min_left_wrist_y != 1 and max_left_wrist_y != -1:
            if jumping_jacks(min_right_wrist_y, min_left_wrist_y, max_right_wrist_y, max_left_wrist_y):
                min_right_wrist_y = 1
                max_right_wrist_y = -1
                min_left_wrist_y = 1
                max_left_wrist_y = -1
                counter += 1
                print(str(counter))

                # check_wrist_position(right_wrist_positions_x, right_wrist_positions_y)
                #print('Left Wrist x: ' + str(left_wrist_position_x) + ' Left Wrist y: ' + str(left_wrist_position_y))
                #print('Right Wrist x: ' + str(right_wrist_positions_x) + ' Right Wrist y: ' + str(right_wrist_positions_y))