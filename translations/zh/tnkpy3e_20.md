# 18\. Python 附加功能

> 原文：[`allendowney.github.io/ThinkPython/chap18.html`](https://allendowney.github.io/ThinkPython/chap18.html)

本书的目标之一是尽量少教你 Python。当有两种方法可以做某事时，我选择了一种并避免提到另一种。有时，我会将第二种方法放进练习中。

现在我想回过头去补充一些被遗忘的好点子。Python 提供了一些不是真正必要的功能——你可以不使用它们写出好的代码——但使用它们，你可以写出更简洁、可读或高效的代码，有时甚至是三者兼具。

## 18.1\. 集合

Python 提供了一个名为`set`的类，用于表示一组唯一的元素。要创建一个空集合，我们可以像使用函数一样使用类对象。

```py
s1 = set()
s1 
```

```py
set() 
```

我们可以使用 `add` 方法添加元素。

```py
s1.add('a')
s1.add('b')
s1 
```

```py
{'a', 'b'} 
```

或者我们可以将任何类型的序列传递给 `set`。

```py
s2 = set('acd')
s2 
```

```py
{'a', 'c', 'd'} 
```

一个元素在 `set` 中只能出现一次。如果你添加一个已经存在的元素，它将没有任何效果。

```py
s1.add('a')
s1 
```

```py
{'a', 'b'} 
```

或者，如果你用一个包含重复元素的序列创建一个集合，结果将只包含唯一元素。

```py
set('banana') 
```

```py
{'a', 'b', 'n'} 
```

本书中的一些练习可以通过集合高效简洁地完成。例如，以下是第十一章中的一个练习解决方案，使用字典来检查序列中是否存在重复元素。

```py
def has_duplicates(t):
    d = {}
    for x in t:
        d[x] = True
    return len(d) < len(t) 
```

这个版本将 `t` 中的元素作为字典中的键添加，然后检查键是否比元素少。使用集合，我们可以像这样编写相同的函数。

```py
def has_duplicates(t):
    s = set(t)
    return len(s) < len(t) 
```

一个元素在集合中只能出现一次，因此，如果 `t` 中的某个元素出现多次，集合将比 `t` 小。如果没有重复元素，集合的大小将与 `t` 相同。

`set` 对象提供了一些方法来执行集合操作。例如，`union` 计算两个集合的并集，它是一个包含两个集合中所有元素的新集合。

```py
s1.union(s2) 
```

```py
{'a', 'b', 'c', 'd'} 
```

一些算术运算符可以与集合一起使用。例如，`-` 运算符执行集合差集运算——结果是一个新集合，包含第一个集合中所有*不*在第二个集合中的元素。

```py
s1 - s2 
```

```py
{'b'} 
```

在第十二章中，我们使用字典查找文档中出现但不在单词列表中的单词。我们使用了以下函数，它接收两个字典，并返回一个仅包含第一个字典中不出现在第二个字典中的键的新字典。

```py
def subtract(d1, d2):
    res = {}
    for key in d1:
        if key not in d2:
            res[key] = d1[key]
    return res 
```

使用集合，我们不必自己编写这个函数。如果 `word_counter` 是一个包含文档中唯一单词的字典，`word_list` 是一个有效单词的列表，我们可以像这样计算集合差异。

```py
set(word_counter) - set(word_list) 
```

结果是一个包含文档中未出现在单词列表中的单词的集合。

关系运算符可以与集合一起使用。例如，`<=` 用于检查一个集合是否是另一个集合的子集，包括它们相等的情况。

```py
set('ab') <= set('abc') 
```

```py
True 
```

使用这些运算符，我们可以利用集合来完成第七章的一些练习。例如，下面是一个使用循环的 `uses_only` 版本。

```py
def uses_only(word, available):
    for letter in word: 
        if letter not in available:
            return False
    return True 
```

`uses_only` 检查 `word` 中的所有字母是否都在 `available` 中。使用集合，我们可以像这样重写它。

```py
def uses_only(word, available):
    return set(word) <= set(available) 
```

如果 `word` 中的字母是 `available` 中字母的子集，那么意味着 `word` 只使用了 `available` 中的字母。

## 18.2\. Counters

`Counter` 类似于集合，但如果一个元素出现多次，`Counter` 会记录该元素出现的次数。如果你熟悉数学中的“多重集”概念，那么 `Counter` 就是表示多重集的自然方式。

`Counter` 类定义在一个名为 `collections` 的模块中，因此你需要导入该模块。然后，你可以像使用函数一样使用类对象，并将字符串、列表或其他类型的序列作为参数传递。

```py
from collections import Counter

counter = Counter('banana')
counter 
```

```py
Counter({'a': 3, 'n': 2, 'b': 1}) 
```

```py
from collections import Counter

t = (1, 1, 1, 2, 2, 3)
counter = Counter(t)
counter 
```

```py
Counter({1: 3, 2: 2, 3: 1}) 
```

`Counter` 对象类似于字典，它将每个键映射到该键出现的次数。与字典一样，键必须是可哈希的。

与字典不同，`Counter` 对象在访问不存在的元素时不会引发异常。相反，它会返回 `0`。

```py
counter['d'] 
```

```py
0 
```

我们可以使用 `Counter` 对象来解决第十章的一个练习，该练习要求编写一个函数，接受两个单词并检查它们是否是字母异位词——即，一个单词的字母是否可以重新排列成另一个单词。

这是使用 `Counter` 对象的一个解决方案。

```py
def is_anagram(word1, word2):
    return Counter(word1) == Counter(word2) 
```

如果两个单词是字母异位词，它们包含相同的字母和相同的出现次数，因此它们的 `Counter` 对象是等价的。

`Counter` 提供了一个名为 `most_common` 的方法，它返回一个值-频率对的列表，按出现频率从高到低排序。

```py
counter.most_common() 
```

```py
[(1, 3), (2, 2), (3, 1)] 
```

它们还提供了方法和运算符来执行类似集合的操作，包括加法、减法、并集和交集。例如，`+` 运算符可以将两个 `Counter` 对象合并，创建一个新的 `Counter`，其中包含两个对象的键以及计数的和。

我们可以通过将 `'bans'` 中的字母制作成 `Counter`，并将其添加到 `'banana'` 中的字母来进行测试。

```py
counter2 = Counter('bans')
counter + counter2 
```

```py
Counter({1: 3, 2: 2, 3: 1, 'b': 1, 'a': 1, 'n': 1, 's': 1}) 
```

你将有机会在本章末的练习中探索其他 `Counter` 操作。

## 18.3\. defaultdict

`collections` 模块还提供了 `defaultdict`，它类似于字典，但如果访问一个不存在的键，它会自动生成一个新值。

创建 `defaultdict` 时，你提供一个函数，用于创建新值。创建对象的函数有时被称为**工厂函数**。内置的用于创建列表、集合等类型的函数可以作为工厂函数使用。

例如，下面是一个创建新 `list` 的 `defaultdict`。

```py
from collections import defaultdict

d = defaultdict(list)
d 
```

```py
defaultdict(list, {}) 
```

请注意，参数是 `list`，它是一个类对象，而不是 `list()`，后者是一个函数调用，用来创建一个新列表。工厂函数只有在我们访问一个不存在的键时才会被调用。

```py
t = d['new key']
t 
```

```py
[] 
```

新的列表，我们称之为`t`，也被添加到了字典中。因此，如果我们修改`t`，变动也会出现在`d`中：

```py
t.append('new value')
d['new key'] 
```

```py
['new value'] 
```

如果你正在创建一个包含列表的字典，通常可以使用`defaultdict`编写更简洁的代码。

在第十一章的一个练习中，我创建了一个字典，将已排序的字母字符串映射到可以用这些字母拼写的单词列表。例如，字符串 `'opst'` 映射到列表 `['opts', 'post', 'pots', 'spot', 'stop', 'tops']`。这是原始代码。

```py
def all_anagrams(filename):
    d = {}
    for line in open(filename):
        word = line.strip().lower()
        t = signature(word)
        if t not in d:
            d[t] = [word]
        else:
            d[t].append(word)
    return d 
```

这是一个使用 `defaultdict` 的更简洁版本。

```py
def all_anagrams(filename):
    d = defaultdict(list)
    for line in open(filename):
        word = line.strip().lower()
        t = signature(word)
        d[t].append(word)
    return d 
```

在章节末尾的练习中，你将有机会练习使用`defaultdict`对象。

```py
from collections import defaultdict

d = defaultdict(list)
key = ('into', 'the')
d[key].append('woods')
d[key] 
```

```py
['woods'] 
```

## 18.4\. 条件表达式

条件语句通常用于选择两个值中的一个，例如这样：

```py
if x > 0:
    y = math.log(x)
else:
    y = float('nan') 
```

该语句检查 `x` 是否为正数。如果是，它会计算其对数。如果不是，`math.log` 会引发一个 ValueError。为了避免程序中断，我们生成一个 `NaN`，这是一个表示“非数字”的特殊浮点值。

我们可以通过**条件表达式**更简洁地编写这个语句。

```py
y = math.log(x) if x > 0 else float('nan') 
```

你几乎可以像读英语一样读这行：“`y` 等于 log-`x`，如果 `x` 大于 0；否则它等于 `NaN`”。

递归函数有时可以通过条件表达式简洁地写出来。例如，这是一个带有条件*语句*的 `factorial` 版本。

```py
def factorial(n):
    if n == 0:
        return 1
    else:
        return n * factorial(n-1) 
```

这是一个带有条件*表达式*的版本。

```py
def factorial(n):
    return 1 if n == 0 else n * factorial(n-1) 
```

条件表达式的另一个用途是处理可选参数。例如，这是一个类定义，包含一个使用条件语句来检查带有默认值的参数的 `__init__` 方法。

```py
class Kangaroo:
    def __init__(self, name, contents=None):
        self.name = name
        if contents is None:
            contents = []
        self.contents = contents 
```

这是一个使用条件表达式的版本。

```py
def __init__(self, name, contents=None):
    self.name = name
    self.contents = [] if contents is None else contents 
```

一般来说，如果两个分支都包含单一的表达式且没有语句，可以用条件表达式替代条件语句。

## 18.5\. 列表推导式

在前几章中，我们已经看到一些例子，我们从一个空列表开始，并通过 `append` 方法逐个添加元素。例如，假设我们有一个包含电影标题的字符串，我们想要将所有单词的大写字母进行转换。

```py
title = 'monty python and the holy grail' 
```

我们可以将其拆分成一个字符串列表，遍历这些字符串，进行大写转换，并将它们追加到一个列表中。

```py
t = []
for word in title.split():
    t.append(word.capitalize())

' '.join(t) 
```

```py
'Monty Python And The Holy Grail' 
```

我们可以通过**列表推导式**更简洁地做同样的事情：

```py
t = [word.capitalize() for word in title.split()]

' '.join(t) 
```

```py
'Monty Python And The Holy Grail' 
```

方括号操作符表示我们正在构建一个新列表。括号内的表达式指定了列表的元素，`for` 子句指示我们正在循环遍历的序列。

列表推导式的语法可能看起来很奇怪，因为循环变量—在这个例子中是 `word`—出现在表达式中，而我们还没有看到它的定义。但你会习惯的。

另一个例子是，在第九章中，我们使用这个循环从文件中读取单词并将它们追加到列表中。

```py
word_list = []

for line in open('words.txt'):
    word = line.strip()
    word_list.append(word) 
```

下面是我们如何将其写成列表推导式的方式。

```py
word_list = [line.strip() for line in open('words.txt')] 
```

列表推导式也可以包含一个`if`子句，用来决定哪些元素会被包含在列表中。例如，这里是我们在第十章中使用的一个`for`循环，用于生成`word_list`中所有回文单词的列表。

```py
palindromes = []

for word in word_list:
    if is_palindrome(word):
        palindromes.append(word) 
```

下面是我们如何用列表推导式做同样的事情。

```py
palindromes = [word for word in word_list if is_palindrome(word)] 
```

当列表推导式作为函数的参数时，我们通常可以省略括号。例如，假设我们想要将\(1 / 2^n\)的值加总，其中\(n\)从 0 到 9。我们可以像这样使用列表推导式。

```py
sum([1/2**n for n in range(10)]) 
```

```py
1.998046875 
```

或者我们可以像这样省略括号。

```py
sum(1/2**n for n in range(10)) 
```

```py
1.998046875 
```

在这个例子中，参数严格来说是一个**生成器表达式**，而不是列表推导式，它实际上并没有创建一个列表。但除此之外，行为是一样的。

列表推导式和生成器表达式简洁且易于阅读，至少对于简单的表达式是如此。它们通常比等效的`for`循环更快，有时甚至快得多。所以，如果你生气我没有早点提到它们，我理解。

但为了我的辩护，列表推导式更难调试，因为你不能在循环内部放置`print`语句。我建议你仅在计算足够简单、你很可能第一次就能写对的情况下使用它们。或者考虑先编写并调试一个`for`循环，再将其转换为列表推导式。

## 18.6\. `any`和`all`

Python 提供了一个内置函数`any`，它接受一个布尔值序列，并在其中任何一个值为`True`时返回`True`。

```py
any([False, False, True]) 
```

```py
True 
```

`any`通常与生成器表达式一起使用。

```py
any(letter == 't' for letter in 'monty') 
```

```py
True 
```

这个例子并不是很有用，因为它与`in`运算符做的事情相同。但我们可以使用`any`来为第七章中的一些练习写出简洁的解法。例如，我们可以像这样编写`uses_none`。

```py
def uses_none(word, forbidden):
  """Checks whether a word avoids forbidden letters."""
    return not any(letter in forbidden for letter in word) 
```

这个函数循环遍历`word`中的字母，检查其中是否有字母在`forbidden`中。使用`any`和生成器表达式的结合是高效的，因为一旦找到了`True`值，它就会立即停止，而不必遍历整个序列。

Python 提供了另一个内置函数`all`，它会在序列中的每个元素都为`True`时返回`True`。我们可以使用它来编写`uses_all`的简洁版本。

```py
def uses_all(word, required):
  """Check whether a word uses all required letters."""
    return all(letter in word for letter in required) 
```

使用`any`和`all`表达式可以简洁、高效且易于阅读。

## 18.7\. 命名元组

`collections`模块提供了一个名为`namedtuple`的函数，可以用来创建简单的类。例如，第十六章中的`Point`对象只有两个属性，`x`和`y`。以下是我们如何定义它的。

```py
class Point:
  """Represents a point in 2-D space."""

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f'({self.x}, {self.y})' 
```

这段代码传达了少量信息却包含了很多代码。`namedtuple`提供了一种更简洁的方式来定义像这样的类。

```py
from collections import namedtuple

Point = namedtuple('Point', ['x', 'y']) 
```

第一个参数是你想创建的类的名称，第二个参数是`Point`对象应该拥有的属性列表。结果是一个类对象，这就是为什么它被赋值给一个首字母大写的变量名。

使用`namedtuple`创建的类提供了一个`__init__`方法，用于将值分配给属性，还有一个`__str__`方法，用于以可读的形式显示对象。所以我们可以像这样创建并显示一个`Point`对象。

```py
p = Point(1, 2)
p 
```

```py
Point(x=1, y=2) 
```

`Point`还提供了一个`__eq__`方法，用于检查两个`Point`对象是否相等——也就是说，它们的属性是否相同。

```py
p == Point(1, 2) 
```

```py
True 
```

你可以通过名称或索引访问命名元组的元素。

```py
p.x, p.y 
```

```py
(1, 2) 
```

```py
p[0], p[1] 
```

```py
(1, 2) 
```

你也可以将命名元组当作元组来使用，如下所示的赋值。

```py
x, y = p
x, y 
```

```py
(1, 2) 
```

但`namedtuple`对象是不可变的。属性初始化后，它们不能被更改。

```py
p[0] = 3 
```

```py
TypeError: 'Point' object does not support item assignment 
```

```py
p.x = 3 
```

```py
AttributeError: can't set attribute 
```

`namedtuple`提供了一种快速定义简单类的方法。缺点是简单类有时并不总是保持简单。你可能会决定稍后为命名元组添加方法。在这种情况下，你可以定义一个新类，从命名元组继承。

```py
class Pointier(Point):
  """This class inherits from Point""" 
```

或者到那时你可以切换到常规的类定义。

## 18.8\. 打包关键字参数

在第十一章中，我们写了一个函数，将它的参数打包成一个元组。

```py
def mean(*args):
    return sum(args) / len(args) 
```

你可以用任意数量的参数调用这个函数。

```py
mean(1, 2, 3) 
```

```py
2.0 
```

但`*`运算符并不会打包关键字参数。因此，带有关键字参数调用此函数会导致错误。

```py
mean(1, 2, start=3) 
```

```py
TypeError: mean() got an unexpected keyword argument 'start' 
```

要打包关键字参数，我们可以使用`**`运算符：

```py
def mean(*args, **kwargs):
    print(kwargs)
    return sum(args) / len(args) 
```

关键字打包参数可以使用任何名称，但`kwargs`是常见的选择。结果是一个字典，它将关键字映射到对应的值。

```py
mean(1, 2, start=3) 
```

```py
{'start': 3} 
```

```py
1.5 
```

在这个例子中，`kwargs`的值被打印出来，但除此之外没有任何效果。

但`**`运算符也可以在参数列表中使用，用来解包字典。例如，这是一个`mean`的版本，它打包收到的任何关键字参数，然后将其解包为`sum`的关键字参数。

```py
def mean(*args, **kwargs):
    return sum(args, **kwargs) / len(args) 
```

现在，如果我们以`start`作为关键字参数调用`mean`，它会传递给`sum`，并作为求和的起始点。在下面的例子中，`start=3`在计算平均值之前将`3`加到总和中，所以总和是`6`，结果是`3`。

```py
mean(1, 2, start=3) 
```

```py
3.0 
```

作为另一个例子，如果我们有一个包含`x`和`y`键的字典，我们可以使用解包运算符来创建一个`Point`对象。

```py
d = dict(x=1, y=2)
Point(**d) 
```

```py
Point(x=1, y=2) 
```

如果没有解包运算符，`d`将被视为单个位置参数，因此它被赋值给`x`，我们会得到一个`TypeError`，因为没有第二个参数可以赋值给`y`。

```py
d = dict(x=1, y=2)
Point(d) 
```

```py
TypeError: Point.__new__() missing 1 required positional argument: 'y' 
```

当你处理具有大量关键字参数的函数时，通常创建并传递指定常用选项的字典是很有用的。

```py
def pack_and_print(**kwargs):
    print(kwargs)

pack_and_print(a=1, b=2) 
```

```py
{'a': 1, 'b': 2} 
```

## 18.9\. 调试

在前面的章节中，我们使用`doctest`来测试函数。例如，这里有一个名为`add`的函数，它接受两个数字并返回它们的和。它包含一个`doctest`，检查`2 + 2`是否等于`4`。

```py
def add(a, b):
  '''Add two numbers.

 >>> add(2, 2)
 4
 '''
    return a + b 
```

这个函数接受一个函数对象并运行它的`doctests`。

```py
from doctest import run_docstring_examples

def run_doctests(func):
    run_docstring_examples(func, globals(), name=func.__name__) 
```

所以我们可以像这样测试`add`函数。

```py
run_doctests(add) 
```

没有输出，这意味着所有的测试都通过了。

Python 提供了另一种用于运行自动化测试的工具，称为`unittest`。它的使用稍微复杂一些，但这里有一个例子。

```py
from unittest import TestCase

class TestExample(TestCase):

    def test_add(self):
        result = add(2, 2)
        self.assertEqual(result, 4) 
```

首先，我们导入`TestCase`，这是`unittest`模块中的一个类。为了使用它，我们必须定义一个继承自`TestCase`的新类，并提供至少一个测试方法。测试方法的名称必须以`test`开头，并应表明它测试的是哪个函数。

在这个例子中，`test_add`通过调用`add`函数、保存结果，并调用`assertEqual`来测试`add`函数。`assertEqual`继承自`TestCase`，它接受两个参数并检查它们是否相等。

为了运行这个测试方法，我们必须运行`unittest`中的一个名为`main`的函数，并提供几个关键字参数。以下函数展示了详细信息——如果您有兴趣，可以向虚拟助手询问它是如何工作的。

```py
import unittest

def run_unittest():
    unittest.main(argv=[''], verbosity=0, exit=False) 
```

`run_unittest`不接受`TestExample`作为参数，而是查找继承自`TestCase`的类。然后，它查找以`test`开头的方法并运行它们。这个过程叫做**测试发现**。

下面是我们调用`run_unittest`时发生的情况。

```py
run_unittest() 
```

```py
----------------------------------------------------------------------
Ran 1 test in 0.000s

OK 
```

`unittest.main`报告它运行的测试数量和结果。在这种情况下，`OK`表示测试通过。

为了查看测试失败时发生了什么，我们将向`TestExample`添加一个错误的测试方法。

```py
%%add_method_to TestExample

    def test_add_broken(self):
        result = add(2, 2)
        self.assertEqual(result, 100) 
```

下面是我们运行测试时发生的情况。

```py
run_unittest() 
```

```py
======================================================================
FAIL: test_add_broken (__main__.TestExample)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/tmp/ipykernel_1109857/3833266738.py", line 3, in test_add_broken
    self.assertEqual(result, 100)
AssertionError: 4 != 100

----------------------------------------------------------------------
Ran 2 tests in 0.000s

FAILED (failures=1) 
```

报告包括失败的测试方法和显示失败位置的错误信息。总结部分表明有两个测试被运行，其中一个失败了。

在下面的练习中，我将建议一些提示，您可以用它们向虚拟助手询问关于`unittest`的更多信息。

## 18.10\. 术语表

**工厂：** 用于创建对象的函数，通常作为参数传递给其他函数。

**条件表达式：** 使用条件语句来选择两个值中的一个的表达式。

**列表推导式：** 一种简洁的方式来遍历序列并创建一个列表。

**生成器表达式：** 类似于列表推导式，但它不创建列表。

**测试发现：** 一种用于查找和运行测试的过程。

## 18.11\. 练习

```py
# This cell tells Jupyter to provide detailed debugging information
# when a runtime error occurs. Run it before working on the exercises.

%xmode Verbose 
```

### 18.11.1\. 向虚拟助手提问

本章有一些话题可能您会想了解。

+   “Python 的 set 类有哪些方法和操作符？”

+   “Python 的 Counter 类有哪些方法和操作符？”

+   “Python 的列表推导式和生成器表达式有什么区别？”

+   “什么时候应该使用 Python 的`namedtuple`而不是定义一个新类？”

+   “打包和解包关键字参数有什么用途？”

+   “`unittest`是如何进行测试发现的？”

+   “除了`assertEqual`，`unittest.TestCase`中最常用的方法有哪些？”

+   “`doctest`和`unittest`的优缺点是什么？”

对于以下练习，考虑请求虚拟助手的帮助，但如同往常一样，请记得测试结果。

### 18.11.2\. 练习

第七章中的一个练习要求编写一个名为`uses_none`的函数，它接受一个单词和一串禁用字母，如果单词中不使用任何禁用字母，则返回`True`。以下是一个解决方案。

```py
def uses_none(word, forbidden):
    for letter in word.lower():
        if letter in forbidden.lower():
            return False
    return True 
```

编写这个函数的版本，使用`set`操作代替`for`循环。提示：询问虚拟助手，“如何计算 Python 集合的交集？”

### 18.11.3\. 练习

拼字游戏是一种棋盘游戏，目标是使用字母瓦片拼写单词。例如，如果我们有字母瓦片`T`、`A`、`B`、`L`、`E`，我们可以拼出`BELT`和`LATE`，但是我们无法拼出`BEET`，因为我们没有两个`E`。

编写一个函数，接受一个字母字符串和一个单词，检查这些字母是否能拼出该单词，考虑每个字母出现的次数。

### 18.11.4\. 练习

在第十七章中的一个练习中，我对`has_straightflush`的解决方案使用了以下方法，它将`PokerHand`分成一个包含四手牌的列表，每手牌都包含相同花色的卡牌。

```py
 def partition(self):
  """Make a list of four hands, each containing only one suit."""
        hands = []
        for i in range(4):
            hands.append(PokerHand())

        for card in self.cards:
            hands[card.suit].add_card(card)

        return hands 
```

编写这个函数的简化版本，使用`defaultdict`。

### 18.11.5\. 练习

这是来自第十一章的一个计算斐波那契数的函数。

```py
def fibonacci(n):
    if n == 0:
        return 0

    if n == 1:
        return 1

    return fibonacci(n-1) + fibonacci(n-2) 
```

编写这个函数的版本，使用单个返回语句，使用两个条件表达式，其中一个嵌套在另一个内部。

### 18.11.6\. 练习

以下是一个递归计算二项式系数的函数。

```py
def binomial_coeff(n, k):
  """Compute the binomial coefficient "n choose k".

 n: number of trials
 k: number of successes

 returns: int
 """
    if k == 0:
        return 1

    if n == 0:
        return 0

    return binomial_coeff(n-1, k) + binomial_coeff(n-1, k-1) 
```

使用嵌套条件表达式重写函数主体。

这个函数的效率不高，因为它会不断计算相同的值。通过如第十章所述的记忆化方法，使其更高效。

```py
binomial_coeff(10, 4)    # should be 210 
```

```py
210 
```

### 18.11.7\. 练习

这是来自第十七章中`Deck`类的`__str__`方法。

```py
%%add_method_to Deck

    def __str__(self):
        res = []
        for card in self.cards:
            res.append(str(card))
        return '\n'.join(res) 
```

使用列表推导或生成器表达式编写这个方法的更简洁版本。

[Think Python: 第 3 版](https://allendowney.github.io/ThinkPython/index.html)

版权所有 2024 [Allen B. Downey](https://allendowney.com)

代码许可证：[MIT 许可证](https://mit-license.org/)

文本许可证：[知识共享署名-非商业性使用-相同方式共享 4.0 国际](https://creativecommons.org/licenses/by-nc-sa/4.0/)
