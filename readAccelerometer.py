

import serial

# for plotting
import matplotlib.pyplot    as plt
import matplotlib.animation as animation

import time

from scipy.fftpack import fft, fftfreq
import numpy as np

# Create figure for plotting
#fig = plt.figure()
#ax = fig.add_subplot(1, 1, 1)
#xs = []
#ys1 = []
#ys2 = []
#ys3 = []

# for ard code 
skip_start = True

read_time        = 10
calibration_time = 2

def animate(i, xs, ys):
    
        # Read temperature (Celsius) from TMP102
        #temp_c = round(tmp102.read_temp(), 2)
    serialString = serialPort.readline()
    data_vect = serialString.decode('Ascii').replace("\r\n", "").replace(".00", "").split(",")

    #print(data_vect)

    if "Start" not in data_vect:
        #print(data_vect)

        # Add x and y to lists
        xs.append(int(data_vect[0]))
        ys1.append(int(data_vect[1]))

        # Limit x and y lists to 20 items
        #xs = xs[-20:]
        #ys = ys[-20:]

        # Draw x and y lists
        ax.clear()
        ax.plot(xs, ys)

        # Format plot
        #plt.xticks(rotation=45, ha='right')
        #plt.subplots_adjust(bottom=0.30)
        plt.title('TMP102 Temperature over Time')
        plt.ylabel('Temperature (deg C)')

def Average(lst):
    return sum(lst) / len(lst)


serialPort = serial.Serial(port = "COM3", baudrate=115200,
                           bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)

serialString = ""                           # Used to hold data coming over UART



while(1):

    # Wait until there is data waiting in the serial buffer
    if(serialPort.in_waiting > 0):

        # Read data out of the buffer until a carraige return / new line is found
        serialString = serialPort.readline()


        # Print the contents of the serial data
        #print(int(serialString))
        #print(serialString.decode('Ascii'))

        # Parse data
        if "Start" in serialString.decode('Ascii'):

            #Buffer and plot setup

            time_var = 0
            time_prev = 0
            time_now  = 0

            tbuff = []
            Xbuff = []
            Ybuff = []
            Zbuff = []
            buff = [tbuff, Xbuff, Ybuff, Zbuff]

            # aminate setup
            
            #ani = animation.FuncAnimation(fig, animate, fargs=(xs, ys1), interval=1)
            #plt.show()

            start_time =+ time.time()
            current_time = 0

            print("Calibrating...")
            # calibrate sensors
            while(calibration_time > current_time):
                if not skip_start:
                    current_time = time.time() - start_time

                    serialString = serialPort.readline()

                    #print(serialString)

                    data_vect = serialString.decode('Ascii').replace("\r\n", "").replace(".00", "").split(",")

                    # convert Strings to ints
                    for i,data in enumerate(data_vect):
                        if i is 0:
                            buff[i].append(int(data))
                        else:
                            buff[i].append(int(data))

                    # print(buff)

                skip_start = not skip_start


            # Sensor Offset
            AvgX = Average(Xbuff)
            AvgY = Average(Ybuff)
            AvgZ = Average(Zbuff)
            AvgA = [0,AvgX, AvgY, AvgZ]

            print("Averages: ", AvgA)
            print("Reading...")

            # clear buffers
            tbuff = []
            Xbuff = []
            Ybuff = []
            Zbuff = []
            buff  = [tbuff, Xbuff, Ybuff, Zbuff]

            start_time =+ time.time()
            current_time = 0

            while(read_time > current_time):
                if not skip_start:
                    current_time = time.time() - start_time

                    serialString = serialPort.readline()

                    #print(serialString)

                    data_vect = serialString.decode('Ascii').replace("\r\n", "").replace(".00", "").split(",")

                    # convert Strings to ints
                    for i,data in enumerate(data_vect):
                        if i is 0:
                            buff[i].append(int(data)/1000)
                        else:
                            buff[i].append(int(data) - AvgA[i])

                    # print(buff)

                skip_start = not skip_start
            # plot buffers
            fig, (ax1, ax2, ax3) = plt.subplots(3)
            fig.suptitle('Accelerometer Readings')
            ax1.plot(buff[0], buff[1])
            ax2.plot(buff[0], buff[2])
            ax3.plot(buff[0], buff[3])
            #plt.show()

            vel_x = []
            vel_y = []
            vel_z = []

            pos_x = []
            pos_y = []
            pos_z = []


            for i, val in enumerate(buff[0]):
                if i > 0:
                    vel_x.append( (buff[1][i] - buff[1][i-1]/(buff[0][i] - buff[0][i-1]) ))
                    vel_y.append( (buff[2][i] - buff[2][i-1]/(buff[0][i] - buff[0][i-1]) ))
                    vel_z.append( (buff[3][i] - buff[3][i-1]/(buff[0][i] - buff[0][i-1]) ))

            #print(vel_x)

            for i, val in enumerate(vel_x):
                if i > 0:
                    pos_x.append( (vel_x[i] - vel_x[i-1]/(buff[0][i] - buff[0][i-1]) ))
                    pos_y.append( (vel_y[i] - vel_y[i-1]/(buff[0][i] - buff[0][i-1]) ))
                    pos_z.append( (vel_z[i] - vel_z[i-1]/(buff[0][i] - buff[0][i-1]) ))

            
            fig, (ax1, ax2, ax3) = plt.subplots(3)
            fig.suptitle('Accelerometer Readings Velocity')
            
            ax1.plot(buff[0][0:len(vel_x)], vel_x)
            ax2.plot(buff[0][0:len(vel_y)], vel_y)
            ax3.plot(buff[0][0:len(vel_z)], vel_z)
            
            """
            ax1.plot(buff[0:len(vel_x)-1], vel_x)
            ax2.plot(buff[0:len(vel_y)-1], vel_y)
            ax3.plot(buff[0:len(vel_z)-1], vel_z)
            """
            
             
            fig, (ax1, ax2, ax3) = plt.subplots(3)
            fig.suptitle('Accelerometer Readings Position')
            ax1.plot(buff[0][0:len(pos_x)], pos_x)
            ax2.plot(buff[0][0:len(pos_y)], pos_y)
            ax3.plot(buff[0][0:len(pos_z)], pos_z)
            

            ## FFT analysis

            N = len(buff[0])
            T = (buff[0][0] - buff[0][N-1])/N

            yf1 = fft(buff[1])
            xf1 = fftfreq(N, T)[:N//2]

            yf2 = fft(buff[2])
            xf2 = fftfreq(N, T)[:N//2]

            yf3 = fft(buff[3])
            xf3 = fftfreq(N, T)[:N//2]

            fig, (ax1, ax2, ax3) = plt.subplots(3)
            ax1.plot(xf1, 2.0/N * np.abs(yf1[0:N//2]))
            ax2.plot(xf2, 2.0/N * np.abs(yf2[0:N//2]))
            ax3.plot(xf3, 2.0/N * np.abs(yf3[0:N//2]))
            plt.grid()
            plt.show()

        
        # Tell the device connected over the serial port that we recevied the data!
        # The b at the beginning is used to indicate bytes!
        # serialPort.write(b"Thank you for sending data \r\n")