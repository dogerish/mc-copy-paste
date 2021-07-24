from utils import getfn, MCP
from selection import readsel

cmds = {}
def getcmd(cmdname: str):
    "Get the command or None if it isn't found"
    if not cmdname in cmds:
        return print(f"\x1b[31m{cmdname}: command not found.\x1b[0m")
    else:
        return cmds[cmdname]

def parse(mc: MCP, string: str, fatal: bool = False) -> None:
    """
    Parse a string fully, running the commands it contains. If fatal is true, any error will be
    printed and stop execution and throw an error. Otherwise, the error message will be printed and
    execution will continue to the next command.
    """
    for line in string.split('\n'):
        for stmt in line.split(';'):
            if not stmt: continue
            args = stmt.split()
            cmd  = getcmd(args[0])
            try:
                if cmd != None: cmd(mc, *args[1:])
            except Exception as e:
                print(f"\x1b[31m{args[0]}: {e}\x1b[0m")
                if fatal: raise e

def mkcmd(cmdname: str):
    "Make a command"
    def mkcmd_dec(cmd):
        cmds[cmdname] = cmd
        return cmd
    return mkcmd_dec

def getdoc(cmdname: str) -> str or None:
    cmd = getcmd(cmdname)
    return cmd and f"{cmdname}\t- {cmd.__doc__.strip()}"

@mkcmd("help")
def h(mc: MCP, cmdname: str = "help") -> None:
    "help <command> | Get help for a command."
    doc = getdoc(cmdname)
    if doc != None: print(doc)

@mkcmd("list")
def l(mc: MCP) -> None:
    "list | List available commands."
    for cmd in cmds: print(getdoc(cmd).split('\n', 1)[0])

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

@mkcmd("source")
def source(mc: MCP, filename: str, fatal: str = None) -> None:
    """
    source <filename> [<fatal>] | Read the file and run the commands inside it.
    If fatal is specified, any errors will stop execution of the rest of the file.
    """
    if filename in mc.source_stack:
        raise Exception(f"Can't source '{filename}' - circular sourcing detected.\nSource stack: {mc.source_stack}")
    mc.source_stack.append(filename)
    with open(filename) as f:
        try:
            parse(mc, f.read(), fatal)
        except Exception as e:
            pass
    mc.source_stack.pop()
