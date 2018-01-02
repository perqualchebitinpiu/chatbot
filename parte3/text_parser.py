#author: Alfonso Breglia
#email: perqualchebitinpiu@gmail.com
#Date: 	 18/01/2018
#Description: semplice parser basato su pattern matching

from textblob import TextBlob
from fuzzywuzzy import fuzz

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
cfg1.add_prod('MAINV', 'BE_VERB | THINK | LIKE |FIND | SEARCH |HAVE | TELL')
cfg1.add_prod('WHW', 'WHAT | WHERE | WHEN')
cfg1.add_prod('OBJ', 'CC NN| DET NN | DET NN CC OBJ')
cfg1.add_prod('CC', 'ABOUT | OF')
cfg1.add_prod('NN', 'ICECREAM | PEN | BOOK')



def get_best_syntax_three(text):

    blob = TextBlob(text)
    ph_list = []
    #trova i token genera le regole semplificate

    #Genera un set di frasi 
    for i in range(50): 
        ph_list.append(cfg1.gen_random_convergent('S'))
    
    for ph in ph_list:
        print(ph + str(fuzz.ratio(ph,blob.upper())))
    
    

get_best_syntax_three("WHERE ABOUT A PEN ABOUT A BOOK")

phrases = [
		"Can you tell me about something?",
		"What do you think about something?",
		"What is the purpose of your trip?",
		"Where is my book?",
		"where is your pencil?",
		"where is the pen?",
		"Do you like ice-cream?"
	]





