import split
import common
import random
reload(split)
reload(common)

def spire(parent, size, iter):
  SPIRE_WIDTH = 2
  N = GEO.findPointAttrib("N")
  if (size[0] > SPIRE_WIDTH and size[2] > SPIRE_WIDTH):
    
    xaxis = HOU.Vector3(1,0,0)
    yaxis = HOU.Vector3(0,1,0)
    zaxis = HOU.Vector3(0,0,1)

    if (size[0] > size[2]):
      axes = [xaxis, zaxis]
    else:
      axes = [zaxis, xaxis]

    axis1Length = axes[0].dot(size)
    u1 = random.choice([ SPIRE_WIDTH / axis1Length, (axis1Length - SPIRE_WIDTH) / axis1Length ])

    axis2Length = axes[1].dot(size)
    u2 = random.choice([ SPIRE_WIDTH / axis2Length, (axis2Length - SPIRE_WIDTH) / axis2Length ])

    shapes = split.splitn(axes[0], 2, [u1], split.Shape(center=parent.position(), size=size))

    side2 = 1 - int(u2 == SPIRE_WIDTH / axis2Length)

    if (u1 == SPIRE_WIDTH / axis1Length): # spire is on the -x side
      shapes[0] = split.splitn(axes[1], 2, [u2], shapes[0])[side2]
      spireBlock = shapes[0]
      boxBlock = shapes[1]
    else: # spire is on the +x side
      shapes[1] = split.splitn(axes[1], 2, [u2], shapes[1])[side2]
      boxBlock = shapes[0]
      spireBlock = shapes[1]

    # get the length of the axis and find an integer split
    axisyLength = yaxis.dot(size)
    dist = round(0.5 * axisyLength)
    u3 = dist / axisyLength

    # Take current parent shape and split into 2 bins
    boxShapes = split.splitn(yaxis, 2, [u3], boxBlock)
    spireShapes = split.splitn(yaxis, 2, [u3], spireBlock)

    p1 = common.createPoint(parent)
    p1.setPosition(boxShapes[0].center)
    p1.setAttribValue("size", boxShapes[0].size)
    p1.setAttribValue("active", 0)

    # p2 = common.createPoint(parent)
    # p2.setPosition(boxShapes[1].center)
    # p2.setAttribValue("size", boxShapes[1].size)
    # p2.setAttribValue("type", "tower_lower")

    p3 = common.createPoint(parent)
    p3.setPosition(spireShapes[0].center)
    p3.setAttribValue("size", spireShapes[0].size)
    p3.setAttribValue("type", "spire_lower")

    p4 = common.createPoint(parent)
    p4.setPosition(spireShapes[1].center)
    p4.setAttribValue("size", spireShapes[1].size)
    p4.setAttribValue("type", "spire_upper")

    norm = -axes[0]
    if (u1 == SPIRE_WIDTH / axis1Length):
      norm = -norm
    p3.setAttribValue(N, norm)
    p4.setAttribValue(N, norm)

    GEO.deletePoints([parent])