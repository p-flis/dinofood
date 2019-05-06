

function addNew(e,thisNode){
e.preventDefault();
var temp = document.getElementById("row-template");
var next = temp.cloneNode(true);
next.id="";
next.display="block";
//document.getElementById("allrows").
temp.parentNode.
insertBefore(next,thisNode.parentNode);
return false;
}

function deleteRow(e,thisNode,timesUp){
e.preventDefault();
var thisRow=thisNode;
var i=0;
for(;i<timesUp;i++){
thisRow=thisRow.parentNode;
}
thisRow.remove();
}


