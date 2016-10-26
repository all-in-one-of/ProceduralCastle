# import HOU
# import GEO

import split
import common
import random
reload(split)
reload(common)

MIN = INPUTS[1].evalParm("min_partitions")
MAX = INPUTS[1].evalParm("max_partitions")
HEIGHT0 = INPUTS[1].evalParm("height_0")

def initializeGroups(parent, size, iter):
    center = HOU.Vector3(parent.attribValue("origin"));
    center[1] = 0
    furthest = min(size[0], size[1]) / 2
    
    count = random.randint(MIN, MAX)
    xshapes = split.splitn(HOU.Vector3(1,0,0), count, [random.random() for x in range(count)], split.Shape(center=parent.position(), size=size))
    for xshape in xshapes:

        count = random.randint(MIN, MAX)
        zshapes = split.splitn(HOU.Vector3(0,0,1), count, [random.random() for x in range(count)], xshape)
        for zshape in zshapes:

            u = random.random()

            shape_center = zshape.center
            shape_center[1] = 0
            dist = center.distanceTo(shape_center)

            u = 1 - dist / furthest + random.uniform(-0.2, 0.2)

            if u < 0.1:
                continue
            newHeight = zshape.size[1] * u
            newSize = HOU.Vector3(zshape.size)
            newSize[1] = newHeight
            yshape = split.Shape(center=zshape.center + HOU.Vector3(0,newHeight/2,0), size=newSize)

            p = common.createPoint(parent)
            p.setPosition(yshape.center)
            p.setAttribValue("size", yshape.size)

            if yshape.size[1] < HEIGHT0:
                p.setAttribValue("type", "level0")
            else:
                p.setAttribValue("type", "tall")

    parent.setAttribValue("active", 0)