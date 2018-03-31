import praw
import praw.reddit

def main():
    username = 'prophase25'
    userAgent = "RLEScraper/0.1 by " + username
    clientId = 'qgnEoTgYm4MdgQ'
    clientSecret = "config"
    password = "config"
    keyDict = {}
    authorLister = []
    counter = 0
    r = praw.Reddit(user_agent = userAgent, client_id=clientId, client_secret=clientSecret, username = username, password = password)
    submission = r.submission(url='https://www.reddit.com/r/RocketLeagueExchange/comments/7flk39/5xbox_anythinggoes_trading_thread_paypal_dlc/')
    submission.comments.replace_more(limit=5)
    for comment in submission.comments.list():


        if comment.author in authorLister:
            pass
        else:
            authorLister.append(comment.author)

            if counter != 0:
                keyDict[comment.author] = comment.body
        counter += 1



    print(keyDict)

main()





