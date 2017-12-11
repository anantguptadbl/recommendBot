from selenium import webdriver
import time
import urllib2
from bs4 import BeautifulSoup
import bs4
import re
import json
import nltk

# CONFIG
# AWS
path_to_phatomJS='/home/ubuntu/recommendBot/flaskapp/phantomjs'
# LOCAL
path_to_phatomJS='/home/anantgupta/Documents/Web/searchResults/phantomjs'

def extractLinks(pageContents):
    soup = BeautifulSoup(pageContents, "html.parser")
    linkElements = soup.find_all("a", attrs={"class":"result__url"})
    linksData=[]
    for linkElement in linkElements[0:2]:
        curStr=linkElement['href']
        validLink=curStr[curStr.find('uddg=') + 5:]
        validLink=validLink.replace('%3A',':').replace('%2F','/').replace('%2D','-')
        print("the validlink is {}".format(validLink))
        browser = webdriver.PhantomJS(executable_path = path_to_phatomJS)
        browser.get(validLink)
        pageContents=browser.page_source
        browser.close()
        print("Got data for {}".format(validLink))
        linksData.append(pageContents)
    return(linksData)


def getElements(childrenList,leafElements):
    curChildrenList=[]
    for x in childrenList:
        if(type(x)==bs4.element.Tag):
            if(len(list(x.children))>1):
                curChildrenList=curChildrenList + list(x.children)
            else:
                leafElements.append(x.text)
    return(curChildrenList)

# Function to 
def getLeafData(soupElement):
    leafElements=[]
    childrenList=list(soupElement.children)
    for x in range(100):
        childrenList=getElements(childrenList,leafElements)
        if(len(childrenList)==0):
            return(CleanLeafData(leafElements))

def CleanLeafData(leafDataList):
    return([re.sub('r[^a-zA-Z0-9_]+',' ',x.replace('\n',' ')) for x in leafDataList if len(x) > 200 and '{' not in x and '>' not in x])

def getLinksForSearchString(searchString):
    searchString=searchString.replace(' ','+')
    searchString=re.sub('r[^a-zA-Z0-9\+]+',' ',searchString)
    webPageLink='https://duckduckgo.com/html/?q=best+places+to+visit+bangalore'
    browser = webdriver.PhantomJS(executable_path = path_to_phatomJS)
    browser.get(webPageLink)
    pageContents=browser.page_source
    browser.close()
    return(extractLinks(pageContents))

def getDataFromLinks(linksData):
    # Change this to DICT later
    leafData=[]
    for curLink in linksData:
        soup=BeautifulSoup(curLink, "html.parser")
        leafData.append(getLeafData(soup))
    return(leafData)

def getNounList(text):
    # Additional check
    text = re.sub('[^0-9a-zA-Z]+', ' ', text)
    wordList=[]
    print("The text is {}".format(text))
    for word in text.split(' '):
	if(len(word) > 0):
            print("the curWord is {}".format(word))
	    if((nltk.pos_tag(word.split())[0][1] in ['NN','NNP','NNS']) & (len(word)<20) & (word[0].istitle()==True)):
                wordList.append(word)
	        print(word)
    return(wordList)

def getImpNouns(fullData):
	import nltk
	allNouns=[]
	for x in fullData:
	    nounList=[]
	    for textVal in x:
		nounList=nounList + getNounList(textVal)
		print("The nounList is {}".format(nounList))
	    nounList=list(set(nounList))
	    allNouns=allNouns + nounList
	return(json.dumps(list(set(allNouns))))	
	
if __name__=="__main__":
    fullData=getDataFromLinks(getLinksForSearchString('things+to+do+in+bangalore'))
    print(fullData[0])
