
async function getGallery() {
    let resp = await callEndpoint("GET", "/gallery/get");
    if (resp.ERROR == null) {
        console.log(resp);
    }
}