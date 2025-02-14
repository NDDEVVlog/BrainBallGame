# EEG.py

import serial  # Now it should work!

import time
from collections import deque
from constants import SF, BUFFER_SEC

class EEGDevice:

    

    def __init__(self, port, baudrate=57600):
        try:
            self.ser = serial.Serial(port, baudrate)  # Initialize serial communication
            self.eeg_buffer = deque(maxlen=SF * BUFFER_SEC)  # Circular buffer for EEG data
            self.attention_value = 0  # Static variable for attention
            self.meditation_value = 0  # Static variable for meditation
                    
            # Print initialization details
            print(f"EEG Device Initialized on {port} with baud rate {baudrate}")
            print(f"Serial Connection Open: {self.ser.is_open}")

        except serial.SerialException as e:
            print(f"ERROR: Failed to connect to {port}: {e}")


    def fetch_data(self):
        """Reads EEG data from the device and updates attention/meditation values."""
        try:
            print("Start to fetch data")

            # Set a timeout to avoid freezing on read
            self.ser.timeout = 2  # Timeout in seconds
            
            # Wait for sync bytes with a timeout
            sync_bytes = self.ser.read_until(b'\xaa\xaa')
            if not sync_bytes:
                raise ValueError("No sync bytes received (Timeout or No Data).")

            payload = []
            checksum = 0

            # Read packet length with timeout
            packet_length = self.ser.read(1)
            if not packet_length:
                raise ValueError("No packet length received.")

            payload_length = packet_length[0]

            # Read payload with timeout
            for i in range(payload_length):
                packet_code = self.ser.read(1)
                if not packet_code:
                    raise ValueError("Incomplete payload received (Timeout).")
                
                tempPacket = packet_code[0]
                payload.append(packet_code)
                checksum += tempPacket

            # Read and verify checksum
            checksum = ~checksum & 0xff
            check = self.ser.read(1)
            if not check or checksum != check[0]:
                raise ValueError("Checksum mismatch or no checksum received.")

            # Process the payload
            i = 0
            while i < payload_length:
                packet = payload[i]
                if packet == b'\x80':  # Raw EEG data
                    if i + 2 >= payload_length:
                        raise ValueError("Incomplete raw EEG data.")
                    
                    i += 2
                    val0, val1 = payload[i], payload[i + 1]
                    raw_value = val0[0] * 256 + val1[0]
                    if raw_value > 32768:
                        raw_value -= 65536
                    self.eeg_buffer.append(raw_value)

                elif packet == b'\x04':  # Attention
                    if i + 1 >= payload_length:
                        raise ValueError("Incomplete attention value.")
                    i += 1
                    self.attention_value = payload[i][0]

                elif packet == b'\x05':  # Meditation
                    if i + 1 >= payload_length:
                        raise ValueError("Incomplete meditation value.")
                    i += 1  
                    self.meditation_value = payload[i][0]
                    
                i += 1

        except serial.SerialTimeoutException:
            print("Serial Timeout: No response from EEG device.")

        except ValueError as ve:
            print(f"ERROR: {ve}")

        except serial.SerialException as se:
            print(f"Serial Error: {se}")

        except Exception as e:
            print(f"Unexpected Error: {e}")





    def close(self):
        self.ser.close()
