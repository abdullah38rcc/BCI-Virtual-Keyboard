# directed graph of bigrams using just first letter pair data
# what, why, when, where, who, how, yes, no, good, bad
# last edit: 6/9
################CHANGES############

##########TODO##############

######################BUGS#######################
# values in bigrph not stored correctly
#   -- see last line of add()
# question in nextProb
##############CURRENTLY WORKING ON##########


def add(lett1,lett2,weight):
    global bigrph
    #print weight
    #item = {weight:lett1,lett2}
    if lett1 not in bigrph:
        bigrph[lett1] = {lett2:weight}
    elif lett2 not in bigrph[lett1]:
        tmp = bigrph[lett1]
        tmp[lett2] = weight
        bigrph[lett1] = tmp
    #print lett1, ':', bigrph[lett1]

def adjacent(lett1, lett2):
    global bigrph
    return lett2 in bigrph[lett1]

def get_weight(lett1,lett2):
    global bigrph
    if adjacent(lett1,lett2):
        tmp = bigrph[lett1]
        return tmp[lett2]
    else: return 0

def buildGraph(lst):
    for item in lst:
        add(item[0],item[1],item[2])
        #map(add,item)
        #print item[0]


def nxtProb(lst):
	mx = max(lst.values())
	nxt = ''
	#why doesn't this work?
	#print lst
	#print max(lst)
	for key in lst:
		#print key
		#print lst[key]
		if lst[key] == mx:
			nxt = key
	return nxt
    
    
    
bigrph = {}
#adjLst = [[1,2,3],[4,5,6]]
#print 2 in adjLst[0]

bigrphLst = [
		['w','h',9.7],
		['h','a',2.4],
		['a','t',0.8],
		['h','e',3.0],
		['e','n',2.7],
		['e','r',0.1],
		['r','e', 11.6],
		['h','y',0.1],
		['h','o',3.4],
		['o','w',2.7],
		['y','e',0.1],
		['e','s',0.5],
		['g','o',2.3],
		['o','o',4.6],
		['o','d',1.4],
		['b','a',1.1],
		['a','d',1.4]
]

buildGraph(bigrphLst)
lett = 'a'
print bigrph[lett]
print nxtProb(bigrph[lett])
#print bigrph
