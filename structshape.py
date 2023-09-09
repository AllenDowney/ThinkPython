"""
This module provides one function, structshape(), which takes
an object of any type and returns a string that summarizes the
"shape" of the data structure; that is, the type, size and
composition.

Copyright 2012 Allen B. Downey
Distributed under the GNU General Public License at gnu.org/licenses/gpl.html.

"""

def structshape(ds):
    """Returns a string that describes the shape of a data structure.

    ds: any Python object

    Returns: string
    """
    typename = type(ds).__name__

    # handle sequences
    sequence = (list, tuple, set, type(iter('')))
    if isinstance(ds, sequence):
        t = []
        for i, x in enumerate(ds):
            t.append(structshape(x))
        rep = '%s of %s' % (typename, listrep(t))
        return rep

    # handle dictionaries
    elif isinstance(ds, dict):
        keys = set()
        vals = set()
        for k, v in ds.items():
            keys.add(structshape(k))
            vals.add(structshape(v))
        rep = '%s of %d %s->%s' % (typename, len(ds), 
                                   setrep(keys), setrep(vals))
        return rep

    # handle other types
    else:
        if hasattr(ds, '__class__'):
            return ds.__class__.__name__
        else:
            return typename


def listrep(t):
    """Returns a string representation of a list of type strings.

    t: list of strings

    Returns: string
    """
    current = t[0]
    count = 0
    res = []
    for x in t:
        if x == current:
            count += 1
        else:
            append(res, current, count)
            current = x
            count = 1
    append(res, current, count)
    return setrep(res)


def setrep(s):
    """Returns a string representation of a set of type strings.

    s: set of strings

    Returns: string
    """
    rep = ', '.join(s)
    if len(s) == 1:
        return rep
    else:
        return '(' + rep + ')'
    return 


def append(res, typestr, count):
    """Adds a new element to a list of type strings.

    Modifies res.

    res: list of type strings
    typestr: the new type string
    count: how many of the new type there are

    Returns: None
    """
    if count == 1:
        rep = typestr
    else:
        rep = '%d %s' % (count, typestr)
    res.append(rep)


if __name__ == '__main__':

    t = [1,2,3]
    print(structshape(t))

    t2 = [[1,2], [3,4], [5,6]]
    print(structshape(t2))

    t3 = [1, 2, 3, 4.0, '5', '6', [7], [8], 9]
    print(structshape(t3))

    class Point:
        """trivial object type"""

    t4 = [Point(), Point()]
    print(structshape(t4))

    s = set('abc')
    print(structshape(s))

    lt = zip(t, s)
    print(structshape(lt))

    d = dict(lt)        
    print(structshape(d))

    it = iter('abc')
    print(structshape(it))
