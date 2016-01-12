'''
Created on Dec 29, 2015

@author: Anirudh
'''


import sys
import csv
import datetime
import numpy as np
import os
import math

# Takes DOE data and converts to DERCAM data for specified aspects. For "aspect" see "aspectname" below
# Example of an input file: hospital-JacksonMS.csv
# Output: The five files in the folder JacksonMS-totalelectricity-DERCAM are written out
buildingname = 'hospital'
location = 'JacksonMS'
aspectname = 'totalelectricity' # A name for the thing of interest
relevant_columns = [1,2,3,5,6]  # Column A is indexed zero. These columns are relevant to the aspectname.
signs = [1,1,1,1,1]             # Coefficients for linear combinations of the columns
year = 2005                     # Determined in part manually
coefficient = float(1)          # Threshold coefficient t. Daily loads greater than (t*sigma)
                                #   are flagged as "peak".

"""Creating the target folders for all the processed files """
# Creating ./hospital-JacksonMS and folder ./hospital-JacksonMS/JacksonMS-totalelectricity-DERCAM/.
# These folders are created if they do not already exist.
targetfolder = './%s-%s/%s-%s-DERCAM/' %(buildingname,location,location,aspectname)
if not os.path.exists(os.path.dirname(targetfolder)):
    os.makedirs(os.path.dirname(targetfolder))

"""Creating the canonical form that isolates the particular aspect and gives a 24 hour profile for each day"""
# Creates file canonicalform-totalelectricity.csv inside of targetfolder
with open(targetfolder + 'canonicalform-%s.csv' %aspectname,'wb') as process:
    processWriter = csv.writer(process) # Set up for writing as a csv file. Lists can be written as comma-delimited rows. 
    with open('%s-%s.csv' %(buildingname,location),'r') as data: #
        dataReader = csv.reader(data)   # Reads in the entire file
        header = next(dataReader)       # Reads the header row as a list header[0], header[1], ...
        processWriter.writerow(['Date', 'Hour 1']+range(25)[2:]) # Date and hours written as column headers
        row = next(dataReader,None)     # Reads the first data row
        
        while True:
            fullday = [] #24 profile for a day
            if row == None:
                break
            
            date = row[0].split()[0]
            month = date.split('/')[0]
            day = date.split('/')[1]
            
            dateobj = datetime.date(year,int(month),int(day))
            
            fullday.append(date)    # fullday will be the entire row being written. Date appended here.
            while row[0].split()[0] == date:  #while we're in the same date
                targetvalue = 0 # targetvalue will be the linear combination of the relevant columns in this row
                for (sign,i) in zip(signs,relevant_columns):
                    targetvalue += sign*float(row[i])
                fullday.append(targetvalue) #append the hourly information
                row = next(dataReader,None) 
                if row == None:
                    break
            
            fullday.append(dateobj.strftime('%a'))
            processWriter.writerow(fullday)
            
# The canonicalform is now all done and written out.           
            

