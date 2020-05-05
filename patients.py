import pickle
class Patients:
    def __init__(self, name, email, gender, dob, phname, phemail):
        self.name=name
        self.email=email
        self.gender=gender
        self.dob=dob #date of birth
        self.phname=phname # physician name
        self.phemail=phemail # physician email

    def __str__(self):
        return "{}{}{}{}{}".format(self.name, self.gender, self.dob, self.phname, self.email)

class ListofPatients:
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
        self.patients.append(p)
        self.savePatient()

    def savePatient(self):
        patientsfile=open("Patients.txt","wb")
        pickle.dump(self.patients,patientsfile)
        patientsfile.close()
        del(patientsfile)

    def showpatients(self):
        for m in self.patients:
            print(m.name,m.gender,m.dob,m.phname,m.phemail)
