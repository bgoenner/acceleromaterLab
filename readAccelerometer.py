

import serial

serialPort = serial.Serial(port = "COM3", baudrate=115200,
                           bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)

serialString = ""                           # Used to hold data coming over UART

skip_start = True

while(1):

    # Wait until there is data waiting in the serial buffer
    if(serialPort.in_waiting > 0):

        # Read data out of the buffer until a carraige return / new line is found
        serialString = serialPort.readline()


        # Print the contents of the serial data
        #print(int(serialString))
        print(serialString.decode('Ascii'))

        # Parse data
        if "Start" in serialString.decode('Ascii'):
            while(1):
                if not skip_start:
                    serialString = serialPort.readline()

                    print(serialString)

                    data_vect = serialString.decode('Ascii').replace("\r\n", "").replace(".00", "").split(",")

                    for i,data in enumerate(data_vect):
                        data_vect[i] = int(data)

                    print(data_vect)

                skip_start = not skip_start

        

        # Tell the device connected over the serial port that we recevied the data!
        # The b at the beginning is used to indicate bytes!
        # serialPort.write(b"Thank you for sending data \r\n")