import random
import math
#This script was created using Python 2.7
#This script uses the standard Python libraries, math and random. Avoidance of dependencies was achieved.
#The data bins created for the telescopic data, the generated RFI and all intermediatry data structures are diplayed to screen
#and written to a text file called, 'RecoverRFI.txt'

def create_radio_t_data (bins): #Create the telescope data
    t_data = []
    for i in range(bins):
        t_data.append(random.gauss(0,1)) #telescope data represented as Gaussian noise with a mean of 0 and a standard deviation of 1
    return t_data


def calculate_stats(dataset):
    # A function to calculate the statistic properties of datasets. Numpy.py performs these calculations but Numpy.py is a non-standard Python library
    tot = 0
    for j in range(len(dataset)):
        tot += dataset[j]
    mean = tot/len(dataset)
    tot_square = 0
    for j in range(len(dataset)):
        square = math.pow((dataset[j] - mean),2)
        tot_square += square
    variance = tot_square/len(dataset)
    stnd_dev = math.sqrt(variance)
    return variance, stnd_dev, mean

def generate_RFI (rfi_samples, bins, rfi_burst_min, rfi_burst_max):
    # A function that generates radio interference
    rfi_data = []
    rfi_burst = random.randrange(2, rfi_samples) #The maximum number of RFI bursts is randomly chosen
    rfi_burst_length = random.randrange(rfi_burst_min,rfi_burst_max) #The number of RFI pulses in a burst is randomly chosen
    rfi_data = [0] * bins
    i = 0
    taken = []
    for i in range(0, rfi_burst): #RFI signals are generated and stored as an array of pulses occuring at random intervals
        start = random.randrange(1,bins)
        end = (start + rfi_burst_length)-1
        if (end < bins) and (start not in taken) and (end not in taken):
            for j in range(start,end+1):
                rfi_amp = random.randrange(5,10) #The amplitude of RFI signals is randomly chosen within a certain range
                rfi_data[j] = rfi_amp
                taken.append(j)
                    
##    print 'Max. No. of RFI Bursts: ', rfi_burst
##    print 'Burst Length: ', rfi_burst_length
    return rfi_data

def add_RFI (rfi, t_data): #RFI is inserted into the telescopic data bins
    modified_data = [x + y for x, y in zip(t_data,rfi)]
    return modified_data
   
def Flag_RFI(received_data, bins, variance_t_data): #RFI is detected using a threshold method
    #Method of RFI detection: The received data (telescopic data with inserted RFI) values are compared to a set threshold value. Data points exceeding this threshold value
    #are flagged as containing RFI
    threshold = 3*variance_t_data #The threshold value is chosen as 3 times the variance of the original telescopic data
    flag = [0] * bins
    positions  =[]
    i = 0
    for i in range(0,len(received_data)):
        if received_data[i] > threshold: 
            flag[i] = 1
    print('Detected RFI in received data. 1 indicates detection of RFI signal')
    
    for i in range(0,len(flag)):
        if flag[i] == 1:
            positions.append(i+1)
    print(flag)
    print('RFI data found in the following positions of the original telescope data stream:')
    print (positions)
    return flag

def Blanking (flags, t_data): #This function 'blanks' data values in the received data bins (original data with inserter RFI) in bins were RFI signales were detected.
    #Blanking sets bins where RFI was detected to '0'
    for i in range(0,len(flags)):
        if flags[i] == 1:
            t_data[i] = 0
    return t_data

def Test (t_data, blanked_data):
    #This function performs a test to check the statistical profiles of the original telescopic data and the flagged and blanked data.
    #If the variance, mean and standard deviation values for these two data sets match, RFI is deemed to have been successfully recovered.
    success = False
    [var1, dev1, mean1] = calculate_stats(t_data)
    [var2, dev2, mean2] = calculate_stats(blanked_data)
    if (var1==var2) and (dev1==dev2) and (mean1==mean2):
        print('RFI successfully detected. Blanked data and original telescope data have the same statistical properties')
        print('Variance and mean of original telesope data: ', var1, mean1)
        print('Variance and mean of blanked data: ', var2, mean2)
        success = True
    return success

##---------------------------------------------------------------------------------------------------------------------------------------------
    
##MAIN PROGRAM
        
bins = 100 #100 bins representing telescope data
rfi_samples =  10 #maximum number of RFI bursts
rfi_burst_length_min = 10
rfi_burst_length_max = 20

file = open("RecoverRFI.txt", "w")
telescope_data = create_radio_t_data (bins)
file.write('Telescope data:')
for item in telescope_data:
    file.write(("%s " % item))
file.write("\n")
print('Telescope data:')
print(telescope_data)

rfi = generate_RFI (rfi_samples, bins, rfi_burst_length_min, rfi_burst_length_max)
file.write('RFI data:')
for item in rfi:
    file.write(("%s " % item))
file.write("\n")
print('RFI:')
print(rfi)

added_RFI_telescope_data = add_RFI (rfi, telescope_data)
print('RFI + Telescope data:')
print(added_RFI_telescope_data)
file.write('RFI + Telescope data:')

for item in added_RFI_telescope_data:
    file.write(("%s " % item))
file.write("\n")
[var_t_data, stnddev, mean] = calculate_stats(telescope_data)

flags = Flag_RFI(added_RFI_telescope_data, bins, var_t_data)
blanked_telescope_data = blanked_data = Blanking(flags, telescope_data)
print('Blanked data:')
print(blanked_telescope_data)
file.write('Blanked data')
for item in blanked_telescope_data:
    file.write(("%s " % item))
file.write("\n")
file.write("\n")
file.write("\n")
success = Test(telescope_data, blanked_telescope_data)
if success:
    file.write('RFI successfully detected')




