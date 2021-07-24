# builtin
import asyncio
# third party
from aioconsole     import ainput
# custom
from utils     import cfg, MCP
from selection import copysel
from commands  import parse

mc = MCP()

async def cmdloop() -> None:
    try: parse(mc, cfg["autoexec"], fatal=True)
    except Exception as e:
        print(f"Error in autoexec; quitting.")
        exit(1)
    mc.log("Ready")
    while True: parse(mc, await ainput() or "list")

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
