from locale import normalize
import re
import json
from tkinter import *
from array import *
from asyncio.windows_events import NULL
from tkinter import messagebox
from tkinter import *

# read file
wordnet_file = open("wordnet.json","r",encoding='utf-8')
wordnet_json = wordnet_file.read()
synsets_file = open("synset.json","r",encoding='utf-8')
synset_json=synsets_file.read()

# parse json data file content to json object
obj_wodnet = json.loads(wordnet_json)
obj_synset = json.loads(synset_json)

# tokenization a sentence
def tokenize():
   text_box.delete(0.0, 'end')
   sentence = txtQene.get()
   tokenized = re.sub('[\!\@\#\$\%\^\«\»\&\*\(\)\…\[\]\{\}\;\“\”\›\’\‘\"\'\:\,\.\‹\/\<\>\?\\\\|\`\´\~\-\=\+\፡\።\፤\;\፦\፥\፧\፨\፠\፣\\n]', ' ',sentence)    
   sentence_list = set(tokenized.split())   

   listToStr = ' '.join([str(elem) for elem in sentence_list])
   
   # Preprocessing section
   #text_box.insert(0.0, "\n\n Tokenization:  " + ", ".join(sentence_list))   
   sentence_normal = normalization(listToStr)
   #text_box.insert(0.0, "\n\n Normalization:  "+ sentence_normal)
   sentence_preprocessed = stopWordRemoval(sentence_normal)
   removedStr = ' '.join([str(elem) for elem in sentence_preprocessed])
   #text_box.insert(0.0, "\n Stop word removal:  "+ removedStr)
   #text_box.insert(0.0,"\n =============")  
   #text_box.insert(0.0,"\n\n Preprocessing")
   
   # Finding "Sem ena Werk"
   if len(removedStr.split()) == 1:
      messagebox.showwarning("Error", "የተሳሳተ የአማርኛ ግጥም ፤ አንድ ቃል ብቻ ነው ያስገቡት፤ እባክዎ እንደገና ይሞክሩ!")
   else:
    hKal = hibrekal(sentence_preprocessed)
   if hKal == None:
      messagebox.showwarning("Error", "ህብረቃሉን ማግኘት አልተቻለም! እባክዎ እንደገና በትክክል ይሞክሩ!")
   else:       
      text_box.insert(0.0, simplifiedLesk(hKal,sentence_preprocessed))    
        
   return 

# Identify ambigious word from a sentense i.e finds the 'hibre kal'
def hibrekal(sentence_preprocessed):
   ambigious=None
   max=0  
   wordnet_list = obj_wodnet['words']
   for st in sentence_preprocessed:   
         syn_list = wordnet_list.get(st)  
         if(syn_list!=None and len(syn_list) > max):
            max=len(syn_list)
            ambigious=st
   if max <= 1:
    return None
   return ambigious 

# counts the number of overlaps with the synset
def overlapcontext(sense, sentence):   
    list = obj_synset[sense]    
    defn = list.get('definition') 
    defn = set(defn.split(" "))
    exmpl = list.get('examples')
    exmpl = set(exmpl.split(" "))

    union_defn_exmpl=defn.union(exmpl)    

    overlap=len(union_defn_exmpl.intersection(sentence))
    return overlap

# word sense disambiguation using lesk algorithm i.e finds the 'Sem' or best sense of 'Hibre Kal'
def simplifiedLesk(hibrekal, sentence):    
    bestsense = None
    maxoverlap = 0
    overlap = 0
    
    # access the 'words' key and assign to list var 
    wordnet_list = obj_wodnet['words']
    synsets=wordnet_list.get(hibrekal)

    for sense in synsets:  
        overlap = overlapcontext(sense,sentence) 
        synset_inner_list=obj_synset[sense]
        hyponyms=synset_inner_list.get('hyponyms')        
        for h in hyponyms:
            overlap+=overlapcontext(h,sentence)
       
        if overlap > maxoverlap:
            maxoverlap = overlap
            bestsense = sense
   
    for s in synsets:
        if s!=bestsense:
           synset_inner_list=obj_synset[s]
           werksense = synset_inner_list.get('definition')
    
    sem_list = obj_synset[bestsense]
    # Here bestsense is the 'Sem' or Wax meaning extracted using lesk algorithm
    bestsense = sem_list.get('definition')

    return " ህብረቃል: " + hibrekal + "\n\n ሰም:-  " + bestsense + "\n\n ወርቅ:- "+ werksense

