node = hou.pwd()
geo = node.geometry()
inputs = node.inputs()

import __builtin__
__builtin__.HOU = hou
__builtin__.GEO = geo
__builtin__.NODE = node
__builtin__.INPUTS = inputs

import random
import city
reload(city)

from city import initial
from city import stack
reload(initial)
reload(stack)

SEED = inputs[1].evalParm("seed")
TYPES = ["initial", "level0", "tall", "box"]
POINT_GROUPS = {}
AXES = [hou.Vector3(1,0,0), hou.Vector3(0,1,0), hou.Vector3(0,0,1)]
GENERATIONS = inputs[1].evalParm("generations")

try:
    geo.addAttrib(hou.attribType.Point, "active", 1)
except hou.OperationFailed:
    pass

try:
    geo.addAttrib(hou.attribType.Point, "Cd", hou.Vector3(1,1,1))
except hou.OperationFailed:
    pass

try:
    geo.addAttrib(hou.attribType.Point, "size", hou.Vector3(10,10,10))
except hou.OperationFailed:
    pass

try:
    geo.addAttrib(hou.attribType.Point, "type", "box")
except hou.OperationFailed:
    pass

try:
    geo.addAttrib(hou.attribType.Point, "origin", hou.Vector3(0,0,0))
except hou.OperationFailed:
    pass

for t in TYPES:
    POINT_GROUPS[t] = geo.createPointGroup(t)

for point in geo.points():
    point.setAttribValue("origin", point.position())
    point.setAttribValue("type", "initial")
    POINT_GROUPS["initial"].add(point)


def makeSeed(*args):
    seed = 0;
    for arg in args:
        seed = seed + abs(arg) + 2 # avoid getting 1's and 0's
    return seed * SEED

RULES = {
    "initial": [initial.initializeGroups],
    "level0": [],
    "tall": [stack.divide],
    "box": []
}

def replacePoint(parent, size, iter):
    random.seed(makeSeed(parent.number(), iter))
    t = point.attribValue("type")
    if t in RULES and point.attribValue("active"):
        if len(RULES[t]):
            op = random.choice(RULES[t])
            new_pts = op(parent, size, iter)


for iter in range(GENERATIONS):
    points = geo.points()[:]
    
    for point in points:
        replacePoint(point, hou.Vector3(point.attribValue("size")), iter)

for point in geo.points():
    t = point.attribValue("type")
    if len(t):
        POINT_GROUPS[t].add(point)