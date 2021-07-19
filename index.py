from selection      import Selection, readsel
from mcpi.minecraft import Minecraft as MC
from time import sleep

mc = MC.create()
mc.postToChat("Connected.")

poss = []

while True:
    for e in mc.events.pollBlockHits():
        poss.append(e.pos)
        mc.postToChat(f"{e.pos.x}, {e.pos.y}, {e.pos.z}")
    if len(poss) >= 2:
        sel = readsel(poss[0], poss[1], mc)
        with open("sel.txt", "w+") as f:
            f.write(str(sel.blocks))
    if len(poss) >= 3:
        sel.paste(poss[2])
    sleep(0.1)
