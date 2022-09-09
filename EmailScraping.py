#! python3
import re, urllib.request, time
from usp.tree import sitemap_tree_for_homepage

emailRegex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+') # regex for validating an email format
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
    emailFile = open("emails.txt", 'a')
    extractedEmail = emailRegex.findall(urlText)
    seen = set(allemails)
    for email in extractedEmail:
        if email not in seen:  # faster than `word not in output`
            seen.add(email)
            emailFile.write(email + "\n")  # appending Emails to a filerea
            allemails.append(email[0])
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
        print(urlText)
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

# Find and Parse Sitemaps to Create List of all website's pages
from usp.tree import sitemap_tree_for_homepage


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
    # Iterate Opened file for getting single url
    for urlLink in listOfUrls:
        urlLink = urlLink.strip('\'"')
        i = i + 1
        emailsLeechFunc(urlLink, i)
    print("Elapsed Time: %s" % (time.time() - start))

def runSearch(url):
    list = getPagesFromSitemap(url)
    finishedlist = getListUniquePages(list)
    finishedlist.append(url)
    runEmailSearch(finishedlist)



runSearch("https://www.example.com")
