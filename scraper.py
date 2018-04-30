import praw
import praw.reddit
from datetime import datetime
from firebase import firebase
import re
import json
import pickle
class Item:
    def __init__(self):
        self.count = 0


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

    def setAvgPriceDollars(self, avgPriceDollars, count):
        self.count += 1
        self.avgPriceDollars = avgPriceDollars/count

    def getAvgPriceDollars(self):
        return self.avgPriceDollars

    def updateItem(self, name, cert = 'none', paint = 'none'):
        self.setName(name)
        self.setCert(cert)
        self.setPaint(paint)

    def saveInfo(self):
        itemInfo = {self.name:[self.cert, self.paint, self.avgPriceDollars]}
        with open('itemInfo.p', 'ab') as fp:
            pickle.dump(itemInfo, fp, protocol=pickle.HIGHEST_PROTOCOL)




def pushToFirebase(self):
    fire = firebase.FirebaseApplication('https://rlprices-9523a.firebaseio.com/', None)
    fire.post('/neworders', self.bigDict)

def checkIsMiddleMan(middleman):
    middlemen = ["Redditor(name='BrandonSalsa')", "Redditor(name='WrK_OG_PRIEST')", "Redditor(name='thuggarl')", "Redditor(name='AerospaceNinja')", "Redditor(name='merkface')", "Redditor(name='Gek_Lhar')", "Redditor(name='itsYAWBEE')", "Redditor(name='sweetrevenge117')"]
    if middleman in middlemen:
        return True


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
    bigDict = {}
    itemCount = 0
    authorLister = []
    counter = 0
    classDict = {}
    certHolder = ''
    paintHolder = ''
    importHolder = ''
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
    paintedWheels = ['chak', 'chakrams', 'loopers', 'photons', 'clocks', 'photon', 'looper', 'lobo', 'voltaic', 'volts', 'troikas', 'pulsus', 'discos', 'spiralis', 'fsl', 'ara', 'zomba', 'septem', 'kalos', 'roulette', 'fireplug', 'triplex', 'k2', 'dracos', 'zombas', 'slk', 'fgsp', 'turbine', 'gaiden', 'saptarishi', 'chrono', 'clockwork', 'revenant', 'grimalkin', 'cauldron', 'yuzo', 'hiro', 'equalizer', 'hikari', 'pepper', 'wreath', 'wonderment', 'nipper', 'balla-carra', 'infinium', 'apex', 'ninja', 'razzle', 'aether', 'doughnut', 'lustrum', 'illuminata', 'hypnotik', 'diomedes', 'kyrios', 'reevrb', 'vortex', 'dieci', 'sunburst', 'tunica', 'spyder', 'alchemist', 'invader', 'stern', 'octavian', 'neptune', 'oem', 'veloce', 'almas', 'rat rod', 'falco', 'lowrider', 'trahere', 'asterias', 'zeta']
    wheels = ['gearlock', 'zt-17', 'flash wheels', 'decenium pro', 'sovereign pro', 'carriage', 'wwe']
    crates = ['triumph', 'triumphs', 'pccs', 'cc1s', 'cc2s', 'cc3s', 'cc4s', 'turbos', 'nitros', 'cc1', 'cc2', 'cc3', 'cc4', 'turbo', 'nitro', 'pcc', 'velocity', 'accelerator', 'secret santa', 'overdrive', 'halloween', 'victory']
    blackMarketDecals = ['dissolver', 'chameleon', 'heat', 'trigon', 'bubbly', '20xx', 'bio', 'slip', 'para', 'spectre', 'tora', 'lab', 'hex', 'storm']
    blackMarketGoalExplosions = ['dueling', 'popcorn', 'hellfire', 'poly', 'party', 'electro', 'sub', 'fireworks', 'toon', 'atomizer', 'ballistic', 'butterflies', 'happy holidays', 'reaper', 'vampire bats']
    paintedBoosts = ['comet', 'springtime flowers', 'geo soul', 'blast ray', 'tsunami', 'toon sketch', 'fractal', 'power shot', 'helios', 'hexphase', 'magic missile', 'neo-thermal', 'tachyon', 'datastream', 'flamethrower', 'ion', 'lightning', 'plasma', 'sacred', 'sparkles', 'standard', 'thermal']
    boosts = ['cold fusion', 'dark matter', 'hypernova', 'pixel fire', 'polygonal', 'proton', 'trinity', 'xeno', 'scary pumpkin', 'feather', 'candy corn', 'yuletide', 'toon smoke', 'hearts', 'lightning', 'lightning yellow', 'treasure', 'ink', 'frostbite', 'magmus', 'taco', 'xmas', 'nether', 'winter']
    paintedDecals = ['lone wolf', 'buzz kill', 'griffon', 'rlcs', 'thanatos', 'christmas tree', 'slimline', 'dune racer', 'funny book', 'jiangshi', 'tribal', 'odd fish', 'stitches', 'heiwa', 'chainsaw', 'rad reindeer', 'froggy', 'mobo', 'egged', 'mgda', 'afterlife', 'suji', 'holiday deco', 'fantasmo', 'unmasked', 'splatter', 'callous bros', 'widows web', 'critters', 'cold front', 'hammer-head', 'mg-88', 'spatter', 'cobra', 'kawaii', 'sticker bomb', 'super rxt', 'gigapede', 'pollinator', 'athena', 'mosher', 'xviii', 'mister monsoon', 'hip-hop']
    decals = ['racer', 'mg-88', 'shisha', 'kilowatt', 'roadkill', 'snakeskin', 'distortion', 'dragon lord', 'ripped comic', 'junk food', 'shibuya', 'dot matrix', 'vice', 'turbo', 'arcana', 'vector', 'boo!', 'royalty', 'pollo caliente', 'mondo', 'maximon', 'oni', 'aqueous', 'combo', 'anubis', 'whizzle', 'wildfire', 'carbonated', 'mean streak', 'hi-tech', 'flower power', 'narwhal', 'warlock', 'flex', 'nine lives', 'twisted tree', 'christmas sweater', 'kaleidoscope', 'swirls']
    finishes = ['circuit board', 'furry', 'glossy block', 'pearlescent matte', 'metallic pearl', 'burlap', 'cookie dough', 'burlap', 'metallic (smooth)', 'moon rock', 'knitted yarn', 'anodized', 'zebra']
    trails = ['blazer', 'friction', 'lightspeed', 'hot rocks', 'lightning', 'hallowtide', 'zig zag', 'candy cane', 'luminous', 'equalizer', 'rainbow']
    antennas = ['koinobori', 'peppermint', 'dandelion seed', 'shadow witch', 'arachnotenna', 'scarecrow jack', 'fuzzy vamp', 'holiday stocking']
    #/rocket league metadata/

    #iterate over submission comments
    for comment in submission.comments.list():

        #todo CHECK: pass over the middlemen comments
        if checkIsMiddleMan(comment.author):
            continue
        #/todo CHECK: pass over the middlemen comments/

        #todo CHECK:pass over the duplicate authors
        elif (comment.author in authorLister):
            continue
        #/todo CHECK: pass over the duplicate authors/

        #todo CHECK: pass over dupe comments
        elif (comment.body in keyDict):
            continue
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
                    quantityW = re.split(r'\s', lW[1])[1]
                    wordList = lW[1].split()
                    wordList2 = lW[0].split()

                    if '$' in quantityH:
                        for word in wordList:
                            #CRATE HANDLING
                            try:
                                int(word)
                                quantityW = int(word)
                            except ValueError:

                                if word.lower() in crates:                            #crates cannot be certified/painted
                                    classDict[word] = float(quantityH.replace('$', ''))        #change $x (maybe: $1) to x and store {word (maybe: cc4): x }
                                    obj = Item()
                                    if 'imports' in wordList:
                                        try:
                                            float(quantityW)
                                            obj.setAvgPriceDollars(classDict[word], int(quantityW))
                                        except ValueError:
                                            obj.setAvgPriceDollars(classDict[word], 1)
                                        importHolder = word + " import"
                                        obj.updateItem(importHolder)
                                        print('imports!')
                                    elif 'import' in wordList:
                                        try:
                                            float(quantityW)
                                            obj.setAvgPriceDollars(classDict[word], int(quantityW))
                                        except ValueError:
                                            obj.setAvgPriceDollars(classDict[word], 1)
                                        importHolder = word + " import"
                                        obj.updateItem(importHolder)
                                        print('imports!')
                                    elif 'Import' in wordList:
                                        try:
                                            float(quantityW)
                                            obj.setAvgPriceDollars(classDict[word], int(quantityW))
                                        except ValueError:
                                            obj.setAvgPriceDollars(classDict[word], 1)
                                        importHolder = word + " import"
                                        obj.updateItem(importHolder)
                                        print('imports!')
                                    elif 'Imports' in wordList:
                                        try:
                                            float(quantityW)
                                            obj.setAvgPriceDollars(classDict[word], int(quantityW))
                                        except ValueError:
                                            obj.setAvgPriceDollars(classDict[word], 1)
                                        importHolder = word + " import"
                                        obj.updateItem(importHolder)
                                        print('imports!')
                                    else:
                                        try:
                                            float(quantityW)
                                            obj.setAvgPriceDollars(classDict[word], int(quantityW))
                                        except ValueError:
                                            obj.setAvgPriceDollars(classDict[word], 1)
                                        obj.updateItem(word)
                                    obj.saveInfo()
                                    print('crates!')
                                    itemCount += 1
                                #/CRATE HANDLING

                                #FINISHES HANDLING
                                elif word.lower() in finishes:                                  #finishes cannot be certified/painted
                                    classDict[word] = quantityH.replace('$', '')        #change $x (maybe: $3) to x and store {word (maybe: furry): x }
                                    obj = Item()
                                    obj.updateItem(word.lower())
                                    try:
                                        float(quantityW)
                                        obj.setAvgPriceDollars(classDict[word], int(quantityW))
                                    except ValueError:
                                        obj.setAvgPriceDollars(classDict[word], 1)
                                    obj.saveInfo()
                                    print('finishes!')
                                    itemCount += 1
                                #/FINISHES HANDLING

                                #ANTENNA HANDLING
                                elif word.lower() in antennas:                                  #antennas cannot be certified/painted
                                    classDict[word] = quantityH.replace('$', '')        #change $x (maybe: $1) to x and store {word (maybe: candy cane): x }
                                    obj = Item()
                                    obj.updateItem(word.lower())
                                    obj.setAvgPriceDollars(quantityH.replace('$',''))
                                    obj.saveInfo()
                                    print('antenna!')
                                    itemCount += 1
                                #/ANTENNA HANDLING

                                #CERT HANDLING
                                elif (word.lower() in certs):                           #check if the word is a certification for their item
                                    certHolder = word.lower()                           #store the cert into a temporary variable until we find the name
                                    print('cert!')
                                #/CERT HANDLING

                                #BMD HANDLING
                                elif word.lower() in blackMarketDecals:                         #BMDs cannot be painted, but can be certified
                                    classDict[word] = float(quantityH.replace('$',''))         #change $x (maybe: $5) to x and store {word (maybe: cc4): x }
                                    obj = Item()
                                    if certHolder:                                      #if one of the previous words was a cert, parser is done
                                        obj.updateItem(word.lower(), certHolder)
                                        try:
                                            float(quantityW)
                                            obj.setAvgPriceDollars(classDict[word], quantityW)
                                        except ValueError:
                                            obj.setAvgPriceDollars(classDict[word], 1)
                                        obj.saveInfo()
                                        print('cert BMD!')
                                    else:
                                        obj.updateItem(word.lower())
                                        try:
                                            float(quantityW)
                                            obj.setAvgPriceDollars(classDict[word], quantityW)
                                        except ValueError:
                                            obj.setAvgPriceDollars(classDict[word], 1)
                                        obj.saveInfo()
                                        print('BMD!')
                                    itemCount += 1
                                #/BMD HANDLING

                                #BMGE HANDLING
                                elif word.lower() in blackMarketGoalExplosions:                 #BMGEs cannot be painted, but can be certified
                                    classDict[word] = float(quantityH.replace('$',''))      #change $x (maybe: $9) to x and store {word (maybe: hellfire): x }
                                    obj = Item()
                                    if certHolder:                                      #if one of the previous words was a cert, parser is done
                                        obj.updateItem(word.lower(), certHolder)
                                        try:
                                            float(quantityW)
                                            obj.setAvgPriceDollars(classDict[word], quantityW)
                                        except ValueError:
                                            obj.setAvgPriceDollars(classDict[word], 1)
                                        obj.saveInfo()
                                        print('cert BMGE!')
                                    else:
                                        obj.updateItem(word.lower())
                                        try:
                                            float(quantityW)
                                            obj.setAvgPriceDollars(classDict[word], quantityW)
                                        except ValueError:
                                            obj.setAvgPriceDollars(classDict[word], 1)
                                        obj.saveInfo()
                                        print('BMGE!')
                                    itemCount += 1
                                #/BMGE HANDLING

                                #UNPAINTED WHEEL HANDLING
                                elif word.lower() in wheels:                                    #some wheels cannot be painted, but can be certified
                                    classDict[word] = float(quantityH.replace('$','') )        #change $x (maybe: $300) to x and store {word (maybe: decennium pro): x }
                                    obj = Item()
                                    if certHolder:                                      #if one of the previous words was a cert, parser is done
                                        obj.updateItem(word.lower(), certHolder)
                                        try:
                                            float(quantityW)
                                            obj.setAvgPriceDollars(classDict[word], quantityW)
                                        except ValueError:
                                            obj.setAvgPriceDollars(classDict[word], 1)
                                        obj.saveInfo()
                                        itemCount += 1
                                        print('cert wheels!')
                                    else:
                                        obj.updateItem(word.lower())
                                        try:
                                            float(quantityW)
                                            obj.setAvgPriceDollars(classDict[word], quantityW)
                                        except ValueError:
                                            obj.setAvgPriceDollars(classDict[word], 1)
                                        obj.saveInfo()
                                        itemCount += 1
                                        print('wheels!')
                                #/UNPAINTED WHEEL HANDLING

                                #UNPAINTED BOOST HANDLING
                                elif word.lower() in boosts:                                    #some boosts cannot be painted, but can be certified
                                    classDict[word] = float(quantityH.replace('$',''))         #change $x (maybe: $9) to x and store {word (maybe: cold fusion): x }
                                    obj = Item()
                                    if certHolder:                                      #if one of the previous words was a cert, parser is done
                                        obj.updateItem(word.lower(), certHolder)
                                        try:
                                            float(quantityW)
                                            obj.setAvgPriceDollars(classDict[word], quantityW)
                                        except ValueError:
                                            obj.setAvgPriceDollars(classDict[word], 1)
                                        obj.saveInfo()
                                        itemCount += 1
                                        print('cert boost!')
                                    else:
                                        obj.updateItem(word.lower())
                                        try:
                                            float(quantityW)
                                            obj.setAvgPriceDollars(classDict[word], quantityW)
                                        except ValueError:
                                            obj.setAvgPriceDollars(classDict[word], 1)
                                        obj.saveInfo()
                                        itemCount += 1
                                        print('boost!')
                                #/UNPAINTED BOOST HANDLING

                                #UNPAINTED DECAL HANDLING
                                elif word.lower() in decals:                                    #some decals cannot be painted, but can be certified
                                    classDict[word] = float(quantityH.replace('$','') )        #change $x (maybe: $0.50) to x and store {word (maybe: racer): x }
                                    obj = Item()
                                    if certHolder:                                      #if one of the previous words was a cert, parser is done
                                        obj.updateItem(word.lower(), certHolder)
                                        try:
                                            float(quantityW)
                                            obj.setAvgPriceDollars(classDict[word], quantityW)
                                        except ValueError:
                                            obj.setAvgPriceDollars(classDict[word], 1)
                                        obj.saveInfo()
                                        itemCount += 1
                                        print('cert decal!')
                                    else:
                                        obj.updateItem(word.lower())
                                        try:
                                            float(quantityW)
                                            obj.setAvgPriceDollars(classDict[word], quantityW)
                                        except ValueError:
                                            obj.setAvgPriceDollars(classDict[word], 1)
                                        obj.saveInfo()
                                        itemCount += 1
                                        print('decal!')
                                #/UNPAINTED DECAL HANDLING

                                #TRAIL HANDLING
                                elif word.lower() in trails:                                    #trails cannot be painted, but can be certified
                                    classDict[word] = float(quantityH.replace('$',''))         #change $x (maybe: $2) to x and store {word (maybe: hot rocks): x }
                                    obj = Item()
                                    if certHolder:                                      #if one of the previous words was a cert, parser is done
                                        obj.updateItem(word.lower(), certHolder)
                                        try:
                                            float(quantityW)
                                            obj.setAvgPriceDollars(classDict[word], quantityW)
                                        except ValueError:
                                            obj.setAvgPriceDollars(classDict[word], 1)
                                        obj.saveInfo()
                                        itemCount += 1
                                        print('cert trail!')
                                    else:
                                        obj.updateItem(word.lower())
                                        try:
                                            float(quantityW)
                                            obj.setAvgPriceDollars(classDict[word], quantityW)
                                        except ValueError:
                                            obj.setAvgPriceDollars(classDict[word], 1)
                                        obj.saveInfo()
                                        itemCount += 1
                                        print('trail!')
                                #/TRAIL HANDLING

                                #PAINT HANDLING
                                elif (word.lower() == 'sky'):                           #if word is sky they will likely follow it with blue
                                    print('sky!')
                                    pass
                                elif (word.lower() == 'titanium'):                      #'' ''   '' titanium ''   ''     ''     '' ''   white
                                    print('titanium!')
                                    pass
                                elif (word.lower() == 'forest'):                        #'' ''   '' forest   ''   ''     ''     '' ''   green
                                    print('forest!')
                                    pass
                                elif (word.lower() == 'burnt'):                         #'' ''   '' burnt    ''   ''     ''     '' ''   sienna
                                    print('burnt!')
                                    pass

                                elif (word.lower() == 'sb'):                            #if word is sb they mean sky blue
                                    paintHolder = word.lower()
                                    print('sb!')
                                elif (word.lower() == 'tw'):                            #'' ''   '' tw ''   ''   titanium white
                                    paintHolder = word.lower()
                                    print('tw!')
                                elif (word.lower() == 'fg'):                            #'' ''   '' fg ''   ''   forest green
                                    paintHolder = word.lower()
                                    print('fg!')
                                elif (word.lower() == 'bs'):                            #'' ''   '' bs ''   ''   burnt sienna (hopefully)
                                    paintHolder = word.lower()
                                    print('bs!')
                                elif (word.lower() == 'crim'):                          #'' ''   '' crim    ''   crimson
                                    paintHolder = word.lower()
                                    print('crim!')

                                elif word in paints:                                    #check if the word is a color for their item
                                    paintHolder = word.lower()                          #store the paint into a temporary variable until we find the name
                                    print('paint!')
                                #/PAINT HANDLING

                                #PAINTED WHEEL HANDLING
                                elif word.lower() in paintedWheels:                             #paintedWheels can be both painted and certified
                                    classDict[word] = float(quantityH.replace('$', ''))
                                    obj = Item()
                                    if certHolder:
                                        try:
                                            float(quantityW)
                                            obj.setAvgPriceDollars(classDict[word], quantityW)
                                        except ValueError:
                                            obj.setAvgPriceDollars(classDict[word], 1)
                                        if paintHolder:
                                            obj.updateItem(word.lower(), certHolder, paintHolder)
                                            print('cert paint wheels!')
                                        else:
                                            obj.updateItem(word.lower(), certHolder)
                                            print('cert wheels!')
                                    else:
                                        try:
                                            float(quantityW)
                                            obj.setAvgPriceDollars(classDict[word], quantityW)
                                        except ValueError:
                                            obj.setAvgPriceDollars(classDict[word], 1)
                                        if paintHolder:
                                            obj.updateItem(word.lower(), 'none', paintHolder)
                                            print('paint wheels!')
                                        else:
                                            obj.updateItem(word.lower())
                                            print('wheels!')
                                    obj.saveInfo()
                                    itemCount += 1

                                #/PAINTED WHEEL HANDLING

                                #CAR BODY HANDLING
                                elif word.lower() in cars:                                      #cars can be both painted and certified
                                    classDict[word] = float(quantityH.replace('$', ''))
                                    obj = Item()
                                    try:
                                        float(quantityW)
                                        obj.setAvgPriceDollars(float(quantityH.replace('$','')), int(quantityW))
                                    except ValueError:
                                        obj.setAvgPriceDollars(float(quantityH.replace('$', '')), 1)
                                    if certHolder:
                                        if paintHolder:
                                            obj.updateItem(word.lower(), certHolder, paintHolder)
                                            print('cert paint car!')
                                        else:
                                            obj.updateItem(word.lower(), certHolder)
                                            print('cert car!')
                                    else:
                                        if paintHolder:
                                            obj.updateItem(word.lower(), 'none', paintHolder)
                                            print('paint car!')
                                        else:
                                            obj.updateItem(word.lower())
                                            print('car!')
                                    obj.saveInfo()
                                    itemCount += 1
                                #/CAR BODY HANDLING

                                #PAINTED DECAL HANDLING
                                elif word.lower() in paintedDecals:                             #paintedDecals can be both painted and certified
                                    classDict[word] = quantityH.replace('$', '')
                                    obj = Item()
                                    try:
                                        float(quantityW)
                                        obj.setAvgPriceDollars(classDict[word], int(quantityW))
                                    except ValueError:
                                        obj.setAvgPriceDollars(classDict[word], 1)
                                    if certHolder:
                                        if paintHolder:
                                            obj.updateItem(word.lower(), certHolder, paintHolder)
                                            print('cert paint decal!')
                                        else:
                                            obj.updateItem(word.lower(), certHolder)
                                            print('cert decal!')
                                    else:
                                        if paintHolder:
                                            obj.updateItem(word.lower(), 'none', paintHolder)
                                            print('paint decal!')

                                        else:
                                            obj.updateItem(word.lower())
                                            print('decal!')
                                    obj.saveInfo()
                                    itemCount += 1
                                #/PAINTED DECAL HANDLING

                                #PAINTED BOOST HANDLING
                                elif word.lower() in paintedBoosts:                             #paintedBoosts can be both painted and certified
                                    classDict[word] = quantityH.replace('$', '')
                                    obj = Item()
                                    try:
                                        float(quantityW)
                                        obj.setAvgPriceDollars(classDict[word], int(quantityW))
                                    except ValueError:
                                        obj.setAvgPriceDollars(classDict[word], 1)
                                    if certHolder:
                                        if paintHolder:
                                            obj.updateItem(word.lower(), certHolder, paintHolder)
                                            print('cert paint boost!')
                                        else:
                                            obj.updateItem(word.lower(), certHolder)
                                            print('cert boost!')
                                    else:
                                        obj.setName(word)
                                        obj.setCert('none')
                                        if paintHolder:
                                            obj.updateItem(word.lower(), 'none', paintHolder)
                                            print('paint boost!')
                                        else:
                                            obj.updateItem(word.lower())
                                            print('boost!')
                                    obj.saveInfo()
                                    itemCount+=1

                                #/PAINTED BOOST HANDLING

                                #NO MATCH HANDLING
                                else:
                                    pass
                                #/NO MATCH HANDLING

                        try:
                            bigDict[itemCount] = {
                                    'timestamp': 5,
                                    'name': obj.getName(),
                                    'cert': obj.getCert(),
                                    'price': obj.getAvgPriceDollars(),
                                    'paint': obj.getPaint(),
                                    'itemCount': 1
                            }
                        except UnboundLocalError:
                            continue

                        certHolder = ''
                        paintHolder = ''
                    else:
                        pass

        counter += 1
    #fire = firebase.FirebaseApplication('https://rlprices-9523a.firebaseio.com/', None)
    #fire.post('/bigBatch1', bigDict)
main()
