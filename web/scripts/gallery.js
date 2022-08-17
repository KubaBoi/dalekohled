
getGallery();

async function getGallery() {
    let resp = await callEndpoint("GET", "/gallery/get");
    if (resp.ERROR == null) {
        var tbl = document.getElementById("glrTable");
        clearTable(tbl);
        for (let i = 0; i < resp.FILES.length; i++) {
            if (resp.FILES[i] == ".gitkeep") continue;
            addRow(tbl, [
                {"text": `<img src="/gallery/${resp.FILES[i]}>"`}
            ])
        }
    }
}