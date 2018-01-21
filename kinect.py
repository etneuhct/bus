from pykinect import nui
import time
import json

counter = 0

def check_wrist_position(x, y):
    if y < 0:
        print('Below')
    if y > 0:
        print('Above')


with nui.Runtime() as kinect:
    kinect.camera.elevation_angle = 0
    kinect.skeleton_engine.enable=True
    start = time.clock()

    while True:
        frame= kinect.skeleton_engine.get_next_frame()
        if time.clock() - start > 5:
            break
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
                #Coordinates of points of interest
                #Wrists
                right_wrist_positions_x = positions[nui.JointId.wrist_right].x
                right_wrist_positions_y = positions[nui.JointId.wrist_right].y

                left_wrist_position_x = positions[nui.JointId.wrist_left].x
                left_wrist_position_y = positions[nui.JointId.wrist_left].y

                #Knees
                right_knee_positions_x = positions[nui.JointId.knee_right].x
                right_knee_positions_y = positions[nui.JointId.knee_right].y

                left_knee_positions_x = positions[nui.JointId.knee_left].x
                left_knee_positions_y = positions[nui.JointId.knee_right].y

                #check_wrist_position(right_wrist_positions_x, right_wrist_positions_y)
                print('Left Wrist x: ' + str(left_wrist_position_x) + ' Left Wrist y: ' + str(left_wrist_position_y))
                print('Right Wrist x: ' + str(right_wrist_positions_x) + ' Right Wrist y: ' + str(right_wrist_positions_y))