import {wallpapersJSONUrl, wallpapersDirUrl, processPath, icons, addBtnAnim, initApiRequests, zippedThemeDirUrl} from "../lib/globals.js";
import {getCookie, setCookie} from "../lib/cookies.js"
import {loadJSONRunFunc} from "../lib/json-elements.js";

const container = document.getElementById("wallpapers-container");

function loadCursor(id, name, wallpaperPath, downloadName, apiEndpoints) {
    let block = document.createElement("div");
    block.className = 'block';

    let img = document.createElement("img");
    img.src = wallpaperPath;
    img.style.marginBottom = "7px";
    img.className = "non-cursor";
    img.alt = name;
    img.title = name;
    block.appendChild(img);

    let grid = document.createElement("div");
    grid.className = 'half-bar';

    let downloadImg = document.createElement("img");
    downloadImg.src = icons.download;
    downloadImg.alt = 'Download Wallpaper';
    downloadImg.className = "non-cursor";
    downloadImg.style.width = "20px";

    let applyThemeMakerImg = document.createElement("img");
    applyThemeMakerImg.src = icons.applyThemeMaker;
    applyThemeMakerImg.alt = "Use this wallpaper in a new theme";
    applyThemeMakerImg.className = "non-cursor";
    applyThemeMakerImg.style.width = "20px";

    let downloadBtn = document.createElement("button");
    downloadBtn.title = `Download ${name} Theme`;
    downloadBtn.appendChild(downloadImg);
    addBtnAnim(downloadBtn);
    downloadBtn.addEventListener("click", () => {
        apiEndpoints.wallpaperDownload(id)
        .then((zipPath) => {
            let lnk = document.createElement("a");
            lnk.href = zippedThemeDirUrl.pathname + zipPath.url;
            lnk.download = downloadName;
            document.body.appendChild(lnk);
            lnk.click();
            document.body.removeChild(lnk);
        });
    })

    let applyThemeMakerBtn = document.createElement("button");
    applyThemeMakerBtn.title = 'Use this wallpaper in a theme';
    applyThemeMakerBtn.appendChild(applyThemeMakerImg);
    addBtnAnim(applyThemeMakerBtn);
    applyThemeMakerBtn.addEventListener("click", () => {
        setCookie("wallpaperid", id);
        setCookie("path", "/");
        setTimeout(() => {
            window.location.href = '/';
        }, 500)
    })

    grid.appendChild(downloadBtn);
    grid.appendChild(applyThemeMakerBtn);
    block.appendChild(grid);
    container.appendChild(block);
};

initApiRequests("WALLPAPER-PAGE")
.then(endpointFuncs => {
    console.log(wallpapersJSONUrl);
    loadJSONRunFunc(wallpapersJSONUrl, data => {
        console.log(data);
        data.forEach(element => {
            let wallpaperPath = processPath(element.wallpaper, wallpapersDirUrl);
            console.log(wallpaperPath);
            loadCursor(element.id, element.name, wallpaperPath, element.download, endpointFuncs);
        });
    }, "WALLPAPER-PAGE")
});