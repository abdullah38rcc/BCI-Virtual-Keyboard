var request=false;var hideSpecialCookieFromJava,messageDivNameFromJava;var bannerTypeFromJava,SpecialTagBannerFromJava;var tagWhereYFromJava="whereY";(function(){var B=function(){if(document.getElementById){return document.getElementById(messageDivNameFromJava)}else{return document.all[messageDivNameFromJava]}};var A=function(F){if(!F){document.cookie=hideSpecialCookieFromJava+"=hide_message; path=/"}var E=B();E.innnerHTML="";E.style.visibility="hidden";E.style.display="none"};var D=function(){if(request.readyState==4){if(request.status==200){var F=request.responseText;if(F.length>0){var E=B();E.innerHTML=F;E.style.visibility="visible";E.style.display="block"}else{A(true)}}}};var C=function(){try{request=new XMLHttpRequest()}catch(F){try{request=new ActiveXObject("Msxml2.XMLHTTP")}catch(F){try{request=new ActiveXObject("Microsoft.XMLHTTP")}catch(F){request=false}}}if(request){try{var E="/servlets/quia.common.modules.SpecialMessageServlet?"+SpecialTagBannerFromJava+"="+bannerTypeFromJava;request.open("GET",E,true);request.onreadystatechange=D;request.send(null)}catch(F){}}};window.hideSpecialMessage=A;window.getSpecialMessage=C})();function handleEnter(C,A){var B=A.keyCode||A.which||A.charCode;return B!=13&&B!=3}function disableAllSubmitButtons(E){if(document.forms&&document.createElement){var F=0,I=document.forms.length,D,C,A,B,G;for(;F<I;F++){A=document.forms[F];D=0;C=A.elements.length;for(;D<C;D++){B=A.elements[D];G=B.type.toLowerCase();if(G=="submit"||G=="reset"){B.disabled=true}}}var H=document.createElement("input");H.style.display="none";H.style.visibility="hidden";if(H.setAttribute){H.setAttribute("name",E.name);H.setAttribute("value",E.value)}else{H.name=E.name;H.value=E.value}E.form.appendChild(H);E.form.submit()}return true}function getYOffset(C){var B=0;if(C.offsetParent){var A=C;while(A.offsetParent){B+=A.offsetTop;A=A.offsetParent}}else{if(C.y){B+=C.y}}return B}function getFormElementInDocument(E){var C=null;if(document.forms){for(var F=0;C==null&&F<document.forms.length;F++){var D=document.forms[F];for(var A=0;C==null&&A<D.length;A++){var B=D.elements[A];if(B.name==E){C=B}}}}return C}function getWindowHeight(){var A=-1;if(window.innerHeight){A=window.innerHeight}else{if(document.documentElement&&document.documentElement.clientHeight&&document.documentElement.clientHeight>0){A=document.documentElement.clientHeight}else{if(document.body.clientHeight){A=document.body.clientHeight}}}return A}function getCurYLoc(){var A=-1;if(window.pageYOffset){A=window.pageYOffset}else{if(document.body.scrollTop){A=document.body.scrollTop}}return A}function saveScrollCoordinates(B){var A=getCurYLoc();if(document.createElement){var D=document.createElement("input");D.name=tagWhereYFromJava;D.id=tagWhereYFromJava;D.value=A;try{D.type="hidden"}catch(C){D.style.visibility="hidden"}B.appendChild(D)}}function scrollToCoordinates(A){if(A!=-1){window.scrollTo(0,A)}}function gotoUrlWithWhereY(A){var B=getCurYLoc();A=A+"&"+tagWhereYFromJava+"="+B;window.location=A}function getWhereYandScroll(F,D){if(F!=null){var C=getFormElementInDocument(F);if(C!=null){var E=getYOffset(C);var A=getWindowHeight();if(E>-1&&A>0){var B=A/4;D=E-B}}}if(D>=0){scrollToCoordinates(D)}}function addLoadEvent(A){YAHOO.util.Event.onDOMReady(A)}(function(){var B="#CCCCCC",F="#444444",A="First Name",G="Last Name",E="firstName",D="lastName";var C=function(J,H,I){J.value=H;J.style.color=I||B};window.QUIAHOME={focus:function(H){if((H.value===A&&H.id===E)||(H.value===G&&H.id===D)){C(H,"",F)}},blur:function(H){if(H.value===""&&H.id===E){C(H,A)}if(H.value===""&&H.id===D){C(H,G)}},prepareFindTeacher:function(){var J=document.getElementById(E),K=J.value,H=document.getElementById(D),I=H.value;if(K===""||K===A){C(J,A)}if(I===""||I===G){C(H,G)}},processFindTeacherSubmit:function(H){var J=document.getElementById(E);var I=document.getElementById(D);if(J.value===A){J.value=""}if(I.value===G){I.value=""}}}})();(function(){var B=YAHOO.util,C=B.Dom,A=B.Event;var F=function(){return true};var E=function(){return false};var D=function(H){var G=(H.type?H.type.toLowerCase():null);return G==="submit"||G==="reset"||G==="image"};window.createBeforeUnload=function(H,K,J){if(YAHOO.env.ua.webkit&&YAHOO.env.ua.webkit<419){return }K=K||E;var I=true;if(!J){I=false;var G=function(){I=true};C.getElementsBy(F,"form",document,function(L){A.addListener(C.getElementsBy(D,"input",L),"click",G);A.addListener(C.getElementsByClassName("switchViewEditLk","a",L),"click",G);L._submit=L.submit;L.submit=function(){G();L._submit()}})}A.addListener(window,"beforeunload",function(L){if(!I&&!K()){if(L){L.returnValue=H}return H}})}})()