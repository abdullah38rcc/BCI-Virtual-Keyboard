import sys

chars      = [chr(i) for i in range(ord('a'), ord('z')+1)] + [" "] 
freqinit   = 1      # the initial count to be added for each bigram pair.
trigrams = dict([((c0,c1,c2), freqinit) for c0 in chars for c1 in chars for c2 in chars])

# Get tri-gram statistics from a corpus of text. I.e., Joe's dissertation.
# Returns a frequency distribution as a dict. E.g., { ('a','a'): 145,   ('a','b'): 29, ...}
def getStats(filename, freq):    
    sys.stderr.write("Gathering statistics on %s\n" % filename)
    f = open(filename)
    text = f.read().lower()
    for i in range(len(text)):
        cur   = text[i]      if           text[i]   in chars else None
        prev  = text[i-1]    if i > 1 and text[i-1] in chars else None
        prev2 = text[i-2]    if i > 2 and text[i-2] in chars else None

        if cur and prev and prev2:
            freq[ (prev2,prev,cur) ] += 1
    f.close()
    return freq


files = ['wordBgrams.txt','tb1.txt','tb2.txt']
for fname in files:
	trigrams = getStats(fname,trigrams)

sys.stderr.write("Outputing trigrams...\n")
fd = open("trigrams.txt",'w')
for c0 in chars:
    for c1 in chars:
        for c2 in chars:
            f = trigrams[(c0,c1,c2)]
            fd.write("%s%s%s, %d\n" % (c0.lower(),c1.lower(),c2.lower(),f))

sys.stderr.write("Done.\n")
fd.close()
