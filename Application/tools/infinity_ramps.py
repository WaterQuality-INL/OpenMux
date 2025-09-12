import numpy as np
import serial.serialutil
import threading
import time
import process_data as pro
import matplotlib.pyplot as plt
from binary_ops import *
from peak_search_engine import search4peak


def plot_thread():
    """
    This function is thread to plot the accuired point in the main graph from the GUI
    :return: displays the measured points in the graph
    """
    global px, py
    name, parameters = pro.get_parameters()
    tt0 = time.perf_counter()
    while Active_control == 'Start':
        pts_x = [volt_dac(bytes_array[0:2]) for bytes_array in byte_read]
        pts_y = [current_conversor(bytes_array[2:4]) for bytes_array in byte_read]
        #pts_x = np.delete(pts_x, [500, 501, 502, 503, 504, 505, 506, 507, 508, 509])
        #pts_y = np.delete(pts_y, [1000, 1001, 1002, 1003, 1004, 1005, 1006, 1007, 1008, 1009])
        try:
            time.sleep(0.2)
            #i_volt = len(pts_x) - 1
            #i_curr = len(pts_y) - 1
            #index = min(i_volt, i_curr)

            py, px = pro.process_this(name, pts_x, pts_y, parameters)

        except IndexError:
            print('IndexError in plot thread')

    tt1 = time.perf_counter() - tt0
    print(f'Plot thread finished in: {tt1 * 1000} ms')


def make_byte_array(ramps, nRamps):
    array = bytes([nRamps, nRepeat, nStep])
    for ramp in ramps:
        for i, item in enumerate(ramp):
            # 16-bit
            bit16 = decimal2signed16bit(int(item))
            byte16 = bits2bytes(bit16, order="RL")
            array = array + byte16

    return array


def read_ser():
    # 40 ms
    ser.read(size=4)  # OCV

    while len(byte_read) < selected_npts-1:
        com = ser.read(size=5)
        byte_read.append(com)
        #print(com)
    ser.read(1)  # 5a


nRepeat = 1
nStep = 1

nRamps_total, ramps_total = get_parameters(nStep)
npts_total = number_pts(ramps_total[:, 2])
selected_npts = 0


ser = serial.Serial('COM10', baudrate=153600, parity=serial.PARITY_ODD)

gain = bytes([6])
Active_control = "Start"
byte_read = []

px = 0
py = 0

window_size = 90

idx0 = 0
idx1 = window_size

threading.Thread(target=plot_thread).start()

print(nRamps_total)

ser.write(b'O')
ser.read(2)

ser.write(b'G' + gain)
ser.read(2)

while idx0 < nRamps_total:
    # 0.05 ms
    #t0 = time.perf_counter()  # Starting timing
    selected_ramps = ramps_total[idx0:idx1, :]
    selected_nRamps = len(selected_ramps)
    selected_npts += number_pts(selected_ramps[:, 2])

    # 1.35 ms
    byte_array1 = make_byte_array(selected_ramps, selected_nRamps)

    # 0.001 ms
    idx0 = idx1
    idx1 += window_size
    if idx1 > nRamps_total:
        idx1 = nRamps_total
    #t05 = time.perf_counter() - t0
    # 21 ms
    #t0 = time.perf_counter()  # Starting timing
    ser.write(b'R' + byte_array1 + b'M' + bytes([0b00100001, 0, 0, 0, 0]))
    #t1 = time.perf_counter() - t0
    #print(f'Pre work elapsed time: {t05 * 1000} ms')
    #print(f'Loading elapsed time: {t1 * 1000} ms')
    read_ser()


ser.write(b'F')
ser.read(1)

Active_control = 'Stop'

plt.plot(px, py, '.')
npx = np.array(px)
npy = np.array(py)
npx = np.delete(npx, [44, 45, 89, 90])
npy = np.delete(npy, [44, 45, 89, 90])
plt.plot(npx, npy)

print('Voltage (V)\tCurrent (A)')
for i, item in enumerate(npx):
    print(f'{i+1}\t{npx[i]}\t{npy[i]}')

search4peak(npx, npy, name='name')
plt.show()

