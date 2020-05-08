# Final Project Python for Programming for IT class
# Author: Wendy Silvestre
# Date: 05/04/2020

from patients import *
from Measures import *

# TkinterLibrary for GUI
from tkinter import *
from tkinter import messagebox


#Instace for class patients and vital signs
patientslist=ListofPatients()
patient=patientslist.patients[0]

ListofMeasures=AllMeasures()

def newvitalssign():
    #clean data entries
    nameSt.set(patient.name)
    dateSt.set('')
    bphint.set(0)
    bplint.set(0)
    tempint.set(0)
    pulseint.set(0)
    respint.set(0)
    gluint.set(0)

def savevitalsigns():
    #save vital signs which are on the screen to the file
    newvitals=Measures(nameSt.get(),dateSt.get(),bphint.get(),bplint.get(),tempint.get(),pulseint.get(),respint.get(),gluint.get())
    ListofMeasures.addmeasure(newvitals)
    messagebox.showinfo("Vital Signs Log","Vital Signs have been saved")
    newvitalssign()

def createCSV():
    #create CSV file for share with other applications
    ListofMeasures.createCSV(nameSt.get())
    messagebox.showinfo("Vital Signs Log","CSV File has been created")

def createPDF():
    #create a PDF file which we can print
    ListofMeasures.createPDF(patient)
    messagebox.showinfo("Vital Signs Log","PDF Report File has been created")

def sendmail():
    #sending an email to the patient's physician with a CSV file
    ListofMeasures.sendemail(patient)
    messagebox.showinfo("Vital Signs Log","Email was sended to " + patient.phname + " " + patient. phemail)

def on_focus_out(event):
    # A feedback for patient when the values are enter to the application
    if event.widget==bphentry:
        bplint.set(0)

    if event.widget==bplentry and bplint.get()!=0:
        if bphint.get()!=0:
            if bphint.get()>=120 and bphint.get()<=129 and bplint.get()<80:
                messagebox.showwarning("Warning","Your blood pressure level is high. You should talk your doctor")
            elif bphint.get()>=130 and bplint.get()>=80:
                messagebox.showwarning("Warning","Your blood pressure level is high. You should talk your doctor")

    if event.widget==pulse and pulseint.get()!=0:
        if pulseint.get()>190:
            messagebox.showwarning("Warning","Your heart rate is high. You should talk your doctor")
        if pulseint.get()<60:
            messagebox.showwarning("Warning","Your heart rate is low. You should talk your doctor")

    if event.widget==resp and respint.get()!=0:
        if respint.get()>50:
            messagebox.showwarning("Warning","Your respiratory rate is high. You should talk your doctor")
        if respint.get()<12:
            messagebox.showwarning("Warning","Your respiratory rate is low. You should talk your doctor")

    if event.widget==glu and gluint.get()!=0:
        if gluint.get()>110:
            messagebox.showwarning("Warning","Your glucose level is high. You should talk your doctor")
        if gluint.get()<60:
            messagebox.showwarning("Warning","Your glucose level is low. You should talk your doctor")

# Main Window

root=Tk()
root.title("Vital Signs Log")

# Menu options
appMenu=Menu()
root.config(menu=appMenu, width=300, heigh=300)

VitalsOptions=Menu(appMenu, tearoff=0)
VitalsOptions.add_command(label="New Vital Signs", command= newvitalssign)
appMenu.add_cascade(label="Vital Signs",menu=VitalsOptions)

# This version do not have available the function for create new patients
PatientsOptions=Menu(appMenu, tearoff=0)
PatientsOptions.add_command(label="New Patient")
appMenu.add_cascade(label="Patients",menu=PatientsOptions)

# Frame which contains every entry box
myFrame=Frame()
myFrame.pack(fill="both", expand=TRUE)

# Entry boxes
nameSt=StringVar()
nameentry=Entry(myFrame, textvariable=nameSt)
nameentry.grid(row=0, column=1, padx=10, pady=10)
namelabel=Label(myFrame, text="Patient's name")
namelabel.grid(row=0, column=0, padx=10, pady=10)

dateSt=StringVar()
dateentry=Entry(myFrame, textvariable=dateSt)
dateentry.grid(row=1, column=1, padx=10, pady=10)
datelabel=Label(myFrame, text="Date")
datelabel.grid(row=1, column=0, sticky="e", padx=10, pady=10)

bphint=IntVar()
bphentry=Entry(myFrame, textvariable=bphint)
bphentry.grid(row=2, column=1, padx=10, pady=10)
bphlabel=Label(myFrame, text="B.P. High")
bphlabel.grid(row=2, column=0, sticky="e", padx=10, pady=10)

bplint=IntVar()
bplentry=Entry(myFrame, textvariable=bplint)
bplentry.grid(row=3, column=1, padx=10, pady=10)
bpllabel=Label(myFrame, text="B.P. Low")
bpllabel.grid(row=3, column=0, sticky="e", padx=10, pady=10)

tempint=IntVar()
temp=Entry(myFrame, textvariable=tempint)
temp.grid(row=4, column=1, padx=10, pady=10)
templabel=Label(myFrame, text="Temp.")
templabel.grid(row=4, column=0, sticky="e", padx=10, pady=10)

pulseint=IntVar()
pulse=Entry(myFrame, textvariable=pulseint)
pulse.grid(row=5, column=1, padx=10, pady=10)
pulselabel=Label(myFrame, text="Pulse")
pulselabel.grid(row=5, column=0, sticky="e", padx=10, pady=10)

respint=IntVar()
resp=Entry(myFrame, textvariable=respint)
resp.grid(row=6, column=1, padx=10, pady=10)
resplabel=Label(myFrame, text="Resp.")
resplabel.grid(row=6, column=0, sticky="e", padx=10, pady=10)

gluint=IntVar()
glu=Entry(myFrame, textvariable=gluint)
glu.grid(row=7, column=1, padx=10, pady=10)
glulabel=Label(myFrame, text="Glucose")
glulabel.grid(row=7, column=0, sticky="e", padx=10, pady=10)

# Frame which contains buttons
myFrame2=Frame()
myFrame2.pack(fill="both", expand=TRUE)

# Buttons
savebuttom=Button(myFrame2, text="Save", command=savevitalsigns)
savebuttom.grid(row=1, column=0, sticky="e", padx=10, pady=10)

createCSVbuttom=Button(myFrame2, text="New CSV File", command=createCSV)
createCSVbuttom.grid(row=1, column=1, padx=10, pady=10)

createPDFbuttom=Button(myFrame2, text="New PDF File", command=createPDF)
createPDFbuttom.grid(row=1, column=2, padx=10, pady=10)

sendemailbuttom=Button(myFrame2, text="Send Email", command=sendmail)
sendemailbuttom.grid(row=1, column=3, padx=10, pady=10)



# Start Application

newvitalssign() #Init Application with a clean screen
root.bind("<FocusOut>", on_focus_out) # linking on_focus_out event to the main window application

# Start GUI
root.mainloop()
