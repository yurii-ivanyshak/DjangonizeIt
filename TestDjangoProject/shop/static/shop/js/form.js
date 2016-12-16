var _selectHeight = 23;

var inputs = new Array();
var selects = new Array();
var labels = new Array();
var radios = new Array();
var radioLabels = new Array();
var checkboxes = new Array();
var checkboxLabels = new Array();
var buttons = new Array();
var selects = new Array();
var all_selects = false;
var active_select = null;
var selectText = "please select";

function is_mac() {
	if (navigator.appVersion.indexOf("Safari") != -1)
	{
		if(!window.getComputedStyle)
		{
			return true;
		}
	}
	
	return false;
}

function initCastomForms() {
	if(!document.getElementById) {return false;}
	getElements();
	separateElements();
	//replaceRadios();
	replaceCheckboxes();
	//replaceSelects();

	var _selects = document.getElementsByTagName('select');
	var _SelctClassName = [];
	if (_selects) {
		for (var i = 0; i < _selects.length; i++) {
			if (_selects[i].className != '' && _selects[i].className != 'outtaHere')
				_SelctClassName[i] = ' drop-'+_selects[i].className;
		}
		for (var i = 0; i < _SelctClassName.length; i++) {
			var _selectDrop = document.getElementById('optionsDiv'+i);
			if (_selectDrop) {
				if (_SelctClassName[i]) 
					_selectDrop.className += _SelctClassName[i];
			}
		}
	}
}


// getting all the required elements
function getElements() {
	var _frms = document.getElementsByTagName("form");
	for (var nf = 0; nf < _frms.length; nf++) {
		if(_frms[nf].className.indexOf("default") == -1) {
			var a = document.forms[nf].getElementsByTagName("input");
			for(var nfi = 0; nfi < a.length; nfi++) {
				inputs.push(a[nfi]);
			}
			var b = document.forms[nf].getElementsByTagName("label");
			for(var nfl = 0; nfl < b.length; nfl++) {
				labels.push(b[nfl]);
			}
			var c = document.forms[nf].getElementsByTagName("select");
			for(var nfs = 0; nfs < c.length; nfs++) {
				selects.push(c[nfs]);
			}
		}
	}
}

// separating all the elements in their respective arrays
function separateElements() {
	var r = 0; var c = 0; var t = 0; var rl = 0; var cl = 0; var tl = 0; var b = 0;
	for (var q = 0; q < inputs.length; q++) {
		if(inputs[q].type == "radio") {
			radios[r] = inputs[q]; ++r;
			for(var w = 0; w < labels.length; w++) {
				if((inputs[q].id) && labels[w].htmlFor == inputs[q].id)
				{
					radioLabels[rl] = labels[w];
				}
			}
			++rl;
		}
		if(inputs[q].type == "checkbox") {
			checkboxes[c] = inputs[q]; ++c;
			for(var w = 0; w < labels.length; w++) {
				if((inputs[q].id) && (labels[w].htmlFor == inputs[q].id))
				{
					checkboxLabels[cl] = labels[w];
				}
			}
			++cl;
		}
		if((inputs[q].type == "submit") || (inputs[q].type == "button")) {
			buttons[b] = inputs[q]; ++b;
		}
	}
}

//replacing radio buttons
function replaceRadios() {
	for (var q = 0; q < radios.length; q++) {
		radios[q].className += " outtaHere";
		var radioArea = document.createElement("div");
		if(radios[q].checked) {
			radioArea.className = "radioAreaChecked";
			if (radioLabels[q])
			{
				radioLabels[q].className += "radioAreaCheckedLabel"
			}
			
		}
		else
		{
			radioArea.className = "radioArea";
		}
		radioArea.id = "myRadio" + q;
		radios[q].parentNode.insertBefore(radioArea, radios[q]);
		radios[q]._ra = radioArea;

		radioArea.onclick = new Function('rechangeRadios('+q+')');
		if (radioLabels[q])
		{
			radioLabels[q].onclick = new Function('rechangeRadios('+q+')');
		}
	}
	return true;
}

