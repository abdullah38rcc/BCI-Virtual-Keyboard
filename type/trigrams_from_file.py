import sys

# USAGE
# python trigrams.py > trigrams.txt


# the symbols to include in the n-gram data (a-z plus space)
chars      = list('abcdefghijklmnopqrstuvwxyz ') 
freqinit   = 0      # the initial count to be added for each n-gram frequency.

# Get tri-gram statistics from a corpus of text. I.e., Joe's dissertation.
# Returns a frequency distribution as a dict. E.g., { ('a','a','a'): 145,   ('a','a','b'): 29, ...}
def getStats(filename):

    sys.stderr.write("Initializing frequency counts for tri-grams to '%d'\n" % (freqinit))
    freq = dict([((c0,c1,c2), freqinit) for c0 in chars for c1 in chars for c2 in chars])

    sys.stderr.write("Gathering statistics on %s\n" % filename)
    f = open(filename)
    text = f.read().lower()
    for i in range(len(text)):
        cur   = text[i]      if           text[i]   in chars else None
        prev  = text[i-1]    if i > 1 and text[i-1] in chars else None
        prev2 = text[i-2]    if i > 2 and text[i-2] in chars else None

        if cur and prev and prev2:
            freq[ (prev2,prev,cur) ] += 1

    return freq


# Read in text file with corpus data on it
trigrams = getStats("hall-phd.txt")
sys.stderr.write("Outputing trigrams...\n")

compress = True
for c0 in chars:
    for c1 in chars:
        for c2 in chars:
            f = trigrams[(c0,c1,c2)]
            if compress and f == 0:
                continue
            sys.stdout.write("%s%s%s, %d\n" % (c0.upper(),c1.upper(),c2.upper(),f))

sys.stderr.write("Done.\n")