# normalization of amharic letters having the same effect on the meaning eg. አ and ዐ, ጸ and ፀ, ሰ and ሠ and ሀ, ሐ, and ኀ
def normalization(sentence):
        rep1=re.sub('[ጸ]','ፀ',sentence)
        rep2=re.sub('[ጹ]','ፁ',rep1)
        rep3=re.sub('[ጺ]','ፂ',rep2)
        rep4=re.sub('[ጻ]','ፃ',rep3)
        rep5=re.sub('[ጼ]','ፄ',rep4)
        rep6=re.sub('[ጽ]','ፅ',rep5)
        rep7=re.sub('[ሠ]','ሰ',rep6)
        rep8=re.sub('[ሡ]','ሱ',rep7)
        rep9=re.sub('[ሢ]','ሲ',rep8)
        rep10=re.sub('[ሣ]','ሳ',rep9)
        rep11=re.sub('[ሤ]','ሴ',rep10)
        rep12=re.sub('[ሥ]','ስ',rep11)
        rep13=re.sub('[ሦ]','ሶ',rep12)
        rep14=re.sub('[ዓኣዐ]','አ',rep13)
        rep15=re.sub('[ዑ]','ኡ',rep14)
        rep16=re.sub('[ዒ]','ኢ',rep15)
        rep17=re.sub('[ዔ]','ኤ',rep16)
        rep18=re.sub('[ዕ]','እ',rep17)
        rep19=re.sub('[ዖ]','ኦ',rep18)
        rep20=re.sub('[ሃኅኃሐሓኻ]','ሀ',rep19)
        rep21=re.sub('[ሑኁዅ]','ሁ',rep20)
        rep22=re.sub('[ኂሒኺ]','ሂ',rep21)
        rep23=re.sub('[ኌሔዄ]','ሄ',rep22)
        rep24=re.sub('[ሕኅ]','ህ',rep23)
        rep25=re.sub('[ኆሖኾ]','ሆ',rep24)
        rep26=re.sub('[ጾ]','ፆ',rep25)
        #Normalizing words with Labialized Amharic characters such as በልቱዋል or  በልቱአል to  በልቷል  
        rep27=re.sub('(ሉ[ዋአ])','ሏ',rep26)
        rep28=re.sub('(ሙ[ዋአ])','ሟ',rep27)
        rep29=re.sub('(ቱ[ዋአ])','ቷ',rep28)
        rep30=re.sub('(ሩ[ዋአ])','ሯ',rep29)
        rep31=re.sub('(ሱ[ዋአ])','ሷ',rep30)
        rep32=re.sub('(ሹ[ዋአ])','ሿ',rep31)
        rep33=re.sub('(ቁ[ዋአ])','ቋ',rep32)
        rep34=re.sub('(ቡ[ዋአ])','ቧ',rep33)
        rep35=re.sub('(ቹ[ዋአ])','ቿ',rep34)
        rep36=re.sub('(ሁ[ዋአ])','ኋ',rep35)
        rep37=re.sub('(ኑ[ዋአ])','ኗ',rep36)
        rep38=re.sub('(ኙ[ዋአ])','ኟ',rep37)
        rep39=re.sub('(ኩ[ዋአ])','ኳ',rep38)
        rep40=re.sub('(ዙ[ዋአ])','ዟ',rep39)
        rep41=re.sub('(ጉ[ዋአ])','ጓ',rep40)
        rep42=re.sub('(ደ[ዋአ])','ዷ',rep41)
        rep43=re.sub('(ጡ[ዋአ])','ጧ',rep42)
        rep44=re.sub('(ጩ[ዋአ])','ጯ',rep43)
        rep45=re.sub('(ጹ[ዋአ])','ጿ',rep44)
        rep46=re.sub('(ፉ[ዋአ])','ፏ',rep45)
        rep47=re.sub('[ቊ]','ቁ',rep46) #ቁ can be written as ቊ
        rep48=re.sub('[ኵ]','ኩ',rep47) #ኩ can be also written as ኵ  
        
        return rep48

# Amharic stop word(s) removal
def stopWordRemoval(listToStr):
    stopwords = ['ነው','እና','ያኛው','ይሄ','ነገርግን', 'ወይም', 'ውስጥ','ላይ', 'እስከ','እንደ']
    list=set(listToStr.split(" "))
    removedList=list.difference(stopwords)  

    return removedList

