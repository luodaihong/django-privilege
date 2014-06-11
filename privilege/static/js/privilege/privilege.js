/*
 * Privilege APP common javascript function
 * 
 * */

var privilegeGlobal = new Object();

//add permission to group, or remove permission from group
privilegeGlobal.changeGroupPermission = function (clickedObj, groupId, permissionId, targetUrl) {
	var domObj = document.getElementById(groupId + permissionId);
	var backupStatu = false;

	if (clickedObj.checked) { //checked, add permission
		var data = {"group_id": groupId, "permission_id": permissionId, "op_code": "add"};
		var color = "green";
		backupStatu = false;
	} else {
		var data = {"group_id": groupId, "permission_id": permissionId, "op_code": "delete"};
		var color = "#333333";
		backupStatu = true;
	}

	$.ajax({
		type: "POST",
		url: targetUrl,
		async: true,
		data: data,
		success: function(response) {
			if (response.status == "ok") {
				domObj.color = color;
			} else {
				domObj.color = "red";
				clickedObj.checked = backupStatu;
				alert(response.msg);
			}
		},
		error: function(){
			domObj.color = "red";
			clickedObj.checked = backupStatu;
			alert("Error.");
		}
	});
	
}

//check search input whether empty
privilegeGlobal.checkBlank = function (objId) {
	var obj = document.getElementById(objId);
	if (obj.value.length > 0) {
		return true;
	} else {
		$("#" + objId).popover('show');
		setTimeout(function(){
			$("#" + objId).popover('destroy');
		}, 2000);
		return false;
	}
}
