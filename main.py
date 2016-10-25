import random
import collections

node = hou.pwd()
geo = node.geometry()
inputs = node.inputs()

SEED = inputs[1].evalParm("seed")

geo.createPointGroup("group1")

AXES = [hou.Vector3(1,0,0), hou.Vector3(0,1,0), hou.Vector3(0,0,1)]
GENERATIONS = inputs[1].evalParm("generations")
Shape = collections.namedtuple('Shape', ['center', 'size'])

def makeSeed(*args):
    seed = 0;
    for arg in args:
        seed = seed + abs(arg) + 2 # avoid getting 1's and 0's
    return seed * SEED

def lerp(val1, val2, u):
    return val1 * (1-u) + val2 * u

def split(axis, u, parent, size, iter):
    axis = axis.normalized()
    
    offset1 = hou.Vector3(0,0,0)
    offset2 = hou.Vector3(0,0,0)
    nSize1 = hou.Vector3(size);
    nSize2 = hou.Vector3(size);
    
    min = parent.position() - size / 2
    max = parent.position() + size / 2
       
    center1 = hou.Vector3(parent.position())
    center2 = hou.Vector3(parent.position())
    
    
    for i in range(3):
        nSize1[i] = lerp(size[i], size[i] * u, axis[i])
        nSize2[i] = lerp(size[i], size[i] * (1-u), axis[i])
        center1[i] = lerp(center1[i], axis.dot(lerp(min, max, u)) - nSize1[i] / 2, axis[i])
        center2[i] = lerp(center2[i], axis.dot(lerp(min, max, 1-u)) + nSize1[i] - nSize2[i]/2, axis[i])
            
    return [Shape(center1, nSize1), Shape(center2, nSize2)]
    
    
def randSplit(parent, size, iter):
    axis = random.choice(AXES)
    shapes = split(axis, random.gauss(0.5, 0.15), parent, size, iter)
    for shape in shapes:
        p = geo.createPoint()
        p.setPosition(shape.center)
        p.setAttribValue("size", shape.size)
    return shapes
    
rules = [randSplit]

def replacePoint(parent, size, iter):
    random.seed(makeSeed(parent.number(), iter))
    op = random.choice(rules)
    new_pts = op(parent, size, iter)
    
for iter in range(GENERATIONS):
    points = geo.points()[:]
    
    for point in points:
        replacePoint(point, hou.Vector3(point.attribValue("size")), iter)
        
    geo.deletePoints(points)