""" From 365 profiles, find a profile for each month. Repeat for typical weekday profile, weekend profile, peakday profile"""
with open(targetfolder + 'weekdayprocess-%s.csv' %aspectname,'wb') as weekdayprocess, open(targetfolder + 'weekendprocess-%s.csv' %aspectname,'wb') as weekendprocess, open(targetfolder + 'peakdayprocess-%s.csv' %aspectname,'wb') as peakdayprocess:
    weekprocessWriter = csv.writer(weekdayprocess) 
    weekendprocessWriter = csv.writer(weekendprocess)
    peakdayprocessWriter = csv.writer(peakdayprocess)
    with open(targetfolder + 'canonicalform-%s.csv' %aspectname,'r') as data:
        dataReader = csv.reader(data)
        header = next(dataReader)
        row = next(dataReader,None) #begin processing row-wise
        
        while True :
            if row == None:
                break
            currentdate = row[0]
            currentmonth = row[0].split('/')[0]
            
            currentday = row[0].split('/')[1]
            currentdateobj = datetime.date(year,int(currentmonth),int(currentday))
            
            weekdays = []
            peakdays = []
            weekends = []
            newweekdays = [] #some weekdays will be reassigned as peakdays
            
            while row[0].split('/')[0] == currentmonth: #process for the month
                if currentdateobj.isoweekday()> 5 : #the profile was a weekend
                    weekends.append(map(float,row[1:25]))
                else:
                    weekdays.append(map(float,row[1:25]))
                row = next(dataReader,None)
                if row == None:
                    break
                currentdateobj = datetime.date(year,int(row[0].split('/')[0]),int(row[0].split('/')[1]))
                
            numpyweekends = np.asarray(weekends) #prepare as numpy array to get averages
            weekendmean = np.mean(numpyweekends,axis = 0).tolist() #typical weekend profile is the average of all weekend profiles           
            numpyweekdays = np.asarray(weekdays) #prepare weekdays as numpy ararys
            normvectors = np.linalg.norm(numpyweekdays,axis = 1) #collect information about the 'norms' of the 24 hour profiles 
            
            #thresholds are based on the weekday norms - mean and standard deviation respectively. threshold1 decides when a weekday is reassigned as a peakday
            #threshold2 is used to deal with the case that there is no variation in the weekday norms whatsoever
            threshold1 = np.mean(normvectors) + coefficient*np.std(normvectors)
            threshold2 = np.mean(normvectors)- float(3/4)*np.std(normvectors)
            
            for day in weekdays: #reassign certain weekdays as peakdays if their norms are greater than threshold1
                if np.linalg.norm(np.asarray(day)) > threshold1:
                    peakdays.append(day)
                elif np.linalg.norm(np.asarray(day))>=math.floor(threshold2): #case where there is no variation in the data/precision issue
                    newweekdays.append(day)    
            
            #newweekmean = np.mean(np.asarray(newweekdays),axis = 0).tolist() #based on the reassigned weekdays, find out the typical weekday profile as an average 
            if peakdays: #there were, in fact, peakdays that crossed the threshold
                numpeak = len(peakdays) #keep track of number of peakdays
                peakmean = np.mean(np.asarray(peakdays),axis =0).tolist()
                newweekmean = np.mean(np.asarray(newweekdays),axis = 0).tolist() #peakday profile is the average of the peakdays
            else: #peak is simply the maximum over the weekdays
                numpeak = '1 (max norm)'
                sumWeekvectors = [sum(x) for x in newweekdays] 
                relevantindex = sumWeekvectors.index(max(sumWeekvectors))
                peakmean = newweekdays[relevantindex]
                del newweekdays[relevantindex]
                newweekmean = np.mean(np.asarray(newweekdays),axis = 0).tolist()    
                
                
            weekprocessWriter.writerow([currentmonth]+newweekmean)
            peakdayprocessWriter.writerow([currentmonth]+peakmean+[numpeak])
            weekendprocessWriter.writerow([currentmonth]+weekendmean)
            
with open(targetfolder + 'dercamprocess-%s.csv' %aspectname,'wb') as dercamsheet:
    dercamsheetWriter = csv.writer(dercamsheet)
    dercamsheetWriter.writerow(['Month'] + range(25)[1:])
    with open(targetfolder + 'weekdayprocess-%s.csv' %aspectname,'r') as weekprocess, \
        open(targetfolder + 'weekendprocess-%s.csv' %aspectname,'r') as weekendprocess, \
        open(targetfolder + 'peakdayprocess-%s.csv' %aspectname,'r') as peakdayprocess:
        weekprocessReader = csv.reader(weekprocess)
        weekendprocessReader = csv.reader(weekendprocess)
        peakdayprocessReader = csv.reader(peakdayprocess)
        while True:
            row = next(weekprocessReader,None)
            if row == None:
                break
            dercamsheetWriter.writerow(row)
        
        while True:
            row = next(peakdayprocessReader,None)
            if row == None:
                break
            dercamsheetWriter.writerow(row)
            
        while True:
            row = next(weekendprocessReader,None)
            if row == None:
                break
            dercamsheetWriter.writerow(row)