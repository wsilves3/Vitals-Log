import pickle
import smtplib, config
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
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
    measures=[]
    def __init__(self):
        fileofmeasures=open("Measures.txt","ab+")
        fileofmeasures.seek(0)
        try:
            self.measures=pickle.load(fileofmeasures)
        except:
            print("The file is empty")
        finally:
            fileofmeasures.close()
            del(fileofmeasures)

    def addmeasure(self,measure):
        self.measures.append(measure)
        self.saveMeasure()

    def saveMeasure(self):
        fileofmeasures=open("Measures.txt","wb")
        pickle.dump(self.measures,fileofmeasures)
        fileofmeasures.close()
        del(fileofmeasures)

    def showmeasures(self):
        for m in self.measures:
            print(m.date,m.bloodph,m.bloodpl,m.temp,m.pulse,m.resp,m.glu)

    def createCVS(self, name):
        cvsfile=open(name+".cvs","w")
        cvsfile.write("Date,BP High,BP Low,BT,HR,RR,GLU\n")
        for m in self.measures:
            if m.name==name:
                cvsfile.write(m.date+','+str(m.bloodph)+','+str(m.bloodpl)+','+str(m.temp)+','+str(m.pulse)+','+str(m.resp)+','+str(m.glu)+'\n')
        cvsfile.close()
        del(cvsfile)

    def createPDF(self,patient):
        title = patient.name+"'s Vital Signs"
        # List of List
        dataforPDF=[[title],['Date','B.P. HIGH','B.P. LOW','B.TEMP.','HEART RATE','R.RESP.','GLUCOSE']]
        for m in self.measures:
            if m.name==patient.name:
                dataforPDF.append([m.date,m.bloodph,m.bloodpl,m.temp,m.pulse,m.resp,m.glu])



        filename=patient.name+".pdf"
        pdf=SimpleDocTemplate(filename,pagesize=letter, title=title)
        table=Table(dataforPDF)
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
        pdf.build(elems)


    def sendemail(self,patient):
        self.createCVS(patient.name) # create CVS File
        cvsfile=patient.name+'.cvs'
        gmail=smtplib.SMTP("smtp.gmail.com", 587)
        gmail.starttls()
        gmail.login(config.account, config.password)

        header=MIMEMultipart()

        header['From']=config.account
        header['To']=patient.phemail
        header['Subject']=patient.name+"'s Vital Signs"
        message='This email has vital signs of '+patient.name
        header.attach(MIMEText(message, 'html'))

        attach=MIMEBase('application', 'octet-stream')
        attach.set_payload(open(cvsfile, 'rb').read())
        encoders.encode_base64(attach)
        attach.add_header('Content-Disposition', "attachment; filename= %s" % cvsfile)
        header.attach(attach)

        gmail.sendmail(header['From'],header['To'],header.as_string())
        gmail.quit()



