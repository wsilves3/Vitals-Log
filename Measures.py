# Picle library for binary file
import pickle
# Libraries for send email
import smtplib, config
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
#Library ReportLab for create PDF File
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle
from reportlab.lib import colors

class Measures:
    def __init__(self, name, date, bloodph, bloodpl, temp, pulse, resp, glu):
        self.name=name #name of patient
        self.date=date # date of measure
        self.bloodph=bloodph # blood pressure high
        self.bloodpl=bloodpl # blood pressure low
        self.temp=temp # body temperature
        self.pulse=pulse # pulse
        self.resp=resp # respiratory rate
        self.glu=glu #glucose

    def __str__(self):
        return "{}{}{}{}{}{}{}{}".format(self.name, self.date, self.bloodph, self.bloodpl, self.temp, self.pulse, self.resp, self.glu)

class AllMeasures:
    # All vital signs are in measures list
    measures=[]
    def __init__(self):
        fileofmeasures=open("Measures.txt","ab+")
        fileofmeasures.seek(0)
        try:
            # loading vital signs from binary file to measures list
            self.measures=pickle.load(fileofmeasures)
        except:
            print("The file is empty")
        finally:
            fileofmeasures.close()
            del(fileofmeasures)

    def addmeasure(self,measure):
        # add new group of vital signs to measures list
        self.measures.append(measure)
        self.saveMeasure()

    def saveMeasure(self):
        fileofmeasures=open("Measures.txt","wb")
        # saving measures list to binary file
        pickle.dump(self.measures,fileofmeasures)
        fileofmeasures.close()
        del(fileofmeasures)

    def showmeasures(self):
        # print of data for debbuging purpose
        for m in self.measures:
            print(m.date,m.bloodph,m.bloodpl,m.temp,m.pulse,m.resp,m.glu)

    def createCSV(self, name):
        # Creating CSV File
        csvfile=open(name+".csv","w")
        csvfile.write("Date,BP High,BP Low,BT,HR,RR,GLU\n")
        for m in self.measures:
            if m.name==name:
                csvfile.write(m.date+','+str(m.bloodph)+','+str(m.bloodpl)+','+str(m.temp)+','+str(m.pulse)+','+str(m.resp)+','+str(m.glu)+'\n')
        csvfile.close()
        del(csvfile)

    def createPDF(self,patient):
        # Creating PDF File
        title = patient.name+"'s Vital Signs"
        # List of List of measures list for use with reportlab library
        # measures is a list but of measures object
        dataforPDF=[[title],['Date','B.P. HIGH','B.P. LOW','B.TEMP.','HEART RATE','R.RESP.','GLUCOSE']]
        for m in self.measures:
            if m.name==patient.name:
                dataforPDF.append([m.date,m.bloodph,m.bloodpl,m.temp,m.pulse,m.resp,m.glu])
        #dataforPDF created

        filename=patient.name+".pdf"
        pdf=SimpleDocTemplate(filename,pagesize=letter, title=title)
        table=Table(dataforPDF)
        # Formatting the PDF File
        style=TableStyle([('BACKGROUND',(0,0),(6,0),colors.green),
                          ('TEXTCOLOR',(0,0),(-1,0),colors.whitesmoke),
                          ('SPAN',(0,0),(6,0)),
                          ('FONTSIZE',(0,0),(-1,0),12),
                          ('ALIGN',(0,1),(-1,0),'CENTER'),
                          ('ALIGN',(1,2),(-1,-1),'RIGHT'),
                          ('BOX',(0,0),(-1,-1),1,colors.black),
                          ('GRID',(0,1),(-1,-1),1,colors.black)
                          ])
        table.setStyle(style)
        elems=[]
        elems.append(table)
        pdf.build(elems) # Building PDF File


    def sendemail(self,patient):
        # Sending email with CSV file to physician's patient
        self.createCSV(patient.name) # create CSV File
        csvfile=patient.name+'.csv'
        #Using a google account to send email
        gmail=smtplib.SMTP("smtp.gmail.com", 587)
        gmail.starttls()
        #config file has user and password of a google account with option to send email
        gmail.login(config.account, config.password)

        # email message
        header=MIMEMultipart()
        header['From']=config.account
        header['To']=patient.phemail
        header['Subject']=patient.name+"'s Vital Signs"
        message='This email has vital signs of '+patient.name
        header.attach(MIMEText(message, 'html'))
        # attach CSV File
        attach=MIMEBase('application', 'octet-stream')
        attach.set_payload(open(csvfile, 'rb').read())
        encoders.encode_base64(attach)
        attach.add_header('Content-Disposition', "attachment; filename= %s" % csvfile)
        header.attach(attach)
        # Sending email
        gmail.sendmail(header['From'],header['To'],header.as_string())
        gmail.quit()



