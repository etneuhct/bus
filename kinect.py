from pykinect import nui
import json

with nui.Runtime() as kinect:
    kinect.camera.elevation_angle = 0
    kinect.skeleton_engine.enable=True
    while True:
        frame= kinect.skeleton_engine.get_next_frame()
        for skeleton in frame.SkeletonData:
            if skeleton.eTrackingState == nui.SkeletonTrackingState.TRACKED:
                positions = skeleton.get_skeleton_positions()
                joints = ['Head',' FootRight ',' AnkleRight ',' KneeRight ',' HipRight ',' FootLeft ',' AnkleLeft ',
                          ' KneeLeft ',' HipLeft ',' HandRight ',' WristRight ',' ElbowRight ',' ShoulderRight ',
                          ' HandLeft ',' WristLeft ',' ElbowLeft ',' ShoulderLeft ',' Head ',' ShoulderCenter ',
                          ' Spine ',' HipCenter ']
                joints = [j.strip() for j in joints]
                positions = {joint: (position.x, position.y, position.w, position.z) for joint, position in zip(joints, positions)}
                result = json.dumps(positions)
                print(result)