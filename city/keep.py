import split
import common
import random
reload(split)
reload(common)

def divide(parent, size, iter):
  # choose either X or Z axis
  axis = random.choice([HOU.Vector3(1,0,0), HOU.Vector3(0,0,1)])
  
  if (size[0] > size[2]):
    axis = HOU.Vector3(1,0,0)
  else:
    axis = HOU.Vector3(0,0,1)

  
  # get the length of the axis and find an integer split
  axisLength = axis.dot(size)
  dist = round(0.5 * axisLength)
  u = dist / axisLength

  if (u == 0 or u == 1):
    return dontkeep(parent, size, iter)

  # Take current parent shape and split into 2 bins
  shapes = split.splitn(axis, 2, [u], split.Shape(center=parent.position(), size=size))

  for shape in shapes:
    s = split.Shape(center=shape.center, size=shape.size)
    newHeight = round(random.uniform(0.6, 1.2) * s.size[1])
    # s.size[1] = newHeight

    # create a new point, from the shape, copying attributes from the parent
    p = common.createPoint(parent)
    p.setPosition(s.center - HOU.Vector3(0, s.size[1] / 2, 0) + HOU.Vector3(0, newHeight / 2, 0))
    # p.setPosition(s.center)
    s.size[1] = newHeight
    p.setAttribValue("size", s.size)
    p.setAttribValue("type", "keep")

  GEO.deletePoints([parent])


def tower(parent, size, iter):
  axis = HOU.Vector3(0,1,0)

  # get the length of the axis and find an integer split
  axisLength = axis.dot(size)
  dist = round(0.5 * axisLength)
  u = dist / axisLength

  # Take current parent shape and split into 2 bins
  shapes = split.splitn(axis, 2, [u], split.Shape(center=parent.position(), size=size))

  for s_idx in range(len(shapes)):
    shape = shapes[s_idx]
    s = split.Shape(center=shape.center, size=shape.size)

    # create a new point, from the shape, copying attributes from the parent
    p = common.createPoint(parent)

    if s_idx == 0:
      p.setPosition(s.center)
      p.setAttribValue("size", s.size)
      p.setAttribValue("type", "tower_lower")
    else:
      p.setAttribValue("type", "tower_upper")

      ratio = size[0] / size[2]
      if (0.8 < ratio and ratio < 1.2):
        s.size[0] *= 0.75
        s.size[2] *= 0.75
        p.setAttribValue("size", s.size)
        p.setPosition(s.center)
      else:
        if (size[0] > size[2]):
          s.center[0] -= size[0]/4
          s.size[0] /= 2
        else:
          s.center[2] -= size[2]/4
          s.size[2] /= 2
        
        s.size[0] *= 0.75
        s.size[2] *= 0.75

        p.setAttribValue("size", s.size)
        p.setPosition(s.center)



  GEO.deletePoints([parent])

def dontkeep(parent, size, iter):
  parent.setAttribValue("type", "dontkeep")