//checking radios
function checkRadios(who) {
	var what = radios[who]._ra;
	for(var q = 0; q < radios.length; q++) {
		if((radios[q]._ra.className == "radioAreaChecked")&&(radios[q]._ra.nextSibling.name == radios[who].name))
		{
			radios[q]._ra.className = "radioArea";
			if (radioLabels[q])
			{
				radioLabels[q].className = radioLabels[q].className.replace("radioAreaCheckedLabel", "");
			}
		}
	}
	what.className = "radioAreaChecked";
	if(radioLabels[who])
		radioLabels[who].className += " radioAreaCheckedLabel";
}

//changing radios
function changeRadios(who) {
	if(radios[who].checked) {
		for(var q = 0; q < radios.length; q++) {
			if(radios[q].name == radios[who].name) {
				radios[q].checked = false;
			} 
			radios[who].checked = true; 
			checkRadios(who);
		}
	}
}

//rechanging radios
function rechangeRadios(who) {
	if(!radios[who].checked) {
		for(var q = 0; q < radios.length; q++) {
			if(radios[q].name == radios[who].name)	{
				radios[q].checked = false; 
			}
			radios[who].checked = true; 
			checkRadios(who);
		}
	}
}

//replacing checkboxes
function replaceCheckboxes() {
	for (var q = 0; q < checkboxes.length; q++) {
		checkboxes[q].className += " outtaHere";
		var checkboxArea = document.createElement("div");
		if(checkboxes[q].checked) {
			checkboxArea.className = "checkboxAreaChecked";
			if(checkboxLabels[q])
				checkboxLabels[q].className += "checkboxAreaCheckedLabel"
		}
		else {
			checkboxArea.className = "checkboxArea";
		}
		checkboxArea.id = "myCheckbox" + q;
		checkboxes[q].parentNode.insertBefore(checkboxArea, checkboxes[q]);
		checkboxes[q]._ca = checkboxArea;
		checkboxArea.onclick = checkboxArea.onclick2 = new Function('rechangeCheckboxes('+q+')');
		if (checkboxLabels[q])
		{
			checkboxLabels[q].onclick = new Function('changeCheckboxes('+q+')');
		}
		
		checkboxes[q].onkeydown = checkEvent;
	}
	return true;
}

//checking checkboxes
function checkCheckboxes(who, action) {
	var what = checkboxes[who]._ca;
	if(action == true) {
		what.className = "checkboxAreaChecked";
		what.checked = true;
		if(checkboxLabels[who])
			checkboxLabels[who].className += " checkboxAreaCheckedLabel";
	}
	if(action == false) {
		what.className = "checkboxArea";
		what.checked = false;
		if(checkboxLabels[who])
			checkboxLabels[who].className = checkboxLabels[who].className.replace("checkboxAreaCheckedLabel", "");
	}
}

//changing checkboxes
function changeCheckboxes(who) {
	if(checkboxes[who].checked) {
		checkCheckboxes(who, false);
	}
	else {
		checkCheckboxes(who, true);
	} 
}

//rechanging checkboxes
function rechangeCheckboxes(who) {
	var tester = false;
	if(checkboxes[who].checked == true) {
		tester = false;
	}
	else {
		tester = true;
	}
	checkboxes[who].checked = tester;
	checkCheckboxes(who, tester);
}

//check event
function checkEvent(e) {
	if (!e) var e = window.event;
	if(e.keyCode == 32) {for (var q = 0; q < checkboxes.length; q++) {if(this == checkboxes[q]) {changeCheckboxes(q);}}} //check if space is pressed
}


