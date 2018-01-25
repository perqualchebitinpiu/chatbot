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

 

#532223263:AAGvEJdfAwMX-W0VYsFWAVAhaZqnjtOB0no
TELEGRAM_TOKEN = "532223263:AAGvEJdfAwMX-W0VYsFWAVAhaZqnjtOB0no"

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
#classifier
cl = NaiveBayesClassifier(train, feature_extractor = chatbot_extractor)  



#definizioni delle grammatiche
grammar = CFG.CFG()
grammar.add_prod('S', 'AUXV NP MAINV OBJ| WHW BE_VERB OBJ |WHW ABOUT OBJ')
grammar.add_prod('NP', 'YOU')
grammar.add_prod('NP', 'I')
grammar.add_prod('AUXV', 'DO | CAN')
grammar.add_prod('DET', 'THE | A')
grammar.add_prod('BE_VERB', 'IS | ARE')
grammar.add_prod('MAINV', 'BE_VERB | THINK | LIKE |FIND | SEARCH |HAVE | TELL |KNOW')
grammar.add_prod('WHW', 'WHAT | WHERE | WHEN')
grammar.add_prod('OBJ', 'CC NN| DET NN | DET NN CC OBJ')
grammar.add_prod('CC', ' OF')
grammar.add_prod('NN', 'ICECREAM | PEN | BOOK')



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
    


# grammar è la grammatiche che usa il bot per
# analizzare le frasi e per comporle
class Perqualchebotinpiu:

    def init(self, type_classifier, grammar):
        self.myname =  "Perqualchebotinpiu"

        #type of word classifier
        self.tcl = type_classifier
        self.grammar  = grammar
        


    #bot actions
    def greatings(self, name):
        if (name): 
            return ["hello: " + name]
        else:
            return ["hello"]


    def search_for_info(self, something_to_search):
        str_v =  ["I googled for " + str(something_to_search)]
        str_v.append("I found this: .... ")
        str_v.append("but I'm not smart enough to understand, sorry")
        return str_v

    def ask_for_info(self, something_unknown):
        return ["I have  very limited vocabulary, I do not understand " + str(something_unknown)]

    def approve_res(self, state):
        if state:
            return ["yes"]
        else:
            return ["no"]
        
    def emit_phrase(self, phr):
        return [phr]

            
        
    def think(self, content,sender_id,sender_name):
        
        # Analizza le frasi che sono arrivate
        sentences = self.stage1(content,sender_id,sender_name)
        
        # Genera una possibile lista di risposte (una risposta puo contenere piu frasi)
        actions_list = self.stage2(sender_id,sender_name,sentences) 
        
        # Analizza le risposte in base alle frasi alle risposte e alla memoria del bot
        # ritorna quell migliore
        best_ans = self.stage3(sender_name, sentences, actions_list)
        
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
            best_syntax_tree = get_best_syntax_tree(sentence,question_grammar)

            
            sentences.append ({"sentence":sentence, "category": category, "syntax_tree":best_syntax_tree})
            
        return  sentences 
    
    def resolve_unknown(self, s):
        pass
    
    def stage2(self, sender_id,sender_name,sentences):
        for s in sentences:
            #3) resolve unknown
            self.resolve_unknown(s)
        
        
        actions  = []
        actions.append(partial(self.ask_for_info,something_to_search = "object to search"))
        actions.append(partial(self.greatings,   name = sender_name))
        actions.append(partial(self.emit_phrase, phr = "good question but I can't answer."))
        
        return actions
    
    
    def stage3(self, sender_name, sentences, actions_list):
        
        best_actions = actions_list[0]
        best_score = -1;
        best_res = []
        
        for actions in actions_list:            
        
            res = []
            for a in actions:
                res += a()
            
            score = self.eval_actions(res)
        
            if score > best_score:
                best_score = score 
                best_actions = actions
                best_res = res
                
        return best_res
        
        
bot_handle = telepot.Bot(TELEGRAM_TOKEN)
print(bot_handle.getMe())
 

while(True):   
    bot = Perqualchebotinpiu(cl, grammar)
    
    resp = bot_handle.getUpdates(offset)
    #gestisci tutti gli aggiornamenti
    for r in resp:
        print(r)
        try:
             
            sender_id  = r["message"]["from"]["id"]
            sender_name = r["message"]["from"]["first_name"]
            if("text" in r["message"]):
                content = r["message"]["text"]

                ret = bot.think(content,sender_id,sender_name)
                for m in ret:
                    bot_handle.sendMessage(sender_id,m)
            else:
                bot_handle.sendMessage(sender_id, "sorry,{:s} I can only read text messages!".format(sender_name))              



        except Exception as e:
            print("Error: {:s}".format(str(e)))

        offset = r["update_id"] + 1

    time.sleep(2)
