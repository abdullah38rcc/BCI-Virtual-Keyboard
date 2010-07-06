// ----------------------------------------------------------------------------
// Copyright (c) 2005, Quia Corporation. All rights reserved.
// ----------------------------------------------------------------------------

/**
 * This is a heavily customized and improved version of the script found on
 * scriptasylum. This version does away with the need for overloading the
 * the onload method which conflicted with some of our existing scripts.
 * In addition, this version is much easier to use since you will no
 * longer need to manually insert a <div id="navtxt"></div> element into
 * the page as the script will now dynamically create that for you.
 *
 * We had to apply the iframe sliver technique to this script so that
 * the popup text would show up ON TOP of select boxes in IE.
 *
 *    http://www.shinydonkey.com/threads/625.aspx
 *
 * $Id$
 */

/*****************************************************************************

ALTTXT V1.6
BY: BRIAN GOSSELIN OF SCRIPTASYLUM.COM

INSTRUCTIONS:

1: NEXT, PLACE THIS STYLE DECLARATION IN THE HEAD SECTION OF YOUR PAGE (JUST CHANGE YOUR SETTINGS):

   .navtext {
   width:235px;
   font-size:8pt;
   font-family:verdana;
   border-width:2px;
   border-style:outset;
   border-color:#006BAE;
   layer-background-color:#FFF6D9;
   background-color:#FFF6D9;
   color:black;
   }

2: THEN, SET THE 6 SETTINGS BELOW ( dofade, centertext, xoffset, yoffset, mousefollow, and hideDelay ) AS DESIRED.

3: LASTLY ADD THE MOUSEOVER/MOUSEOUT EVENT HANDLERS TO EACH LINK THAT YOU WANT THIS EFFECT FOR:

     EXAMPLE: <a href="scriptasylum.com" onmouseover="writetxt('Popup text')" onmouseout="writetxt(0)">Link text</a>



NOTES:

  > YOU CAN CAUSE A BOX *NOT* TO DISAPPEAR ONCE THE MOUSE LEAVES THE LINK BY SIMPLY OMITTING THE
    onmouseout="writetxt(0)" PART. THIS WILL CAUSE THE CURRENT BOX TO REMAIN VISIBLE. THIS IS BEST
    USED WHEN mousefollow MODE IS DISABLED (SET TO false).

  > YOU CAN SET THE PADDING STYLE ATTRIBUTE *ONLY* IN THE navtxt DIV ITSELF AND *NOT* IN THE STYLE
    SHEET AT THE TOP OF THE PAGE. OTHERWISE NS4 DISPLAYS SOME WEIRD BEHAVIOR. ALSO, THE PADDING ATTRIBUTE
    ONLY HAS AN EFFECT IN IE4+ AND NS6+.

******************************************************************************/

var dofade=false;       // ENABLES FADE-IN EFFECT (FOR IE4+ AND NS6 ONLY)

var centertext=false;  // CENTERS THE TEXT INSIDE THE BOX. YOU CAN'T SIMPLY
                       // DO THIS VIA "STYLE" BECAUSE OF NS4.
                       // OTHERWISE, TEXT IS LEFT-JUSTIFIED.

var xoffset=9;         // HORIZONTAL PIXEL COUNT FROM CURSOR

//var yoffset=25;        // VERTICAL PIXEL COUNT FROM CURSOR
var yoffset=20;

var mousefollow=true; // ENABLES MOUSE FOLLOW MODE WHERE THE BOX CONTINUES
                       // TO FOLLOW THE MOUSE. SET TO false TO
                       // LOCK THE BOX WHEREVER IT INITIALLY APPEARS.

var hideDelay=300;     // DELAY IN MILLISECONDS ( 1 SECOND = 1000 MILLISECONDS)
                       // FROM WHEN YOU HOVER OUT OF LINK AND THE BOX
                       // DISAPPEARS ONLY WHEN "mousefollow" IS SET TO "false".
                       // THIS WILL GIVE THE USER TIME TO CLICK A LINK OR
                       // WHATEVER IN THE BOX BEFORE IT DISAPPEARS.



var isInitialized = false;

//////////////////// NO NEED TO EDIT BEYOND THIS POINT ////////////////////////


