import json
import tkinter
import re

class Count:
    def __init__(self):
        self.current=1
counter = Count()

def importInfo():
    with open("allData.json", encoding="utf-8") as f:
        return json.loads(f.read())

def getInfo(kanji=None):#main search fxn
    if kanji==None:
        kanji = srchEntry.get()
    try:
        counter.current = data[kanji]['count']
        kanjiLabel.configure(text=kanji, font=('Helvetica bold',40))
        formattedEty = cleanEty(data[kanji]['etymology'])
        etyLabel.delete("1.0", "end")
        etyLabel.insert('end', chars=kanji + f"  ({counter.current})  " + data[kanji]['meanings'] + "\n\n")
        etyLabel.insert('end', chars=formattedEty + "\n\n")
        etyLabel.insert('end', chars=data[kanji]['mnemonic'] + "\n\n")
        etyLabel.insert('end', chars=str(data[kanji]['readings']) + "\n\n")
        test = xRef(data[kanji]['etymology'], data[kanji]['count'])
        etyLabel.insert('end', chars="References: " + test)
    except:
        print("No info on that...")

def cleanEty(rawEty):#clean up etymology text for display
    print(rawEty)
    tempStr=""
    count=0
    for char in rawEty:
        tempStr+=char
        count+=1
        if count>=70 and char in [' ', '/']:
            tempStr+="\n"
            count=0
    tempStr+="\n"
    return tempStr

def turnPage(turnDir):
    match turnDir:
        case 'r':#move r
            if (counter.current+1>len(dataTrack)):
                counter.current=1
            else:
                counter.current+=1
        case 'l':#move l
            if (counter.current-1==0):
                counter.current=len(dataTrack)
            else:
                counter.current-=1
    getInfo(dataTrack[counter.current])

def xRef(ety, selfNum):#find number of references in etymology, find corresponding kanji, display at bottom
    nums = re.sub("\D"," ",ety).split()#list of numbers as strings
    refList = []
    for num in nums:
        if int(num)!=selfNum:
            refList.append(num)
    trimRefList = []
    for ref in refList:
        if ref not in trimRefList:
            trimRefList.append(ref)
    refStr = ""
    for ref in trimRefList:
        refStr+=dataTrack[int(ref)] + ", "
    return refStr[:len(refStr)-2]#gets rid of last ", "

data = importInfo()

dataTrack = {}
count=1
for entry in data:
    data[entry]['count']=count
    dataTrack[count]=entry
    count+=1
    
root = tkinter.Tk()

root.title("Kanji Helper")
root.configure(bg="yellow")

kanjiLabel = tkinter.Label(master=root, justify = 'center', text="")
kanjiLabel.grid(row=0, column=1)
kanjiLabel.configure(bg="#ffa1ce")

etyLabel = tkinter.Text(master=root)
etyLabel.grid(row=2, column=1, pady=1)
etyLabel.configure(bg="#ffa1ce")

srchEntry =  tkinter.Entry(master=root)
srchEntry.grid(row=5, column=1)
srchEntry.configure(bg="#ffa1ce")

srchButton = tkinter.Button(master=root, command=getInfo, text="Search")
srchButton.grid(row=6, column=1)
srchButton.configure(bg="#ffa1ce")

lftButton = tkinter.Button(master=root, text="<", command=lambda:[turnPage('l')])
lftButton.grid(row=5, column=0)
lftButton.configure(bg="#ffa1ce")

rtButton = tkinter.Button(master=root, text=">", command=lambda:[turnPage('r')])
rtButton.grid(row=5, column=2)
rtButton.configure(bg="#ffa1ce")

root.after(1000, getInfo('一'))#start off at first kanji, 

root.mainloop()
