import serial.tools.list_ports
import serial
import time

target_yaw = 0.0
target_pitch = 0.0


def find_arduino():
    """
    Automatically detects the Arduino's COM port.
    """
    ports = serial.tools.list_ports.comports()
    for port in ports:
        if "Arduino" in port.description or "USB-SERIAL" in port.description:
            return port.device
    return None

def check_arduino_connection(arduino_port):
    """
    Checks if the Arduino is connected and responding.
    """
    try:
        with serial.Serial(arduino_port, baudrate=9600, timeout=0) as arduino:
            time.sleep(2)  # Wait for Arduino to initialize
            # arduino.write(b"PING\n")  # Send test command
            # response = arduino.readline().decode().strip()
            
            return arduino
    except serial.SerialException:
        return False
# Connect to Arduino (update COM port if needed)
# arduino = serial.Serial(port='COM3', baudrate=9600, timeout=1)
# time.sleep(2)  # Allow connection to establish

# Target angles (North, 0° altitude)


def read_mpu_data(arduino):
    """Reads MPU-6050 data from Arduino."""
    print(arduino)
    arduino.write(b"GET_MPU\n")  # Request MPU values
    line = arduino.readline().decode().strip()
    if line.startswith("MPU:"):
        values = line.replace("MPU:", "").split(",")
        return float(values[0]), float(values[1])  # Yaw, Pitch
    return None, None

def correct_position(arduino):
    """Continuously adjust stepper motors until MPU matches target."""
    print(arduino)
    while True:
        current_yaw, current_pitch = read_mpu_data(arduino)
        if current_yaw is None or current_pitch is None:
            continue

        print(f"Current Yaw: {current_yaw}°, Current Pitch: {current_pitch}°")
        
        # Check if the laser is aligned
        if abs(current_yaw - target_yaw) < 0.5 and abs(current_pitch - target_pitch) < 0.5:
            print("Laser is perfectly aligned!")
            break  # Stop adjusting

        # Send correction commands
        correction_cmd = f"{target_yaw},{target_pitch}\n"
        arduino.write(correction_cmd.encode())
        time.sleep(1)  # Give time for movement

# Start correction
# correct_position()

if __name__ == "__main__":
    port_no = find_arduino()
    arduino = check_arduino_connection(port_no)
    print(arduino)
    correct_position(arduino)
