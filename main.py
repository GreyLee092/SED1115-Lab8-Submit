import math
import time
from machine import Pin, PWM

# GPIO pin setup for servos
shoulder_servo = PWM(Pin(0))
elbow_servo = PWM(Pin(1))
shoulder_servo.freq(50)
elbow_servo.freq(50)

# Jig constants
AX = -50.0
AY = 139.5
LA = 155.0
LB = 155.0
OFFSET_A = 75.0
OFFSET_B = 150.0


def set_raw_angle(servo, angle):
    """Sends a raw angle (0 to 180 deg) to a servo via PWM duty cycle."""
    angle = max(0.0, min(180.0, angle))
    # 0.5 ms (1638) to 2.5 ms (8192) duty cycle at 50 Hz
    duty = int(1638 + (angle / 180.0) * (8192 - 1638))
    servo.duty_u16(duty)


def inverse_kinematics(Cx, Cy):
    """Calculates required servoA and servoB angles (in degrees) for target (Cx, Cy)."""
    ac = math.sqrt((AX - Cx) ** 2 + (AY - Cy) ** 2)  # Equation (1)
    abase_c = math.sqrt((AX - Cx) ** 2 + Cy ** 2)  # Equation (2)

    cos_bac = max(-1.0, min(1.0, (LA ** 2 + ac ** 2 - LB ** 2) / (2 * LA * ac)))
    angle_bac = math.acos(cos_bac)  # Equation (3)

    sin_acb = max(-1.0, min(1.0, (LA * math.sin(angle_bac)) / LB))
    angle_acb = math.asin(sin_acb)  # Equation (4)

    cos_yac = max(-1.0, min(1.0, (AY ** 2 + ac ** 2 - abase_c ** 2) / (2 * AY * ac)))
    angle_yac = math.acos(cos_yac)  # Equation (5)

    alpha = math.degrees(angle_bac + angle_yac)  # Equation (6)
    beta = math.degrees(angle_bac + angle_acb)  # Equation (7)

    servo_a = alpha - OFFSET_A  # Equation (8)
    servo_b = OFFSET_B - beta  # Equation (9)
    
    return servo_a, servo_b


def calibration_setup(filename):
    """Reads calibration_data_X.txt and returns a dictionary mapping angle -> (err_shoulder, err_elbow)."""
    error_table = {}
    with open(filename, "r") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split(",")
            angle = int(parts[0])
            err_shoulder = float(parts[1])
            err_elbow = float(parts[2])
            error_table[angle] = (err_shoulder, err_elbow)
    return error_table


def interpolate_error(angle, error_table, servo_index):
    """Linearly interpolates servo error between 10-degree table steps."""
    angle = max(0.0, min(180.0, angle))
    lower = int(angle // 10) * 10
    upper = min(180, lower + 10)
    
    if lower == upper:
        return error_table[lower][servo_index]
        
    err_low = error_table[lower][servo_index]
    err_high = error_table[upper][servo_index]
    
    fraction = (angle - lower) / 10.0
    return err_low + fraction * (err_high - err_low)


def send_compensated_angle(desired_A, desired_B, error_table):
    """Looks up interpolated error, adjusts desired angles, and commands servos."""
    err_A = interpolate_error(desired_A, error_table, 0)
    err_B = interpolate_error(desired_B, error_table, 1)
    
    # Subtract measured error (actual - desired) to compensate
    compensated_A = desired_A - err_A
    compensated_B = desired_B - err_B
    
    set_raw_angle(shoulder_servo, compensated_A)
    set_raw_angle(elbow_servo, compensated_B)


def draw_test_shape(calibrated=False, error_table=None):
    """Draws a segmented square to compare uncalibrated vs. calibrated accuracy."""
    corners = [(60, 80), (140, 80), (140, 160), (60, 160), (60, 80)]
    steps_per_edge = 20
    
    for i in range(len(corners) - 1):
        x0, y0 = corners[i]
        x1, y1 = corners[i + 1]
        for step in range(steps_per_edge + 1):
            t = step / steps_per_edge
            x = x0 + t * (x1 - x0)
            y = y0 + t * (y1 - y0)
            
            sA, sB = inverse_kinematics(x, y)
            if calibrated and error_table is not None:
                send_compensated_angle(sA, sB, error_table)
            else:
                set_raw_angle(shoulder_servo, sA)
                set_raw_angle(elbow_servo, sB)
            time.sleep(0.05)


if __name__ == "__main__":
    # Read calibration data from file
    cal_table = calibration_setup("calibration_data_X.txt")
    
    print("Drawing uncalibrated shape...")
    draw_test_shape(calibrated=False)
    
    input("Swap pen or paper, then press Enter to draw calibrated shape...")
    
    print("Drawing calibrated shape...")
    draw_test_shape(calibrated=True, error_table=cal_table)
    print("Done!")