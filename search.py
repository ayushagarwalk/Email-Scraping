from googlesearch import search
from EmailScraping import runEmailSearch

list = search('strange', num_results=1000)
runEmailSearch(list)
