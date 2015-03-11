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
