import threading
import bluetooth
import time
import threading

LINE_COUNT = 5
COLUMN_COUNT = 6

AVG_COUNT = 10

user_input = ""

#uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"

print("Performing inquiry...")

nearby_devices = bluetooth.discover_devices(duration=8, lookup_names=True,
                                            flush_cache=True, lookup_class=False)

print("Found {} devices".format(len(nearby_devices)))

for addr, name in nearby_devices:
    try:
        print("   {} - {}".format(addr, name))
    except UnicodeEncodeError:
        print("   {} - {}".format(addr, name.encode("utf-8", "replace")))

addr1 = "FC:F5:C4:01:22:92"

service_matches = bluetooth.find_service(uuid=None, address=addr1)

if len(service_matches) == 0:
    print("Couldn't find the SampleServer service.")

first_match = service_matches[0]
port = first_match["port"]
name = first_match["name"]
host = first_match["host"]

print("Connecting to \"{}\" on {}".format(name, port))

# Create the client socket
sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
sock.connect((host, port))

print("Connected. Type something...")

while True:
    print("Write something:")
    data = input()
    if not data:
        break
    sock.send(data)
    break

recieved_count = 0
data_count = 0
sum_1 = 0
sum_2 = 0
sum_3 = 0
sum_4 = 0
sum_5 = 0
loop_end = time.perf_counter()

'''def input_function(name):
    while True:
        user_input = input()
        print("Copy that:", user_input)
        if user_input == "exit":
            break

thread = threading.Thread(target=input_function, args=(1,), daemon=True)
thread.start()'''

try:
    while True:
        
        data = sock.recv(1024)          #remember this is blocking, it won't pass until it recieves something new
        loop_start = time.perf_counter()
        print("Recieve Time: ", loop_end - loop_start)    #print sensor receive time time. How long were we waiting?
        data_str = str(data)
    
        with open('raw_chatter.csv', 'a') as the_file:
            if recieved_count == 0:
                write_line = "Start Recording at:" + str(loop_start) + '\n'
                the_file.write(write_line)
            write_line = str(loop_start) + ': ' + data_str
            the_file.write(write_line)
                   
        data_str = data_str[2:len(data_str)-1]
        print(data_str)
        data_array = data_str.split("\\n", maxsplit = LINE_COUNT)
        
        print(data_array)
        print(len(data_array))

        if len(data_array) > 1:
            #handling incomplete lines
            data_array.pop(LINE_COUNT)      #max split of 5 gives 6 lines, gotta drop the last one. max split of 4 doesn't trim remaining \n
            print("2nd line:", data_array[1])

            for line in data_array:
                line_array = line.split(', ', maxsplit = COLUMN_COUNT)
                
                try:
                    sensor_time = int(line_array[0])
                    hx711_1 = int(line_array[1])
                    hx711_2 = int(line_array[2])           
                    hx711_3 = int(line_array[3])
                    hx711_4 = int(line_array[4])
                    hx711_5 = int(line_array[5])

                    #if avg count == 1 write header
                    if data_count < AVG_COUNT:
                        sum_1 = hx711_1 + sum_1
                        sum_2 = hx711_2 + sum_2
                        sum_3 = hx711_3 + sum_3
                        sum_4 = hx711_4 + sum_4
                        sum_5 = hx711_5 + sum_5
                    elif data_count == AVG_COUNT:
                        hx711_1_avg = sum_1//AVG_COUNT
                        hx711_2_avg = sum_2//AVG_COUNT
                        hx711_3_avg = sum_3//AVG_COUNT
                        hx711_4_avg = sum_4//AVG_COUNT
                        hx711_5_avg = sum_5//AVG_COUNT
                        #average out and report sample
                    else:
                        hx711_1 = hx711_1 - hx711_1_avg
                        hx711_2 = hx711_2 - hx711_2_avg
                        hx711_3 = hx711_3 - hx711_3_avg
                        hx711_4 = hx711_4 - hx711_4_avg
                        hx711_5 = hx711_5 - hx711_5_avg
                    
                    with open('data_stream.csv', 'a') as the_file:
                        write_line = str(sensor_time) + ", " + str(hx711_1) + ", " + str(hx711_2) + ", " + str(hx711_3) + ", " + str(hx711_4) + ", " + str(hx711_5) + "\n"
                        the_file.write(write_line) #insert processed string line
                        print("Wrote file:", write_line)

                        '''if user_input != "":
                            write_line = user_input + ", "
                            the_file.write(write_line) 
                            print("wrote your input")fprdsf sdf 
                            user_input = ""
                        else:
                            write_line = "\n"
                            the_file.write(write_line)'''
                    
                    data_count = data_count+1                  

                except ValueError:
                    print("Invalid Input: ", line)

        if not data:
            break
        
        loop_end = time.perf_counter()
        loop_time = loop_end - loop_start
        print("Loop Time:", loop_time)
        
        recieved_count = recieved_count+1
        print("Received Count: ", recieved_count)
        print("Data Count:", data_count)

        if recieved_count > 100000:
            break

except OSError:
    pass

print("Not Stuck!")