function replaceSelects() {
	for(var q = 0; q < selects.length; q++) {
	if (!selects[q].replaced && selects[q].offsetWidth && selects[q].className.indexOf("default") == -1)
	{
		selects[q]._number = q;
		//create and build div structure
		var selectArea = document.createElement("div");
		var left = document.createElement("span");
		left.className = "left";
		selectArea.appendChild(left);
		
		var disabled = document.createElement("span");
		disabled.className = "disabled";
		selectArea.appendChild(disabled);
		
		selects[q]._disabled = disabled;
		var center = document.createElement("span");
		var button = document.createElement("a");
		var text = document.createTextNode(selectText);
		center.id = "mySelectText"+q;
		
		var stWidth = selects[q].offsetWidth;
		selectArea.style.width = stWidth + "px";
		if (selects[q].parentNode.className.indexOf("type2") != -1){
			button.href = "javascript:showOptions("+q+",true)";
		} else {
			button.href = "javascript:showOptions("+q+",false)";
		}
		button.className = "selectButton";
		selectArea.className = "selectArea";

		selectArea.className += " " + selects[q].className;
		selectArea.id = "sarea"+q;
		center.className = "center";
		center.appendChild(text);
		selectArea.appendChild(center);
		selectArea.appendChild(button);
		
		//hide the select field
		selects[q].className += " outtaHere";
		//insert select div
		selects[q].parentNode.insertBefore(selectArea, selects[q]);
		//build & place options div

		var optionsDiv = document.createElement("div");
		var optionsListParent = document.createElement("div");
		optionsListParent.className = "select-center";
		var optionsListParent2 = document.createElement("div");
		optionsListParent2.className = "select-center-right";
		var optionsList = document.createElement("ul");
		optionsDiv.innerHTML += "<div class='select-top'><div class='select-top-left'></div><div class='select-top-right'></div></div>";
		optionsListParent.appendChild(optionsListParent2);
		optionsListParent.appendChild(optionsList);
		optionsDiv.appendChild(optionsListParent);
		
		selects[q]._options = optionsList;
		
		optionsDiv.style.width = stWidth + "px";
		optionsDiv._parent = selectArea;
		
		optionsDiv.className = "optionsDivInvisible";
		optionsDiv.id = "optionsDiv"+q;
		
	
		populateSelectOptions(selects[q]);
		optionsDiv.innerHTML += "<div class='select-bottom'><div class='select-bottom-left'></div><div class='select-bottom-right'></div></div>";
		document.getElementsByTagName("body")[0].appendChild(optionsDiv);
		selects[q].replaced = true;
		}
	all_selects = true;
	}
}

//collecting select options
function populateSelectOptions(me) {
	me._options.innerHTML = "";
	
	for(var w = 0; w < me.options.length; w++) {
		if(me.options[w].title.indexOf("title") == -1) {
			var optionHolder = document.createElement('li');
			var optionLink = document.createElement('a');
			var optionTxt;
			if (me.options[w].title.indexOf('image') != -1) {
				optionTxt = document.createElement('img');
				optionSpan = document.createElement('span');
				optionTxt.src = me.options[w].title;
				optionSpan = document.createTextNode(me.options[w].text);
			} else {
				optionTxt = document.createTextNode(me.options[w].text);
			}
			
			optionLink.href = "javascript:showOptions("+me._number+"); selectMe('"+me.id+"',"+w+","+me._number+");";
			if (me.options[w].title.indexOf('image') != -1) {
				optionLink.appendChild(optionTxt);
				optionLink.appendChild(optionSpan);
			} else {
				optionLink.appendChild(optionTxt);
			}
			optionHolder.appendChild(optionLink);
			me._options.appendChild(optionHolder);
			//check for pre-selected items
			if(me.options[w].selected) {
				selectMe(me.id,w,me._number);
			}
		}
		else if(me.options[w].selected)
			selectMe(me.id,w,me._number);
	}
	if (me.disabled) {
		me._disabled.style.display = "block";
	}
	else {
		me._disabled.style.display = "none";
	}
}

