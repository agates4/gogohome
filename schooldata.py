import csv
import random
f = open('schools.csv', 'rb')
reader = csv.reader(f)
        #f.close()

class SchoolData():
    def __init__(self):
        print "creating SchoolData obj"

    def get_data_from_csv(self, priority): #pass in a priority (1-3) based on how much they value school
        zip_codes=[] 
        if priority==1:
            for items in reader:
                try:
                    if float(items[16]) > 65:
                        print items[16]
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
        data = random.choice(data)
        data = data[-10:]
        data = data[:5]
        return data 

#print SchoolData().get_zip(2)


