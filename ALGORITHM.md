## Algorithm returning a list which contains all the days between the day of the function call and an asked limit date:
These are Python functions which can be linked together to get a full list or separately to get different informations according to different parameters.
For a fully functional program you need to work with the library `datetime`
```
# Function checking whether it is a leap year or not:
def bissextile():
    year = int(datetime.today().strftime('%Y'))
    if year%4==0:
        if year%100==0 and year%400==0 or year%100!=0:
            return 1
    return 0
```
```
# Function returning the number of days in a month according to the given month in parameter:
def lenMonth(m):
    dayArray = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    if  m-1==1:
        return dayArray[m-1] + bissextile()
    else:
        return dayArray[m-1]
```
```
# Function checking if the program went through all the days between the day of the request and the limit date:
def checkYear(val,month,day):
    ar = val[len(val)-1].split("-")
    if int(ar[1])==month and int(ar[2])==day:
        ret = val
        return(ret)
    else:
        return checkMonth(val)
```
```
# function checking if the program went through all the days of one month :
def checkMonth(val):
    ar = val[len(val)-1].split("-")
    if int(ar[2]) == lenMonth(int(ar[1])):
        return newDay(val,True)
    else:
        return newDay(val)
```
```
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
 ```