//selecting me
function selectMe(selectFieldId,linkNo,selectNo) {
	selectField = selects[selectNo];
	for(var k = 0; k < selectField.options.length; k++) {
		if(k==linkNo) {
			selectField.options[k].selected = true;
		}
		else {
			selectField.options[k].selected = false;
		}
	}
	
	//show selected option
	textVar = document.getElementById("mySelectText"+selectNo);
	var newText;
	var optionSpan;
	if (selectField.options[linkNo].title.indexOf('image') != -1) {
		newText = document.createElement('img');
		newText.src = selectField.options[linkNo].title;
		optionSpan = document.createElement('span');
		optionSpan = document.createTextNode(selectField.options[linkNo].text);
	} else {
		newText = document.createTextNode(selectField.options[linkNo].text);
	}
	if (selectField.options[linkNo].title.indexOf('image') != -1) {
		if (textVar.childNodes.length > 1) textVar.removeChild(textVar.childNodes[0]);
		textVar.replaceChild(newText, textVar.childNodes[0]);	
		textVar.appendChild(optionSpan);	
	} else {
		if (textVar.childNodes.length > 1) textVar.removeChild(textVar.childNodes[0]);
		textVar.replaceChild(newText, textVar.childNodes[0]);	
	}
	if (selectField.onchange && all_selects)
		{
			eval(selectField.onchange());
		}
}
//showing options
function showOptions(g) {
		_elem = document.getElementById("optionsDiv"+g);
		var divArea = document.getElementById("sarea"+g);
		if (active_select && active_select != _elem) {
			active_select.className = active_select.className.replace('optionsDivVisible','optionsDivInvisible');
			active_select.style.height = "auto";
			_active.className = _active.className.replace('selectAreaActive','');
		}
		if(_elem.className.indexOf("optionsDivInvisible") != -1) {
			_elem.style.left = "-9999px";
			_elem.style.top = findPosY(divArea) + _selectHeight + 'px';
			_elem.className = _elem.className.replace('optionsDivInvisible','');
			_elem.className += " optionsDivVisible";
			/*if (_elem.offsetHeight > 200)
			{
				_elem.style.height = "200px";
			}*/
			_elem.style.left = findPosX(divArea) + 'px';
			divArea.className += ' selectAreaActive';
			_active = divArea;
			
			active_select = _elem;
			if(document.documentElement)
			{
				document.documentElement.onclick = hideSelectOptions;
			}
			else
			{
				window.onclick = hideSelectOptions;
			}
		}
		else if(_elem.className.indexOf("optionsDivVisible") != -1) {
			_elem.style.height = "auto";
			_elem.className = _elem.className.replace('optionsDivVisible','');
			_elem.className += " optionsDivInvisible";
			divArea.className = divArea.className.replace('selectAreaActive','');
		}
		
		// for mouseout
		/*_elem.timer = false;
		_elem.onmouseover = function() {
			if (this.timer) clearTimeout(this.timer);
		}
		_elem.onmouseout = function() {
			var _this = this;
			this.timer = setTimeout(function(){
				_this.style.height = "auto";
				_this.className = _this.className.replace('optionsDivVisible','');
				if (_elem.className.indexOf('optionsDivInvisible') == -1)
					_this.className += " optionsDivInvisible";
			},200);
		}*/
}
_active = false;
function hideSelectOptions(e)
{
	if(active_select)
	{
		if(!e) e = window.event;
		var _target = (e.target || e.srcElement);
		if(isElementBefore(_target,'selectArea') == 0 && isElementBefore(_target,'optionsDiv') == 0)
		{
			active_select.className = active_select.className.replace('optionsDivVisible', '');
			active_select.className = active_select.className.replace('optionsDivInvisible', '');
			active_select.className += " optionsDivInvisible";
			_active.className = _active.className.replace('selectAreaActive','');
			active_select = false;

			if(document.documentElement)
			{
				document.documentElement.onclick = function(){};
			}
			else
			{
				window.onclick = null;
			}
		}
	}
}

function isElementBefore(_el,_class)
{
	var _parent = _el;	
	do
	{
		_parent = _parent.parentNode;
	}
	while(_parent && _parent.className != null && _parent.className.indexOf(_class) == -1)
	
	if(_parent.className && _parent.className.indexOf(_class) != -1)
	{
		return 1;
	}
	else
	{
		return 0;
	}
	
}

function findPosY(obj) {
	var posTop = 0;
	while (obj.offsetParent) {posTop += obj.offsetTop; obj = obj.offsetParent;}
	return posTop;
}
function findPosX(obj) {
	var posLeft = 0;
	while (obj.offsetParent) {posLeft += obj.offsetLeft; obj = obj.offsetParent;}
	return posLeft;
}
window.onload = initCastomForms;