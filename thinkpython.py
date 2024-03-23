import contextlib
import io
import re

from IPython.core.magic import register_cell_magic
from IPython.core.magic_arguments import argument, magic_arguments, parse_argstring


def traceback(mode):
    """Set the traceback mode.

    mode: string
    """
    with contextlib.redirect_stdout(io.StringIO()):
        get_ipython().run_cell(f'%xmode {mode}')
    

traceback('Minimal')


def extract_function_name(text):
    """Find a function definition and return its name.

    text: String

    returns: String or None
    """
    pattern = r"def\s+(\w+)\s*\("
    match = re.search(pattern, text)
    if match:
        func_name = match.group(1)
        return func_name
    else:
        return None


@register_cell_magic
def add_method_to(args, cell):

    # get the name of the function defined in this cell
    func_name = extract_function_name(cell)
    if func_name is None:
        return f"This cell doesn't define any new functions."

    # get the class we're adding it to
    namespace = get_ipython().user_ns
    class_name = args
    cls = namespace.get(class_name, None)
    if cls is None:
        return f"Class '{class_name}' not found."

    # save the old version of the function if it was already defined
    old_func = namespace.get(func_name, None)
    if old_func is not None:
        del namespace[func_name]

    # Execute the cell to define the function
    get_ipython().run_cell(cell)

    # get the newly defined function
    new_func = namespace.get(func_name, None)
    if new_func is None:
        return f"This cell didn't define {func_name}."

    # add the function to the class and remove it from the namespace
    setattr(cls, func_name, new_func)
    del namespace[func_name]

    # restore the old function to the namespace
    if old_func is not None:
        namespace[func_name] = old_func

    
@register_cell_magic
def expect_error(line, cell):
    try:
        get_ipython().run_cell(cell)
    except Exception as e:
        get_ipython().run_cell('%tb')



@magic_arguments()
@argument('exception', help='Type of exception to catch')
@register_cell_magic
def expect(line, cell):
    args = parse_argstring(expect, line)
    exception = eval(args.exception)
    try:
        get_ipython().run_cell(cell)
    except exception as e:
        get_ipython().run_cell("%tb")


