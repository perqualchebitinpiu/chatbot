#author: Alfonso Breglia
#email: perqualchebitinpiu@gmail.com
#Date: 	 18/01/2018
#Description: codice sorgente del bot di telegram Perqualchebotinpiu_bot

from textblob import TextBlob
from fuzzywuzzy import fuzz
from textblob.classifiers import NaiveBayesClassifier
from functools import partial
import telepot
import time
import CFG

offset = 0

#classifier
cl = NaiveBayesClassifier(train, feature_extractor = chatbot_extractor)   

#definiamo il nostro classificatore personalizzato
def chatbot_extractor(document):

    blob = TextBlob(document)	
    words = blob.upper().words 
    #print(words)
    feat = {}
    #question
    feat ["contain(WHERE)"]  = "WHERE"  in  words
    feat ["contain(WHAT)"]   = "WHAT"  	in  words
    feat ["contain(HOW)"]    = "HOW"  	in  words
    feat ["contain(WHICH)"]  = "WHICH"  in  words
    #punteggiatura
    feat ["contain(?)"] 	 = "?"  	in  words
    feat ["contain(.)"] 	 = "."  	in  words
    #command
    feat ["contain(DO)"] 	 = "DO"  in  words
    feat ["contain(FIND)"] 	 = "FIND"  in  words
    feat ["contain(GET)"]    = "GET"  in  words
    feat ["contain(TELL)"] 	 = "TELL"  in  words
    feat ["contain(SEARCH)"] = "SEARCH"  in  words
    #approval
    feat ["contain(YES)"]    = "YES"  in  words
    feat ["contain(NO)"] 	 = "NO"  in  words
    feat ["contain(OK)"] 	 = "OK"  in  words
    feat ["contain(GOOD)"]   = "GOOD"  in  words
    #saluti
    feat ["contain(HELLO)"]  = "HELLO"  in  words
    feat ["contain(HI)"] 	 = "HI"  in  words
    feat ["contain(BYE)"] 	 = "BYE"  in  words
    feat ["contain(HEY)"] 	 = "HEY"  in  words
    #statements
    feat ["contain(THINK)"]  = "THINK"  in  words
    feat ["contain(LIKE)"] 	 = "LIKE"  in  words
    feat ["contain(FEEL)"]   = "FEEL"  in  words

    return feat        


#classifier
train = [
    ('What time is it?', 'question'),
    ('where is Naples?', 'question'),
    ('How long is it been?', 'question'),
    ('which one is the champion?', 'question'),
    ('do the thing', 'command'),
    ('find the way to Naples', 'command'),
    ("get me the summary", 'command'),
    ("search on internet", 'command'),
    ('tell me the time', 'command'),
    ('hello bot', 'greeting'),
    ('hi there', 'greeting'),
    ('hey bot', 'greeting'),
    ('I do not like my job.', 'statement'),
	("I feel amazing!", 'statement'),
	("I feel better", 'statement'),
	("you think like a bot", 'statement')
    ]




# grammar è la grammatiche che usa il bot per
# analizzare le frasi e per comporle
class Perqualchebotinpiu:

    def init(self, type_classifier, grammar):
        self.myname =  "Perqualchebotinpiu"
        #532223263:AAGvEJdfAwMX-W0VYsFWAVAhaZqnjtOB0no
        self.TOKEN = "532223263:AAGvEJdfAwMX-W0VYsFWAVAhaZqnjtOB0no"
        #type of word classifier
        self.tcl = type_classifier
        self.grammar  = grammar
        
        bot_handle = telepot.Bot(TOKEN)
        print(bot_handle.getMe())

    def think(self, content,sender_id,sender_name):
        
        # Analizza le frasi che sono arrivate
        sentences = self.stage1(content,sender_id,sender_name)
        
        # Genera una possibile lista di risposte (una risposta puo contenere piu frasi)
        ans_list  = self.stage2(sender_id,sender_name,sentences) 
        
        # Analizza le risposte in base alle frasi alle risposte e alla memoria del bot
        # ritorna quell migliore
        best_ans = self.stage3(sender_name, sentences, ans_list,  bot_memory)
        
        return best_ans
        
    def stage1(self, content,sender_id,sender_name):
    
        blob = TextBlob(content)
        
        sentences = []
        #estrai dalle frasi delle features
        for sentence in blob.sentences:
            sentence = str(sentence)            
            #1) trova la categoria 
            category = cl.classify(sentence)
            #2) genera il sintax tree
            best_ph = get_best_syntax_three(sentence,question_grammar)
            
            sentences.append ({"sentence":sentence, "category": category, ""})
            
        return  sentences 

        
        

#definizioni delle grammatiche
question_grammar = CFG.CFG()
question_grammar.add_prod('S', 'AUXV NP MAINV OBJ| WHW BE_VERB OBJ |WHW ABOUT OBJ')
question_grammar.add_prod('NP', 'YOU')
question_grammar.add_prod('NP', 'I')
question_grammar.add_prod('AUXV', 'DO | CAN')
question_grammar.add_prod('DET', 'THE | A')
question_grammar.add_prod('BE_VERB', 'IS | ARE')
question_grammar.add_prod('MAINV', 'BE_VERB | THINK | LIKE |FIND | SEARCH |HAVE | TELL |KNOW')
question_grammar.add_prod('WHW', 'WHAT | WHERE | WHEN')
question_grammar.add_prod('OBJ', 'CC NN| DET NN | DET NN CC OBJ')
question_grammar.add_prod('CC', ' OF')
question_grammar.add_prod('NN', 'ICECREAM | PEN | BOOK')




