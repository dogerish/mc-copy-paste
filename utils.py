import json
from mcpi.minecraft import Minecraft as MC
# handle configuration
with open("cfg.json", 'r') as f:
    cfg = json.load(f)

def log(mc: MC, message: str):
    if cfg["verbose"]["console"]: print(message)
    if cfg["verbose"]["game"]:    mc.postToChat(message)
