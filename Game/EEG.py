# EEG.py

import serial  # Now it should work!

import time
from collections import deque
from constants import SF, BUFFER_SEC

class EEGDevice:

    

    def __init__(self, port, baudrate=57600):
        self.ser = serial.Serial(port, baudrate)  # Initialize serial communication
        self.eeg_buffer = deque(maxlen=SF * BUFFER_SEC)  # Circular buffer for EEG data
        self.attention_value = 0  # Static variable for attention
        self.meditation_value = 0  # Static variable for meditation

    def fetch_data(self):
        """Reads EEG data from the device and updates attention/meditation values."""
        self.ser.read_until(b'\xaa\xaa')  # Wait for sync bytes
        payload = []
        checksum = 0
        packet_length = self.ser.read(1)
        payload_length = packet_length[0]

        for i in range(payload_length):
            packet_code = self.ser.read(1)
            tempPacket = packet_code[0]
            payload.append(packet_code)
            checksum += tempPacket

        checksum = ~checksum & 0xff
        check = self.ser.read(1)

        if checksum != check[0]:
            print("ERROR: Checksum mismatch!")
            return

        i = 0
        while i < payload_length:
            packet = payload[i]
            if packet == b'\x80':  # Raw EEG data
                i += 2
                val0, val1 = payload[i], payload[i + 1]
                raw_value = val0[0] * 256 + val1[0]
                if raw_value > 32768:
                    raw_value -= 65536
                self.eeg_buffer.append(raw_value)
            elif packet == b'\x04':  # Attention
                i += 1
                self.attention_value = payload[i][0]
            elif packet == b'\x05':  # Meditation
                i += 1  
                self.meditation_value = payload[i][0]
            i += 1

    def close(self):
        self.ser.close()
