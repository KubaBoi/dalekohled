
async function readCamSetts() {
    let resp = await callEndpoint("GET", "/camera/readSettings");
    if (resp.ERROR == null) {
        document.getElementById("shutSpInp").value = resp.SS;
        document.getElementById("briInp").value = resp.BRI;
        document.getElementById("contInp").value = resp.CONT;
    }
    else {
        showErrorAlert(response.ERROR, alertTime);
    }
}

async function capture() {
    await callEndpoint("GET", "/camera/capture");
}

async function setDefault() {
    await callEndpoint("GET", "/camera/setDef");
    readCamSetts();
}

async function changedSetts() {
    let req = {
        "FPS": document.getElementById("fpsInp").value,
        "RES": document.getElementById("resInp").value.split("x"), 
        "ANN": document.getElementById("annInp").value,
        "SS": document.getElementById("shutSpInp").value * 1000, 
        "BRI": document.getElementById("briInp").value, 
        "CONT": document.getElementById("contInp").value, 
        "EXP": document.getElementById("expInp").value, 
        "AWB": document.getElementById("awbInp").value
    };
    
    let resp = await callEndpoint("POST", "/camera/changeSettings", req);
    if (resp.ERROR != null) {
        showErrorAlert(response.ERROR, alertTime);
    }
} 