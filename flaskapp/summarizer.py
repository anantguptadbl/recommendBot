from selenium import webdriver
import time
import urllib2
from bs4 import BeautifulSoup
import bs4
import re
import json
import nltk
import os,site
import subprocess
from subprocess import Popen
# CONFIG
# AWS
#path_to_phatomJS='/home/ubuntu/recommendBot/flaskapp/phantomjs'
#site.addsitedir('/home/ubuntu/.local/lib/python2.7/site-packages')
#nltk.data.path.append("/home/ubuntu/nltk_data/")
# LOCAL
path_to_phatomJS='/home/anantgupta/Documents/Web/searchResults/phantomjs'

def extractLinks(pageContents):
    #p = subprocess.Popen(["echo", "hello world"], stdout=subprocess.PIPE)
    soup = BeautifulSoup(pageContents, "html.parser")
    linkElements = soup.find_all("a", attrs={"class":"result__url"})
    linksData=[]
    commonLinksData=[]
    for linkElement in linkElements:
        curStr=linkElement['href']
        validLink=curStr[curStr.find('uddg=') + 5:]
        validLink=validLink.replace('%3A',':').replace('%2F','/').replace('%2D','-')
        if('duckduckgo.com' not in validLink):
            print("the validlink is {}".format(validLink))
    	    browser = webdriver.PhantomJS(executable_path = path_to_phatomJS,service_log_path=os.path.devnull)
            #browser = webdriver.PhantomJS(executable_path = path_to_phatomJS,service_log_path='/home/ubuntu/recommendBot/flaskapp/ghostdriver.log')
            browser.get(validLink)
            pageContents=browser.page_source
            browser.close()
            browser.quit()
	    #print p.communicate()
            print("Got data for {}".format(validLink))
            linksData.append(pageContents)
    for linkElement in linkElements:
        curStr=linkElement['href']
        validLink=curStr[curStr.find('uddg=') + 5:]
        validLink=validLink.replace('%3A',':').replace('%2F','/').replace('%2D','-')
        print("the validlink is {}".format(validLink))
        if('duckduckgo.com' not in validLink):
	    if(validLink.find('.com') > 0):	
            	validLink=validLink[0:validLink.find('.com')+4]
	    elif(validLink.find('.gov') > 0):	
            	validLink=validLink[0:validLink.find('.gov')+4]
	    elif(validLink.find('.co') > 0):	
            	validLink=validLink[0:validLink.find('.co')+6]
		
    	    browser = webdriver.PhantomJS(executable_path = path_to_phatomJS,service_log_path=os.path.devnull)
            #browser = webdriver.PhantomJS(executable_path = path_to_phatomJS,service_log_path='/home/ubuntu/recommendBot/flaskapp/ghostdriver.log')
            browser.get(validLink)
            pageContents=browser.page_source
            browser.close()
            browser.quit()
	    #print p.communicate()
            print("Got data for {}".format(validLink))
            commonLinksData.append(pageContents)
    #try:
    #    p.kill()
    #except OSError:
    #    # can't kill a dead proc
    #    pass
    return([linksData,commonLinksData])
    

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
    #webPageLink='https://duckduckgo.com/html/?q=best+places+to+visit+bangalore'
    webPageLink='https://duckduckgo.com/html/?q={}'.format(searchString)
    browser = webdriver.PhantomJS(executable_path = path_to_phatomJS,service_log_path=os.path.devnull)
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
    #print("The text is {}".format(text))
    for word in text.split(' '):
	if(len(word) > 0):
            #print("the curWord is {}".format(word))
	    if((nltk.pos_tag(word.split())[0][1] in ['NN','NNP','NNS']) & (len(word)<20) & (word[0].istitle()==True)):
                wordList.append(word)
	        #print(word)
    return(wordList)

def getImpNouns(fullData):
	allNouns=[]
	for x in fullData:
	    nounList=[]
	    for textVal in x:
		nounList=nounList + getNounList(textVal)
		#print("The nounList is {}".format(nounList))
	    nounList=list(set(nounList))
	    allNouns=allNouns + nounList
	return(json.dumps(list(set(allNouns))))	

def getAllNouns(fullData):
    allNouns=[]
    for x in fullData:
        nounList=[]
        for textVal in x:
            nounList=nounList + getNounList(textVal)
        nounList=list(set(nounList))
        allNouns=allNouns + nounList
    return(list(set(allNouns)))

def getOntologyOfWordFromDBPedia(curWord):
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:14.0) Gecko/20100101 Firefox/14.0.1'}
    url='http://dbpedia.org/sparql?default-graph-uri=http%3A%2F%2Fdbpedia.org&query=PREFIX%20dbres%3A%20%3Chttp%3A%2F%2Fdbpedia.org%2Fresource%2F%3E%0D%0APREFIX%20rdf%3A%3Chttp%3A%2F%2Fwww.w3.org%2F1999%2F02%2F22-rdf-syntax-ns%23%3E%0D%0Aselect%20%3Fo%20where%20%7Bdbres%3A{}%20rdf%3Atype%20%3Fo%7D%20LIMIT%20100&format=text%2Fhtml&timeout=30000&debug=on'.format(curWord)
    #rint("the url for sparql is {}".format(url))
    req=urllib2.Request(url,headers=headers)
    response=urllib2.urlopen(req)
    pageData = response.read()
    soup=BeautifulSoup(pageData, "html.parser")
    return([x['href'].replace('http://dbpedia.org/ontology/','') for x in soup.find_all('a') if 'http://dbpedia.org/ontology' in x['href']])

def getosmDetails(searchString):
    #url1='http://nominatim.openstreetmap.org/search?q=135+pilkington+avenue,+birmingham&format=xml&polygon=1&addressdetails=1'
    url1='https://nominatim.openstreetmap.org/search.php?q={}&polygon_geojson=1&format=json'.format(searchString)
    #print("the url for geocoding is {}".format(url1))
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:14.0) Gecko/20100101 Firefox/14.0.1'}
    req=urllib2.Request(url1,headers=headers)
    response=urllib2.urlopen(req)
    pageData = response.read()
    resultJSON=json.loads(pageData)
    if(len(resultJSON)>0):
        if('lat' in resultJSON[0]):
            resultLatitude=resultJSON[0]['lat']
            resultLongitude=resultJSON[0]['lon']
            resultClass=resultJSON[0]['class']
            resultType=resultJSON[0]['type']
            return({'lat':resultLatitude,'lon':resultLongitude,'class':resultClass,'type':resultType,'textVal':searchString})
    return({'lat':'','lon':'','class':'','type':'','textVal':searchString})
	
if __name__=="__main__":
    fullData=getDataFromLinks(getLinksForSearchString('things+to+do+in+bangalore'))
    print(fullData[0])
