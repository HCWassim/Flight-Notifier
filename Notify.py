# Library:
import smtplib
import ast 
from email.message import EmailMessage
import http.client, urllib.request, urllib.parse, urllib.error
from datetime import datetime
# Function to send an Email:
def emailAlert(subject,body,to):
    # Attribution of the values:
    msg = EmailMessage()
    msg.set_content(body)
    msg['subject'] = subject
    msg['to'] = to
    # Account sending the alert:
    user = "examplemail@gmail.com"
    msg['from'] = user
    password = "XXXXXXXXXXXX"
    # Server:
    server = smtplib.SMTP("smtp.gmail.com",587)
    server.starttls()
    server.login(user,password)
    server.send_message(msg)
    server.quit()
# FORMAT: YYYY-MM-DD - Functions checking every days between the date of the request and the limit date asked by the users
# Function checking whether it is a leap year or not:
def bissextile():
    year = int(datetime.today().strftime('%Y'))
    if year%4==0:
        if year%100==0 and year%400==0 or year%100!=0:
            return 1
    return 0
# Function returning the number of days in a month according to the given month in parameter:
def lenMonth(m):
    dayArray = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    if  m-1==1:
        return dayArray[m-1] + bissextile()
    else:
        return dayArray[m-1]
# Function checking if the program went through all the days between the day of the request and the limit date:
def checkYear(val,month,day):
    ar = val[len(val)-1].split("-")
    if int(ar[1])==month and int(ar[2])==day:
        ret = val
        return(ret)
    else:
        return checkMonth(val)
# function checking if the program went through all the days of one month :
def checkMonth(val):
    ar = val[len(val)-1].split("-")
    if int(ar[2]) == lenMonth(int(ar[1])):
        return newDay(val,True)
    else:
        return newDay(val)
# function adding a new day to the final day:
def newDay(val,bool=False):
    ar = val[len(val)-1].split("-")
    if bool:
        d = ar[0]+"-"+str(int(ar[1])+1).zfill(2)+"-01"
        val.append(d)
        return checkYear(val)
    else:
        d = ar[0]+"-"+ar[1]+"-"+str(int(ar[2])+1).zfill(2)
        val.append(d)
        return checkYear(val)
# Transavia's API - Function searching all the available flight according to the departure IATA and the arrival IATA and the limit date
def searchFlight(IATA1,IATA2,month,d):
    # KEY & API's parameter:
    headers = {'apikey': 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX',} # Request headers
    # Daily research:
    days = checkYear([datetime.today().strftime('%Y-%m-%d')],month,d)
    for day in days:
        day = day.split("-")
        day = "".join(day)
        params = urllib.parse.urlencode({'origin': IATA1,'destination': IATA2,'originDepartureDate': day,}) # Parameters
        try:
            conn = http.client.HTTPSConnection('api.transavia.com')
            conn.request("GET", "/v1/flightoffers/?%s" % params, "{body}", headers)
            response = conn.getresponse()
            data = response.read()
            if len(data)>0:
                conn.close()
                return data
        except Exception as e:
            return("[Errno {0}] {1}".format(e.errno, e.strerror))
# Flight Research example:
ar = searchFlight("ORY","ALG")
if ar:
    ar = ar.decode("utf-8")
    ar = ast.literal_eval(ar)
    allInfo = []
    allInfo.append([str(ar["resultSet"]["count"])])
    for i in ar["flightOffer"]:
        allInfo.append([i["outboundFlight"]["id"],i["outboundFlight"]["departureDateTime"],str(i["pricingInfoSum"]["totalPriceOnePassenger"]),i["deeplink"]["href"]])
    # Writing of the final message:
    d = allInfo[1][1].split("T")
    e = d[0].split("-")
    e = e[2]+"/"+e[1]+"/"+e[0]
    content = allInfo[0][0]+" offres pour le "+e+": \n \n"
    for info in allInfo:
        if len(info)>2:
            content = content + "Identifiant: " + info[0] + " \n"
            time = info[1].split("T")
            content = content + "Départ le "+time[0]+" à "+time[1]+" \n"
            content = content + "A partir de "+info[2]+"€ \n"
            content = content + "Réservation: "+ info[3] + " \n"+" \n"
    # Sending the email to different emails adresses:
    if __name__ == '__main__':
        emailAlert("Flight Notifier",content,"example1@gmail.com")
        emailAlert("Flight Notifier",content,"example2@orange.fr")
