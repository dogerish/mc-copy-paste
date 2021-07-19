from mcpi.minecraft import Minecraft
from mcpi.vec3      import Vec3

# a selection - holds block data and relative positions
class Selection:
    def __init__(self, blocks: list, mc: Minecraft):
        self.blocks = blocks
        self.mc     = mc
        self.size   = Vec3(len(self.blocks), len(self.blocks[0]), len(self.blocks[0][0]))

    def paste(self, pos: Vec3):
        for x in range(self.size.x):
            for y in range(self.size.y):
                for z in range(self.size.z):
                    block = self.blocks[x][y][z]
                    self.mc.setBlock(pos.x + x, pos.y + y, pos.z + z, block.id, block.data)

def readsel(a: Vec3, b: Vec3, mc: Minecraft):
    blocks = []
    if b.x < a.x: a.x, b.x = b.x, a.x
    if b.y < a.y: a.y, b.y = b.y, a.y
    if b.z < a.z: a.z, b.z = b.z, a.z
    for x in range(b.x - a.x + 1):
        blocks.append([])
        for y in range(b.y - a.y + 1):
            blocks[x].append([])
            for z in range(b.z - a.z + 1):
                blocks[x][y].append(mc.getBlockWithData(a.x + x, a.y + y, a.z + z))
    return Selection(blocks, mc)
