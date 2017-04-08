    #f.close()
import csv
import random

class SchoolData():
    def __init__(self):
        print "creating SchoolData obj"

    def get_data_from_csv(self, priority): #pass in a priority (1-3) based on how much they value school

        f = open('schools.csv', 'rb')
        reader = csv.reader(f)
        zip_codes=[] 
        if priority==1:
            for items in reader:
                try:
                    if float(items[16]) > 65:
                        zip_codes.append(items[7]) 
                except:
                    pass
                    
            return zip_codes

        if priority==2:
            for items in reader:
                try:
                    if float(items[16]) < 65 and float(items[16]) > 45:
                        zip_codes.append(items[7]) 
                except:
                    print items[16]
            return zip_codes
    
        if priority==3:
            for items in reader:
                try:
                    if float(items[16]) < 45:
                        zip_codes.append(items[7]) 
                except:
                    pass
            return zip_codes

    def get_zip(self, priority):
        data = self.get_data_from_csv(priority)
        print data
        data = random.choice(data)

        try:
            data = data[-10:]
            data = data[:5]
        except:
            self.get_zips(priority)
        return data 

#jprint SchoolData().get_zip(1)

