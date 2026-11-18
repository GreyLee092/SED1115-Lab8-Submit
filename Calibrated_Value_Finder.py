#this function searches for the boundry angles to interpolate

import pandas as pd
from pandas import DataFrame
#math for rounding
import math

#function for getting shoulder calibration interpolation bounds
def shoulder(inter):
    #is the upper bound of interpolated value, rounded to next 10th
    hi = math.ceil(float(inter)/ 10) * 10
    #lower bound of interpolated value, rounded to previous 10th
    lo = math.floor(float(inter)/ 10) * 10
    #print for debugging
    print(hi, lo)
    #gets shoulder calibration values
    #creates dataframe from file
    df = DataFrame(pd.read_csv("/Users/greysonlee/PycharmProjects/PenPlotter/Shoulder_Servo_Calibration_Values.csv"))
    #copies as to not read again
    df1 = df.copy()
    #returns value for the high bound
    hi_bound = df1.loc[df["angle"] == hi, "difference"]
    #converts to string without header or index text
    hi_bound = hi_bound.to_string(index=False, header=False)
    #copies as to not read again
    df2 = df.copy()
    #returns value for the low bound
    df2 = df2.loc[df["angle"] == lo, "difference"]
    #converts to string without header or index text
    lo_bound = df2.to_string(index=False, header=False)
    #returns elbow bounds and their values
    return hi_bound, hi, lo_bound, lo

#function for getting elbow calibration interpolation bounds
def elbow(inter):
    #is the upper bound of interpolated value, rounded to next 10th
    hi = math.ceil(float(inter)/ 10) * 10
    #lower bound of interpolated value, rounded to previous 10th
    lo = math.floor(float(inter)/ 10) * 10
    #print for debugging
    print(hi, lo)
    #gets elbow calibration values
    #creates dataframe from file
    df = DataFrame(pd.read_csv("/Users/greysonlee/PycharmProjects/PenPlotter/Elbow_Servo_Calibrated_Values.csv"))
    #copies as to not read again
    df1 = df.copy()
    #returns value for the high bound
    hi_bound = df1.loc[df["angle"] == hi, "difference"]
    #converts to string without header or index text
    hi_bound = hi_bound.to_string(index=False, header=False)
    #copies as to not read again
    df2 = df.copy()
    #returns value for the low bound
    df2 = df2.loc[df["angle"] == lo, "difference"]
    #converts to string without header or index text
    lo_bound = df2.to_string(index=False, header=False)
    #returns elbow bounds and their values
    return hi_bound, hi, lo_bound, lo

#for coding / debugging
#inputs would be from calculations block
user_input1 = input("Enter angle number for shoulder: ")
#calls shoulder calibration function
#returns the interpolation bounds and bound values
hi_S, hi_valS, lo_S, lo_valS = shoulder(user_input1)
user_input2 = input("Enter angle number for elbow: ")
#calls elbow calibration function
#returns the interpolation bounds and bound values
hi_E, hi_valE, lo_E, lo_valE = elbow(user_input2)
#print statement for debugging
print(f"Shoulder hi bound:{hi_valS} = {hi_S}", type(hi_S))
print(f"Shoulder lo bound:{lo_valS} = {lo_S}", type(lo_S))
print(f"Elbow hi bound:{hi_valE} = {hi_E}", type(hi_E))
print(f"Elbow lo bound:{lo_valE} = {lo_E}", type(lo_E))
