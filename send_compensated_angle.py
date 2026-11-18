import math

from Calibrated_Value_Finder import bound_searcher
from Servo_Angle_Translator import translate

def calculation(x_coor, y_coor):
    vector = hypotenuse_length(x_coor, y_coor)
    angle_shoulder, angle_elbow = angles(vector/2)
    angle_shoulder = bound_searcher(angle_shoulder,"Shoulder_Servo_Calibration_Values.csv")
    angle_elbow = bound_searcher(angle_elbow, "Elbow_Servo_Calibrated_Values.csv")
    return angle_shoulder, angle_elbow

def hypotenuse_length(x, y):
    #shoulder root x position
    origin_x = -50
    #shoulder root y position
    origin_y = 139.5
    #returns length of vector
    return math.sqrt(math.pow(x-origin_x, 2) + math.pow(y-origin_y, 2))

def angles(adjacent):
    hypotenuse = 15
    angle_a = math.degrees(math.acos(adjacent/hypotenuse))
    angle_b = 180 - (2 * angle_a)
    return angle_a, angle_b

def servo_interpolation(angle, b, c, d, e):
    upper_bound_target = b
    upper_bound_real =  c
    lower_bound_target = d
    lower_bound_real =  e
    #finds slope
    slope = ((upper_bound_real - lower_bound_real) /
             (upper_bound_target - lower_bound_target))
    #y intercept
    y_intercept = upper_bound_real - (slope * upper_bound_target)
    #returns y value of inputted x coordinate
    return slope * angle + y_intercept

def main(x_pos, y_pos):
    while True:
        #calls function to calculate servo angles
        shoulder_angle, elbow_angle = calculation(x_pos, y_pos)
        hi_bound, hi_value, lo_bound, lo_value = bound_searcher(shoulder_angle,
                                                    "Shoulder_Servo_Calibration_Values.csv")
        top_bound, top_value, bot_bound, bot_value = bound_searcher(elbow_angle,
                                                    "Elbow_Servo_Calibrated_Values.csv")
        #runs interpolation function for shoulder angle then translates shoulder servo
        translate(servo_interpolation(shoulder_angle, hi_bound, hi_value, lo_bound, lo_value))
        #runs interpolation function for elbow angle then translates elbow servo
        translate(servo_interpolation(elbow_angle, top_bound, top_value, bot_bound, bot_value))



