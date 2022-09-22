#! python3
import re, urllib.request, time
from bs4 import BeautifulSoup
from usp.tree import sitemap_tree_for_homepage

emailRegex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+', re.VERBOSE) # regex for validating an email format
"""emailRegex = re.compile(r'''
#example :
#something-.+_@somedomain.com
(
([a-zA-Z0-9_.+]+
@
[a-zA-Z0-9_.+]+
(\.[A-Z|a-z]{2,})+)
)
''', re.VERBOSE)"""
allemails = []


# Extacting Emails
def extractEmailsFromUrlText(urlText):
    soup = BeautifulSoup(urlText, 'html.parser')
    # kill all script and style elements
    for script in soup(["script", "style"]):
        script.extract()  # rip it out
    # get text
    text = soup.get_text()
    # break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
    # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # drop blank lines
    text = '\n'.join(chunk for chunk in chunks if chunk)
    text = text.replace('\n', ' ')  # creates a single block of text
    words = text.split()  # splits the entire text into seperate words
    isValid(words)


def isValid(wordlist):
    emailFile = open("emails.txt", 'a')
    regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+') # regex for validating an email format
    for email in wordlist:
        seen = set(allemails)
        if email not in seen and re.fullmatch(regex, email): # faster than `word not in output`
            allemails.append(email)
            seen.add(email)
            emailFile.write(email + "\n")  # appending Emails to a fileread
    lenh = len(allemails)
    print("\tNumber of Emails : %s\n" % lenh)
    emailFile.close()

# HtmlPage Read Func
def htmlPageRead(url, i):
    try:
        start = time.time()
        headers = {'User-Agent': 'Mozilla/5.0'}
        request = urllib.request.Request(url, None, headers)
        response = urllib.request.urlopen(request)
        urlHtmlPageRead = response.read()
        urlText = urlHtmlPageRead.decode()
        print("%s.%s\tFetched in : %s" % (i, url, (time.time() - start)))
        extractEmailsFromUrlText(urlText)
    except:
        pass


# EmailsLeechFunction
def emailsLeechFunc(url, i):
    try:
        htmlPageRead(url, i)
    except urllib.error.HTTPError as err:
        if err.code == 404:
            try:
                url = 'http://webcache.googleusercontent.com/search?q=cache:' + url
                htmlPageRead(url, i)
            except:
                pass
        else:
            pass
    except:
        pass


# Find and Parse Sitemaps to Create List of all website's pages
def getPagesFromSitemap(fullDomain):
    listPagesRaw = []

    tree = sitemap_tree_for_homepage(fullDomain)
    for page in tree.all_pages():
        listPagesRaw.append(page.url)

    return listPagesRaw


# Go through List Pages Raw output a list of unique pages links
def getListUniquePages(listPagesRaw):
    listPages = []
    for page in listPagesRaw:
        if page in listPages:
            pass
        else:
            listPages.append(page)
    return listPages

def runEmailSearch(listOfUrls):
    start = time.time()
    i = 0
    # Iterate list for getting single url
    for urlLink in listOfUrls:
        urlLink = urlLink.strip('\'"')
        i = i + 1
        emailsLeechFunc(urlLink, i)
    print("Elapsed Time: %s" % (time.time() - start))
    time.sleep(5)

def runSearch(url):
    basiclist = getPagesFromSitemap(url)
    finishedlist = getListUniquePages(basiclist)
    finishedlist.append(url) # add homepage to list to be parsed
    runEmailSearch(finishedlist)




#runSearch("") # enter the website you want to search here - ensutre full url "https://www.example.com"
