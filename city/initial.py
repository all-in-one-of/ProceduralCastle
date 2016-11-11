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

# Takes a point and begins splitting recursively over x/z axis until some minimum bin size is hit
# then spawns a box centered at each point parameratized by the point's attributes 
def initializeGroups(parent, size, iter):
    center = HOU.Vector3(GEO.points()[0].attribValue("origin"))
    center[1] = 0
    furthest = min(size[0], size[1]) / 2
    
    # count = random.randint(MIN, MAX)
    # xshapes = split.splitn(HOU.Vector3(1,0,0), count, [random.choice([0.25, 0.5, 0.75]) for x in range(count)], split.Shape(center=parent.position(), size=size))
    # for xshape in xshapes:

    #     count = random.randint(MIN, MAX)
    #     zshapes = split.splitn(HOU.Vector3(0,0,1), count, [random.random() for x in range(count)], xshape)
    #     for zshape in zshapes:

    #         u = random.random()

    #         shape_center = zshape.center
    #         shape_center[1] = 0
    #         dist = center.distanceTo(shape_center)

    #         u = 1 - dist / furthest + random.uniform(-0.2, 0.2)

    #         if u < 0.1:
    #             continue
    #         newHeight = zshape.size[1] * u
    #         newsize = HOU.Vector3(zshape.size)
    #         newsize[1] = newHeight
    #         yshape = split.Shape(center=zshape.center + HOU.Vector3(0,newHeight/2,0), size=newsize)

    #         p = common.createPoint(parent)
    #         p.setPosition(yshape.center)
    #         p.setAttribValue("size", yshape.size)

    #         if yshape.size[1] < HEIGHT0:
    #             p.setAttribValue("type", "level0")
    #         else:
    #             p.setAttribValue("type", "tall")

    def spawnBox(parentsize, parentCenter):
        u = random.random()
        newHeight = size[1] * u
        newsize = HOU.Vector3(parentsize)
        newsize[1] = newHeight
        s = split.Shape(center=parentCenter + HOU.Vector3(0,newHeight/2,0), size=newsize)

        p = common.createPoint(parent)
        p.setPosition(s.center)
        p.setAttribValue("size", s.size)
        p.setAttribValue("type", "level0")

    axis = random.choice([HOU.Vector3(1,0,0), HOU.Vector3(0,0,1)])
    axisLength = axis.dot(size)
    dist = round(0.5 * axisLength)
    u = dist / axisLength

    # If we get to the point where our bins are too small, stop and spawn boxes.
    if u == 1 or u == 0:
        spawnBox(size, parent.position())
        parent.setAttribValue("active", 0)
        return

    # Take current parent shape and split into n bins
    shapes = split.splitn(axis, 2, [u], split.Shape(center=parent.position(), size=size))

    # for each shape 
    for shape in shapes:
        # If we've hit the iteration cap, stop recursing and spawn box, randomizing height
        if iter > 2:
            spawnBox(shape.size, shape.center)

        # Otherwise split more 
        else:
            s = split.Shape(center=shape.center, size=shape.size)
            p2 = common.createPoint(parent)
            p2.setPosition(s.center)
            p2.setAttribValue("size", s.size)
            p2.setAttribValue("type", "initial")

        
        
        
        
        # if random.random() > 0.9:
            
        # else:
        #     p.setAttribValue("type", "level0")


    parent.setAttribValue("active", 0)