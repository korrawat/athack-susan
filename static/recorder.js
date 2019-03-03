var buttonRecord = document.getElementById("record");
var buttonStop = document.getElementById("stop");
var buttonCapture = document.getElementById("capture");

var contrastDown = document.getElementById("ct-down");
var contrastUp = document.getElementById("ct-up");

buttonStop.disabled = true;

contrastDown.onclick = function() {
    console.log('contrast down clicked');

    var xhr = new XMLHttpRequest();

    var cVal = parseFloat(document.getElementById('ct-txt').text).toFixed(2);
    console.log(cVal);
    cVal = cVal - .1;
    cval = cVal.toFixed(2);
    console.log(cVal);
    document.getElementById('ct-txt').text = cVal;

    // XMLHttpRequest
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function() {
        if (xhr.readyState == 4 && xhr.status == 200) {
            // alert(xhr.responseText);
        }
    }
    xhr.open("POST", "/tools");
    xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    xhr.send(JSON.stringify({ ct: cVal, bg: 1, zm: 1 }));

}

contrastUp.onclick = function() {
    console.log('contrast up clicked');

    var cVal = parseFloat(document.getElementById('ct-txt').text);
    console.log(cVal);
    cVal = cVal + .1;
    console.log(cVal)
    cval = parseFloat(cVal).toFixed(2);
    document.getElementById('ct-txt').text = cVal;

}

buttonCapture.onclick = function() {
    console.log("capture clciked");

    // XMLHttpRequest
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function() {
        if (xhr.readyState == 4 && xhr.status == 200) {
            // alert(xhr.responseText);
        }
    }
    xhr.open("POST", "/capture_status");
    xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    xhr.send(JSON.stringify({ status: "true" }));
}

buttonRecord.onclick = function() {
    // var url = window.location.href + "record_status";
    buttonRecord.disabled = true;
    buttonStop.disabled = false;

    // disable download link
    var downloadLink = document.getElementById("download");
    downloadLink.text = "";
    downloadLink.href = "";

    document.getElementById("recording").style.display = "block"

    // XMLHttpRequest
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function() {
        if (xhr.readyState == 4 && xhr.status == 200) {
            // alert(xhr.responseText);
        }
    }
    xhr.open("POST", "/record_status");
    xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    xhr.send(JSON.stringify({ status: "true" }));
};

buttonStop.onclick = function() {
    buttonRecord.disabled = false;
    buttonStop.disabled = true;

    document.getElementById("recording").style.display = "none";


    // XMLHttpRequest
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function() {
        if (xhr.readyState == 4 && xhr.status == 200) {
            // alert(xhr.responseText);

            // enable download link
            var downloadLink = document.getElementById("download");
            downloadLink.text = "Finished Recording";
            // downloadLink.href = "./static/video.avi";
        }
    }
    xhr.open("POST", "/record_status");
    xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    xhr.send(JSON.stringify({ status: "false" }));
};