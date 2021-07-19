from selection      import Selection, readsel
from mcpi.minecraft import Minecraft as MC
from time import sleep
import json

# handle configuration
with open("cfg.json", 'r') as f:
    cfg = json.load(f)

def log(message: str):
    if cfg["verbose"]["console"]: print(message)
    if cfg["verbose"]["game"]:    mc.postToChat(message)

mc   = MC.create()
poss = []
sel  = Selection([[[]]], mc)
log("Ready.")

while True:
    for e in mc.events.pollBlockHits():
        poss.append(e.pos)
        info = f"Endpoint {len(poss)}" if len(poss) < 3 else "Pasting to"
        log(f"{info}: {e.pos.x}, {e.pos.y}, {e.pos.z}")
        if len(poss) == 2:
            log("Copying selection.")
            sel = readsel(poss[0], poss[1], mc)
        elif len(poss) > 2:
            log("Pasting selection.")
            sel.paste(poss[2])
            poss.clear()
    sleep(0.1)