def get_best_syntax_three(text, cfg):
    
    blob = TextBlob(text)
    ph_list = []
    #trova i token genera le regole semplificate
    #Taglia l'albero a vari livelli fino e genera le frasi
    #cfg.print_grammar()
    #print()
    for depth in range(4):
        cfg_copy = CFG.CFG(cfg.prod)
        cfg_copy.prune(blob.upper().words,depth)
        if "S" in cfg_copy.prod:
            #Genera un set di frasi 
            for i in range(10): 
                sent,tree = cfg_copy.gen_random_convergent('S')
                ph_list.append({"S":sent,"Tree":tree,"Score":0})
        else:
            break
                
    
    for ph in ph_list:
        ph["Score"] = fuzz.ratio(ph["S"],blob.upper())
    
    max_score = ph_list[0]["Score"]
    best_ph = ph_list[0]
    for ph in ph_list:
        if ph["Score"]> max_score:
            max_score = ph["Score"]
            best_ph  =  ph
    
    #print(best_ph)
    return best_ph


    
def greatings(name):
    if (name): 
        return ["hello: " + name]
    else:
        return ["hello"]
        

def search_for_info(something_to_search):
    str_v =  ["I googled for " + str(something_to_search)]
    str_v.append("I found this: .... ")
    str_v.append("but I'm not smart enough to understand, sorry")
    return str_v

def ask_for_info(something_unknown):
    return ["I have  very limited vocabulary, I do not understand " + str(something_unknown)]

def approve_res(state):
    if state:
        return ["yes"]
    else:
        return ["no"]
    
def Prephrases(phr):
    return [phr]

    
def parse_tree(tree):
    #trova il tipo di frase e chiama la successiva funzione
    PH= "."
    for p in tree["Tree"]:
        PH += p[0]+"."
    print (PH)
    actions = []
    if PH == ".WHW.BE_VERB.OBJ.":
        parse_WHW_BE_VERB_OBJ(tree["Tree"],actions)
    elif PH== ".WHW.ABOUT.OBJ.":
        parse_WHW_ABOUT_OBJ(tree["Tree"],actions)
    elif PH== ".AUXV.NP.MAINV.OBJ.":
        parse_AUXV_NP_MAINV_OBJ(tree["Tree"],action)
    else:
        action.append(partial(ask_for_info,something_to_search=tree[2][1][1]))

    return actions
    
def  parse_WHW_BE_VERB_OBJ(tree, action):
    if tree[0][1][0][0] == "WHAT":
        action.append(partial(Prephrases, phr=("so you want to know what " + str(tree[2][1][1]) + " is")))
        action.append(partial(search_for_info,something_to_search=tree[2][1][1]))

    elif tree[0][1][0][0] == "WHERE":
        action.append(partial(Prephrases, phr=("so you want to know where " + str(tree[2][1][1]) + " is")))
        action.append(partial(search_for_info,something_to_search=tree[2][1][1]))

    else:
        action.append(partial(ask_for_info,something_to_search=tree[2][1][1]))

def  parse_WHW_ABOUT_OBJ(tree, action):
    if tree[0][1][0][0] == "WHAT":
        action.append(partial(Prephrases, phr=("so you want to know something about: " + str(tree[2][1][1]))))
        action.append(partial(search_for_info,something_to_search=tree[2][1][1]))
    else:
        action.append(partial(ask_for_info,something_to_search=tree[2][1][1]))


def parse_AUXV_NP_MAINV_OBJ  (tree, action):      
    action.append(partial(Prephrases, phr="good question but I can't answer."))
    
#Each of these functions perform the corresponding action

def do_greatings(sentence,sender_id,sender_name):
    res = ["hello, {:s}".format(sender_name)] 
    return res
    
def do_command(sentence,sender_id,sender_name):
    res = ["I don't feel like doing anythink!"]
    return res


def do_question(sentence,sender_id,sender_name):
    best_ph = get_best_syntax_three(sentence,question_grammar)

    actions = parse_tree(best_ph)

    res = []
    for a in actions:
        res += a()
    return res

def do_statement(sentence,sender_id,sender_name):
    res = ["Ok, I don't have any memory!"]
    return res


def do_formula(sentence,sender_id,sender_name):
    res = ["I can't do computation"]
    return res

def think(content,sender_id,sender_name):
    blob = TextBlob(content)

    ret =[]
    for sentence in blob.sentences:
        sentence = str(sentence)
        #1) first do text categorization
        category = cl.classify(sentence)
        print(category)
        #2) perform the corresponding action
        if category == "command":
            res = do_command(sentence,sender_id,sender_name)
        elif category == "question":
            res = do_question(sentence,sender_id,sender_name)
        elif category == "statement":
            res = do_statement(sentence,sender_id,sender_name)
        elif category == "formula":
            res = do_formula(sentence,sender_id,sender_name)  
        elif category == "greeting":
            res = do_greatings(sentence,sender_id,sender_name)  
        ret = res

    return ret


while(True):
    resp = bot.getUpdates(offset)
    #gestisci tutti gli aggiornamenti
    for r in resp:
        print(r)
        try:
             
            sender_id  = r["message"]["from"]["id"]
            sender_name = r["message"]["from"]["first_name"]
            if("text" in r["message"]):
                content = r["message"]["text"]

                ret = think(content,sender_id,sender_name)
                for m in ret:
                    bot.sendMessage(sender_id,m)
            else:
                bot.sendMessage(sender_id, "sorry,{:s} I can only read text messages!".format(sender_name))              



        except Exception as e:
            print("Error: {:s}".format(str(e)))

        offset = r["update_id"] + 1

    time.sleep(2)
