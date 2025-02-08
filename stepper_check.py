import streamlit as st
import serial
import serial.tools.list_ports
import time

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
        with serial.Serial(arduino_port, baudrate=9600, timeout=2) as arduino:
            time.sleep(2)  # Wait for Arduino to initialize
            arduino.write(b"PING\n")  # Send test command
            response = arduino.readline().decode().strip()
            return response == "PONG"
    except serial.SerialException:
        return False

def send_stepper_command(arduino_port, stepper1_steps, stepper2_steps):
    """
    Sends stepper motor step commands to the Arduino.
    """
    try:
        with serial.Serial(arduino_port, baudrate=9600, timeout=2) as arduino:
            time.sleep(2)  # Wait for Arduino to initialize
            command = f"{stepper1_steps},{stepper2_steps}\n"
            arduino.write(command.encode())
            return f"Command sent: Stepper 1 = {stepper1_steps} steps, Stepper 2 = {stepper2_steps} steps"
    except serial.SerialException as e:
        return f"Error: {e}"

def test_stepper_movement(arduino_port):
    """
    Tests movement of two stepper motors by sending test commands to Arduino.
    """
    try:
        with serial.Serial(arduino_port, baudrate=9600, timeout=2) as arduino:
            time.sleep(2)  # Wait for Arduino to initialize
            
            # Test stepper movement
            test_positions = [
                (200, 200),  # Stepper 1: 200 steps, Stepper 2: 200 steps
                (400, 400),  # Stepper 1: 400 steps, Stepper 2: 400 steps
                (600, 600),  # Stepper 1: 600 steps, Stepper 2: 600 steps
                (800, 800)   # Stepper 1: 800 steps, Stepper 2: 800 steps
            ]
            
            for pos in test_positions:
                command = f"{pos[0]},{pos[1]}\n"
                arduino.write(command.encode())
                time.sleep(2)  # Wait for steppers to move

    except serial.SerialException as e:
        return f"Error during stepper test: {e}"

# Streamlit UI
st.title("Sky Watch Stepper Motor Controller")
st.markdown("Control two stepper motors to point to planets, stars, or calibrate them.")

# Find Arduino COM port
arduino_port = find_arduino()
if arduino_port:
    if check_arduino_connection(arduino_port):
        st.success(f"Arduino detected and connected on port: {arduino_port}")
    else:
        st.error("Arduino detected but not responding. Check connections.")
else:
    st.error("Arduino not found. Please connect it and refresh the app.")

# Stepper Control Section
st.header("Stepper Motor Control")
stepper1_steps = st.slider("Stepper 1 Steps", min_value=0, max_value=2000, value=1000, step=10)
stepper2_steps = st.slider("Stepper 2 Steps", min_value=0, max_value=2000, value=1000, step=10)

if st.button("Send Command"):
    if arduino_port:
        response = send_stepper_command(arduino_port, stepper1_steps, stepper2_steps)
        st.write(response)
    else:
        st.error("Arduino not connected. Please check the connection.")

# Stepper Test Section
st.header("Test Stepper Movement")
if st.button("Run Stepper Test"):
    if arduino_port:
        response = test_stepper_movement(arduino_port)
        st.write("Stepper movement test completed.")
    else:
        st.error("Arduino not connected. Please check the connection.")

# Calibration Section
st.header("Calibration")
st.markdown("Use this section to calibrate the stepper motors using reference points.")
calibration_preset = st.selectbox(
    "Select Calibration Preset",
    ["Select", "Reference Point 1", "Reference Point 2"]
)

if calibration_preset == "Reference Point 1":
    st.info("Setting steppers to Reference Point 1 (Stepper 1 = 500 steps, Stepper 2 = 250 steps)")
    if st.button("Calibrate to Reference Point 1"):
        if arduino_port:
            response = send_stepper_command(arduino_port, 500, 250)
            st.write(response)
        else:
            st.error("Arduino not connected. Please check the connection.")

elif calibration_preset == "Reference Point 2":
    st.info("Setting steppers to Reference Point 2 (Stepper 1 = 250 steps, Stepper 2 = 500 steps)")
    if st.button("Calibrate to Reference Point 2"):
        if arduino_port:
            response = send_stepper_command(arduino_port, 250, 500)
            st.write(response)
        else:
            st.error("Arduino not connected. Please check the connection.")

# Live Updates Section
st.header("Live Updates")
st.markdown("Feature under development: Live visibility updates for stars and planets based on your GPS coordinates and time.")
st.info("Stay tuned for future updates!")
