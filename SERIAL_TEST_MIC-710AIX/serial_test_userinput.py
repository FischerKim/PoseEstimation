#!/usr/bin/python3

import serial
import sys
import time

RTS_TX=1
RTS_RX=0

# delay after send (ms)
send_delay = 0.01
# delay after recv (ms)
recv_delay = 0.05
m_count = 5;

def main(device, mode, is_client, message=""):
    if mode == "232":
        test_serial(device, is_client, True, message)

    elif mode == "485":
        test_serial(device, is_client, True, message)
		
    elif mode == "422":
        test_serial(device, is_client, False, message)


def serial_init(ser, is_rts):
    if not is_rts:
        ser.setRTS(RTS_TX)


def serial_set_rts(ser, is_rts, enable):
    if is_rts:
        ser.setRTS(enable)

def serial_open(device, is_client, is_rts):
    ser = None
    if is_client:
        ser = serial.Serial(device, baudrate=115200, timeout=3.0)
    else:
        ser = serial.Serial(device, baudrate=115200, timeout=None)

    ser.close()
    ser.open()

    serial_init(ser, is_rts)
    ser.reset_input_buffer()
    ser.reset_output_buffer()

    return ser

def test_serial(device, is_client, is_rts, message):
    ser = serial_open(device, is_client, is_rts)

    if is_client:
        m_count = int(input("How many times to send packets?: "))
        i = 0
        count = 0
        while True:
            msg = bytes(message + '#' + str(i) + '\n', encoding='utf-8')
            i += 1
            print('->', msg)
            serial_set_rts(ser, is_rts, RTS_TX)
            
            ser.write(msg)
            time.sleep(send_delay)
            serial_set_rts(ser, is_rts, RTS_RX)
            
            read_bytes = ser.read_until()
            print('<-', read_bytes)
            
            if msg == read_bytes:
                print('good')
                count += 1
            else:
                print('fail')
                sys.exit()
            
            if count == m_count:
                print('pass')
                sys.exit()
            
            time.sleep(1)
    else:
        while True:
            serial_set_rts(ser, is_rts, RTS_RX)
            read_bytes = ser.read_until()
            print('<-', read_bytes)
            time.sleep(recv_delay)
            
            serial_set_rts(ser, is_rts, RTS_TX)
            ser.write(read_bytes)
            time.sleep(send_delay)

            serial_set_rts(ser, is_rts, RTS_TX)
            print('->', read_bytes)


if __name__ == '__main__':
    size = len(sys.argv)
    mode = sys.argv[1]
    device = sys.argv[2]

    if size == 4:
        print('Client Mode')
        message = sys.argv[3]

        if len(message) > 12:
            print("Message length is larger than 12 chars.")
            sys.exit()
        
        main(device, mode, True, message)

    elif size == 3: 
        print('Server Mode')
        main(device, mode, False)

    else:
        print("Usage:")
        print("      python3 serial.py mode device [message]")
        sys.exit()

