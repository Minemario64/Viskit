from pathlib import Path
from zipfile import ZipFile
from api.zipping import zipPaths
from api.gentraverse import genLookup
from tqdm import tqdm
import sys

MODE: int = 0
if len(sys.argv) == 2 and (sys.argv[1] == "--keep" or sys.argv[1] == "-k"):
    MODE = 1

def copyFilesRec(dirPath: Path, copyDirPath: Path, excludedNames: list[str] = []) -> None:
    for path in dirPath.iterdir():
        if path.name in excludedNames:
            continue

        if path.is_file():
            mirrorPath: Path = copyDirPath.joinpath(path.name)
            mirrorPath.touch()
            with path.open("rb") as file:
                content: bytes = file.read()

            with mirrorPath.open("wb") as file:
                file.write(content)

        elif path.is_dir():
            mirrorPath: Path = copyDirPath.joinpath(path.name)
            mirrorPath.mkdir()
            copyFilesRec(path, mirrorPath)

def rmFilesRec(dirPath: Path) -> None:
    for path in dirPath.iterdir():
        if path.is_file():
            path.unlink()

        elif path.is_dir():
            rmFilesRec(path)

    dirPath.rmdir()

print(Path.cwd())

ACTIVATE_PATH = Path("api/assets/activate/").resolve()
PROD_PATH = Path.home().joinpath(r"OneDrive - Fulton County Schools\Documents\Code_Projects\Python\ThemeMaker\prod").resolve()
TMP_PATH = Path("tmp/").resolve()
CURZIP_ASSET_PATH = Path("api/assets/cursorSets").resolve()
ROOT_PATH = Path("api/").resolve()

if ACTIVATE_PATH.exists():
    rmFilesRec(ACTIVATE_PATH)

ACTIVATE_PATH.mkdir()
copyFilesRec(PROD_PATH, ACTIVATE_PATH)

if MODE == 1:
    TMP_PATH.mkdir(exist_ok=True)
else:
    TMP_PATH.mkdir()

for dirname in tqdm(genLookup(CURZIP_ASSET_PATH, ['.txt'], ROOT_PATH), "Updating cursor sets"):
    zipPath = CURZIP_ASSET_PATH.joinpath(dirname).joinpath("cursors.zip")
    if not zipPath.exists():
        continue

    if TMP_PATH.joinpath(dirname).exists() and MODE == 1:
        continue

    with ZipFile(zipPath) as zipFile:
        zipFile.extractall(TMP_PATH.joinpath(dirname))

    if TMP_PATH.joinpath(dirname).joinpath("themedata").exists():
        rmFilesRec(TMP_PATH.joinpath(dirname).joinpath("themedata/_internal"))
        TMP_PATH.joinpath(dirname).joinpath("install.bat").unlink(True)
        TMP_PATH.joinpath(dirname).joinpath("uninstall.bat").unlink(True)
        TMP_PATH.joinpath(dirname).joinpath("themedata/_internal").mkdir()
        copyFilesRec(ACTIVATE_PATH.joinpath("themedata/_internal"), TMP_PATH.joinpath(dirname).joinpath("themedata/_internal"))
        copyFilesRec(ACTIVATE_PATH, TMP_PATH.joinpath(dirname), ["themedata"])
        zipPaths(TMP_PATH.joinpath(dirname).iterdir(), zipPath, TMP_PATH.joinpath(dirname))