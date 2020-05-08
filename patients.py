# Picle library for binary file
import pickle
class Patients:
    def __init__(self, name, email, gender, dob, phname, phemail):
        self.name=name #name of patient
        self.email=email #email of patient
        self.gender=gender #gender of patient
        self.dob=dob #date of birth
        self.phname=phname # physician's name
        self.phemail=phemail # physician's email

    def __str__(self):
        return "{}{}{}{}{}".format(self.name, self.gender, self.dob, self.phname, self.email)

class ListofPatients:
    # All patients are in patients list
    patients=[]
    def __init__(self):
        patientsfile=open("Patients.txt","ab+")
        patientsfile.seek(0)
        try:
            self.patients=pickle.load(patientsfile)
        except:
            print("The file is empty")
        finally:
            patientsfile.close()
            del(patientsfile)

    def addpatient(self,p):
        # adding a patient en the list
        self.patients.append(p)
        self.savePatient()

    def savePatient(self):
        # saving patients list to a binary file
        patientsfile=open("Patients.txt","wb")
        pickle.dump(self.patients,patientsfile)
        patientsfile.close()
        del(patientsfile)

    def showpatients(self):
        # print patients for debugging purpose
        for m in self.patients:
            print(m.name,m.gender,m.dob,m.phname,m.phemail)
