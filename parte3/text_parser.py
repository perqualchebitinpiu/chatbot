#author: Alfonso Breglia
#email: perqualchebitinpiu@gmail.com
#Date: 	 18/01/2018
#Description: semplice parser basato su pattern matching

from textblob import TextBlob
import re

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
cfg1.add_prod('S', 'NP VP')
cfg1.add_prod('NP', 'Det N | Det N')
cfg1.add_prod('NP', 'I | he | she | Joe')
cfg1.add_prod('VP', 'V NP | VP')
cfg1.add_prod('Det', 'a | the | my | his')
cfg1.add_prod('N', 'elephant | cat | jeans | suit')
cfg1.add_prod('V', 'kicked | followed | shot')

for i in range(10):
	print (cfg1.gen_random('S'))


phrases = [
		"Can you tell me about something?",
		"What do you think about something?",
		"What is the purpose of your trip?",
		"Where is my book?",
		"where is your pencil?",
		"where is the pen?",
		"Do you like ice-cream?"
	]


for ph in phrases:
	blob = TextBlob(ph)
	blob.upper()

	tag_string = ""
	for tag in blob.tags:
		tag_string += tag[1] + ",";
	tag_string = tag_string[0:-1]
	print(str(blob.tags) +tag_string)





prog = re.compile(r"WP,VBP,PRP,VB,IN,NN")
result = prog.match(tag_string)

if(result):
	print("True")
else:
	print("False")	
