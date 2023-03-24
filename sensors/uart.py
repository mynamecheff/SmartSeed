from machine import UART
import time

# Define pins for UART communication
rx = 16
tx = 17

# Initialize serial communication through UART
uart = UART(2, baudrate=115200, rx=rx, tx=tx, timeout=10)

while True:
  
  # Send data to Raspberry Pi
  uart.write("Hello Raspberry Pi!\n")

  # Wait for 1 second
  time.sleep(1)
