import praw
import praw.reddit

def main():
    #i scrape reddit, i scrape a specific post, i scrape only comments on that specific post.
    #TODO: i scrape facebook, i scrape a specific group, i scrape only posts in that specific group.

    #token information
    handle = 'prophase25'
    userAgent = "RLEScraper/0.1 by " + handle
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
    submission.comments.replace_more(limit = 5)
    #/prior work/


    #iterate over submission comments
    for comment in submission.comments.list():

        #todo CHECK: over the middlemen comments
        if (comment.author == "Redditor(name='BrandonSalsa')"):
            pass#eroonie
        if (comment.author == "Redditor(name='WRKOGPriest')"):
            pass#eroonie
        if (comment.author == "Redditor(name='WesELMOwes')"):
            pass#eroonie
        if (comment.author == "Redditor(name='Modulartor')"):
            pass#eroonie
        if (comment.author == "Redditor(name='TheModuloMan')"):
            pass#eroonie
        #/todo CHECK: over the middlemen comments/

        #todo CHECK:pass over the duplicate authors
        if comment.author in authorLister:
            pass#abippity
        #/todo CHECK: pass over the duplicate authors/

        #todo CHECK: pass over dupe comments
        if comment.body in keyDict:
            pass#adiddly
        #/todo CHECK: pass over dupe comments/

        #todo CHECK: pass over replies
        if comment.body in comment.replies:
            pass#adoodly
        #/todo CHECK: pass over replies/


        else: #if not a middleman, reply, duplicate author, or duplicate post
            authorLister.append(comment.author)

            if counter != 0: #sticky pass
                keyDict[comment.author] = comment.body

        counter += 1 #de sticks

    #bork
    #bork
    #bork

    #/iterate over submission comments/

    #show me what you got
    print(keyDict)
    #/show me what you got/

main()
