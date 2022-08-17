
async function readCamSetts() {
    let resp = await callEndpoint("GET", "/camera/readSettings");
    if (resp.ERROR == null) {
        document.getElementById("shutSpInp").value = resp.BRI;
        document.getElementById("briInp").value = resp.BRI;
        document.getElementById("contInp").value = resp.CONT;
    }
    else {
        showErrorAlert(response.ERROR, alertTime);
    }
}

async function capture() {

}