import socket
from pathlib import Path

Path("ip").write_text(socket.gethostbyname(socket.gethostname()))