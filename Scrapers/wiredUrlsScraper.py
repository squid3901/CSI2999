import requests, time
from bs4 import BeautifulSoup


def getReviews(listPageRootUrl, pageNumber):
    currentPage = requests.get(listPageRootUrl + str(pageNumber))
    phoneList = []
    soup = BeautifulSoup(currentPage.content, "html.parser")
    x = soup.find_all("li")
    for y in x:
        try:
            lk = y.find('a', class_='clearfix pad')['href']
        except:
            pass                #easiest way to deal with "None" results

        headline = y.find('h2', string=lambda text: 'review' in text.lower())
        if headline != None:
            phoneName = headline.text.replace("Review:","").strip()
            if "and" in phoneName:
                pList = phoneName.replace(" and ", "@").split("@")
                for z in pList:
                    phoneList.append(z)
                    phoneList.append(lk)
            else:
                phoneList.append(phoneName)
                phoneList.append(lk)
    return phoneList

def getAllReviews(listPageRootUrl, pageNumber, timeSleep):
    fullPhoneList = []
    if timeSleep < 3:
        timeSleep = 5
    timeSleep = float(timeSleep)
    while requests.get(listPageRootUrl + str(pageNumber)).ok:
        pagePhoneList = getReviews(listPageRootUrl, pageNumber)
        for x in pagePhoneList:
            fullPhoneList.append(x)
        print(pagePhoneList)
        fancySleep(timeSleep)
        pageNumber += 1
    print("Reached end of reviews.")
    return fullPhoneList

def printCsv(fullPhoneList):
    wOutput = open("WiredURLs.csv", "w+", encoding="utf8")
    endIndex = len(fullPhoneList)
    for n in range(int(endIndex/2)):
        phoneName = str(fullPhoneList[n*2])
        phoneUrl = str(fullPhoneList[(n*2)+1])
        wOutput.write(phoneName + "," + phoneUrl + "\n")


def fancySleep(timeSleep):
    print("sleeping " + str(int(timeSleep)) + " seconds", end="", flush=True)  # https://stackoverflow.com/questions/5598181/multiple-prints-on-the-same-line-in-python
    time.sleep(timeSleep / 4)
    print(" .", end="", flush=True)
    time.sleep(timeSleep / 4)
    print(" .", end="", flush=True)
    time.sleep(timeSleep / 4)
    print(" .")
    time.sleep(timeSleep / 4)


printCsv(getAllReviews("https://www.wired.com/category/reviews/phones/page/", 1, 10))