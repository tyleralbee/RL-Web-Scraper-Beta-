import praw
import praw.reddit
from datetime import datetime
import re
import json

def checkIsMiddleMan(middleman):
    middlemen = ["Redditor(name='BrandonSalsa')", "Redditor(name='WrK_OG_PRIEST')", "Redditor(name='thuggarl')", "Redditor(name='AerospaceNinja')", "Redditor(name='merkface')", "Redditor(name='Gek_Lhar')", "Redditor(name='itsYAWBEE')", "Redditor(name='sweetrevenge117')"]
    if middleman in middlemen:
        pass


def main():
    #i scrape reddit, i scrape a specific post, i scrape only comments on that specific post.
    #TODO: i scrape facebook, i scrape a specific group, i scrape only posts in that specific group.

    #token information
    handle = 'prophase25'
    userAgent = "RLEScraper/0.3 by " + handle
    clientId = 'qgnEoTgYm4MdgQ'
    clientSecret = "ImRfDVCN_hJ2wCfQs5VXYqNlp8o"
    pw = "TOREPLACE"
    #/token information/

    #state variables
    keyDict = {}
    authorLister = []
    counter = 0
    url = 'https://www.reddit.com/r/RocketLeagueExchange/comments/7flk39/5xbox_anythinggoes_trading_thread_paypal_dlc/'
    #/state variables/

    #prior work
    r = praw.Reddit(user_agent = userAgent, client_id = clientId, client_secret = clientSecret, username = handle, password = pw)
    submission = r.submission(url = url)
    submission.comment_sort = 'new'
    submission.comments.replace_more(limit = 10)
    #/prior work/


    #iterate over submission comments
    for comment in submission.comments.list():

        #todo CHECK: pass over the middlemen comments
        checkIsMiddleMan(comment.author)
        #/todo CHECK: pass over the middlemen comments/

        #todo CHECK:pass over the duplicate authors
        if comment.author in authorLister:
            pass
        #/todo CHECK: pass over the duplicate authors/

        #todo CHECK: pass over dupe comments
        if comment.body in keyDict:
            pass
        #/todo CHECK: pass over dupe comments/

        else: #if not a middleman, reply, duplicate author, or duplicate post
            authorLister.append(comment.author)

            if counter != 0: #sticky pass
                p = re.compile('\[[hH]\] \$\d')

                if p.match(comment.body) is not None:
                    keyDict[str(comment.author)] = (comment.body, datetime.fromtimestamp(
                        comment.created_utc
                    ).strftime('%Y-%m-%d %H:%M:%S'), comment.permalink)



        counter += 1


    #/iterate over submission comments/

    #handle keyDict

    #/handle keyDict/



    #show me what you got
    print(keyDict)
    # reddit_json = json.dumps(keyDict)
    split_pattern = re.compile('\[W\]')
    l = split_pattern.split(keyDict['Ecyra'][0])
    quantity = re.split(r'\s', l[1])[1]
    item_name = re.split(r'\d', l[1])[1]
    print(l)
    print(quantity)
    print(item_name)
    # print(reddit_json.keys)
    # lr = json.loads(r)

    #keyDict.clear()
    #/show me what you got/

    #parse me what you got
    #parser(dudeWhereIsMyCar)
    #/parse me what you got/

main()





