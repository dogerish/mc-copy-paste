from utils import getfn, MCP
from selection import readsel

def write(mc: MCP, filename: str) -> None:
    "Write the selction to a file."
    filename = getfn(filename)
    mc.log(f"Saving selection to '{filename}'")
    mc.sel.write(filename)
    mc.done()

def read(mc: MCP, filename: str) -> None:
    "Read a selection from a file"
    filename = getfn(filename)
    mc.log(f"Reading selection from '{filename}'")
    mc.sel = readsel(filename, mc)
    mc.done()
