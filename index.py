# builtin
import asyncio
# third party
from aioconsole     import ainput
# custom
from utils     import MCP
from selection import copysel
from commands  import getcmd

mc = MCP()

async def cmdloop() -> None:
    mc.log("Ready")
    while True:
        args = (await ainput()).split(' ')
        args[0] = args[0] or "list"
        try:
            cmd = getcmd(args[0])
            if cmd != None: cmd(mc, *args[1:])
        except Exception as e:
            print(f"\x1b[31m{args[0]}: {e}.\x1b[0m")

async def blockhitloop() -> None:
    while True:
        for e in mc.events.pollBlockHits():
            mc.coords.append(e.pos)
            mc.log(f"Selected block at {e.pos.x}, {e.pos.y}, {e.pos.z}")
            if (mc.mode == "normal" or mc.mode == "copy") and len(mc.coords) == 2:
                mc.log("Copying...")
                mc.sel = copysel(*mc.coords, mc)
                mc.done()
                if mc.mode == "copy": mc.coords.clear()
            elif mc.mode == "paste" or (mc.mode == "normal" and len(mc.coords) > 2):
                mc.log("Pasting...")
                mc.sel.paste(mc.coords[2] if mc.mode == "normal" else mc.coords[0])
                mc.coords.clear()
                mc.done()
        await asyncio.sleep(0.1)

async def main() -> None:
    await asyncio.gather(cmdloop(), blockhitloop())

if __name__ == "__main__": asyncio.run(main())
