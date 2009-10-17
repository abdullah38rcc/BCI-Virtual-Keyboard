import random
from operator import itemgetter

chars      = [chr(i) for i in range(ord('a'), ord('z')+1)] + [" "] 
freqinit   = 1000000000      # the initial count to be added for each bigram pair.
errorrate  = 0.2    # how often the classifer makes mistakes.
correction = 0.2    # error-correction weight (what probabilities get weighted by if )
threshold_diff = 0.2    # stop after 0.9 probability of meaning to select letter.                
limit      = 0      # if non-zero, stop after at most this many iterations and select letter

# Get bi-gram statistics from a corpus of text. I.e., Joe's dissertation.
# Returns a frequency distribution as a dict. E.g., { ('a','a'): 145,   ('a','b'): 29, ...}
def getStats(filename):

    print "Initializing frequency counts for bi-grams to '%d'" % (freqinit)
    freq = dict([((c,p), freqinit) for c in chars for p in chars])

    print "Gathering statistics on", filename
    f = open(filename)
    text = f.read().lower()
    for i in range(len(text)):
        cur  = text[i]      if           text[i]   in chars else None
        prev = text[i-1]    if i > 1 and text[i-1] in chars else None

        if cur and prev:
            freq[ (prev,cur) ] += 1

    return freq

# From frequency table (returned above) produce the probability distribution
# for every letter given that `prev` came before it. Returns a distribution
# such as {'a': 0.199, 'b': 0.052, ...}
def conditionalOn(j, prev=" "):
    return normalize( dict([(pair[1], j[pair]) for pair in j if pair[0]==prev ]) )


# --- Helper functions for distributions. ---

 
# Normalize distribution. I.e., make all the numbers sum to one.
def normalize(d):
    tot = sum([d[k] for k in d])
    return multiply(d, 1.0/tot)

# Multiply or add elements of distribtuion by a number `n`
def multiply(d, n=1):
    return dict([(k, d[k]*n) for k in d])
    
def addition(d, n=0):
    return dict([(k, d[k]+n) for k in d])

# Remove elements from the distribution whose probability is zero. (Mainly for display purposes.)
def removeZeros(d):
    return dict([(k, d[k]) for k in d if d[k] != 0.0])    

# Display a distribution, and print out a graph of the probabilities.
def prettyPrint(d):
    tot = sum([d[k] for k in d])
    keys = d.keys()
    keys.sort()
    for k in keys:
        prob = (d[k] / float(tot))
        n    = int( round(prob * 74) )
        print k.ljust(3) + "#" * n + "." * (74-n) + " %.5f" % (prob)


# --- Functions for distributing letters into "boxes" using Huffman trees ---


# Build a Huffman tree from distribution. Return root node.
# Each node is a 3-element tuple (prob, char, {children})
# where children is a dict with a "left" and "right" element.
def huffman(d):
    nodes = [ (d[k], k, {"left":None, "right":None}) for k in d ]
    while len(nodes) > 1:
        nodes.sort()
        left  = nodes.pop(0)
        right = nodes.pop(0)
        nodes.append(((left[0]+right[0]), None, {"left":left, "right":right}))
    return nodes[0]

# Return all leaves of a tree (or subtree) under a given node, t. Returned
# as a distribution (a dict) such as such as {'a': 0.199, 'b': 0.052, ...}
def leaves(t):
    if t[1]: return {t[1]: t[0]}
    else:
        dist = leaves(t[2]["left"])
        dist.update(leaves(t[2]["right"]))
        return dist



# --- Begin main interactive demo ---


joint      = getStats("hall-phd.txt")       # calculate the bi-gram statistics from scratch
probs      = conditionalOn(joint, " ")      # start w/ the probability of each letter coming after a space
string     = ""                             # the string the user is to type
samples    = 0                              # the number of iterations so far to select a letter
totsamples = 0                              # total number of iterations
errors     = 0                              # classifier errors experienced so far to select a letter
toterrors  = 0                              # total number of errors
error      = False                          # (for displaying) whether an error occured in the last selection 


# Loop until terminated (Ctrl-C)
while True:
    
    # Distribute letters into two boxes using the two sub-trees of the root of a huffman tree.
    # Also, remove elements that have no chance of being selected, and sort alphabetically.
    h = huffman( probs )
    left_keys  = removeZeros(leaves(h[2]["left"])).keys()
    right_keys = removeZeros(leaves(h[2]["right"])).keys()
    left_keys.sort()
    right_keys.sort()

    # Display the current letter probabilities, as well as the two "boxes" (i.e., choices) of letters.
    prettyPrint( probs )
    print "STRING:", string + "_"
    print "CHOICE 1:", ", ".join(left_keys)
    print "CHOICE 2:", ", ".join(right_keys)

    # Get input from user. (Display a prompt to the user and save result.)
    choice      = raw_input("[%d samples (%d tot), %d errors (%d tot)] %s? " % (samples, totsamples, errors, toterrors, ("OOPS!" if error else "")))

    # Make sure choice is either the string "1" or "2"
    if choice not in ["1", "2"]:
        print "No selection. Choose 1 or 2."
        continue

    samples    += 1
    totsamples += 1
    
    # Simulate error 20% of the time (or whatever errorrate is) by swapping choices
    error   = False
    if random.random() < errorrate:
        errors    += 1
        toterrors += 1
        error     = True
        print "CLASSIFICATION ERROR (simulated)"
        if   choice == "1": choice = "2"
        elif choice == "2": choice = "1"
    
    # Perform choice. Recalulate the probability user means to select each letter
    # by weighting all the selected letters by 80% and all the unselected letters
    # by 20% (or whatever `correction` is set to)
    if choice == "1":
        probs =      multiply(leaves(h[2]["left"]),  1-correction)
        probs.update(multiply(leaves(h[2]["right"]), correction))
        probs = normalize(probs)
    elif choice == "2":
        probs =      multiply(leaves(h[2]["left"]),  correction)
        probs.update(multiply(leaves(h[2]["right"]), 1-correction))
        probs = normalize(probs)
        
    #print "b4 limit"
    # Test whether a letter has been selected. Select and "restart" whenever
    # the probability exceeds 90% (or `threshold`) or a limit on the number
    # of iterations is reached, if specified.
    if limit:
        if samples == limit:
            max_k = (" ",-1)
            for k in probs:
                if probs[k] > max_k[1]:
                    max_k = (k, probs[k])
            string += max_k[0]
            probs   = conditionalOn(joint, max_k[0])
            samples = 0
            errors  = 0
            print "LIMIT ON ITERATIONS REACHED"
            continue
    print "after limit"
    #TEST threshold difference
    sorted_probs = sorted(probs.items(), key=itemgetter(1), reverse=True)
    tot          = sorted_probs[0][1] + sorted_probs[1][1]
    diff         = sorted_probs[0][1]/tot - sorted_probs[1][1]/tot
    print "DIFF =", diff
    if diff > threshold_diff:
        k = sorted_probs[0][0]
        string += k
        probs   = conditionalOn(joint, k)
        samples = 0
        errors  = 0
        continue