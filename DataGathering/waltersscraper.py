from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import re

def beautify(summaryLine):
    '''Makes the text readable by removing leading whitespaces, unnecessary apostrophes, quotation marks, dashes, brackets, special characters like \n and \r and so.
    Returns a nicely formatted string'''

    #this whole stuff could maybe be optimized but I'm too lazy and it seems to work fine for now

    #remove all the newline symbols and other useless stuff
    stripped = re.sub(r"\[|\]|'?\\[n|r]'?,?|' ',", '', summaryLine)
    #remove superflous ', and ",
    stripped = re.sub(r"[\"|'],", '\n\n', stripped)
    #remove backslashes in front of apostrophes
    stripped = re.sub(r"\\'", "'", stripped)
    #finally remove leading spaces, ' and " in any combination so the text starts with a letter
    stripped = re.sub(r"^\W+", '', stripped, flags=re.MULTILINE)
    return stripped

def getSummaries(_print=False):
    '''Returns a list of game summaries
    for some reason you really have to access summary[index] to get something useful out of it, 
    otherwise there will be brackets and \n and so in the text. I have no idea why this is, but accessing the individual indices will help
    '''
    if(_print):
        print("Collecting game summaries...")

    summaries = []
    #walter has collected nfl reviews from the years 2008 to 2020
    for year in range(8, 20):
        #there are up to 20 play weeks in each year
        for week in range(1, 20):
            url = "https://walterfootball.com/nflreview20{:02d}_{:02d}.php".format(year, week)
            print("Trying to access {}...".format(url))
            req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
            page = urlopen(req).read()
            soup = BeautifulSoup(page, "html.parser")
            
            #get all game names. these may be inside of <li> tags but are definetly marked by <b> tags. 
            #because walter is a **** that doesnt understand common sense and programming he sometimes has the last (or even more?) 
            #line of his report in the same <li> tag as the matchup (team names + scores)
            #I have to get all the text between the first and last <b> [Team] [Score], [Team] [Score] </b>, no matter in which list item they are stored



            #the ids of the game summaries starts with 5 digits that are composed of year and gameweek (YYYYW)
            #not all games have these kinds of ids. i have to find a different way to extract the games that dont use this schematic
            reg = "^[0-9]{5}" #id= re.compile(reg)
            for summary in soup.find_all('div', id="MainContentBlock"):
                print(summary)
                line = summary.findAll(text=True)
                linetext = beautify(str(line))
                print("--", linetext)
                summaries.append(linetext)

    print("Collected {} summaries".format(len(summaries)))
    return summaries

summaries = getSummaries(True)
