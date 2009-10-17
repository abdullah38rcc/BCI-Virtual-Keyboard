# partition.py -- by leonardo maffi, V. 2.3, April 4 2005.

try: # Import Psyco if available.
    import psyco
except ImportError:
    _psy = False
else:
    _psy = True


if _psy:
    def _fromStartFun(seq, n, lseq):
        #Faster for lseq very big, but not the faster for smaller lseq
        result = []
        for i in xrange(0, lseq, n):
            result.append(seq[i:i+n])
        return result

    def _fromEndFun(seq, n, lseq, lseqmodn):
        #Faster for lseq very big, but not the faster for smaller lseq
        result = []
        for i in xrange(lseqmodn, lseq, n):
            result.append(seq[i:i+n])
        return result

    psyco.bind(_fromStartFun)
    psyco.bind(_fromEndFun)
else:
    def _fromStartFun(seq, n, lseq):
        return list(seq[i:i+n] for i in xrange(0, lseq, n))

    def _fromEndFun(seq, n, lseq, lseqmodn):
        return list(seq[i:i+n] for i in xrange(lseqmodn, lseq, n))



_missing = object()

def partition(seq, n=2, fromstart=True, filler=_missing):
    """partition(seq, n=2, fromstart=True, filler=_missing): iterable. It divides seq in
    parts with len n. Works on lists, tuples, and strings/unicodes.
    With fromstart=False the aligment starts from the end of the sequence.
    If len(seq)%n!=0 fills the final group with filler (if filler is present).
    For a string gives a list of strings. For a list or tuple gives a list of tuple. Ex:
      r6 = range(1,7)
      r7 = range(1,8)
      partition(r6, 1) == [[1], [2], [3], [4], [5], [6]]
      partition([]) == []
      partition([1,], 1) == [[1]]
      partition(r7) == [[1, 2], [3, 4], [5, 6], [7]]
      partition(r7, 2, fromstart=False) == [[1], [2, 3], [4, 5], [6, 7]]
      partition(r7, 2, fromstart=False, filler=0) == [[0, 1], [2, 3], [4, 5], [6, 7]]
      r6 = tuple(r6)
      partition(r6, 7, filler=0) == ((1, 2, 3, 4, 5, 6, 0),)
      r6 = "123456"
      partition(r6, 0.9, fromstart=False) == ["1", "2", "3", "4", "5", "6"]
      partition(r6, 0.4, fromstart=False) == "123456"
    """
    if not isinstance(seq, (list, str, unicode, tuple)):
        raise TypeError, "in partition: seq isn't a list, str, unicode or tuple."
    if not isinstance(n, (int, long, float)):
        raise TypeError, "in partition: n isn't a int, long or float."
    if not isinstance(fromstart, bool):
        raise TypeError, "in partition: fromstart isn't a bool."
    if isinstance(seq, list):
        tyseq = 1
    elif isinstance(seq, tuple):
        tyseq = 2
    else:
        tyseq = 3
    if tyseq==3:
        assert filler is _missing or isinstance(filler, (str, unicode)), \
        "in xpartion: if seq is a str/unicode, then filler must be a str/unicode too (or nothing)."
    lseq = len(seq)
    n = int(round(n))
    if lseq==0 or n<1:
        return seq
    elif lseq == n or (lseq <= n and filler is _missing):
        if tyseq==2:
            return (seq,)
        else:
            return [seq]
    elif tyseq==3 and n == 1:
        return list(seq)
    else:
        lseqmodn = lseq % n
        restbool = bool(lseqmodn)
        fillbool = restbool and not (filler is _missing)

        if fillbool:
            if tyseq==1:
                fill = [filler] * (n-lseqmodn)
            elif tyseq==2:
                fill = (filler,) * (n-lseqmodn)
            else:
                fill = filler * (n-lseqmodn)

        if fromstart:
            result = _fromStartFun(seq, n, lseq)
            if fillbool:
                result[-1] += fill
        else:
            result = _fromEndFun(seq, n, lseq, lseqmodn)
            if restbool:
                rest = seq[:lseqmodn]
                if fillbool:
                    rest = fill + rest
                result = [rest] + result

        if tyseq==2: result = tuple(result)
        return result


