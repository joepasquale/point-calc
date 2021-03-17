import tkinter as tk
from appJar import gui
import pandas as pd
import numpy as np
import datetime

#import csvs to serve as pseudo-db
interviewFile = pd.read_csv('dicts/interviewList.csv')
deliveryFile = pd.read_csv('dicts/deliveryList.csv')
quizFile = pd.read_csv('dicts/quizList.csv')
totalFile = pd.read_csv('dicts/totalList.csv')
brotherList = pd.read_csv('dicts/brotherList.csv')

#store names in lists for autocomplete
workers = totalFile['name'].tolist()
members = brotherList['name'].tolist()


#add interview to list
def addInterview(name, recipient, date):
    global interviewFile
    #check to see if interview has happened (check recipient and name combo, return error if occurred)
    if not interviewFile.query('name == @name & recipient == @recipient').empty:
        app.setLabel("ioutput", "According to the DB, this interview has occurred")
        return
    else:
        #otherwise add data to csv. append row to df then save df contents to csv
        interviewFile = interviewFile.append(
            {'name': name, 'recipient': recipient, 'date': date}, ignore_index=True)
        interviewFile.to_csv('dicts/interviewList.csv', index=False)
        #show successful output in gui
        query = str(name) + ", " + str(recipient) + ", " + str(date)
        app.setLabel("ioutput", "Added " + query + " to disk")
        return

#add interview to list
def addDelivery(name, recipient, date):
    global deliveryFile
    #add delivery to list, no need for redundancy check (one person can get multiple orders a day)
    deliveryFile = deliveryFile.append(
        {'name': name, 'recipient': recipient, 'date': date}, ignore_index=True)
    deliveryFile.to_csv('dicts/deliveryList.csv', index=False)
    #show successful output
    query = str(name) + ", " + str(recipient) + ", " + str(date)
    app.setLabel("doutput", "Added " + query + " to disk")
    return

#add quiz to list
def addQuiz(name, score, date):
    global quizFile
    #check to see if quiz has been input already (unlikely that someone will test twice for one date)
    if not quizFile.query('name == @name & score == @score & date == @date').empty:
        app.setLabel("qoutput", "This test has been entered")
        return
    else:
        #otherwise add data to csv. append row to df then save df contents to csv
        quizFile = quizFile.append(
            {'name': name, 'score': score, 'date': date}, ignore_index=True)
        quizFile.to_csv('dicts/quizList.csv', index=False)
        #show successful output
        query = str(name) + ", " + str(score) + ", " + str(date)
        app.setLabel("qoutput", "Added " + query + " to disk")
        return

#calculate totals based on point schema provided (not included)
def loadTotals():
    global totalFile
    '''
    iterator is to go over each row. probably would be a good idea to just change this to a map function,
    but i still am struggling with my understanding of pandas, much less map/reduce functions
    '''
    iterator = totalFile.iterrows()
    #df to mimic total file columns... could also just be the columns of totalfile if you need it to be?
    df = pd.DataFrame(columns=['name', 'total', 'itotal', 'dtotal', 'qtotal'])
    #calculate total points by each category
    for i, row in iterator:
        #calc interview points: total portion of interviews held by current selection compared to total interview. score max at 100
        curName = row['name']
        interviewNum = interviewFile.query('name == @curName')
        itotal = (len(interviewNum)/len(interviewFile)) * 100
        #calc delivery points. 6 points per delivery
        dNum = deliveryFile.query('name == @curName')
        dtotal = len(dNum) * 6
        #calc quiz points. 15 points for every quiz that is 90 or higher
        qSet = quizFile.query('score > 89')
        quizNum = qSet.query('name==@curName')
        qtotal = len(quizNum) * 15
        #sum all columns for grand total, add total for each person by row
        total = itotal + qtotal + dtotal
        df = df.append({'name': curName, 'total': total, 'itotal': itotal, 'dtotal': dtotal, 'qtotal': qtotal, },
                       ignore_index=True)
    #update total value list, output success message
    totalFile = df
    totalFile.to_csv('dicts/totalList.csv', index=False)
    app.setLabel("toutput", "Totals computed and stored at dicts/totalList.csv")
    app.addTable("table1", [[totalFile.columns.values], totalFile.values()])

