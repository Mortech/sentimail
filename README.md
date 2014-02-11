sentimail
=========

Visualization tool for sentiments in email



 # ian's code
    if fileName in emailList:
        tempEmail = emailList[fileName][1]
        if time in tempEmail.dates:
            tempEmail.dates[time][1] += 1
        else:
            tempEmail.dates.append([time,1])
    else:
        tempEmail = emailAddress(fileName)
        tempEmail.dates.append([time,1])
        emailList.append([fileName, tempEmail])