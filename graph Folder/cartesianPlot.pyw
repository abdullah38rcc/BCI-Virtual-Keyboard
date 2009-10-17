"""
cartesianPlot.py - V.1.6, April 24 2005.
Plot black lines, blue arrows, and red dots on the cartesian plane in a Tk window.

Original version from Anton Vredegoor <anton@vredegoor.doge.nl>
http://home.hccnet.nl/a.vredegoor/cartesian/cartesian.py
Much modified by leonardo maffi.
"""

from Tkinter import Tk, Canvas, BOTH, YES
# from util import frange # It's copied below


def frange(start, end=None, inc=None): # From util module!
    "A range function that accepts noninteger increments."
    # From Cookbook 66472 by Dinu Gherman.
    # (Another function that creates 2D, 3D... arrays, can be created too.)
    from math import ceil
    if inc == None: inc = 1.0
    if end == None:
        end = start + 0.0
        start = 0.0
    else: start += 0.0 # force it to be a float
    count = int( ceil((end-start)/inc) )
    L = [None,] * count
    for i in xrange(count):
        L[i] = start + i * inc
    return L


class Transformer:
    "Convert from worldcoordinates into viewportcoordinates."
    __slot__ = ["mx", "my", "c1", "c2"]

    def __init__(self, world, viewport):
        x_min, y_min, x_max, y_max = map(float, world)
        X_min, Y_min, X_max, Y_max = map(float, viewport)
        f_x = (X_max-X_min) / (x_max-x_min)
        f_y = (Y_max-Y_min) / (y_max-y_min)
        self.mx = min(f_x, f_y)
        self.my = -self.mx
        x_c = (x_min+x_max) / 2
        y_c = (y_min+y_max) / 2
        X_c = (X_min+X_max) / 2
        Y_c = (Y_min+Y_max) / 2
        self.c1 = X_c - self.mx*x_c
        self.c2 = Y_c - self.my*y_c

    def onepoint(self, x1, y1):
        # For one point
        return self.mx*x1 + self.c1, self.my*y1 + self.c2

    def twopoints(self, x1, y1, x2, y2):
        # For two points
        sc1 = self.c1
        sc2 = self.c2
        smx = self.mx
        smy = self.my
        return x1*smx+sc1, y1*smy+sc2, x2*smx+sc1, y2*smy+sc2



