from googlesearch import search
from EmailScraping import runEmailSearch

list = search('*"@gmail.com"', num_results=10000000000)
runEmailSearch(list)