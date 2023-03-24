from machine import UART
import time

# Define pins for UART communication
rx = 16
tx = 1# Initialize seri
import serial

# Define serial port configuration
serial_port = '/dev/ttyAMA0'
baud_rate = 115200

# Initialize serial communication object
ser = serial.Serial(serial_port, baud_rate)

while True:
    # Read incoming data from ESP32
    data = ser.readline().decode("utf-8")

    # Print the received data
    print(data)
