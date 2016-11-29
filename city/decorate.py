import common
import math
import random
reload(common)

def decorateWithWalls(point):
  size = HOU.Vector3(point.attribValue("size"))
  center = HOU.Vector3(point.position())
  min = center - size / 2
  max = center + size / 2

  WALL_WIDTH = 0.2
  N = GEO.findPointAttrib("N")

  def buildFloor(y, height):
    y_center = min[1] + y + 0.5

    def setTypes(p):
      if (y == int(size[1]) - 1):
        if p is not None:
          p.setAttribValue('type', 'wall_top')
      else:
        if p is not None:
          p.setAttribValue('type', 'wall' + str(height))

    for x in range(int(size[0])):
      x_pos = min[0] + x + 0.5
      x_offset = (size[0] - math.floor(size[0])) / 2.0
      
      p1 = common.createPoint(point)
      p1.setPosition((x_pos + x_offset, y_center, min[2] + WALL_WIDTH / 2))
      
      p2 = common.createPoint(point)
      p2.setPosition((x_pos + x_offset, y_center, max[2] - WALL_WIDTH / 2))
      
      p1.setAttribValue(N, (0.0,0.0,-1.0))
      p2.setAttribValue(N, (0.0,0.0,1.0))

      p1.setAttribValue('size', (1.0, 1.0, WALL_WIDTH))
      p2.setAttribValue('size', (1.0, 1.0, WALL_WIDTH))
      
      setTypes(p1)
      setTypes(p2)

    for z in range(int(size[2])):
      z_pos = min[2] + z + 0.5
      z_offset = ((max[2] - min[2]) - math.floor(max[2] - min[2])) / 2.0
      
      p1 = common.createPoint(point)
      p1.setPosition((min[0] + WALL_WIDTH / 2, y_center, z_pos + z_offset))

      p2 = common.createPoint(point)
      p2.setPosition((max[0] - WALL_WIDTH / 2, y_center, z_pos + z_offset))

      p1.setAttribValue(N, (-1.0,0.0,0.0))
      p2.setAttribValue(N, (1.0,0.0,0.0))

      p1.setAttribValue('size', (1.0, 1.0, WALL_WIDTH))
      p2.setAttribValue('size', (1.0, 1.0, WALL_WIDTH))

      setTypes(p1)
      setTypes(p2)
  
  
  # iterate over floors
  y = 0
  floorHeight = 3
  while y < int(size[1]) - 1:
    while floorHeight > int(size[1]) - 1 - y:
      floorHeight -= 1
    
    if floorHeight > 1 and random.random() < math.sqrt(y / size[1]):
      floorHeight = random.choice([r + 1 for r in range(floorHeight)])

    buildFloor(y, floorHeight)
    y += floorHeight

  buildFloor(int(size[1]) - 1, 1)
  
  
  # build ceiling
  for x in range(int(size[0])):
    x_pos = min[0] + x + 0.5
    x_offset = (size[0] - math.floor(size[0])) / 2.0
    
    for z in range(int(size[2])):
      z_pos = min[2] + z + 0.5
      z_offset = ((max[2] - min[2]) - math.floor(max[2] - min[2])) / 2.0

      p = common.createPoint(point)
      p.setPosition((x_pos + x_offset, max[1], z_pos + z_offset))
      p.setAttribValue('size', (1.0, 0.1, 1.0))


def decorateSpire(point):
  size = HOU.Vector3(point.attribValue("size"))
  center = HOU.Vector3(point.position())
  min = center - size / 2
  max = center + size / 2

  N = GEO.findPointAttrib("N")

  # iterate over floors
  for y in range(int(size[1])):
    y_center = min[1] + y + 0.5

    p = common.createPoint(point)
    p.setPosition((center[0], y_center, center[2]))
    p.setAttribValue('size', (size[0], 1.0, size[2]))
    t = point.attribValue('type')
    if (t == 'spire_upper'):
      p.setAttribValue('type', 'spire_segment')
    else:
      p.setAttribValue('type', 'spire_connection')

def decorateArchTower(point):
  size = HOU.Vector3(point.attribValue("size"))
  center = HOU.Vector3(point.position())
  _min = center - size / 2
  _max = center + size / 2

  for y in range(0,6,2):
    y_center = _min[1] + y + max(0, int(size[1]) - 6) + 0.5

    p = common.createPoint(point)
    p.setPosition((center[0], y_center, center[2]))
    p.setAttribValue('size', (1.0, 1.0, 1.0))
    p.setAttribValue('type', 'arch')

def decorate(point):
  t = point.attribValue('type')
  if (t == 'keep' or t == 'dontkeep' or t == 'tower_lower' or t == 'tower_upper' or t == 'terminal_keep'):
    decorateWithWalls(point)
  elif ("spire" in t):
    decorateSpire(point)
  elif (t == 'arch_tower'):
    decorateArchTower(point)
  else:
    p = common.createPoint(point)