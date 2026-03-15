const list = []

function btnDelete(){
  return confirm("削除してもよろしいでしょうか?")
}

function createUser(){
  const email = document.querySelector("email")
  const first_name = document.querySelector("first_name")
  const last_name = document.querySelector("last_name")

  //入力チェック
  if(!email.checkValidity() || !first_name.checkValidity() || !last_name.checkValidity()){
    return;
  }

  const form = document.getElementById("form")
  form.setAttribute("action","/createUser")
  form.submit()
}

function btnEditUser(index){
  const line =[]
  line.user_id = document.querySelector("#user_id"+index).value
  line.email = document.querySelector("#email"+index).innerHTML
  line.first_name = document.querySelector("#first_name"+index).innerHTML
  line.last_name = document.querySelector("#last_name"+index).innerHTML
  line.administrator_flg = document.querySelector("#administrator_flg"+index).checked

  //編集前の情報を保持する
  tr = document.querySelector("#tr"+index)
  list[index] = tr.innerHTML;
  tr.innerHTML  = "<td><input class=\"input form-control\" type=\"text\" name=\"email"+index+"\" value=\""+line.email+"\"></td>";
  tr.innerHTML += "<td><input class=\"input form-control\" type=\"text\" name=\"first_name"+index+"\" value=\""+line.first_name+"\"></td>";
  tr.innerHTML += "<td><input class=\"input form-control\" type=\"text\" name=\"last_name"+index+"\" value=\""+line.last_name+"\"></td>";
  tr.innerHTML += "<td><input class=\"input form-checkbox\"type=\"checkbox\" name=\"administrator_flg"+index+"\" "+ (line.administrator_flg ? "checked = \"checked\"" :"")+ "></td>";
  tr.innerHTML += "<td><button type=\"button\" class=\"btn btn-secondary\" onclick=\"return btnCancel("+index+")\">戻す</button></td>"
  tr.innerHTML += "<td><button type=\"button\" onclick=\"return editUser("+line.user_id+","+index+")\" class=\"btn btn-primary\" >更新</button></td>"
  tr.innerHTML += "<td></td>"
}

function editUser(user_id,index){
  const form = document.getElementById("form")
  document.getElementById("index").setAttribute("value",index)
  form.setAttribute("action","/editUser/user_id="+user_id)
  form.submit()
}

function btnCancel(index){
  document.getElementById("tr"+index).innerHTML = list[index]
}