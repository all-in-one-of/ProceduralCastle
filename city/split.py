import collections
import random

import common
reload(common)

Shape = collections.namedtuple('Shape', ['center', 'size'])

def splitn(axis, n, rands, box):
    axis = axis.normalized()

    shapes = [Shape(HOU.Vector3(box.center), HOU.Vector3(box.size)) for x in range(n)]
    
    # get the min/max, keeping only components specified by `axis`
    min = common.compMul3(axis, box.center - box.size / 2) + common.compMul3(HOU.Vector3(1,1,1) - axis, box.center)
    max = common.compMul3(axis, box.center + box.size / 2) + common.compMul3(HOU.Vector3(1,1,1) - axis, box.center)

    binSize = float(1) / (n-1);
    splits = [min]
    for x in range(n-1):
        u = (x + rands[x]) * binSize
        # u = random.uniform((x + 0.3) * binSize, (x+0.7) * binSize) # get random parametrization along axis
        offset = min + common.compMul3(box.size, axis * u)
        splits.append(offset)
    splits.append(max)

    for x in range(n):
        nSize = HOU.Vector3()
        diff = splits[x+1] - splits[x]
        for i in range(3):
            # copy size, but set components specified by axis to the difference between adjacent splits
            nSize[i] = common.lerp(box.size[i], diff[i], axis[i])
        shapes[x] = Shape(center=common.lerp(splits[x], splits[x+1], 0.5), size=nSize)

    return shapes