import matplotlib.pyplot as plt
import matplotlib.patches as patches

from matplotlib.transforms import Bbox, TransformedBbox

# TODO: Study this https://matplotlib.org/stable/tutorials/text/annotations.html#sphx-glr-tutorials-text-annotations-py


def override(d1, **d2):
    """Add key-value pairs to d.

    d1: dictionary
    d2: keyword args to add to d

    returns: new dict
    """
    d = d1.copy()
    d.update(d2)
    return d

def underride(d1, **d2):
    """Add key-value pairs to d only if key is not in d.

    d1: dictionary
    d2: keyword args to add to d

    returns: new dict
    """
    d = d2.copy()
    d.update(d1)
    return d

def diagram(width=5, height=1, **options):
    fig, ax = plt.subplots(**options)

    # TODO: dpi in the notebook should be 100, in the book it should be 300 or 600
    # fig.set_dpi(100)

    # Set figure size
    fig.set_size_inches(width, height)

    plt.rc('font', size=8)

    # Set axes position
    ax.set_position([0, 0, 1, 1])

    # Set x and y limits
    ax.set_xlim(0, width)
    ax.set_ylim(0, height)
    
    # Remove the spines, ticks, and labels
    despine(ax)
    return ax

def despine(ax):
    # Remove the spines
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)

    # Remove the axis labels
    ax.set_xticklabels([])
    ax.set_yticklabels([])

    # Remove the tick marks
    ax.tick_params(axis='both', which='both', length=0, width=0)

def adjust(x, y, bbox):
    """Adjust the coordinates of a point based on a bounding box.
    
    x: x coordinate
    y: y coordinate
    bbox: Bbox object
    
    returns: tuple of coordinates
    """
    width = bbox.width
    height = bbox.height + 0.2
    t = width, height, x - bbox.x0, y - bbox.y0 + 0.1
    return [round(x, 2) for x in t]

def get_bbox(ax, handle):
    bbox = handle.get_window_extent()
    transformed = TransformedBbox(bbox, ax.transData.inverted())
    return transformed

def draw_bbox(ax, bbox, **options):
    options = underride(options, facecolor='gray', alpha=0.1, linewidth=0)
    rect = patches.Rectangle((bbox.xmin, bbox.ymin), bbox.width, bbox.height, **options)
    handle = ax.add_patch(rect)
    bbox = get_bbox(ax, handle)
    return bbox

def draw_box_around(ax, bboxes, **options):
    bbox = Bbox.union(bboxes)
    return draw_bbox(ax, padded(bbox), **options)

def padded(bbox, dx=0.1, dy=0.1):
    """Add padding to a bounding box.
    """
    [x0, y0], [x1, y1] = bbox.get_points()
    return Bbox([[x0-dx, y0-dy], [x1+dx, y1+dy]])

def make_binding(name, value, **options):
    """Make a binding between a name and a value.
    
    name: string
    value: any type

    returns: Binding object
    """
    if not isinstance(value, Frame):
        value = Value(repr(value))

    return Binding(Value(name), value, **options)

def make_mapping(key, value, **options):
    """Make a binding between a key and a value.

    key: any type
    value: any type

    returns: Binding object
    """
    return Binding(Value(repr(key)), Value(repr(value)), **options)

def make_dict(d, name='dict', **options):
    """Make a Frame that represents a dictionary.
    
    d: dictionary
    name: string
    options: passed to Frame
    """
    mappings = [make_mapping(key, value) for key, value in d.items()]
    return Frame(mappings, name=name, **options)

def make_frame(d, name='frame', **options):
    """Make a Frame that represents a stack frame.
    
    d: dictionary
    name: string
    options: passed to Frame
    """
    bindings = [make_binding(key, value) for key, value in d.items()]
    return Frame(bindings, name=name, **options)

class Binding(object):
    def __init__(self, name, value=None, **options):
        """ Represents a binding between a name and a value.

        name: Value object
        value: Value object
        """
        self.name = name
        self.value = value
        self.options = options

    def draw(self, ax, x, y, **options):
        options = override(self.options, **options)
        dx = options.pop('dx', 0.4)
        dy = options.pop('dy', 0)
        draw_value = options.pop('draw_value', True)

        bbox1 = self.name.draw(ax, x, y, ha='right')
        bboxes = [bbox1]

        arrow = Arrow(dx=dx, dy=dy, **options)
        bbox2 = arrow.draw(ax, x, y)

        if draw_value:
            bbox3 = self.value.draw(ax, x+dx, y+dy)
            # only include the arrow if we drew the value
            bboxes.extend([bbox2, bbox3])

        bbox = Bbox.union(bboxes)
        # draw_bbox(ax, self.bbox)
        self.bbox = bbox
        return bbox


class Element(object):
    def __init__(self, index, value, **options):
        """ Represents a an element of a list.

        index: integer
        value: Value object
        """
        self.index = index
        self.value = value
        self.options = options

    def draw(self, ax, x, y, dx=0.15, **options):
        options = override(self.options, **options)
        draw_value = options.pop('draw_value', True)

        bbox1 = self.index.draw(ax, x, y, ha='right', fontsize=6, color='gray')
        bboxes = [bbox1]

        if draw_value:
            bbox2 = self.value.draw(ax, x+dx, y)
            bboxes.append(bbox2)

        bbox = Bbox.union(bboxes)
        self.bbox = bbox
        # draw_bbox(ax, self.bbox)
        return bbox
    

