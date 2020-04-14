import PySimpleGUI as sg
import time
import subprocess
import psutil
import os
class GuiWindow():
    layout = [[sg.Text('Enter Amazon URL'), sg.InputText(),sg.Button('Submit', key='urlSubmit')],
             [sg.Text('Enter your Email: '), sg.InputText(),sg.Button('Add',key='emailAdd')],
             [sg.Text(size=(25,1),key='infoText')],
             [sg.Button('Start Scraping',key='start'),sg.Button('Stop',key='stop')],
             [sg.Exit()]
                ]

    window = sg.Window('Amazon Price Detector', layout)
    id = 0
    while True:
        event, values = window.read(timeout = 10)
        if event is None or event == 'Exit':
            break
        if event == 'emailAdd':
            email = open("Emails.txt",'a')
            email.write(values[1]+"\n")
            email.close()

        if event == 'urlSubmit':
            amazonLink = open("Links.txt",'a')
            amazonLink.write(values[0]+"\n")
            amazonLink.close()
        if event == 'start':
            p = subprocess.Popen("WebscraperV1.exe",creationflags=subprocess.CREATE_NEW_CONSOLE)
            id = p.pid
        if event == 'stop':
            parent_pid = id   # my example
            parent = psutil.Process(parent_pid)
            for child in parent.children(recursive=True):  # or parent.children() for recursive=False
                child.kill()
            parent.kill()




    window.close()
