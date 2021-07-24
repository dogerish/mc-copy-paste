from utils import getfn, MCP
from selection import readsel

cmds = {}
def getcmd(cmdname: str):
    "Get the command or None if it isn't found"
    if not cmdname in cmds:
        return print(f"\x1b[31m{cmdname}: command not found.\x1b[0m")
    else:
        return cmds[cmdname]

def mkcmd(cmdname: str):
    "Make a command"
    def mkcmd_dec(cmd):
        cmds[cmdname] = cmd
        return cmd
    return mkcmd_dec

def getdoc(cmdname: str) -> str or None:
    cmd = getcmd(cmdname)
    return cmd and f"{cmdname}\t- {cmd.__doc__}"

@mkcmd("help")
def h(mc: MCP, cmdname: str = "help") -> None:
    "help <command> | Get help for a command."
    doc = getdoc(cmdname)
    if doc != None: print(doc)

@mkcmd("list")
def l(mc: MCP) -> None:
    "list | List available commands."
    for cmd in cmds: print(getdoc(cmd))

@mkcmd("write")
def w(mc: MCP, filename: str) -> None:
    "write <filename> | Write the selection to a file."
    filename = getfn(filename)
    mc.log(f"Saving selection to '{filename}'")
    mc.sel.write(filename)
    mc.done()

@mkcmd("read")
def r(mc: MCP, filename: str) -> None:
    "read <filename> | Read the selection from a file."
    filename = getfn(filename)
    mc.log(f"Reading selection from '{filename}'")
    mc.sel = readsel(filename, mc)
    mc.done()

@mkcmd("mode")
def setmode(mc: MCP, mode: str = None) -> None:
    "mode <mode> | Sets the mode. Modes include: normal, copy, paste."
    if mode == None:
        mc.log(f"Current mode is '{mc.mode}'.")
        return
    if not mode in ["normal", "copy", "paste"]:
        raise ValueError(f"'{mode}' is not a valid mode.")
    mc.mode = mode
    mc.coords.clear()
    mc.log(f"Set mode to {mc.mode} and cleared stored coordinates.")
