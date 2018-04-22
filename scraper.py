import praw
import praw.reddit
from datetime import datetime
import re
import json

class Item:
    def __init__(self):
        self.count = 1


    def setName(self, name):
        self.name = name

    def getName(self):
        return self.name

    def setCert(self, cert):
        self.cert = cert

    def getCert(self):
        return self.cert

    def setPaint(self, paint):
        self.paint = paint

    def getPaint(self):
        return self.paint

    def setAvgPriceDollars(self, avgPriceDollars):
        self.avgPriceDollars = avgPriceDollars

    def getAvgPriceDollars(self):
        return self.avgPriceDollars

    def updateAvgPricesDollars(self, data):
        self.count += 1
        self.avgPriceDollars = ((data + self.getAvgPriceDollars)/self.count)




def checkIsMiddleMan(middleman):
    middlemen = ["Redditor(name='BrandonSalsa')", "Redditor(name='WrK_OG_PRIEST')", "Redditor(name='thuggarl')", "Redditor(name='AerospaceNinja')", "Redditor(name='merkface')", "Redditor(name='Gek_Lhar')", "Redditor(name='itsYAWBEE')", "Redditor(name='sweetrevenge117')"]
    if middleman in middlemen:
        pass


def main():
    #i scrape reddit, i scrape a specific post, i scrape only comments on that specific post.
    #TODO: i scrape facebook, i scrape a specific group, i scrape only posts in that specific group.

    #token information
    handle = 'TOREPLACE'
    userAgent = "TOREPLACE" + handle
    clientId = 'TOREPLACE'
    clientSecret = "TOREPLACE"
    pw = "TOREPLACE"
    #/token information/

    #state variables
    keyDict = {}
    authorLister = []
    counter = 0
    classDict = {}
    certHolder = ''
    paintHolder = ''
    url = 'https://www.reddit.com/r/RocketLeagueExchange/comments/7flk39/5xbox_anythinggoes_trading_thread_paypal_dlc/'
    #/state variables/

    #prior work
    r = praw.Reddit(user_agent = userAgent, client_id = clientId, client_secret = clientSecret, username = handle, password = pw)
    submission = r.submission(url = url)
    submission.comment_sort = 'new'
    submission.comments.replace_more(limit = 10)
    #/prior work/

    #rocket league metadata
    paints = ['black', 'sienna', 'cobalt', 'crimson', 'green', 'grey', 'lime', 'orange', 'pink', 'purple', 'saffron', 'blue', 'white']
    certs = ['acrobat', 'aviator', 'goalkeeper', 'guardian', 'juggler', 'paragon', 'playmaker', 'scorer', 'show-off', 'sniper', 'striker', 'sweeper', 'tactician', 'turtle', 'victor']
    cars = ['samurai', 'werewolf', 'imperator', 'jäger', 'animus', 'centio', 'endo', 'mantis', 'octane', 'merc', 'road hog', 'breakout', 'venom', 'x-devil']
    paintedwheels = ['chak', 'photon', 'looper', 'lobo', 'voltaic', 'troika', 'pulsus', 'disco', 'spiralis', 'fsl', 'ara', 'zomba', 'septem', 'kalos', 'roulette', 'fireplug', 'triplex', 'k2', 'draco', 'slk', 'fgsp', 'turbine', 'gaiden', 'saptarishi', 'chrono', 'clockwork', 'revenant', 'grimalkin', 'cauldron', 'yuzo', 'hiro', 'equalizer', 'hikari', 'pepper', 'wreath', 'wonderment', 'nipper', 'balla-carra', 'infinium', 'apex', 'ninja', 'razzle', 'aether', 'doughnut', 'lustrum', 'illuminata', 'hypnotik', 'diomedes', 'kyrios', 'reevrb', 'vortex', 'dieci', 'sunburst', 'tunica', 'spyder', 'alchemist', 'invader', 'stern', 'octavian', 'neptune', 'oem', 'veloce', 'almas', 'rat rod', 'falco', 'lowrider', 'trahere', 'asterias', 'zeta']
    wheels = ['gearlock', 'zt-17', 'flash wheels', 'decenium pro', 'sovereign pro', 'carriage', 'wwe']
    crates = ['triumph', 'cc1', 'cc2', 'cc3', 'cc4', 'turbo', 'nitro', 'pcc', 'velocity', 'accelerator', 'secret santa', 'overdrive', 'halloween', 'victory']
    blackmarketdecals = ['dissolver', 'chameleon', 'heat', 'trigon', 'bubbly', '20xx', 'bio', 'slip', 'para', 'spectre', 'tora', 'lab', 'hex', 'storm']
    blackmarketgoalexplosions = ['dueling', 'popcorn', 'hellfire', 'poly', 'party', 'electro', 'sub', 'fireworks', 'toon', 'atomizer', 'ballistic', 'butterflies', 'happy holidays', 'reaper', 'vampire bats']
    paintedboosts = ['comet', 'springtime flowers', 'geo soul', 'blast ray', 'tsunami', 'toon sketch', 'fractal', 'power shot', 'helios', 'hexphase', 'magic missile', 'neo-thermal', 'tachyon', 'datastream', 'flamethrower', 'ion', 'lightning', 'plasma', 'sacred', 'sparkles', 'standard', 'thermal']
    boosts = ['cold fusion', 'dark matter', 'hypernova', 'pixel fire', 'polygonal', 'proton', 'trinity', 'xeno', 'scary pumpkin', 'feather', 'candy corn', 'yuletide', 'toon smoke', 'hearts', 'lightning', 'lightning yellow', 'treasure', 'ink', 'frostbite', 'magmus', 'taco', 'xmas', 'nether', 'winter']
    painteddecals = ['lone wolf', 'buzz kill', 'griffon', 'rlcs', 'thanatos', 'christmas tree', 'slimline', 'dune racer', 'funny book', 'jiangshi', 'tribal', 'odd fish', 'stitches', 'heiwa', 'chainsaw', 'rad reindeer', 'froggy', 'mobo', 'egged', 'mgda', 'afterlife', 'suji', 'holiday deco', 'fantasmo', 'unmasked', 'splatter', 'callous bros', 'widows web', 'critters', 'cold front', 'hammer-head', 'mg-88', 'spatter', 'cobra', 'kawaii', 'sticker bomb', 'super rxt', 'gigapede', 'pollinator', 'athena', 'mosher', 'xviii', 'mister monsoon', 'hip-hop']
    decals = ['racer', 'mg-88', 'shisha', 'kilowatt', 'roadkill', 'snakeskin', 'distortion', 'dragon lord', 'ripped comic', 'junk food', 'shibuya', 'dot matrix', 'vice', 'turbo', 'arcana', 'vector', 'boo!', 'royalty', 'pollo caliente', 'mondo', 'maximon', 'oni', 'aqueous', 'combo', 'anubis', 'whizzle', 'wildfire', 'carbonated', 'mean streak', 'hi-tech', 'flower power', 'narwhal', 'warlock', 'flex', 'nine lives', 'twisted tree', 'christmas sweater', 'kaleidoscope', 'swirls']
    finishes = ['circuit board', 'furry', 'glossy block', 'pearlescent matte', 'metallic pearl', 'burlap', 'cookie dough', 'burlap', 'metallic (smooth)', 'moon rock', 'knitted yarn', 'anodized', 'zebra']
    trails = ['blazer', 'friction', 'lightspeed', 'hot rocks', 'lightning', 'hallowtide', 'zig zag', 'candy cane', 'luminous', 'equalizer', 'rainbow']
    antennas = ['koinobori', 'peppermint', 'dandelion seed', 'shadow witch', 'arachnotenna', 'scarecrow jack', 'fuzzy vamp', 'holiday gift']
    #/rocket league metadata/

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
                    split_patternW = re.compile('\[W\]', flags=re.IGNORECASE)
                    lW = split_patternW.split(keyDict[str(comment.author)][0])

                    print(lW)

                    quantityH = re.split(r'\s', lW[0])[1]

                    if '$' in quantityH:
                        for word in lW[1]:
                            if (word.lower() in crates):
                                classDict[word] = quantityH.replace('$', '')
                                obj = Item()
                                obj.setName(word)
                                obj.setAvgPriceDollars(quantityH.replace('$',''))
                            elif (word.lower() == 'sky'):
                                pass
                            elif (word.lower() == 'titanium'):
                                pass
                            elif (word.lower() == 'forest'):
                                pass
                            elif (word.lower() == 'burnt'):
                                pass
                            elif (word.lower() in certs):
                                certHolder = word.lower()
                            elif word in paints:
                                paintHolder = word.lower()
                            elif word in blackmarketdecals:
                                classDict[word] = quantityH.replace('$','')
                                obj = Item()
                                if certHolder:
                                    obj.setName(word)
                                    obj.setCert(certHolder)
                                else:
                                    obj.setName(word)

                            elif word in blackmarketgoalexplosions:
                                classDict[word] = quantityH.replace('$','')
                                obj = Item()
                                if certHolder:
                                    obj.setName(word)
                                    obj.setCert(certHolder)
                                else:
                                    obj.setName(word)

                            elif word in cars:
                                classDict[word] = quantityH.replace('$', '')
                                obj = Item()
                                if certHolder:
                                    obj.setName(word)
                                    obj.setCert(certHolder)
                                    if paintHolder:
                                        obj.setPaint(paintHolder)
                                else:
                                    obj.setName(word)
                                    if paintHolder:
                                        obj.setPaint(paintHolder)

                            elif word in paintedboosts:
                                classDict[word] = quantityH.replace('$', '')
                                obj = Item()
                                if certHolder:
                                    obj.setName(word)
                                    obj.setCert(certHolder)
                                    if paintHolder:
                                        obj.setPaint(paintHolder)
                                else:
                                    obj.setName(word)
                                    if paintHolder:
                                        obj.setPaint(paintHolder)

                            elif word in painteddecals:
                                classDict[word] = quantityH.replace('$', '')
                                obj = Item()
                                if certHolder:
                                    obj.setName(word)
                                    obj.setCert(certHolder)
                                    if paintHolder:
                                        obj.setPaint(paintHolder)
                                else:
                                    obj.setName(word)
                                    if paintHolder:
                                        obj.setPaint(paintHolder)
                            elif word in paintedwheels:
                                classDict[word] = quantityH.replace('$', '')
                                obj = Item()
                                if certHolder:
                                    obj.setName(word)
                                    obj.setCert(certHolder)
                                    if paintHolder:
                                        obj.setPaint(paintHolder)
                                else:
                                    obj.setName(word)
                                    if paintHolder:
                                        obj.setPaint(paintHolder)
                            elif word in finishes:
                                obj = Item()
                                obj.setName(word)
                                obj.setAvgPriceDollars(quantityH.replace('$',''))
                            elif word in wheels:
                                classDict[word] = quantityH.replace('$', '')
                                obj = Item()
                                if certHolder:
                                    obj.setName(word)
                                    obj.setCert(certHolder)
                                else:
                                    obj.setName(word)

                            elif word in boosts:
                                classDict[word] = quantityH.replace('$','')
                                obj = Item()
                                if certHolder:
                                    obj.setName(word)
                                    obj.setCert(certHolder)
                                else:
                                    obj.setName(word)
                        item_nameW = re.split(r'\s', lW[1])
                        certHolder = ''
                        paintHolder = ''

                    else: #user has an item
                        item_nameH = re.split(r'\s', lW[0])[1]


                    quantityW = re.split(r'\s', lW[1])[1]


                    print(quantityH)
                    #print(item_nameH)

                    #print(quantityW)
                    print(item_nameW)



        counter += 1


    #/iterate over submission comments/

    #handle keyDict

    #/handle keyDict/



    #show me what you got
    #print(keyDict)
    # reddit_json = json.dumps(keyDict)



    #print(lW)





    # print(reddit_json.keys)
    # lr = json.loads(r)

    #keyDict.clear()
    #/show me what you got/

    #parse me what you got
    #parser(dudeWhereIsMyCar)
    #/parse me what you got/

main()