class Value(object):
    def __init__(self, value):
        self.value = value
        self.options = dict(ha='left', va='center')
        self.bbox = None
        
    def draw(self, ax, x, y, **options):
        options = override(self.options, **options)

        handle = ax.text(x, y, self.value, **options)
        bbox = self.bbox = get_bbox(ax, handle)
        # draw_bbox(ax, bbox)
        self.bbox = bbox
        return bbox
    

class Arrow(object):
    def __init__(self, **options):
        # Note for the future about dotted arrows
        # self.arrowprops = dict(arrowstyle="->", ls=':')
        arrowprops = dict(arrowstyle="->", color='gray')
        options = underride(options, arrowprops=arrowprops)
        self.options = options
        
    def draw(self, ax, x, y, **options):
        options = override(self.options, **options)
        dx = options.pop('dx', 0.5)
        dy = options.pop('dy', 0)
        shim = options.pop('shim', 0.02)

        handle = ax.annotate("", [x+dx, y+dy], [x+shim, y], **options)
        bbox = get_bbox(ax, handle)
        self.bbox = bbox
        return bbox
    
    
class ReturnArrow(object):
    def __init__(self, **options):
        style = "Simple, tail_width=0.5, head_width=4, head_length=8"
        options = underride(options, arrowstyle=style, color="gray")
        self.options = options
        
    def draw(self, ax, x, y, **options):
        options = override(self.options, **options)
        value = options.pop('value', None)
        dx = options.pop('dx', 0)
        dy = options.pop('dy', 0.4)
        shim = options.pop('shim', 0.02)

        x += shim
        arrow = patches.FancyArrowPatch((x, y), (x+dx, y+dy),
                             connectionstyle="arc3,rad=.6", **options)
        handle = ax.add_patch(arrow)
        bbox = get_bbox(ax, handle)

        if value is not None:
            handle = plt.text(x+0.15, y+dy/2, str(value), ha='left', va='center')
            bbox2 = get_bbox(ax, handle)
            bbox = Bbox.union([bbox, bbox2])

        self.bbox = bbox
        return bbox
    

class Frame(object):
    def __init__(self, bindings, **options):
        self.bindings = bindings
        self.options = options
        
    def draw(self, ax, x, y, **options):
        options = override(self.options, **options)
        name = options.pop('name', '')
        value = options.pop('value', None)
        dx = options.pop('dx', 0)
        dy = options.pop('dy', 0)
        offsetx = options.pop('offsetx', 0)
        offsety = options.pop('offsety', 0)
        shim = options.pop('shim', 0)
        loc = options.pop('loc', 'top')
        box_around = options.pop('box_around', None)
        
        x += offsetx
        y += offsety
        save_y = y

        if len(self.bindings) == 0:
            bbox = Bbox([[x, y], [x, y]])
            bboxes = [bbox]
        else:
            bboxes = []

        # draw the bindings
        for binding in self.bindings:
            bbox = binding.draw(ax, x, y)
            bboxes.append(bbox)
            x += dx
            y += dy
        
        if box_around:
            bbox1 = draw_bbox(ax, box_around, **options)
        else:   
            bbox1 = draw_box_around(ax, bboxes, **options)
        bboxes.append(bbox1)

        if value is not None:
            arrow = ReturnArrow(value=value)
            x = bbox1.xmax + shim
            bbox2 = arrow.draw(ax, x, save_y, value=value)
            bboxes.append(bbox2)

        if name:
            if loc == 'top':
                x = bbox1.xmin
                y = bbox1.ymax + 0.02
                handle = plt.text(x, y, name, ha='left', va='bottom')
            elif loc == 'left':
                x = bbox1.xmin - 0.1
                y = save_y
                handle = plt.text(x, y, name, ha='right', va='center') 
            bbox3 = get_bbox(ax, handle)
            bboxes.append(bbox3)

        bbox = Bbox.union(bboxes)
        self.bbox = bbox
        return bbox
    

class Stack(object):
    def __init__(self, frames, **options):
        self.frames = frames
        self.options = options
        
    def draw(self, ax, x, y, **options):
        options = override(self.options, **options)
        dx = options.pop('dx', 0)
        dy = options.pop('dy', -0.4)
        
        # draw the frames
        bboxes = []
        for frame in self.frames:
            bbox = frame.draw(ax, x, y)
            bboxes.append(bbox)
            x += dx
            y += dy
        
        bbox = Bbox.union(bboxes)
        self.bbox = bbox
        return bbox
    
def make_rebind(name, seq):
    bindings = []
    for i, value in enumerate(seq):
        dy = dy=-0.3*i
        if i == len(seq)-1:
            binding = make_binding(name, value, dy=dy)
        else:
            arrowprops = dict(arrowstyle="->", color='gray', ls=':')
            binding = make_binding('', value, dy=dy, arrowprops=arrowprops)
        bindings.append(binding)
        
    return bindings

def make_element(index, value):
    return Element(Value(index), Value(repr(value)))

def make_list(seq, name='list', **options):
    elements = [make_element(index, value) for index, value in enumerate(seq)]
    return Frame(elements, name=name, **options)

def draw_bindings(bindings, ax, x, y):
    bboxes = []
    for binding in bindings:
        bbox = binding.draw(ax, x, y)
        bboxes.append(bbox)

    bbox = Bbox.union(bboxes)
    return bbox