// ----------------------------------------------------------------------------
function altProps() {
  this.w3c=(document.getElementById)?true:false;
  this.ns4=(document.layers)?true:false;
  this.ie4=(document.all && !this.w3c)?true:false;
  this.ie5=(document.all && this.w3c)?true:false;
  this.ns6=(this.w3c && navigator.appName.indexOf("Netscape")>=0 )?true:false;
  this.w_y=0;
  this.w_x=0;
  this.navtxt=null;
  this.boxheight=0;
  this.boxwidth=0;
  this.ishover=false;
  this.ieop=0;
  this.op_id=0;
  this.oktomove=false;
  this.dy=0;
  this.iframeSliver = null;
  this.useiframe = navigator.userAgent.toLowerCase().indexOf('msie') !=-1;    // Can be used to test if IE

  // Fix a bug with IE where appending to the dom before it's ready causes "Operation Aborted"
  this.domready = !this.useiframe;
  if (this.useiframe) {
    // This test was copied from mootools
    if (!document.getElementById('ie_ready')) {
      var src = (window.location.protocol == 'https:') ? '://0' : 'javascript:void(0)';
      document.write('<script id="ie_ready" defer src="' + src + '"><\/script>');
      document.getElementById('ie_ready').onreadystatechange = function(){
        if (this.readyState == 'complete') AT.domready = true;
      };
    }
  }
}

var AT=new altProps();

// ----------------------------------------------------------------------------
function isDefined(testVar){
  try { if (typeof(testVar) != "undefined") return true; }
  catch (e) { }
  return false;
}

// ----------------------------------------------------------------------------
function toggle_centertext(){
  centertext=!centertext;
}

// ----------------------------------------------------------------------------
function toggle_mousefollow(){
  mousefollow=!mousefollow;
}

// ----------------------------------------------------------------------------
function toggle_dofade(){
  dofade=!dofade;
  if(!dofade)AT.ieop=100;
}

// ----------------------------------------------------------------------------
function getwindowdims(){
  if (!isDefined(AT)) return;
  AT.w_y=(AT.ie5||AT.ie4)?document.body.clientHeight:window.innerHeight;
  AT.w_x=(AT.ie5||AT.ie4)?document.body.clientWidth:window.innerWidth;
}

// ----------------------------------------------------------------------------
function getboxwidth(){
  if (!isDefined(AT)) return;
  if (AT.ns4) {
    AT.boxwidth=(AT.navtxt.document.width)?
      AT.navtxt.document.width : AT.navtxt.clip.width;
  }
  else if (AT.ie4) {
    AT.boxwidth=(AT.navtxt.style.pixelWidth)?
      AT.navtxt.style.pixelWidth : AT.navtxt.offsetWidth;
  }
  else {
    AT.boxwidth=(AT.navtxt.style.width)?
      parseInt(AT.navtxt.style.width) : parseInt(AT.navtxt.offsetWidth);
  }

}

// ----------------------------------------------------------------------------
function getboxheight(){
  if (!isDefined(AT)) return;
  if(AT.ns4) {
    AT.boxheight=(AT.navtxt.document.height)?
      AT.navtxt.document.height : AT.navtxt.clip.height;
  }
  else if(AT.ie4) {
    AT.boxheight=(AT.navtxt.style.pixelHeight)?
      AT.navtxt.style.pixelHeight : AT.navtxt.offsetHeight;
  }
  else {
    AT.boxheight=parseInt(AT.navtxt.offsetHeight);
  }
}

// ----------------------------------------------------------------------------
function movenavtxt(x,y){
  if (!isDefined(AT)) return;

  if(AT.ns4)AT.navtxt.moveTo(x,y);
  else{
    AT.navtxt.style.left=x+'px';
    AT.navtxt.style.top=y+'px';
  }

  // Move the iframe sliver
  if(AT.useiframe) {
    if(AT.ns4)AT.iframeSliver.moveTo(x,y);
    else{
      AT.iframeSliver.style.left=x+'px';
      AT.iframeSliver.style.top=y+'px';
    }
  }
}

// ----------------------------------------------------------------------------
function getpagescrolly(){
  if (!isDefined(AT)) return;
  if(AT.ie5||AT.ie4)return document.body.scrollTop;
  else return window.pageYOffset;
}

// ----------------------------------------------------------------------------
function getpagescrollx(){
  if (!isDefined(AT)) return;
  if(AT.ie5||AT.ie4)return document.body.scrollLeft;
  else return window.pageXOffset;
}

// ----------------------------------------------------------------------------
function writeindiv(text){
  if (!isDefined(AT)) return;
  if(AT.ns4){
    AT.navtxt.document.open();
    AT.navtxt.document.write(text);
    AT.navtxt.document.close();
  }
  else {
    AT.navtxt.innerHTML=text;
  }
}


