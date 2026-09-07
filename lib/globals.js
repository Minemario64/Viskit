export function addBtnAnim(btn) {
    btn.addEventListener("mousedown", () => {
        btn.style.padding = "7px";
        btn.style.margin = "6px";
    });

    btn.addEventListener('mouseleave', () => {
        btn.style.padding = '10px';
        btn.style.margin = "3px";
    });

    btn.addEventListener('mouseup', () => {
        btn.style.padding = '13px';
        btn.style.margin = "0px";
        setTimeout(() => {
            btn.style.padding = '10px';
            btn.style.margin = '3px';
        }, 150)
    });
}

export const icons = {
    download: new URL("../assets/icons/download-ico.png", import.meta.url),
    applyThemeMaker: new URL("../assets/icons/pic-icon.png", import.meta.url)
}

export const ipLogUrl = new URL("../ip", import.meta.url);

export const zippedThemeDirUrl = new URL("../api/temp/", import.meta.url);

export function initApiRequests(debugCallID) {
    return fetch(ipLogUrl)
    .then(response => {
        if (!response.ok) {
            throw new Error(`Cannot get IP Log (⚠ ${debugCallID} cannot run)`);
        }
        return response.text();
    }).then(text => {
        console.log("IP LOG TRIMMED: ", text.trimEnd());
        return text.trimEnd();
    })
    .then(ip => {
        return {
            wallpaperDownload: (id) => {
                return fetch(`http://${ip}:5000/wallpaper/download/${id}`, {
                    method: "POST",
                    headers: { "Content-Type": "application/json"}
                })
                .then(response => {
                    if (response.status !== 201) {
                        throw Error("Failed to create zip wallpaper");
                    }
                    return response.json();
                })
                .catch(error => {
                    console.error(`Error Downloading Wallpaper (⚠ ${debugCallID}):`, error);
                });
            }
        }
    })
};

export const presetsJSONUrl = new URL("../assets/presets.json", import.meta.url);
export const wallpapersJSONUrl = new URL("../assets/wallpapers.json", import.meta.url);

export const presetsDirUrl = new URL("../assets/themes/presets/", import.meta.url);
export const wallpapersDirUrl = new URL("../assets/themes/wallpapers/", import.meta.url);

export const previewUrl = new URL("../presets/preview/", import.meta.url);

export const envVarPaths = {
    IMG: new URL("../assets/images/", import.meta.url),
    WALLPAPERS: new URL("../assets/themes/wallpapers/", import.meta.url)
}

export function procPathVars(str, nullPath) {
    console.log(str, nullPath);
    switch (str.toUpperCase()) {
        case "$IMG":
            return envVarPaths.IMG

        case "$WALLPAPERS":
            return envVarPaths.WALLPAPERS

        default:
            return nullPath
    }
}

export function processPath(pathStr, basePath) {
    console.log(`PROCPATH(${pathStr}, ${basePath.pathname})`)
    if (pathStr[0] === "$") {
        let parts = pathStr.split(":", 2);
        console.log(parts);
        let dirPath = procPathVars(parts[0], basePath);
        return dirPath.pathname + parts[1];
    } else {
        return basePath.pathname + pathStr;
    }
}

export const possibleThemeAttrs = [
    "bg",
    "accent",
    "mode",
    "cursor", // When there will be a preset theme with a preset cursor theme
    "soundscape" // Will be custom file for all the changed sounds for the theme, will be supported directly in themeMaker
];

export const themeAttrNames = [
    "Background Image",
    "Accent Color",
    "Mode",
    "__undefined_display(CUR)__", // Cursor will be shown a different block, and is not supposed to be like this
    "__undefined_display(SNDSCPE)__" // Soundscape will be shown a different block, and is not supposed to be like this
];

export function themeAttrResolve(themeValue, type) {
    switch (type) {
        case "mode":
            switch (themeValue) {
                case "dark":
                    return "#191919";

                case "light":
                    return "#fff";
            }
            break;

        case "accent":
            switch (themeValue) {
                case "blue":
                    return "#0078d7"
            }
            return themeValue;
    }
}