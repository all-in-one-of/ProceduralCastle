import keep
import split
import common
import random
reload(split)
reload(keep)
reload(common)

def makeArch(parent, size, iter):
  # if point.attribValue("type")
  if (size[0] > size[2]):
    axis = HOU.Vector3(1,0,0)
  else:
    axis = HOU.Vector3(0,0,1)

  axisLength = axis.dot(size)
  dist = round(0.5 * axisLength)
  u = dist / axisLength

  if (axisLength < 4):
    return

  shapes = split.splitn(axis, 2, [u], split.Shape(center=parent.position(), size=size))

  tmp_points = []
  for shape in shapes:
    s = split.Shape(center=shape.center, size=shape.size)
    newHeight = round(random.uniform(0.6, 1.2) * s.size[1])
    # s.size[1] = newHeight

    # create a new point, from the shape, copying attributes from the parent
    p = common.createPoint(parent)
    p.setPosition(s.center - HOU.Vector3(0, s.size[1] / 2, 0) + HOU.Vector3(0, newHeight / 2, 0))
    # p.setPosition(s.center)
    s.size[1] = newHeight
    p.setAttribValue("size", s.size - axis * 0.5)
    p.setAttribValue("type", "terminal_keep")
    tmp_points.append(p)
  
  tmp_points[0].setPosition(tmp_points[0].position() - axis * 0.25)
  tmp_points[1].setPosition(tmp_points[1].position() + axis * 0.25)

  min_height = min(tmp_points[0].attribValue('size')[1], tmp_points[1].attribValue('size')[1])
  arch = common.createPoint(parent)
  arch.setAttribValue("size", HOU.Vector3(1, min_height, 1))
  arch.setPosition(
    HOU.Vector3(
      tmp_points[0].position()[0] + (tmp_points[0].attribValue('size')[0] / 2 + 0.5) * axis[0],
      parent.position()[1] - size[1] / 2 + min_height / 2, 
      tmp_points[0].position()[2] + (tmp_points[0].attribValue('size')[2] / 2 + 0.5) * axis[2]
    )
  )
  arch.setAttribValue("type", "arch_tower")

  N = GEO.findPointAttrib("N")
  arch.setAttribValue(N, axis)

  GEO.deletePoints([parent])