__all__ = ["partition"]


if __name__ == '__main__': # Test -------------------------------
    from time import clock
    n = 5*10**5 # ************

    print "partition test:"
    print "partition asserts... "
    part = partition

    print "Asserts: list, no filler, from start:"
    r6 = range(1,7) # [1,2,3,4,5,6]
    r7 = range(1,8) # [1,2,3,4,5,6,7]
    assert part(r6, 1) == [[1], [2], [3], [4], [5], [6]]
    assert part(r6, 2) == [[1, 2], [3, 4], [5, 6]]
    assert part(r6, 3) == [[1, 2, 3], [4, 5, 6]]
    assert part(r6, 4) == [[1, 2, 3, 4], [5, 6]]
    assert part(r7, 2) == [[1, 2], [3, 4], [5, 6], [7]]
    assert part(r6, 1.6) == [[1, 2], [3, 4], [5, 6]]
    assert part(r6, 1.1) == [[1], [2], [3], [4], [5], [6]]
    assert part(r6, 0.9) == [[1], [2], [3], [4], [5], [6]]
    assert part(r6, 0.4) == [1, 2, 3, 4, 5, 6]
    assert part([], 0.4) == []
    assert part(r6, 7) == [[1, 2, 3, 4, 5, 6]]
    assert part(r6, 6) == [r6]
    assert part([1,], 1) == [[1]]
    assert part([1,], 3) == [[1]]
    assert part([], 2) == []

    print "Asserts: list, no filler, from end:"
    assert part(r6, 1, False) == [[1], [2], [3], [4], [5], [6]]
    assert part(r6, 2, False) == [[1, 2], [3, 4], [5, 6]]
    assert part(r6, 3, False) == [[1, 2, 3], [4, 5, 6]]
    assert part(r6, 4, False) == [[1, 2], [3, 4, 5, 6]]
    assert part(r7, 2, False) == [[1], [2, 3], [4, 5], [6, 7]]
    assert part(r6, 1.6, False) == [[1, 2], [3, 4], [5, 6]]
    assert part(r6, 1.1, False) == [[1], [2], [3], [4], [5], [6]]
    assert part(r6, 0.9, False) == [[1], [2], [3], [4], [5], [6]]
    assert part(r6, 0.4, False) == [1, 2, 3, 4, 5, 6]
    assert part([], 0.4, False) == []
    assert part(r6, 7, False) == [[1, 2, 3, 4, 5, 6]]
    assert part(r6, 6, False) == [r6]
    assert part([1,], 1, False) == [[1]]
    assert part([1,], 3, False) == [[1]]
    assert part([], 2, False) == []

    print "Asserts: list, with filler, from start:"
    assert part(r6, 1, filler=0) == [[1], [2], [3], [4], [5], [6]]
    assert part(r6, 2, filler=0) == [[1, 2], [3, 4], [5, 6]]
    assert part(r6, 3, filler=0) == [[1, 2, 3], [4, 5, 6]]
    assert part(r6, 4, filler=0) == [[1, 2, 3, 4], [5, 6, 0, 0]]
    assert part(r7, 2, filler=0) == [[1, 2], [3, 4], [5, 6], [7, 0]]
    assert part(r6, 1.6, filler=0) == [[1, 2], [3, 4], [5, 6]]
    assert part(r6, 1.1, filler=0) == [[1], [2], [3], [4], [5], [6]]
    assert part(r6, 0.9, filler=0) == [[1], [2], [3], [4], [5], [6]]
    assert part(r6, 0.4, filler=0) == [1, 2, 3, 4, 5, 6]
    assert part([], 0.4, filler=0) == []
    assert part(r6, 7, filler=0) == [[1, 2, 3, 4, 5, 6, 0]]
    assert part(r6, 6, filler=0) == [r6]
    assert part([1,], 1, filler=0) == [[1]]
    assert part([1,], 3, filler=0) == [[1,0,0]]
    assert part([], 2, filler=0) == []

    print "Asserts: list, with filler, from end:"
    assert part(r6, 1, False, filler=0) == [[1], [2], [3], [4], [5], [6]]
    assert part(r6, 2, False, filler=0) == [[1, 2], [3, 4], [5, 6]]
    assert part(r6, 3, False, filler=0) == [[1, 2, 3], [4, 5, 6]]
    assert part(r6, 4, False, filler=0) == [[0, 0, 1, 2], [3, 4, 5, 6]]
    assert part(r7, 2, False, filler=0) == [[0, 1], [2, 3], [4, 5], [6, 7]]
    assert part(r6, 1.6, False, filler=0) == [[1, 2], [3, 4], [5, 6]]
    assert part(r6, 1.1, False, filler=0) == [[1], [2], [3], [4], [5], [6]]
    assert part(r6, 0.9, False, filler=0) == [[1], [2], [3], [4], [5], [6]]
    assert part(r6, 0.4, False, filler=0) == [1, 2, 3, 4, 5, 6]
    assert part([], 0.4, False, filler=0) == []
    assert part(r6, 7, False, filler=0) == [[0, 1, 2, 3, 4, 5, 6]]
    assert part(r6, 6, False, filler=0) == [r6]
    assert part([1,], 1, False, filler=0) == [[1]]
    assert part([1,], 3, False, filler=0) == [[0,0,1]]
    assert part([], 2, False, filler=0) == []

    # **************************************

    print "Asserts: tuple, no filler, from start:"
    r6 = tuple(range(1,7)) # (1,2,3,4,5,6)
    r7 = tuple(range(1,8)) # (1,2,3,4,5,6,7)
    assert part(r6, 1) == ((1,), (2,), (3,), (4,), (5,), (6,))
    assert part(r6, 2) == ((1, 2), (3, 4), (5, 6))
    assert part(r6, 3) == ((1, 2, 3), (4, 5, 6))
    assert part(r6, 4) == ((1, 2, 3, 4), (5, 6))
    assert part(r7, 2) == ((1, 2), (3, 4), (5, 6), (7,))
    assert part(r6, 1.6) == ((1, 2), (3, 4), (5, 6))
    assert part(r6, 1.1) == ((1,), (2,), (3,), (4,), (5,), (6,))
    assert part(r6, 0.9) == ((1,), (2,), (3,), (4,), (5,), (6,))
    assert part(r6, 0.4) == (1, 2, 3, 4, 5, 6)
    assert part((), 0.4) == ()
    assert part(r6, 7) == ((1, 2, 3, 4, 5, 6),)
    assert part(r6, 6) == (r6,)
    assert part((1,), 1) == ((1,),)
    assert part((1,), 3) == ((1,),)
    assert part((), 2) == ()

    print "Asserts: tuple, no filler, from end:"
    assert part(r6, 1, False) == ((1,), (2,), (3,), (4,), (5,), (6,))
    assert part(r6, 2, False) == ((1, 2), (3, 4), (5, 6))
    assert part(r6, 3, False) == ((1, 2, 3), (4, 5, 6))
    assert part(r6, 4, False) == ((1, 2), (3, 4, 5, 6))
    assert part(r7, 2, False) == ((1,), (2, 3), (4, 5), (6, 7))
    assert part(r6, 1.6, False) == ((1, 2), (3, 4), (5, 6))
    assert part(r6, 1.1, False) == ((1,), (2,), (3,), (4,), (5,), (6,))
    assert part(r6, 0.9, False) == ((1,), (2,), (3,), (4,), (5,), (6,))
    assert part(r6, 0.4, False) == (1, 2, 3, 4, 5, 6)
    assert part((), 0.4, False) == ()
    assert part(r6, 7, False) == ((1, 2, 3, 4, 5, 6),)
    assert part(r6, 6, False) == (r6,)
    assert part((1,), 1, False) == ((1,),)
    assert part((1,), 3, False) == ((1,),)
    assert part((), 2, False) == ()

    print "Asserts: tuple, with filler, from start:"
    assert part(r6, 1, filler=0) == ((1,), (2,), (3,), (4,), (5,), (6,))
    assert part(r6, 2, filler=0) == ((1, 2), (3, 4), (5, 6))
    assert part(r6, 3, filler=0) == ((1, 2, 3), (4, 5, 6))
    assert part(r6, 4, filler=0) == ((1, 2, 3, 4), (5, 6, 0, 0))
    assert part(r7, 2, filler=0) == ((1, 2), (3, 4), (5, 6), (7, 0))
    assert part(r6, 1.6, filler=0) == ((1, 2), (3, 4), (5, 6))
    assert part(r6, 1.1, filler=0) == ((1,), (2,), (3,), (4,), (5,), (6,))
    assert part(r6, 0.9, filler=0) == ((1,), (2,), (3,), (4,), (5,), (6,))
    assert part(r6, 0.4, filler=0) == (1, 2, 3, 4, 5, 6)
    assert part((), 0.4, filler=0) == ()
    assert part(r6, 7, filler=0) == ((1, 2, 3, 4, 5, 6, 0),)
    assert part(r6, 6, filler=0) == (r6,)
    assert part((1,), 1, filler=0) == ((1,),)
    assert part((1,), 3, filler=0) == ((1,0,0),)
    assert part((), 2, filler=0) == ()

    print "Asserts: tuple, with filler, from end:"
    assert part(r6, 1, False, filler=0) == ((1,), (2,), (3,), (4,), (5,), (6,))
    assert part(r6, 2, False, filler=0) == ((1, 2), (3, 4), (5, 6))
    assert part(r6, 3, False, filler=0) == ((1, 2, 3), (4, 5, 6))
    assert part(r6, 4, False, filler=0) == ((0, 0, 1, 2), (3, 4, 5, 6))
    assert part(r7, 2, False, filler=0) == ((0, 1), (2, 3), (4, 5), (6, 7))
    assert part(r6, 1.6, False, filler=0) == ((1, 2), (3, 4), (5, 6))
    assert part(r6, 1.1, False, filler=0) == ((1,), (2,), (3,), (4,), (5,), (6,))
    assert part(r6, 0.9, False, filler=0) == ((1,), (2,), (3,), (4,), (5,), (6,))
    assert part(r6, 0.4, False, filler=0) == (1, 2, 3, 4, 5, 6)
    assert part((), 0.4, False, filler=0) == ()
    assert part(r6, 7, False, filler=0) == ((0, 1, 2, 3, 4, 5, 6),)
    assert part(r6, 6, False, filler=0) == (r6,)
    assert part((1,), 1, False, filler=0) == ((1,),)
    assert part((1,), 3, False, filler=0) == ((0,0,1),)
    assert part((), 2, False, filler=0) == ()

    # ******************

    print "Asserts: str, no filler, from start:"
    r6 = "123456"
    r7 = "1234567"
    assert part(r6, 1) == ["1", "2", "3", "4", "5", "6"]
    assert part(r6, 2) == ["12", "34", "56"]
    assert part(r6, 3) == ["123", "456"]
    assert part(r6, 4) == ["1234", "56"]
    assert part(r7, 2) == ["12", "34", "56", "7"]
    assert part(r6, 1.6) == ["12", "34", "56"]
    assert part(r6, 1.1) == ["1", "2", "3", "4", "5", "6"]
    assert part(r6, 0.9) == ["1", "2", "3", "4", "5", "6"]
    assert part(r6, 0.4) == "123456"
    assert part("", 0.4) == ""
    assert part(r6, 7) == [r6]
    assert part(r6, 6) == [r6]
    assert part("1", 1) == ["1"]
    assert part("1", 3) == ["1"]
    assert part("", 2) == ""

    print "Asserts: str, no filler, from end:"
    assert part(r6, 1, False) == ["1", "2", "3", "4", "5", "6"]
    assert part(r6, 2, False) == ["12", "34", "56"]
    assert part(r6, 3, False) == ["123", "456"]
    assert part(r6, 4, False) == ["12", "3456"]
    assert part(r7, 2, False) == ["1", "23", "45", "67"]
    assert part(r6, 1.6, False) == ["12", "34", "56"]
    assert part(r6, 1.1, False) == ["1", "2", "3", "4", "5", "6"]
    assert part(r6, 0.9, False) == ["1", "2", "3", "4", "5", "6"]
    assert part(r6, 0.4, False) == "123456"
    assert part("", 0.4, False) == ""
    assert part(r6, 7, False) == [r6]
    assert part(r6, 6, False) == [r6]
    assert part("1", 1, False) == ["1"]
    assert part("1", 3, False) == ["1"]
    assert part("", 2, False) == ""

    print "Asserts: str, with filler, from start:"
    assert part(r6, 1, filler="0") == ["1", "2", "3", "4", "5", "6"]
    assert part(r6, 2, filler="0") == ["12", "34", "56"]
    assert part(r6, 3, filler="0") == ["123", "456"]
    assert part(r6, 4, filler="0") == ["1234", "5600"]
    assert part(r7, 2, filler="0") == ["12", "34", "56", "70"]
    assert part(r6, 1.6, filler="0") == ["12", "34", "56"]
    assert part(r6, 1.1, filler="0") == ["1", "2", "3", "4", "5", "6"]
    assert part(r6, 0.9, filler="0") == ["1", "2", "3", "4", "5", "6"]
    assert part(r6, 0.4, filler="0") == "123456"
    assert part("", 0.4, filler="0") == ""
    assert part(r6, 7, filler="0") == ["1234560"]
    assert part(r6, 6, filler="0") == [r6]
    assert part("1", 1, filler="0") == ["1"]
    assert part("1", 3, filler="0") == ["100"]
    assert part("", 2, filler="0") == ""

    print "Asserts: str, with filler, from end:"
    assert part(r6, 1, False, filler="0") == ["1", "2", "3", "4", "5", "6"]
    assert part(r6, 2, False, filler="0") == ["12", "34", "56"]
    assert part(r6, 3, False, filler="0") == ["123", "456"]
    assert part(r6, 4, False, filler="0") == ["0012", "3456"]
    assert part(r7, 2, False, filler="0") == ["01", "23", "45", "67"]
    assert part(r6, 1.6, False, filler="0") == ["12", "34", "56"]
    assert part(r6, 1.1, False, filler="0") == ["1", "2", "3", "4", "5", "6"]
    assert part(r6, 0.9, False, filler="0") == ["1", "2", "3", "4", "5", "6"]
    assert part(r6, 0.4, False, filler="0") == "123456"
    assert part("", 0.4, False, filler="0") == ""
    assert part(r6, 7, False, filler="0") == ["0123456"]
    assert part(r6, 6, False, filler="0") == [r6]
    assert part("1", 1, False, filler="0") == ["1"]
    assert part("1", 3, False, filler="0") == ["001"]
    assert part("", 2, False, filler="0") == ""

    print "passed."
    print

    print "Some partition timings with n=", n
    s = tuple(range(n))
    t1 = clock()
    partition(s, 2)
    t2 = clock()
    print "1) Time tuple=", round(t2-t1, 3), "s."

    s = range(n) # list
    t1 = clock()
    partition(s, 2)
    t2 = clock()
    print "2) Time list=", round(t2-t1, 3), "s."

    s = "a" * n # string
    t1 = clock()
    partition(s, 2)
    t2 = clock()
    print "3) Time string=", round(t2-t1, 3), "s."
    """
    Some partition timings with n= 500000
    1) Time tuple= 2.474 s.
    2) Time list= 3.573 s.
    3) Time string= 0.331 s.

    1) Time tuple= 2.474 s.
    2) Time list= 3.542 s.
    3) Time string= 0.341 s.
    """