from mcpi.minecraft import Minecraft
from mcpi.vec3      import Vec3
from mcpi.block     import Block

# a selection - holds block data and relative positions
class Selection:
    def __init__(self, blocks: list, mc: Minecraft):
        self.blocks = blocks
        self.mc     = mc
        self.size   = Vec3(len(self.blocks[0][0]), len(self.blocks[0]), len(self.blocks))

    def paste(self, pos: Vec3) -> None:
        for z in range(self.size.z):
            for y in range(self.size.y):
                for x in range(self.size.x):
                    block = self.blocks[z][y][x]
                    self.mc.setBlock(pos.x + x, pos.y + y, pos.z + z, block.id, block.data)

    def write(self, filename: str) -> None:
        with open(filename, 'w') as f:
            for layer in self.blocks:
                for row in layer:
                    for i, block in enumerate(row):
                        end = '\t' if i < self.size.x - 1 else '\n'
                        f.write(f'{block.id}:{block.data}{end}')
                f.write('\n')

# copies a selection between coordinates a and b in a minecraft session
# arguments after mc (the minecraft connection) are passed to the Selection constructor
def copysel(a: Vec3, b: Vec3, mc: Minecraft, *args, **kwargs) -> Selection:
    blocks = []
    for axis in "xyz":
        aa, ba = getattr(a, axis), getattr(b, axis)
        setattr(a, axis, min(aa, ba))
        setattr(b, axis, max(aa, ba))
    for z in range(b.z - a.z + 1):
        blocks.append([])
        for y in range(b.y - a.y + 1):
            blocks[z].append([])
            for x in range(b.x - a.x + 1):
                blocks[z][y].append(mc.getBlockWithData(a.x + x, a.y + y, a.z + z))
    return Selection(blocks, mc, *args, **kwargs)

# reads a selection from a file
# all arguments after the filename are passed to the Selection constructor
def readsel(filename: str, *args, **kwargs) -> Selection:
    blocks = [[]]
    with open(filename) as f:
        z, y = 0, 0
        for line in f.readlines():
            if line == '\n':
                blocks.append([])
                z += 1
                y = 0
                continue
            blocks[z].append([])
            for block in line.split('\t'):
                bID, bdata = block.split(':')
                blocks[z][y].append(Block(int(bID), int(bdata)))
            y += 1
    blocks.pop() # remove blank one
    return Selection(blocks, *args, **kwargs)