#function to handle appjar/tkinter button presses
def eventHandler(button):
    if "Close" in button:
        app.hideAllSubWindows(useStopFunction=True)
    elif button == "Add Interview":
        addInterview(app.getEntry("i1"), app.getEntry(
            "i2"), app.getDatePicker("idate"))
    elif button == "Add Delivery":
        addDelivery(app.getEntry("d1"), app.getEntry(
            "d2"), app.getDatePicker("ddate"))
    elif button == "Add Quiz":
        addQuiz(app.getEntry("q1"), app.getEntry(
            "q2"), app.getDatePicker("qdate"))
    elif button == "Load Totals":
        loadTotals()
    else:
        return


#create gui
with gui("Window", "400x200") as app:
    app.setBg("lightblue")
    app.addLabel("title", "Welcome to PointCalc")

    #add buttons for main menu
    app.addNamedButton("Log Interview", "ientry", app.showSubWindow)
    app.addNamedButton("Log Delivery", "dentry", app.showSubWindow)
    app.addNamedButton("Log Quiz", "qentry", app.showSubWindow)
    app.addNamedButton("View Totals", "totalview", app.showSubWindow)
    app.addButton("Exit", app.stop)

    #subwindow for interviews
    with app.subWindow("ientry"):
        app.addLabel("iheader", "Add an Interview", row=0, colspan=2)
        app.addLabel("i1Label", "Enter Name of Interviewer:", row=1, column=0)
        app.addAutoEntry("i1", workers, row=1, column=1)
        app.addLabel(
            "i2Label", "Enter Name of Person Interviewed:", row=2, column=0)
        app.addAutoEntry("i2", members, row=2, column=1)
        app.addLabel(
            "idateLabel", "Enter Date of Interview (MM/DD/YYYY):", row=3, column=0)
        app.addDatePicker("idate", row=3, column=1)
        app.addButtons(["Add Interview", "Close Interview Entry"],
                       eventHandler, row=4, colspan=2)
        app.addEmptyLabel("ioutput", row=5, colspan=2)

    #subwindow for deliveries
    with app.subWindow("dentry"):
        app.addLabel("dheader", "Add a Delivery", row=0, colspan=2)
        app.addLabel("d1Label", "Enter Name of Courier:", row=1, column=0)
        app.addAutoEntry("d1", workers, row=1, column=1)
        app.addLabel("d2Label", "Enter Name of Recipient:", row=2, column=0)
        app.addAutoEntry("d2", members, row=2, column=1)
        app.addLabel(
            "ddateLabel", "Enter Date of Delivery (MM/DD/YYYY):", row=3, column=0)
        app.addDatePicker("ddate", row=3, column=1)
        app.addButtons(["Add Delivery", "Close Delivery Entry"],
                       eventHandler, row=4, colspan=2)
        app.addEmptyLabel("doutput", row=5, colspan=2)

    #subwindow for quizzes
    with app.subWindow("qentry"):
        app.addLabel("qheader", "Add a Quiz", row=0, colspan=2)
        app.addLabel("q1Label", "Enter Name of Participant:", row=1, column=0)
        app.addAutoEntry("q1", workers, row=1, column=1)
        app.addLabel("q2Label", "Enter Score:", row=2, column=0)
        app.addNumericEntry("q2", row=2, column=1)
        app.addLabel(
            "qdateLabel", "Enter Date of Quiz (MM/DD/YYYY):", row=3, column=0)
        app.addDatePicker("qdate", row=3, column=1)
        app.addButtons(["Add Quiz", "Close Quiz Entry"],
                       eventHandler, row=4, colspan=2)
        app.addEmptyLabel("qoutput", row=5, colspan=2)

    #subwindow to load total
    with app.subWindow("totalview"):
        app.addLabel("theader", "View Total Statistics", row=0, colspan=2)
        app.addButtons(["Load Totals", "Close Total View"],
                       eventHandler, row=1, colspan=2)
        app.addEmptyLabel("toutput", row=2, colspan=2)

app.go()
