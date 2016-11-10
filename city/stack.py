
import split

def divide(parent, size, iter):
    shapes = split.splitn(HOU.Vector3(0,1,0), 2, [0.5], split.Shape(center=parent.position(), size=size))

    bottom = shapes[0]
    top = shapes[1]

    parent.setAttribValue("active", 0)
    # GEO.deletePoints([parent])