def cartesianPlot(window_title="Cartesian plot", points=None, lines=None, arrows=None, loops=None,
                  pointW=None, lineW=None, arrowW=None, loopW=None,
                  pointColors=None, lineColors=None, arrowColors=None, loopColors=None,
                  pointLabels=None, plot_range=None, grid_spacing=None, axes=False):
    """cartesianPlot(window_title="Cartesian plot", points=None, lines=None, arrows=None, loops=None,
                  pointW=None, lineW=None, arrowW=None, loopW=None,
                  pointColors=None, lineColors=None, arrowColors=None, loopColors=None,
                  pointLabels=None, plot_range=None, grid_spacing=None, axes=False):
    Plot black lines, blue arrows, red dots, and green self-loops on the cartesian plane with Tkinter.
      windowtitle must be a string or unicode. absent ==> "Cartesian plot"
      points must be a list of pairs of coordinates.
      arrows must be a list of pairs of one pair of coordinates.
      lines must be a list of pairs of one pair of coordinates.
      loops is a list of points (pairs of coordinates) that have a self loop (useful for graphs).
      pointW,lineW,arrowW,loopW are lists of widths of the points/lines, as a float in [0,20],
        their lenght is the same of the lists they refer to.
      pointColors,lineColors,arrowColors,loopColors are lists of RGB triads, their lenghts are
        the same of the lists they refer to, each color component is a float in [0,1].
      pointLabels is an optional sequence of labels (any object that can be converted in a string)
        to be shown near the points. Its lenght is the same as points sequence.
      plot_range must be a sequence of 4 coordinates (minx, miny, maxx, maxy). None ==> full auto.
      grid_spacing must be a number. None ==> no grid.
      If axes=True it shows axes too.
      Grid and axes are plotted first, then lines, and points are plotted last."""

    def colorConvert(rgb):
        """colorConvert(r,g,b): convert a RGB tuple containing real numbers in [0,1], in a hex
        color for tkinter in the form: #rrggbb"""
        r,g,b = rgb
        return "#%02x%02x%02x" % ( min(max(0, r*255), 255), min(max(0, g*255), 255),
                                   min(max(0, b*255), 255))


    def wfilter(w):
        "wfilter(w): filter the width."
        return min(max(1, float(w)), 20)


    def compute_plot_range(points, lines, arrows):
        minx = miny = 1e30
        maxx = maxy = -1e30
        if points:
            for x,y in points:
                maxx = max(maxx, x)
                maxy = max(maxy, y)
                minx = min(minx, x)
                miny = min(miny, y)
        if loops:
            for x,y in loops:
                maxx = max(maxx, x)
                maxy = max(maxy, y)
                minx = min(minx, x)
                miny = min(miny, y)
        if arrows:
            for (x1,y1),(x2,y2) in arrows:
                maxx = max(maxx, x1, x2)
                maxy = max(maxy, y1, y2)
                minx = min(minx, x1, x2)
                miny = min(miny, y1, y2)
        if lines:
            for (x1,y1),(x2,y2) in lines:
                maxx = max(maxx, x1, x2)
                maxy = max(maxy, y1, y2)
                minx = min(minx, x1, x2)
                miny = min(miny, y1, y2)
        if (maxx-minx) < 1e-15:
            maxx += 1
            minx -= 1
        if (maxy-miny) < 1e-15:
            maxy += 1
            miny -= 1
        marginx = (maxx-minx)*0.03
        maxx += marginx
        minx -= marginx
        marginy = (maxy-miny)*0.03
        maxy += marginy
        miny -= marginy
        return minx, miny, maxx, maxy


    def configure(event):
        global GT
        canvas.delete('all')
        width = float(canvas.winfo_width())
        height = float(canvas.winfo_height())
        viewport = (pad, pad, width-pad, height-pad)
        GT = Transformer(plot_range, viewport)
        drawbackground()
        if grid_spacing: drawgrid()
        if axes: drawaxes()
        if arrows: drawarrows()
        if lines: drawlines()
        if loops: drawloops()
        if points: drawpoints()


    def drawbackground():
        canvas.create_rectangle(GT.twopoints(*plot_range), fill='white', outline='')


    def drawgrid():
        minx, miny, maxx, maxy = plot_range
        gtt = GT.twopoints
        sccl = canvas.create_line
        for x in frange(0, maxx, grid_spacing):
            sccl(gtt(x, miny, x, maxy), fill='grey90', tag='all')
        for x in frange(0, minx, -grid_spacing):
            sccl(gtt(x, miny, x, maxy), fill='grey90', tag='all')
        for y in frange(0, maxy, grid_spacing):
            sccl(gtt(minx, y, maxx, y), fill='grey90', tag='all')
        for y in frange(0, miny, -grid_spacing):
            sccl(gtt(minx, y, maxx, y), fill='grey90', tag='all')


    def drawaxes():
        minx, miny, maxx, maxy = plot_range
        gtt = GT.twopoints
        sccl = canvas.create_line
        sccl(gtt(0, miny, 0, maxy), fill='grey84', width=2, tag='all')
        sccl(gtt(minx, 0, maxx, 0), fill='grey84', width=2, tag='all')


    def drawpoints():
        ps = 2
        color = 'red'
        cco = canvas.create_oval
        gto = GT.onepoint
        if pointLabels:
            cct = canvas.create_text
            len_pointLabels = len(pointLabels)
            for i,(x,y) in enumerate(points):
                x1,y1 = gto(x, y)
                if pointW: ps = pointW[i]
                if pointColors: color = pointColors[i]
                cco(x1-ps, y1-ps, x1+ps, y1+ps, outline='white', fill=color)
                if i < len_pointLabels: # Show point label
                    label = str(pointLabels[i])
                    if len(label) > 22: # if label is too much long:
                        label = label[:14] + "..." + label[-3:] # Shorten label
                    cct(x1+9,y1-6, font="Courier 6", text=label, fill="magenta4")
        else:
            for i,(x,y) in enumerate(points):
                x1,y1 = gto(x, y)
                if pointW: ps = pointW[i]
                if pointColors: color = pointColors[i]
                cco(x1-ps, y1-ps, x1+ps, y1+ps, outline='white', fill=color)


    def drawarrows():
        color = 'blue'
        w = 1
        gtt = GT.twopoints
        ccl = canvas.create_line
        arrshape = (10, 10, 2)
        for i,((x1,y1),(x2,y2)) in enumerate(arrows):
            if arrowW: w = arrowW[i]
            if arrowColors: color = arrowColors[i]
            ccl(gtt(x1, y1, x2, y2), arrow="last", width=w, arrowshape=arrshape, fill=color)


    def drawlines():
        color = 'black'
        w = 1
        gtt = GT.twopoints
        ccl = canvas.create_line
        for i,((x1,y1),(x2,y2)) in enumerate(lines):
            if lineW: w = lineW[i]
            if lineColors: color = lineColors[i]
            ccl(gtt(x1, y1, x2, y2), width=w, fill=color)


    def drawloops():
        color = 'green4'
        w = 1
        gto = GT.onepoint
        ps = 2
        ps2 = 4 + 0.011 * min(canvas.winfo_width(), canvas.winfo_height())
        ps3 = ps2*2
        cco = canvas.create_oval
        ccl = canvas.create_line
        arrshape = (10, 10, 2)
        for i,(x,y) in enumerate(loops):
            if loopW: w = loopW[i]
            if loopColors: color = loopColors[i]
            x1,y1 = gto(x, y)
            cco(x1-ps2, y1-ps3, x1+ps2, y1, outline=color, fill='', width=w)
            ccl(x1+ps, y1, x1, y1+ps, arrow="last", arrowshape=arrshape, fill=color, width=w)
            #cco(x1-ps, y1-ps, x1+ps, y1+ps, outline='white', fill='red')


    master = Tk()
    master.title( str(window_title) )
    WIDTH = HEIGHT = 500
    pad = 3
    if points == []: points = None
    if pointLabels == []: pointLabels = None
    if lines == []: lines = None
    if arrows == []: arrows = None
    if pointW == []: pointW = None
    if pointW: pointW = map(wfilter, pointW)
    if lineW == []: lineW = None
    if lineW: lineW = map(wfilter, lineW)
    if arrowW == []: arrowW = None
    if arrowW: arrowW= map(wfilter, arrowW)
    if loopW == []: loopW = None
    if loopW: loopW = map(wfilter, loopW)

    if pointColors == []: pointColors = None
    if pointColors: pointColors = map(colorConvert, pointColors)
    if lineColors == []: lineColors = None
    if lineColors: lineColors = map(colorConvert, lineColors)
    if arrowColors == []: arrowColors = None
    if arrowColors: arrowColors = map(colorConvert, arrowColors)
    if loopColors == []: loopColors = None
    if loopColors: loopColors = map(colorConvert, loopColors)
    if not plot_range:
        plot_range = compute_plot_range(points, lines, arrows)
    canvas = Canvas(master, width=WIDTH, height=HEIGHT, bg='grey')
    canvas.pack(fill=BOTH, expand=YES)
    viewport = (pad, pad, WIDTH-pad, HEIGHT-pad)
    master.bind("<Escape>", lambda event='ignored': master.destroy())
    master.bind("<Configure>", configure)
    master.mainloop()


