

def lerp(val1, val2, u):
    return val1 * (1-u) + val2 * u

def compMul3(vec1, vec2):
    return HOU.Vector3(vec1[0] * vec2[0], vec1[1] * vec2[1], vec1[2] * vec2[2])

def createPoint(parent):
    p = GEO.createPoint()
    for attrib in GEO.pointAttribs():
        p.setAttribValue(attrib.name(), parent.attribValue(attrib.name()))
    return p