import math

def cubic_interp(x0, x, y):
    """
    Cubic spline from one-dimensional arrays

    x0: Array of floats to interpolate at
    x : Array of floats in increasing order
    y : Array of floats to interpolate

    Returns array of interpolaated values
    """
    def diff(lst): # numpy-like diff
        size = len(lst) - 1
        r = [0] * size
        for i in range(size): r[i] = lst[i+1] - lst[i] 
        return r
    
    def list_searchsorted(listToInsert, insertInto): # numpy-like searchsorted
        def float_searchsorted(floatToInsert, insertInto):
            for i in range(len(insertInto)):
                if floatToInsert <= insertInto[i]: return i
            return len(insertInto)
        return [float_searchsorted(i, insertInto) for i in listToInsert]
    
    def clip(lst, min_val, max_val, inPlace = False): # numpy-like clip
        if not inPlace: lst = lst[:]  
        for i in range(len(lst)):
            if lst[i] < min_val:
                lst[i] = min_val
            elif lst[i] > max_val:
                lst[i] = max_val  
        return lst
    
    def subtract(a,b):
        return a - b
    
    size = len(x)
    xdiff = diff(x)
    ydiff = diff(y)

    Li   = [0] * size
    Li_1 = [0] * (size - 1)
    z    = [0] * (size)

    Li[0] = math.sqrt(2 * xdiff[0])
    Li_1[0] = 0.0
    B0 = 0.0
    z[0] = B0 / Li[0]

    for i in range(1, size - 1, 1):
        Li_1[i] = xdiff[i-1] / Li[i-1]
        Li[i] = math.sqrt(2 * (xdiff[i-1] + xdiff[i]) - Li_1[i-1] * Li_1[i-1])
        Bi = 6 * (ydiff[i] / xdiff[i] - ydiff[i-1] / xdiff[i-1])
        z[i] = (Bi - Li_1[i-1] * z[i-1]) / Li[i]

    i = size - 1
    Li_1[i-1] = xdiff[-1] / Li[i-1]
    Li[i] = math.sqrt(2 * xdiff[-1] - Li_1[i-1] * Li_1[i-1])
    Bi = 0.0
    z[i] = (Bi - Li_1[i-1] * z[i-1]) / Li[i]

    i = size - 1
    z[i] = z[i] / Li[i]
    for i in range(size - 2, -1, -1):
        z[i] = (z[i] - Li_1[i-1] * z[i+1]) / Li[i]

    index = list_searchsorted(x0, x)
    index = clip(index, 1, size - 1)

    xi1 = [x[num] for num in index]
    xi0 = [x[num-1] for num in index]
    yi1 = [y[num] for num in index]
    yi0 = [y[num-1] for num in index]
    zi1 = [z[num] for num in index]
    zi0 = [z[num-1] for num in index]
    hi1 = list(map(subtract, xi1, xi0) )

    f0 = [0] * len(hi1)
    for j in range(len(f0)):
        f0[j] = zi0[j] / (6 * hi1[j]) * (xi1[j] - x0[j]) ** 3 + \
                zi1[j] / (6 * hi1[j]) * (x0[j] - xi0[j]) ** 3 + \
                (yi1[j] / hi1[j] - zi1[j] * hi1[j] / 6) * (x0[j] - xi0[j]) + \
                (yi0[j] / hi1[j] - zi0[j] * hi1[j] / 6) * (xi1[j] - x0[j])        
    
    return f0