// ----------------------------------------------------------------------------
function writeindivCompact(width, text){
  if (!isDefined(AT)) return;
  if(AT.ns4){
    AT.navtxt.document.open();
    AT.navtxt.document.write(text);
    AT.navtxt.document.close();
  }
  else {
    AT.navtxt.innerHTML=
      "<table border=0 cellpadding=0 cellspacing=0 width=" + width + "><tr><td>"
      + "<font size=2>"
      + text
      + "</font>"
      + "</td></tr></table>"
      ;
  }
}

// ----------------------------------------------------------------------------
function writetxtcss(text, cssclass) {
  if (!isDefined(AT) || !AT.domready) return;

  initializePopupWindow(cssclass);

  if(dofade && (AT.ie4||AT.w3c))clearInterval(AT.op_id);

  if(text!=0) {

    if(!mousefollow)clearTimeout(AT.dy);


    // Show the iframeSliver
    if(AT.useiframe) {
      if(AT.ns4)AT.iframeSliver.visibility="show";
      else{
        AT.iframeSliver.style.display="block";
      }
    }

    AT.oktomove=true;
    AT.ishover=true;



    if(AT.w3c||AT.ie4)AT.navtxt.style.textAlign=(centertext)?"center":"left";


    // Attempt to write the text into the popup window
    writeindiv(text);


    // Make the popup visible. This MUST be called before we run getboxwidth
    // and getboxheight because those methods will not have the correct
    // values if navtxt is not visible yet
    if(AT.ns4)AT.navtxt.visibility="show";
    else{
      AT.navtxt.style.visibility="visible";
      AT.navtxt.style.display="block";
    }



    getboxwidth();
    getboxheight();


    // If the boxwidth is over 250 pixels wide, then let's perform the
    // "smart" popup window resizing algorithm
    if (AT.boxwidth > 250) {

    // Check to see if the width is MUCH larger than the height.
    // If it is, then we need to try to "square" off the popup window
      if (AT.boxwidth > (AT.boxheight*2)) {
        writeindivCompact(250, text);
        getboxwidth();
        getboxheight();
      }


      // Check to see if the height is MUCH larger than the width.
      // If it is, then we need to try to "square" off the popup window
      // by using a larger box width
      if (AT.boxheight > (AT.boxwidth*2)) {
        writeindivCompact(500, text);
        getboxwidth();
        getboxheight();
      }

    }




    if((AT.w3c||AT.ie4) && dofade){
      if(AT.ie4||AT.ie5)AT.navtxt.style.filter="alpha(opacity=0)";
      if(AT.ns6)AT.navtxt.style.MozOpacity=0;
      AT.ieop=0;
      AT.op_id=setInterval('incropacity()',50);
    }

    // set the iframe sliver to be the same size and position as the navtxt
    margin=(AT.ie4||AT.ie5)?0:25;
    if(AT.useiframe) {
      AT.iframeSliver.width = AT.boxwidth-margin;
      AT.iframeSliver.height = AT.boxheight-margin;
    }

  }
  else{
    if(mousefollow)hideAlttxt();
    else AT.dy=setTimeout('hideAlttxt()',hideDelay);
  }


}
// ----------------------------------------------------------------------------
function writetxt(text) {
  writetxtcss(text, "navtext");
}

// ----------------------------------------------------------------------------
function writetxtnowrap(text) {
  writetxtcss(text, "navtextnowrap");
}

// ----------------------------------------------------------------------------
function hideAlttxt(){
  if (!isDefined(AT)) return;
  if(AT.ns4)AT.navtxt.visibility="hide";
  else{
    AT.navtxt.style.display="none";
    AT.navtxt.style.visibility="hidden";
  }
  movenavtxt(-AT.boxwidth-10,0);
  writeindiv('');



  // Hide the iframeSliver
  if(AT.useiframe) {
    if(AT.ns4)AT.iframeSliver.visibility="hide";
    else{
      //    AT.iframeSliver.style.visibility="hidden";
      AT.iframeSliver.style.display="none";
    }
  }
}

// ----------------------------------------------------------------------------
function incropacity() {
  if (!isDefined(AT)) return;
  if(AT.ieop<=100){
    AT.ieop+=7;
    if(AT.ie4||AT.ie5)AT.navtxt.style.filter="alpha(opacity="+AT.ieop+")";
    if(AT.ns6)AT.navtxt.style.MozOpacity=AT.ieop/100;
  }else clearInterval(AT.op_id);
}

