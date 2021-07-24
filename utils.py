import json
from mcpi.minecraft import Minecraft as MC
from selection import Selection

# handle configuration
with open("cfg.json", 'r') as f:
    cfg = json.load(f)

# puts the filename in a dir automatically
getfn = lambda fn: fn if fn[0] == '/' else f"{cfg['seldir']}{fn}"

# Minecraft Copy Paste
class MCP(MC):
    def __init__(self, *args, **kwargs):
        self.__dict__.update(MC.create(*args, **kwargs).__dict__)
        self.mode   = "normal"
        self.sel    = Selection([[[]]], self)
        self.coords = []
        self.source_stack = []

    def log(self, message: str) -> None:
        if cfg["verbose"]["console"]: print(message)
        if cfg["verbose"]["game"]:    self.postToChat(message)

    def done(self) -> None: self.log("Done.")
