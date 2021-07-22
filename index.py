import asyncio
import json
from aioconsole     import ainput
from mcpi.minecraft import Minecraft as MC
from selection      import Selection, copysel
import commands

# handle configuration
with open("cfg.json", 'r') as f:
    cfg = json.load(f)

def log(message: str):
    if cfg["verbose"]["console"]: print(message)
    if cfg["verbose"]["game"]:    mc.postToChat(message)

mc   = MC.create()
poss = []
sel  = Selection([[[]]], mc)

async def cmdloop():
    log("Ready")
    while True:
        args = (await ainput()).split(' ')
        if args[0].startswith("__") or not hasattr(commands, args[0]):
            print(f"\x1b[31m{args[0]}: command not found.\x1b[0m")
        else:
            try: getattr(commands, args[0])(*args[1:])
            except Exception as e: print(f"\x1b[31m{args[0]}: {e}.\x1b[0m")

async def blockhitloop():
    while True:
        for e in mc.events.pollBlockHits():
            poss.append(e.pos)
            info = f"Endpoint {len(poss)}" if len(poss) < 3 else "Pasting to"
            log(f"{info}: {e.pos.x}, {e.pos.y}, {e.pos.z}")
            if len(poss) == 2:
                log("Copying selection.")
                sel = copysel(poss[0], poss[1], mc)
                log("Saving selection...")
                sel.write("sels/sel")
                log("Saved.")
            elif len(poss) > 2:
                log("Pasting selection.")
                sel.paste(poss[2])
                poss.clear()
                log("Pasted.")
        await asyncio.sleep(0.1)

async def main():
    await asyncio.gather(cmdloop(), blockhitloop())

if __name__ == "__main__": asyncio.run(main())
