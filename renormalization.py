'''
Created on Nov 23, 2015

@author: Anirudh
'''

import csv

buildingname = 'hospital'
location = 'JacksonMS'
aspectname = 'gasfacility'
relevant_indices_read = [7]
relevant_indices_output = [7,8,9,10]


with open('DOEtotals-%s-%s-%s.csv' %(buildingname,location,aspectname),'wb') as facilitytotals:
    facilitytotalsWriter = csv.writer(facilitytotals)
    facilitytotalsWriter.writerow(['Month','kWh'])
    with open('%s-%s.csv' %(buildingname,location),'r') as data:
        dataReader = csv.reader(data)
        header = next(dataReader)
        row = next(dataReader)
        while True:
            if row == None:
                break;
            date = row[0].split()[0]
            month = date.split('/')[0]
            facilitySum = 0
            while row[0].split()[0].split('/')[0]== month:
                for i in relevant_indices_read:
                    facilitySum += float(row[i])
                row = next(dataReader,None)
                if row == None:
                    break;
            facilitytotalsWriter.writerow([month,facilitySum])

with open('factors-%s-%s-%s.csv' %(buildingname,location,aspectname),'wb') as factors:
    factorsWriter = csv.writer(factors)
    factorsWriter.writerow(['Month','Scaling Factor'])
    with open('realtotals-%s-%s-%s.csv' %(buildingname,location,aspectname),'r') as numerators:
        numeratorsReader = csv.reader(numerators)
        header1 = next(numeratorsReader)
        row1 = next(numeratorsReader)
        with open('DOEtotals-%s-%s-%s.csv' %(buildingname,location,aspectname),'r') as denominators:
            denominatorsReader = csv.reader(denominators)
            header2 = next(denominatorsReader)
            row2 = next(denominatorsReader)
            while True:
                month = row2[0]
                scalingfactor = float(row1[1])/float(row2[1])
                factorsWriter.writerow([month,scalingfactor])
                row1 = next(numeratorsReader,None)
                row2 = next(denominatorsReader,None)
                if row1 == None and row2 == None:
                    break;
                
with open('boosted%s-%s.csv' %(buildingname,location),'wb') as boosted:
    boostedWriter = csv.writer(boosted)
    with open('factors-%s-%s-%s.csv' %(buildingname,location,aspectname),'r') as factors:
        factorsReader = csv.reader(factors)
        header = next(factorsReader)
        facrow = next(factorsReader)
        with open('%s-%s.csv' %(buildingname,location),'r') as data:
            dataReader = csv.reader(data)
            row = next(dataReader)
            
            outputlist_header = []
            for i in relevant_indices_output:
                outputlist_header.append(row[i])
            
            
            boostedWriter.writerow(['Month']+outputlist_header)
            row = next(dataReader)

            while True:
                scaling = float(facrow[1])
                while int(facrow[0]) == int(row[0].split()[0].split('/')[0]):
                    outputlist = []
                    for i in relevant_indices_output:
                        outputlist.append(row[i])
                    boostedWriter.writerow([row[0]] + map(lambda x: scaling*x,map(float,outputlist)))
                    row = next(dataReader,None)
                    if row == None:
                        break;
                if row ==None:
                    break;
                facrow = next(factorsReader)
                if facrow == None:
                    break;
                    
                    
            
             
                
                
            