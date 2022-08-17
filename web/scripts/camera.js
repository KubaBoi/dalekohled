
async function readCamSetts() {
    let resp = await callEndpoint("GET", "/camera/readSettings");
    if (resp.ERROR == null) {
        console.log(resp);
    }
    else {
        showErrorAlert(response.ERROR, alertTime);
    }
}

async function capture() {

}