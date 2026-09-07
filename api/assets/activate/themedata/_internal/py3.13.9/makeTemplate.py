from pathlib import Path
from typing import Literal
import os

def importFromJSON(filename: str | Path) -> dict:
    from json import load

    filepath = Path(filename) if isinstance(filename, str) else filename
    if filepath.exists():
        with open(filepath, "r") as file:
            return load(file)

    raise FileNotFoundError(f"'{str(filepath)}' does not exist")

templateReplaceKeys: dict[str, str] = {
    "name": r"%__--==(\x1)__--==--__%",
    "wib": r"%__--==(\x2)WIB__--==--__%",
    "mouse": r"%__--==(\x3)MOS__--==--__%",
    "select": r"%__--==(\x4)SEL__--==--__%",
    "text": r"%__--==(\x5)TXT__--==--__%",
    "busy": r"%__--==(\x6)BSY__--==--__%",
    "arrow-all": r"%__--==(\x10)ALL__--==--__%",
    "arrow-nesw": r"%__--==(\x11)NSW_--==--__%",
    "arrow-nwse": r"%__--==(\x12)NSE__--==--__%",
    "arrow-ns": r"%__--==(\x13)NSA__--==--__%",
    "arrow-ew": r"%__--==(\x14)EWA__--==--__%",
    "wallpaper": r"%__--==(\x7)WLL__--==--__%",
    "mode": r"%__--==(\x8)MDE__--==--__%",
    "screensaver": r"%__--==(\x9)SCR__--==--__%",
    "accent": r"%__--==(\xA)CLR__--==--__%"
}

defaultCursorPaths: dict[str, str] = {
    "wib": r"%SystemRoot%\cursors\aero_working.ani",
    "mouse": r"%SystemRoot%\cursors\aero_arrow.cur",
    "select": r"%SystemRoot%\cursors\aero_link.cur",
    "text": r"",
    "busy": r"%SystemRoot%\cursors\aero_busy.ani",
    "arrow-all": r"%SystemRoot%\cursors\aero_move.cur",
    "arrow-nesw": r"%SystemRoot%\cursors\aero_nesw.cur",
    "arrow-nwse": r"%SystemRoot%\cursors\aero_nwse.cur",
    "arrow-ns": r"%SystemRoot%\cursors\aero_ns.cur",
    "arrow-ew": r"%SystemRoot%\cursors\aero_ew.cur"
}

# Colors for decoding Theme color
defaultColor: str = r"#0078D7"
defaultCursor: dict[str, Path] = {key: Path(os.path.expandvars(val)).resolve() for key, val in defaultCursorPaths.items()}
defaultWallpaper: Path = Path(os.path.expandvars(r"%SystemRoot%\web\wallpaper\Windows\img0.jpg")).resolve()

def makeTheme(name: str, cursor: dict[str, Path] | None = None, wallpaper: Path | None = None, mode: Literal['dark', 'light'] = 'light', accentColor: str | None = None, screensaver: Path | None = None) -> None:
    with Path("template.theme").open("r", encoding="utf-8") as file:
        content: str = file.read()

    for replaceKey, replaceVal in zip(templateReplaceKeys.values(), [name] + [val for val in ((defaultCursor | cursor).values() if cursor is not None else defaultCursor.values())] + [defaultWallpaper if wallpaper is None else wallpaper, mode, '' if screensaver is None else screensaver, defaultColor if accentColor is None else accentColor]):
        print(replaceKey, replaceVal)
        if replaceKey == templateReplaceKeys["accent"]:
            replaceVal = f"0XC4{replaceVal.removeprefix("#")}" # type: ignore
            print(f"Transformed Color: {replaceVal}")

        content = content.replace(replaceKey, str(replaceVal.resolve()) if isinstance(replaceVal, Path) else replaceVal)

    filepath: Path = Path("myTheme.theme")
    filepath.touch()
    with filepath.open("w", encoding="utf-8") as file:
        file.write(content)

def makeThemeFromRep(filepath: Path) -> None:
    repPath: Path = filepath.resolve()
    if not repPath.exists():
        raise FileNotFoundError(f"path '{repPath}' does not exist.")

    if not repPath.is_file():
        raise FileNotFoundError(f"path '{repPath}' is a directory.")

    json = importFromJSON(repPath)
    json.pop("pathname")
    absCurPaths: dict[str, Path] = {}

    if json.get("cursor") is not None:
        for key, path in json['cursor'].items():
            if key == "work-in-bg":
                absCurPaths['wib'] = Path(os.path.expandvars(path)).resolve()
                continue

            absCurPaths[key] = Path(os.path.expandvars(path)).resolve()

        json["cursor"] = absCurPaths

    if json.get('wallpaper') is not None:
        json['wallpaper'] = Path(os.path.expandvars(json['wallpaper'])).resolve()

    if json.get("screensaver") is not None:
        json['screensaver'] = Path(os.path.expandvars(json['screensaver'])).resolve()

    makeTheme(**json)