# Finding the amharic stem word for each word in qene and synset
def stem(input1):
	
	# RULE 1 - Take input as it is
	print(input1)
	collection = [input1]

	# RULE 2 - Take out the right most suffix - From input 1
	input2 = re.match("(.+)(እዉ|ዉ|ው|ኣዊ|ና|ም|ማ|ል|ነ|ኣቸ)",input1)
	if input2:
		print(input2.group(1)+'-'+input2.group(2)) 
		input2 = input2.group(1); 
		collection.append(input2)
	else:
		input2 = input1

	# RULE 3 - Take out the inner most suffix
	input3 = re.match('(.+)(ኦች|ባቸ|ዋቸ)',input2)	
	input3 = re.match('(.+)(ች|ኩ|ክ|ኣቸ|ዋል)',input2) if not input3 else input3
	if input3:
		print(input3.group(1)+'-'+input3.group(2))
		input3 = input3.group(1)
		collection.append(input3)
	else:
		input3 = input2	
	
	# RULE 4 - Take out the most left prefix - From input 1
	input4 = re.match('(የተ|እንደ|እንዲ|አል)(.+)',input1)
	input4 = re.match('(የ|ይ|ማስ|ለ|ከ|እንድ|በ|ስለ)(.+)',input1) if not input4 else input4
	if input4:
		print(input4.group(1)+'-'+input4.group(2))
		input4 = input4.group(2)
		collection.append(input4)
	else:
		input4 = input1	
	
	# RULE 5 - Take out the right most suffix - From input 4
	input5 = re.match('(.+)(እዉ|ዉ|ው|ኣዊ|ና|ም|ማ|ል|ነ|ቸ)',input4)
	if input5: 
		print(input5.group(1)+'-'+input5.group(2))
		input5 = input5.group(1)
		collection.append(input5)
	else:
		input5 = input4

	# RULE 6 - Take out the inner most suffix - From input 4
	input6 = re.match('(.+)(ኦች|ባቸ|ዋቸ)',input5)	
	input6 = re.match('(.+)(ች|ኩ|ክ|ቸ|ዋል)',input5) if not input6 else input6
	if input6:
		print(input6.group(1)+'-'+input6.group(2))
		input6 = input6.group(1)
		collection.append(input6)
	else:
		input6 = input5
	
	# RULE 7 - Take out the inner most prefix - From input 1
	input7 = re.match('(ተ|ሚ|ም|መ|ማይት|ማ|ባለ|ይት)(.+)',input4)
	if input7:
		print(input7.group(1)+'-'+input7.group(2))
		input7 = input7.group(2)
		collection.append(input7)
	else:
		input7 = input4

	# RULE 8 - Take out the right most suffix - From input 7
	input8 = re.match('(.+)(እዉ|ዉ|ው|ኣዊ|ና|ም|ማ|ል|ነ)',input7)	                        
	if input8: 
		print(input8.group(1)+'-'+input8.group(2)); 
		input8 = input8.group(1)
		collection.append(input8)
	else: 
		input8 = input4
	

	# RULE 9 - Take out the innermost suffix - From input 8
	input9 = re.match('(.+)([^እኢኣኧኦኡ])’?',input8)
	if input9:
		print(input9.group(1)+'-'+input9.group(2)); 
		input9 = input9.group(1)
		collection.append(input9)
	else:
		input9 = input4

    # RULE 9 - Take out the innermost suffix - From input 8
	input9 = re.match('(.+)([^እኢኣኧኦኡ])’?',input8)
	if input9:
		print(input9.group(1)+'-'+input9.group(2)); 
		input9 = input9.group(1)
		collection.append(input9)
	else:
		input9 = input4
    
	return collection

wordnet_file.close()
synsets_file.close()

window=Tk()

# add widgets here
window.title('የአማርኛ ቅኔ ሰምና ወርቅ መፍቻ')
window.geometry ("700x450+10+20")
window.configure (bg='azure3')

# Label widgets
lblQene=Label(window, text="ስንኝዎን ያስገቡ:-\n\n\n",  fg='#14365D', bg='#C1CDCD', font=("Arial", 12))
lblQene.pack(side=LEFT)
lblQene.place(x=15, y=70)
# Entry widgets
txtQene=Entry(window, bd= 3, text="", width=50, font=('Arial 12'))
#txtQene.pack(side=RIGHT)
txtQene.place(x=15, y=100)

# Clear the entry field
def clear():
   txtQene.delete(0, END)

# Button widgets
print (" ")
btnQene=Button(window, text="ፍቺውን ይመልከቱ", fg='#14365D', bg='#C1CDCD', font='12', command=tokenize)
btnQene.place(x=15, y=130)
btnClear=Button(window, text="እንደገና ይሞክሩ", fg='#14365D', bg='#C1CDCD', font='12', command=clear)
btnClear.place(x=160, y=130)

frame = Frame(window)
text_box = Text(frame, bd=5, height=7, width=75, wrap=WORD, bg='#F5F5DC')
text_box.pack(side=RIGHT,expand=True)
sb = Scrollbar(frame)
sb.pack(side=BOTTOM, fill=BOTH)
text_box.config(yscrollcommand=sb.set)
sb.config(command=text_box.yview)
frame.pack(expand=TRUE)
frame.place(x=15, y=180)
window.mainloop()
