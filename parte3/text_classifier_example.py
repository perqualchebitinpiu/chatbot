#author: Alfonso Breglia
#email: perqualchebitinpiu@gmail.com
#Date: 	 18/01/2018
#Description: semplice text classifier
from textblob import TextBlob
from textblob.classifiers import NaiveBayesClassifier


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

    
test = [
    ('the beer was good.', 'statement'),
    ('I do not enjoy my job', 'statement'),
    ("I ain't feeling dandy today.", 'statement'),
    ("I feel amazing!", 'statement'),
    ('Gary is a friend of mine.', 'statement')
    ]    
    

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

cl = NaiveBayesClassifier(train, feature_extractor= chatbot_extractor)   
cl.show_informative_features(30) 

print(cl.classify("what time is it?"))
print(cl.classify("hello"))
print(cl.classify("How old are you?"))
print(cl.classify("what is your name?"))
print(cl.classify("I feel cool"))
print(cl.classify("search the time on internet"))


