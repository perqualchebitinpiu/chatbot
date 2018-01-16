#author: Alfonso Breglia
#email: perqualchebitinpiu@gmail.com
#Date: 	 18/01/2018
#Description: semplice parser basato su pattern matching

import urllib.request as urllib2

    
from textblob import TextBlob
from fuzzywuzzy import fuzz
from googlesearch.googlesearch import GoogleSearch
from functools import partial


#"Do you like ice-cream?"  -> "VBP,PRP,IN,NN"
#Can you tell me about something?" -> "MD,PRP,VB,PRP,IN,NN"
#"What is the purpose of your trip?"" -> "WP,VBZ,DT,NN,IN,PRP$,NN"

#S 	     -> AUXV NP MAINV OBJ| WHW BE_VERB OBJ.
#NP		 -> YOU | I . 
#AUXV    -> DO | CAN .
#DET 	 -> THE | A .
#BE_VERB -> IS | ARE . 
#MAINV  -> BE_VERB | THINK | LIKE |FIND | SEARCH |HAVE | TELL.
#WHW	-> WHAT | WHERE | WHEN. 
#OBJ    -> CC NN| DET NN | DET NN CC OBJ .
#CC		-> ABOUT | OF .
#NN     -> ICECREAM | PEN | BOOK.





import CFG

cfg1 = CFG.CFG()
cfg1.add_prod('S', 'AUXV NP MAINV OBJ| WHW BE_VERB OBJ |WHW ABOUT OBJ')
cfg1.add_prod('NP', 'YOU')
cfg1.add_prod('NP', 'I')
cfg1.add_prod('AUXV', 'DO | CAN')
cfg1.add_prod('DET', 'THE | A')
cfg1.add_prod('BE_VERB', 'IS | ARE')
cfg1.add_prod('MAINV', 'BE_VERB | THINK | LIKE |FIND | SEARCH |HAVE | TELL |KNOW')
cfg1.add_prod('WHW', 'WHAT | WHERE | WHEN')
cfg1.add_prod('OBJ', 'CC NN| DET NN | DET NN CC OBJ')
cfg1.add_prod('CC', ' OF')
cfg1.add_prod('NN', 'ICECREAM | PEN | BOOK')


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
# sent,tree = cfg1.gen_random_convergent('S')
# print()

# print(sent)

#Where does he live?

# cfg1.prune(sent.split())

# cfg1.print_grammar()
# print()

# sent,tree = cfg1.gen_random_convergent('S')
# print(sent)


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

best_ph = get_best_syntax_three("what is a cat",cfg1)

print (best_ph)
actions = parse_tree(best_ph)

print(actions)

res = []
for a in actions:
    res += a()
    
print (res)