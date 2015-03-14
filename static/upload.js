
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

    var formData = new FormData($(this)[0]);
    console.log("andy")
    console.log("formData")
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