__all__ = ["cartesianPlot"] # Export this name only.


if __name__=='__main__': # Demo -----------------------------------
    if 0:
        wt = "Graph1" # absent ==> "Cartesian plot"
        pr = (-10,-10,10,10) # absent ==> auto
        gs = 1 # absent ==> no grid and axes.
        p = (a,b,c,d,e) = (-3,2),(6,8),(4,4),(-5,-2),(6,3)
        ar = [(a,b),(c,d)]
        f,g = (-3.5,7.5), (5.5,-5.5)
        l = [(f,g),(g,e)]
        lo = [(3,3)]
        cartesianPlot(window_title=wt, points=p, lines=l, arrows=ar, loops= lo, plot_range=pr,
                      grid_spacing=gs, axes=True)

    if 0:
        wt = "Random"
        from random import random
        xn = xrange(100)
        l = [ ( (random(),random()), (random(),random()) ) for i in xn ]
        p = [ (random(),random()) for i in xn ]
        lo = [ (random(),random()) for i in xn ]
        low = [random()*7 for i in xrange(len(lo))]
        loc = [(random(),random(),random()) for i in xrange(len(lo))]
        cartesianPlot(window_title=wt, points=p, lines=l, loops=lo, loopW=low, loopColors=loc,
                      grid_spacing=0.05)

    if 0:
        from random import random
        p = (p1, p2, p3, p4, p5) = ((2,5),(6,3),(6,-1),(-2,-1),(-2,3))
        l = [(p1,p2),(p2,p3),(p3,p4),(p4,p5),(p5,p1),(p2,p5)]
        pointW = [1,2,3,4,5]
        arrowW = [6,5,4,3,2,1]
        pointColors = [(255,0,0), (0,255,0), (0,0,255), (255,255,0), (255,0,255)]
        arrowColors = [(random(),random(),random()) for i in xrange(len(l))]
        cartesianPlot(window_title="house", points=p, arrows=l,
                      pointW=pointW, arrowW=arrowW, pointColors=pointColors, arrowColors=arrowColors,
                      grid_spacing=1, axes=True)

    if 0:
        p = (p1, p2, p3) = ((30,60),(70,60),(50,20))
        cartesianPlot(window_title="test", points=p, grid_spacing=10)

    if 1:
        from random import random
        coords = "500 500;500 410;500 590;500 320;320 499;499 680;680 500;500 230;309 309;230 499;309 690;499 770;690 690;770 500;690 309;500 140;362 167;245 245;167 362;140 499;167 637;245 754;362 832;499 860;637 832;754 754;832 637;860 500;832 362;754 245;637 167;500 50;412 58;327 84;249 125;181 181;125 249;84 327;58 412;50 499;58 587;84 672;125 750;181 818;249 874;327 915;412 941;499 950;587 941;672 915;750 874;818 818;874 750;915 672;941 587;950 500;941 412;915 327;874 249;818 181;750 125;672 84;587 58".split(";")
        p = [map(int, e.split()) for e in coords]
        pl = range(len(p))
        #from numberToWords import numberToWords
        #from string import capitalize
        #pl = [capitalize(numberToWords(r)) for r in range(len(coords))]

        arcs = "2 1;3 1;4 2;5 2;6 3;7 3;8 4;9 4;10 5;11 5;12 6;13 6;14 7;15 7;16 8;17 8;18 9;19 9;20 10;21 10;22 11;23 11;24 12;25 12;26 13;27 13;28 14;29 14;30 15;31 15;32 16;33 16;34 17;35 17;36 18;37 18;38 19;39 19;40 20;41 20;42 21;43 21;44 22;45 22;46 23;47 23;48 24;49 24;50 25;51 25;52 26;53 26;54 27;55 27;56 28;57 28;58 29;59 29;60 30;61 30;62 31;63 31".split(";")
        arcs2 = [map(int, arc.split()) for arc in arcs]
        l = [ (p[p1-1],p[p2-1]) for p1,p2 in arcs2 ]
        ps = [random()*10 for i in xrange(len(p))]
        pc = [(random(),random(),random()) for i in xrange(len(p))]
        lw = [random()*10 for i in xrange(len(l))]
        lc = [(random(),random(),random()) for i in xrange(len(l))]
        cartesianPlot(window_title="Graph2", points=p, lines=l, pointLabels=pl, pointW=ps,
                      lineW=lw, lineColors=lc, pointColors=pc, axes=True)
