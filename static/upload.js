
//$("submitPhoto").onClick()=uploadPhoto();
function uploadPhoto(){
    console.log('new');
    var content = document.getElementById("form");
    console.log(content);
    $.ajax({
	type: "POST",
	timeout: 50000,
	url: "http://127.0.0.1:5000/photos/",
	data: content,
	success: function (data) {
            alert('success');
            return false;
	}
    });

}


function test(){
    
    console.log($("photo").file);
}

$(document).ready(function () {
    $("#uploadbutton").click(function () {
        var filename = $("#photo").val();

        $.ajax({
            type: "POST",
            url: "http://127.0.0.1:5000/photos/",
            enctype: 'multipart/form-data',
            data: {
                file: filename
            },
            success: function () {
                alert("Data Uploaded: ");
            }
        });
    });
});




$("form#uploadform").submit(function(){

    var formData = new FormData($(this).serialize());
    console.log("andy")
    console.log(formData)
    $.ajax({
        url: "http://127.0.0.1:5000/photos/",
        type: 'POST',
        data: formData,
	enctype: 'multipart/form-data',
        success: function (data) {
            alert(data)
        },
        cache: false,
        contentType: false,
        processData: false
    });

    return false;
});

//$("submitPhoto").onClick()=uploadPhoto();

function uploadPhoto(){
    if (!window.File || !window.FileReader || !window.FileList || !window.Blob) {
      alert('The File APIs are not fully supported in this browser.');
      return;
    }   
    console.log("here");
    input = document.getElementById('imageInput');
    if (!input) {
      alert("Um, couldn't find the fileinput element.");
    }
    else if (!input.files) {
      alert("This browser doesn't seem to support the `files` property of file inputs.");
    }
    else if (!input.files[0]) {
      alert("Please select a file before clicking 'Load'");               
    }
    else {
	console.log("here another");
	var numFiles = $("imageInput").file.length;
	console.log(numFiles);
	file = input.files[0];
	fr = new FileReader();
	fr.onload = receivedText;
	//fr.readAsText(file);
	fr.readAsDataURL(file);
    }

    
}

function receivedText() {           
    //result = fr.result;
    document.getElementById('editor').appendChild(document.createTextNode(fr.result))
}   