// ----------------------------------------------------------------------------
function moveobj(evt){
  if (!isDefined(AT)) return;
  mx=(AT.ie5||AT.ie4)?event.clientX:evt.pageX;
  my=(AT.ie5||AT.ie4)?event.clientY:evt.pageY;
  if(AT.ishover && AT.oktomove){
    margin=(AT.ie4||AT.ie5)?5:25;
    if(AT.ns6)if(document.height+27-window.innerHeight<0)margin=15;
    if(AT.ns4)if(document.height-window.innerHeight<0)margin=10;
    if(AT.ns4||AT.ns6)mx-=getpagescrollx();
    if(AT.ns4)my-=getpagescrolly();
    xoff=mx+xoffset;
    yoff=(my+AT.boxheight+yoffset-((AT.ns6)?
      getpagescrolly():0)>=AT.w_y)? -5-AT.boxheight-yoffset: yoffset;

    // Make sure the yPosition is at least below the top of the
    // browswer window to avoid clipping
    yPosition = my+yoff+((!AT.ns6)?getpagescrolly():0);
    if (yPosition <= getpagescrolly()) {
      yPosition = getpagescrolly() + 5;
    }

    xPosition =
      Math.min(AT.w_x-AT.boxwidth-margin, Math.max(2,xoff))+getpagescrollx();

    movenavtxt(xPosition, yPosition);
    if(!mousefollow)AT.oktomove=false;
  }
}



// ----------------------------------------------------------------------------
// This method has been changed to be an actual initialization call as opposed
// to overriding the onload method. This should be safe since we will be
// dynamically creating the div that we need to use rather than relying
// on the browser to create it from the page itself.
function initializePopupWindow(cssclass) {
  if (!isDefined(AT) || !AT.domready) return;

  if (!isInitialized) {

    var popWindowDiv = document.createElement("div");
    popWindowDiv.id = "navtxt";
    popWindowDiv.className = cssclass;
    popWindowDiv.style.visibility = "hidden";
    popWindowDiv.style.position = "absolute";
    popWindowDiv.style.top = "0px";
    popWindowDiv.style.left = "-400px";
    popWindowDiv.style.zIndex = "10000";
    popWindowDiv.style.padding = "10px";
    document.body.appendChild(popWindowDiv);


    if(AT.useiframe) {
      var iframeWindowDiv = document.createElement("iframe");
      iframeWindowDiv.src="javascript:false";
      iframeWindowDiv.id = "iframeSliver";
      iframeWindowDiv.style.position = "absolute";
      iframeWindowDiv.style.display = "none";
      iframeWindowDiv.style.frameborder = "0";
      iframeWindowDiv.style.scrolling = "no";
      iframeWindowDiv.style.marginwidth = "0";
      iframeWindowDiv.style.marginheight = "0";
      iframeWindowDiv.width = "1";
      iframeWindowDiv.height = "1";
      iframeWindowDiv.style.top = "0";
      iframeWindowDiv.style.left = "-400px";
      document.body.appendChild(iframeWindowDiv);
    }


    AT.navtxt = null;

    if (AT.ns4) {
      AT.navtxt = document.layers['navtxt'];
      if(AT.useiframe) AT.iframeSliver = document.layers['iframeSliver'];
    }
    else if (AT.ie4) {
      AT.navtxt = document.all['navtxt'];
      if(AT.useiframe) AT.iframeSliver = document.all['iframeSliver'];
    }
    else if (AT.w3c) {
      AT.navtxt = document.getElementById('navtxt');
      if(AT.useiframe) AT.iframeSliver = document.getElementById('iframeSliver');
    }


    getboxwidth();
    getboxheight();
    getwindowdims();
    if(AT.ie4||AT.ie5&&dofade)AT.navtxt.style.filter="alpha(opacity=100)";
    AT.navtxt.onmouseover=function(){
      if(!mousefollow)clearTimeout(AT.dy);
    }
    AT.navtxt.onmouseout=function(){
      if(!mousefollow)AT.dy=setTimeout('hideAlttxt()',hideDelay);
    }
    if(AT.ns4)document.captureEvents(Event.MOUSEMOVE);
    document.onmousemove=moveobj;
    window.onresize=getwindowdims;

    isInitialized=true;

  }

}
