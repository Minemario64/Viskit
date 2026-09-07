export const possibleCursorTypes = [
    "mouse",
    "select",
    "busy",
    "text",
    "work-in-bg",
    "arrow-all",
    "arrow-nesw",
    "arrow-nwse",
    "arrow-ns",
    "arrow-ew"
];

export const cursorTypeNames = [
    "Mouse",
    "Select",
    "Busy",
    "Text",
    "Work in Background",
    "Move",
    "Diagonal Arrow 1",
    "Diagonal Arrow 2",
    "Arrow Vertical",
    "Arrow Horizontal"
];

export const globalCursorsJSONUrl = new URL('../Assets/cursors.json', import.meta.url).href;
export const requestCursorsJSONUrl = new URL('../Assets/requested-cursors.json', import.meta.url).href;

export const curImgsDirUrl = new URL('../../api/assets/cursorImgs/', import.meta.url);
export const curSetsDirUrl = new URL("../../api/assets/cursorSets/", import.meta.url);

export const rootUrl = new URL("../../", import.meta.url);

export const mixApiEndpoints = {
    getCursors: 'http://$[IPV4]:5000/curloads/cursors/',
    postMix: 'http://$[IPV4]:5000/curloads/mix'
}