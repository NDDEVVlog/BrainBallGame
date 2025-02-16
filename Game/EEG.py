# EEG.py

import serial  # Now it should work!

import time
from collections import deque
from constants import SF, BUFFER_SEC
import numpy as np
from scipy.signal import butter, lfilter
class EEGDevice:

    

    def __init__(self, port, baudrate=57600):
        try:
            self.ser = serial.Serial(port, baudrate)  # Initialize serial communication
            self.eeg_buffer = deque(maxlen=SF * BUFFER_SEC)  # Circular buffer for EEG data
            self.attention_value = 0  # Static variable for attention
            self.meditation_value = 0  # Static variable for meditation
            
            self.avg_attention=0
            self.avg_meditation=0
                    # New: Store last 5 seconds (20 updates)
            self.attention_history = deque(maxlen=64)
            self.meditation_history = deque(maxlen=64)
            # Print initialization details
            print(f"EEG Device Initialized on {port} with baud rate {baudrate}")
            print(f"Serial Connection Open: {self.ser.is_open}")

        except serial.SerialException as e:
            print(f"ERROR: Failed to connect to {port}: {e}")



    def fetch_data(self):
        """
        Reads one data packet from the EEG device, verifies the checksum,
        and updates the EEG buffer.
        """
        try:
            if self.ser.in_waiting < 2:
                return  # Skip if not enough data

            # Read until sync bytes (0xAA 0xAA)
            sync = self.ser.read_until(b'\xaa\xaa')
            if len(sync) < 2:
                return  

            # Read packet length
            packet_length = self.ser.read(1)
            if not packet_length:
                return  
            packet_length = packet_length[0]

            # Read payload
            payload = self.ser.read(packet_length)
            if len(payload) != packet_length:
                return  

            # Verify checksum
            checksum = sum(payload) & 0xFF
            checksum = (~checksum) & 0xFF
            received_checksum = self.ser.read(1)
            if not received_checksum or received_checksum[0] != checksum:
                return  # Skip invalid packets

            # Reset data for this packet
            self.data = {}

            # Parse payload
            i = 0
            while i < len(payload):
                code = payload[i]
                i += 1

                if code >= 0x80:  # Extended code
                    if i >= len(payload):
                        return  
                    length = payload[i]
                    i += 1
                    if code == 0x80 and length == 2:  # EEG raw data
                        if i + 1 >= len(payload):
                            return  
                        val0, val1 = payload[i], payload[i + 1]
                        raw_value = (val0 << 8) | val1
                        if raw_value > 32768:
                            raw_value -= 65536
                        self.eeg_buffer.append(raw_value)
                        self.data['eeg_raw'] = raw_value
                        i += 2
                    else:
                        i += length
                #else:  # Simple code
                #    if i >= len(payload):
                #        return  
                #    value = payload[i]
                #    i += 1
#
                #    if code == 0x02:  # Signal quality
                #        self.quality = value
                #    elif code == 0x04:  # Attention
                #        self.attention_value = value
                #        print(f"Attention Value: {self.attention_value}")
                #    elif code == 0x05:  # Meditation
                #        self.meditation_value = value
                #        print(f"Mediation Value: {self.meditation_value}")
                       
            self.compute_attention_meditation()
        except Exception as e:
            print(f"Error in fetch_data: {e}")

    
    def butter_bandpass(self, lowcut, highcut, fs, order=4):
        nyq = 0.5 * fs
        low = lowcut / nyq
        high = highcut / nyq
        b, a = butter(order, [low, high], btype='band')
        return b, a

    def bandpass_filter(self, data, lowcut=1.0, highcut=50.0, fs=512, order=4):
        try:
            b, a = self.butter_bandpass(lowcut, highcut, fs, order)
            return lfilter(b, a, data)
        except Exception as e:
            print(f"Error in bandpass_filter: {e}")
            return data  

    def compute_attention_meditation(self):
        print("Compute Attention Meditation")
        if len(self.eeg_buffer) < 128:
            return

        try:
            # Convert deque to NumPy array
            eeg_signal = np.array(list(self.eeg_buffer)[-128:], dtype=np.float32)
            filtered_signal = self.bandpass_filter(eeg_signal)

            # FFT for frequency analysis
            fft_values = np.abs(np.fft.rfft(filtered_signal))
            fft_freqs = np.fft.rfftfreq(len(filtered_signal), 1 / 512)

            # Compute power in different frequency bands
            delta_power = np.sum(fft_values[(fft_freqs >= 1) & (fft_freqs < 4)])
            theta_power = np.sum(fft_values[(fft_freqs >= 4) & (fft_freqs < 8)])
            alpha_power = np.sum(fft_values[(fft_freqs >= 8) & (fft_freqs < 13)])
            beta_power = np.sum(fft_values[(fft_freqs >= 13) & (fft_freqs < 30)])
            gamma_power = np.sum(fft_values[(fft_freqs >= 30) & (fft_freqs < 50)])

            if (delta_power + theta_power) > 0:
                self.attention_value = int((beta_power / (delta_power + theta_power)) * 100)
                self.meditation_value = int((alpha_power+theta_power) / beta_power  ) * 100

            # Store values in history for 5-second averaging
            self.attention_history.append(self.attention_value)
            self.meditation_history.append(self.meditation_value)

            # Compute average over last 5 seconds
            self.avg_attention = round( np.mean(self.attention_history)) if self.attention_history else 0
            self.avg_meditation = round (np.mean(self.meditation_history)) if self.meditation_history else 0

            print(f"Current Attention: {self.attention_value}, Avg Attention (5s): {self.avg_attention:.2f}")
            print(f"Current Meditation: {self.meditation_value}, Avg Meditation (5s): {self.avg_meditation:.2f}")

        except Exception as e:
            print(f"Error in compute_attention_meditation: {e}")

    def print_values(self):
        print(f"\U0001F9E0 Attention: {self.attention_value} | \U0001F9D8 Meditation: {self.meditation_value}")






    def close(self):
        self.ser.close()
