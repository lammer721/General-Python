import serial
import time
import numpy as np

ser = serial.Serial(
    port='/dev/ttyUSB0', baudrate=115200)

print("connected to: " + ser.portstr)
count=1
time.sleep(1)

#with open('somefile.csv', 'a') as the_file:
#    the_file.write("today is:")

avg_1 = 0
avg_2 = 0
avg_3 = 0
averagecnt = 50

for i in range(averagecnt):
    
    ser.readline()
    line = ser.readline()
    count = count+1
 
    time.sleep(0.01)

    string_line = str(line)
    string_line = string_line[3:]
    string_line = string_line[:len(string_line)-5]
    array = string_line.split(", ")
    avg_1 += int(array[1])
    avg_2 += int(array[2])
    avg_3 += int(array[3])
    print(array[1])
    print(array[2])
    print(array[3])
    print(i)

avg_1 = avg_1//averagecnt
avg_2 = avg_2//averagecnt
avg_3 = avg_3//averagecnt
time_0 = int(array[0])

print(avg_1)
print(avg_2)
print(avg_3)
print(time_0)

while True:

    milliseconds = int(round(time.time() * 1000))
    
    ser.readline()
    line = ser.readline()
    count = count+1

    string_line = str(line)
    string_line = string_line[3:]
    string_line = string_line[:len(string_line)-5]
    array = string_line.split(", ")


    time_stamp = (int(array[0]) - time_0)/10
    read_1 = int(array[1]) - avg_1
    read_2 = int(array[2]) - avg_2
    read_3 = int(array[3]) - avg_3

    out_line = str(time_stamp) + ', ' + str(read_1) + ', ' + str(read_2) + ', ' + str(read_3) + '\n'

    print(time_stamp, ", ", read_1, ", ", read_2, ", ", read_3)

    with open('somefile.csv', 'a') as the_file:
        the_file.write(out_line)

ser.close()