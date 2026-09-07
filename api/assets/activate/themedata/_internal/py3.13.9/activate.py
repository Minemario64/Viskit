print("Running...")

from makeTemplate import makeThemeFromRep, Path, os, importFromJSON
from copy import deepcopy

def exportToJSON(data: dict, filename: str | Path, indent : bool = True) -> None:
    from json import dumps, dump

    filepath = Path(filename) if isinstance(filename, str) else filename
    if filepath.exists():
        if indent:
            with open(filepath, "w") as file:
                file.write(dumps(data, indent=4))
        else:
            with open(filepath, "w") as file:
                dump(data, file)

repPath: Path = Path("../../theme.rep").resolve()
initJSON: dict[str, str | dict[str, str]] = importFromJSON(repPath)
base: dict[str, str | dict[str, str]] = deepcopy(initJSON)
pathname: str = initJSON['pathname'] # type: ignore
themePath: Path = Path("myTheme.theme").resolve()
rootPath: Path = Path("../../../").resolve()
installPathLogPath: Path = Path("installPath").resolve()
normThemePath: Path = Path(os.path.expandvars(fr"%localappdata%\Microsoft\Windows\Themes\curTheme_{pathname.split("/")[-1]}.theme")).resolve()
if initJSON.get("cursor") is not None or initJSON.get("wallpaper") is not None or initJSON.get("screensaver") is not None:
    setPath: Path = Path.home().joinpath(f"Documents/cursors/{pathname}")
    setPath.mkdir(exist_ok=True, parents=True)
    if initJSON.get("cursor") is not None:
        for key, path in initJSON['cursor'].items(): # type: ignore
            with rootPath.joinpath(path).open("rb") as file:
                curContent: bytes = file.read()

            docPath = setPath.joinpath(path)
            docPath.touch()
            with docPath.open("wb") as file:
                file.write(curContent)

            initJSON['cursor'][key] = str(docPath.resolve()) # type: ignore

    if initJSON.get("wallpaper") is not None:
        path = initJSON['wallpaper']
        with rootPath.joinpath(path).open("rb") as file: # type: ignore
            wllContent: bytes = file.read()

            docPath = setPath.joinpath(path) # type: ignore
            docPath.touch()
            with docPath.open("wb") as file:
                file.write(wllContent)

            initJSON['wallpaper'] = str(docPath.resolve()) # type: ignore

    if initJSON.get("screensaver") is not None:
        path = initJSON['screensaver']
        with rootPath.joinpath(path).open("rb") as file: # type: ignore
            wllContent: bytes = file.read()

            docPath = setPath.joinpath(path) # type: ignore
            docPath.touch()
            with docPath.open("wb") as file:
                file.write(wllContent)

            initJSON['screensaver'] = str(docPath.resolve()) # type: ignore

exportToJSON(initJSON, repPath)

if not normThemePath.exists():
    print("Creating Theme Path...")
    makeThemeFromRep(repPath)
    with themePath.open("r", encoding="utf-8") as file:
        content: str = file.read()

    themePath.unlink()
    normThemePath.parent.mkdir(parents=True, exist_ok=True)
    normThemePath.touch()
    with normThemePath.open("w", encoding="utf-8") as file:
        file.write(content)

exportToJSON(base, repPath)

if not installPathLogPath.exists():
    installPathLogPath.touch()

with installPathLogPath.open("w") as log:
    log.write(str(normThemePath.resolve()))

os.startfile(normThemePath.resolve())