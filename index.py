# builtin
import asyncio
# third party
from aioconsole     import ainput
from mcpi.minecraft import Minecraft as MC
# custom
from utils     import cfg, log as rawlog
from selection import Selection, copysel
import commands

mc   = MC.create()
log  = lambda msg: rawlog(mc, msg)
poss = []
sel  = Selection([[[]]], mc)

async def cmdloop() -> None:
    log("Ready")
    while True:
        args = (await ainput()).split(' ')
        if args[0].startswith("__") or not hasattr(commands, args[0]):
            print(f"\x1b[31m{args[0]}: command not found.\x1b[0m")
        else:
            ctx = { "mc": mc, "sel": sel }
            try: getattr(commands, args[0])(ctx, *args[1:])
            except Exception as e: print(f"\x1b[31m{args[0]}: {e}.\x1b[0m")

async def blockhitloop() -> None:
    while True:
        for e in mc.events.pollBlockHits():
            poss.append(e.pos)
            info = f"Endpoint {len(poss)}" if len(poss) < 3 else "Pasting to"
            log(f"{info}: {e.pos.x}, {e.pos.y}, {e.pos.z}")
            if len(poss) == 2:
                log("Copying...")
                global sel
                sel = copysel(poss[0], poss[1], mc)
                log("Done")
            elif len(poss) > 2:
                log("Pasting...")
                sel.paste(poss[2])
                poss.clear()
                log("Done.")
        await asyncio.sleep(0.1)

async def main():
    await asyncio.gather(cmdloop(), blockhitloop())

if __name__ == "__main__": asyncio.run(main())
