# builtin
import asyncio
# third party
from aioconsole     import ainput
# custom
from utils     import MCP
from selection import copysel
import commands

mc = MCP()
async def cmdloop() -> None:
    mc.log("Ready")
    while True:
        args = (await ainput()).split(' ')
        if args[0].startswith("__") or not hasattr(commands, args[0]):
            print(f"\x1b[31m{args[0]}: command not found.\x1b[0m")
        else:
            try: getattr(commands, args[0])(mc, *args[1:])
            except Exception as e: print(f"\x1b[31m{args[0]}: {e}.\x1b[0m")

async def blockhitloop() -> None:
    while True:
        for e in mc.events.pollBlockHits():
            mc.coords.append(e.pos)
            info = f"Endpoint {len(mc.coords)}" if len(mc.coords) < 3 else "Pasting to"
            mc.log(f"{info}: {e.pos.x}, {e.pos.y}, {e.pos.z}")
            if len(mc.coords) == 2:
                mc.log("Copying...")
                mc.sel = copysel(*mc.coords, mc)
                mc.done()
            elif len(mc.coords) > 2:
                mc.log("Pasting...")
                mc.sel.paste(mc.coords[2])
                mc.coords.clear()
                mc.done()
        await asyncio.sleep(0.1)

async def main() -> None:
    await asyncio.gather(cmdloop(), blockhitloop())

if __name__ == "__main__": asyncio.run(main())
