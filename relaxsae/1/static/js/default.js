

function isEmpty(value){
	return value.length == 0;	
}

function checkuser(){
	var value = regiest_form.username.value;
	if (isEmpty(value)){
		document.getElementById('username').innerHTML = "<div class='alert'>用户名不能为空</div>";	
		return false;
	}
	var xmlhttp;
	if (window.XMLHttpRequest)
	{// code for IE7+, Firefox, Chrome, Opera, Safari
		xmlhttp=new XMLHttpRequest();
	}
	else
	{// code for IE6, IE5
		xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");
	}
	xmlhttp.onreadystatechange=function()
	{
		if (xmlhttp.readyState==4 && xmlhttp.status==200){
			if (xmlhttp.responseText.indexOf('ok') < 0){
				document.getElementById('username').innerHTML = "<div class='alert'>此用户名已存在</div>";	
				return false;
			}else{
				document.getElementById('username').innerHTML = "";	
				return true;
			}
		}else{
			return true;	
		}
	}
    xmlhttp.open("GET", "/checkuser?username="+value, true);  
    xmlhttp.send();
}
function checkpasswd1(){	
	var value = regiest_form.passwd1.value;
	if (value.length < 6){
		document.getElementById('passwd1').innerHTML = "<div class='alert'>密码最少6位</div>";	
		return false;
	}else{
		document.getElementById('passwd1').innerHTML = "";		
		return true;
	}
}

function checkpasswd2(){
	var value = regiest_form.passwd2.value;
	if (!isEmpty(regiest_form.passwd1.value) && isEmpty(document.getElementById('passwd1').innerHTML)){
		if (value != regiest_form.passwd1.value){
			document.getElementById('passwd2').innerHTML = "<div class='alert'>两次密码输入不一致</div>";	
			return false;
		}else{
			document.getElementById('passwd2').innerHTML = "";		
			return true;
		}
	}else{
		return true;	
	}
}

function checkemail(){
	var value = regiest_form.email.value;
	if (isEmpty(value)){
		document.getElementById('email').innerHTML = "<div class='alert'>邮箱不能为空</div>";		
		return false;	
	}else{
		if (value.indexOf('@') < 0 || value.indexOf('.') < 0){
			document.getElementById('email').innerHTML = "<div class='alert'>请填写正确的邮箱</div>";
			return false;	
		}else{		
			if (value.lastIndexOf('.') - value.indexOf('@') < 2 || value[value.length-1] == "."){
				document.getElementById('email').innerHTML = "<div class='alert'>请填写正确的邮箱</div>";
				return false;	
			}else{
				document.getElementById('email').innerHTML = "";
				return true;	
			}
		}
	}
}

function checktelephone(){
	var value = regiest_form.telephone.value;
	if (isEmpty(value)){
		document.getElementById('telephone').innerHTML = "<div class='alert'>手机不能为空</div>";	
		return false;	
	}else{
		if (value.length != 11 || value[0] != '1'){
			document.getElementById('telephone').innerHTML = "<div class='alert'>请填写正确的手机号码</div>";		
			return false;	
		}else{
			document.getElementById('telephone').innerHTML = "";	
			return true;	
		}
	}
}

function checkgender(){
	if (regiest_form.gender[0].checked || regiest_form.gender[1].checked){
		document.getElementById('gender').innerHTML = "";
		return true;
	}else{
		document.getElementById('gender').innerHTML="<div class='alert'>请选择性别</div>";
		return false;
	}
}

function checkregiest(){
	checkuser();
	if (!isEmpty(document.getElementById('username').innerHTML))	return false;
	if (!checkpasswd1()) return false;
	if (!checkpasswd1()) return false;
	if (!checkemail()) return false;
	if (!checktelephone()) return false;
	if (!checkgender()) return false;
	document.getElementById('regiest_submit').value="提交中...";
	document.getElementById('regiest_submit').disabled=true;
	return true;	
}

function isempty(str){
	var i = 0;
	for(i=0;i<str.length;++i){
		if (str[i] == ' ')
			continue;
		else
			break;
	}
	if(i == str.length){
		return 1;
	}
	return 0;
}

function check(){
	if(isempty(new_sub_form.title.value)){
		alert('标题不能为空！');
		return false;
	}
	
	if(isempty(new_sub_form.body.value)){
		alert('内容不能为空！');
		return false;
	}
}

function checksub(){
	if(isempty(answer_form.text.value)){
		alert('内容不能为空！');
		return false;
	}
}

function printme()
{
	OpenWindow=window.open("", "newwin", "height=600, width=1000,toolbar=no,scrollbars="+scroll+",menubar=no");
	OpenWindow.document.write("	<link href='/css/bootstrap.css' rel='stylesheet' />"+
	"<link href='/css/bootstrap.min.css' rel='stylesheet' />"+
	"<link href='/css/bootstrap-responsive.css' rel='stylesheet' />"+
	"<link href='/css/bootstrap-responsive.min.css' rel='stylesheet' />"+
	"<link href='/css/default.css' rel='stylesheet' />");
	OpenWindow.document.write(document.getElementById('print').innerHTML);
	OpenWindow.document.close();
	OpenWindow.print();
}

function tolow(){
	getWidth();
		window.scrollTo(2000,2000);
}
function join(id){
	var postStr = "id="+id;
	var xmlhttp;
	if (window.XMLHttpRequest)
	{// code for IE7+, Firefox, Chrome, Opera, Safari
		xmlhttp=new XMLHttpRequest();
	}
	else
	{// code for IE6, IE5
		xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");
	}
	xmlhttp.onreadystatechange=function()
	{
		if (xmlhttp.readyState==4 && xmlhttp.status==200)
		{
			if (xmlhttp.responseText.indexOf('参加成功') > -1){
				document.getElementById("div_join").innerHTML="<div class='alert alert-success'><button type='button' class='close' data-dismiss='alert'>&times;</button><strong>报名成功！</strong></div>";
			}else	if(xmlhttp.responseText.indexOf('已经参加') > -1){
				document.getElementById("div_join").innerHTML="<div class='alert'><button type='button' class='close' data-dismiss='alert'>&times;</button><strong>已经报名了，无需再次报名！</strong></div>";
			}else	if(xmlhttp.responseText.indexOf('出问题') > -1){
				document.getElementById("div_join").innerHTML="<div class='alert alert-error'><button type='button' class='close' data-dismiss='alert'>&times;</button><strong>出错了，返回再试试！</strong></div>";
			}else{
				document.getElementById("div_join").innerHTML="未知错误！";
			}
		}
	}
    xmlhttp.open("POST", "/join", true);  
    xmlhttp.setRequestHeader("Content-Type","application/x-www-form-urlencoded");  
    xmlhttp.send(postStr);  
}


function logout()
{
	var xmlhttp;
	if (window.XMLHttpRequest)
	{// code for IE7+, Firefox, Chrome, Opera, Safari
		xmlhttp=new XMLHttpRequest();
	}
	else
	{// code for IE6, IE5
		xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");
	}
	xmlhttp.onreadystatechange=function()
	{
		if (xmlhttp.readyState==4 && xmlhttp.status==200)
		{
			window.location.href="/home";
		}
	}
    xmlhttp.open("GET", "/logout", true);  
    xmlhttp.send();
}

function clear_user(){
	document.getElementById("div_login").innerHTML="";
	document.getElementById("regiestModal").innerHTML="";
	getWidth();
}