import os
import win32com.client as win32
import sqlite3

# connect to database
conn = sqlite3.connect('vodomjeri.db')
# curson
cursor = conn.cursor()
address = cursor.execute("SELECT Kontakt_email FROM Zgrada")

olApp = win32.Dispatch('Outlook.Application')
olNS = olApp.GetNameSpace('MAPI')


for row in address:     

    mailItem = olApp.CreateItem(0)
    mailItem.Subject = 'Naziv maila'
    mailItem.BodyFormat = 1
    mailItem.Body = "Neki tekst"
    mailItem.To = address

    mailItem.Attachments.Add(os.path.join(os.getcwd(), 'Neki_excel.xlsx'))
    mailItem.Attachments.Add(os.path.join(os.getcwd(), 'Neki_pdf.pdf'))

    mailItem.Display()
    mailItem.Save()
    mailItem.Send()
