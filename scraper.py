import praw
import praw.reddit
from datetime import datetime
import re
import json
import pickle
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

    def saveInfo(self):
        itemInfo = {self.name:[self.cert, self.paint, self.avgPriceDollars]}
        with open('itemInfo.p', 'wb') as fp:
            pickle.dump(itemInfo, fp, protocol=pickle.HIGHEST_PROTOCOL)


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
    pw = "nvojtaejtyler96"
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

    #rocket league metadata TODO: deal with spaces
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
    antennas = ['koinobori', 'peppermint', 'dandelion seed', 'shadow witch', 'arachnotenna', 'scarecrow jack', 'fuzzy vamp', 'holiday stocking']
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

                            #CRATE HANDLING
                            if (word.lower() in crates):                            #crates cannot be certified/painted
                                classDict[word] = quantityH.replace('$', '')        #change $x (maybe: $1) to x and store {word (maybe: cc4): x }
                                #TODO: check if object is already created
                                #if object created, update avg price
                                obj = Item()                                        #if not:create an object instance
                                obj.setName(word)
                                obj.setAvgPriceDollars(quantityH.replace('$',''))
                            #/CRATE HANDLING

                            #FINISHES HANDLING
                            elif word in finishes:                                  #finishes cannot be certified/painted
                                classDict[word] = quantityH.replace('$', '')        #change $x (maybe: $3) to x and store {word (maybe: furry): x }
                                #TODO: check if object is already created
                                #if object created, update avg price
                                obj = Item()
                                obj.setName(word)
                                obj.setAvgPriceDollars(quantityH.replace('$',''))
                            #/FINISHES HANDLING

                            #FINISHES HANDLING
                            elif word in antennas:                                  #antennas cannot be certified/painted
                                classDict[word] = quantityH.replace('$', '')        #change $x (maybe: $1) to x and store {word (maybe: candy cane): x }
                                #TODO: check if object is already created
                                #if object created, update avg price
                                obj = Item()
                                obj.setName(word)
                                obj.setAvgPriceDollars(quantityH.replace('$',''))
                            #/FINISHES HANDLING

                            #CERT HANDLING
                            elif (word.lower() in certs):                           #check if the word is a certification for their item
                                certHolder = word.lower()                           #store the cert into a temporary variable until we find the name
                            #/CERT HANDLING

                            #BMD HANDLING
                            elif word in blackmarketdecals:                         #BMDs cannot be painted, but can be certified
                                classDict[word] = quantityH.replace('$','')         #change $x (maybe: $5) to x and store {word (maybe: cc4): x }
                                # TODO: check if object is already created
                                # if object created, update avg price
                                obj = Item()
                                if certHolder:                                      #if one of the previous words was a cert, parser is done
                                    obj.setName(word)
                                    obj.setCert(certHolder)
                                    obj.setAvgPriceDollars(quantityH.replace('$', ''))
                                else:
                                    obj.setName(word)
                                    obj.setAvgPriceDollars(quantityH.replace('$', ''))
                            #/BMD HANDLING

                            #BMGE HANDLING
                            elif word in blackmarketgoalexplosions:                 #BMGEs cannot be painted, but can be certified
                                classDict[word] = quantityH.replace('$','')         #change $x (maybe: $9) to x and store {word (maybe: hellfire): x }
                                # TODO: check if object is already created
                                # if object created, update avg price
                                obj = Item()
                                if certHolder:                                      #if one of the previous words was a cert, parser is done
                                    obj.setName(word)
                                    obj.setCert(certHolder)
                                    obj.setAvgPriceDollars(classDict[word])
                                    obj.saveInfo()
                                else:
                                    obj.setName(word)
                            #/BMGE HANDLING

                            #UNPAINTED WHEEL HANDLING
                            elif word in wheels:                                    #some wheels cannot be painted, but can be certified
                                classDict[word] = quantityH.replace('$','')         #change $x (maybe: $300) to x and store {word (maybe: decennium pro): x }
                                # TODO: check if object is already created
                                # if object created, update avg price
                                obj = Item()
                                if certHolder:                                      #if one of the previous words was a cert, parser is done
                                    obj.setName(word)
                                    obj.setCert(certHolder)
                                    obj.setAvgPriceDollars(classDict[word])
                                    obj.saveInfo()
                                else:
                                    obj.setName(word)
                            #/UNPAINTED WHEEL HANDLING

                            #UNPAINTED BOOST HANDLING
                            elif word in boosts:                                    #some boosts cannot be painted, but can be certified
                                classDict[word] = quantityH.replace('$','')         #change $x (maybe: $9) to x and store {word (maybe: cold fusion): x }
                                # TODO: check if object is already created
                                # if object created, update avg price
                                obj = Item()
                                if certHolder:                                      #if one of the previous words was a cert, parser is done
                                    obj.setName(word)
                                    obj.setCert(certHolder)
                                    obj.setAvgPriceDollars(classDict[word])
                                    obj.saveInfo()
                                else:
                                    obj.setName(word)
                            #/UNPAINTED BOOST HANDLING

                            #UNPAINTED DECAL HANDLING
                            elif word in decals:                                    #some decals cannot be painted, but can be certified
                                classDict[word] = quantityH.replace('$','')         #change $x (maybe: $0.50) to x and store {word (maybe: racer): x }
                                # TODO: check if object is already created
                                # if object created, update avg price
                                obj = Item()
                                if certHolder:                                      #if one of the previous words was a cert, parser is done
                                    obj.setName(word)
                                    obj.setCert(certHolder)
                                    obj.setAvgPriceDollars(classDict[word])
                                    obj.saveInfo()
                                else:
                                    obj.setName(word)
                            #/UNPAINTED DECAL HANDLING

                            #TRAIL HANDLING
                            elif word in trails:                                    #trails cannot be painted, but can be certified
                                classDict[word] = quantityH.replace('$','')         #change $x (maybe: $2) to x and store {word (maybe: hot rocks): x }
                                # TODO: check if object is already created
                                # if object created, update avg price
                                obj = Item()
                                if certHolder:                                      #if one of the previous words was a cert, parser is done
                                    obj.setName(word)
                                    obj.setCert(certHolder)
                                    obj.setAvgPriceDollars(classDict[word])
                                    obj.saveInfo()
                                else:
                                    obj.setName(word)
                            #/TRAIL HANDLING

                            #PAINT HANDLING
                            elif (word.lower() == 'sky'):                           #if word is sky they will likely follow it with blue
                                pass
                            elif (word.lower() == 'titanium'):                      #'' ''   '' titanium ''   ''     ''     '' ''   white
                                pass
                            elif (word.lower() == 'forest'):                        #'' ''   '' forest   ''   ''     ''     '' ''   green
                                pass
                            elif (word.lower() == 'burnt'):                         #'' ''   '' burnt    ''   ''     ''     '' ''   sienna
                                pass

                            elif (word.lower() == 'sb'):                            #if word is sb they mean sky blue
                                pass
                            elif (word.lower() == 'tw'):                            #'' ''   '' tw ''   ''   titanium white
                                pass
                            elif (word.lower() == 'fg'):                            #'' ''   '' fg ''   ''   forest green
                                pass
                            elif (word.lower() == 'bs'):                            #'' ''   '' bs ''   ''   burnt sienna (hopefully)
                                pass
                            elif (word.lower() == 'crim'):                          #'' ''   '' crim    ''   crimson
                                pass

                            elif word in paints:                                    #check if the word is a color for their item
                                paintHolder = word.lower()                          #store the paint into a temporary variable until we find the name
                            #/PAINT HANDLING
                            
                            #PAINTED WHEEL HANDLING
                            elif word in paintedwheels:                             #paintedwheels can be both painted and certified
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
                            #/PAINTED WHEEL HANDLING
                            
                            #CAR BODY HANDLING
                            elif word in cars:                                      #cars can be both painted and certified
                                classDict[word] = quantityH.replace('$', '')
                                obj = Item()
                                if certHolder:
                                    obj.setName(word)
                                    obj.setCert(certHolder)
                                    obj.setAvgPriceDollars(classDict[word])
                                    obj.saveInfo()
                                    if paintHolder:
                                        obj.setPaint(paintHolder)
                                else:
                                    obj.setName(word)
                                    if paintHolder:
                                        obj.setPaint(paintHolder)
                            #/CAR BODY HANDLING
                            
                            #PAINTED DECAL HANDLING
                            elif word in painteddecals:                             #painteddecals can be both painted and certified
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
                            #/PAINTED DECAL HANDLING
                            
                            #PAINTED BOOST HANDLING
                            elif word in paintedboosts:                             #paintedboosts can be both painted and certified
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
                            #/PAINTED BOOST HANDLING
                                        

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

main()
