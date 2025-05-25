# 11\. 元组

> 原文：[`allendowney.github.io/ThinkPython/chap11.html`](https://allendowney.github.io/ThinkPython/chap11.html)

本章介绍了另一个内建类型——元组，并展示了列表、字典和元组如何协同工作。它还介绍了元组赋值和一个对具有可变长度参数列表的函数非常有用的特性：打包和解包操作符。

在练习中，我们将使用元组以及列表和字典来解决更多的单词谜题，并实现高效的算法。

有一点需要注意：“tuple”有两种发音方式。有些人说“tuh-ple”，与“supple”押韵。但在编程的上下文中，大多数人说“too-ple”，与“quadruple”押韵。

## 11.1\. 元组像列表一样

元组是一个值的序列。这些值可以是任何类型，并且按整数索引，因此元组与列表非常相似。重要的区别是元组是不可变的。

创建元组时，可以编写一个由逗号分隔的值列表。

```py
t = 'l', 'u', 'p', 'i', 'n'
type(t) 
```

```py
tuple 
```

尽管不是必须的，但通常会将元组括在圆括号中。

```py
t = ('l', 'u', 'p', 'i', 'n')
type(t) 
```

```py
tuple 
```

要创建一个包含单一元素的元组，必须包括一个结尾逗号。

```py
t1 = 'p',
type(t1) 
```

```py
tuple 
```

括号中的单个值不是元组。

```py
t2 = ('p')
type(t2) 
```

```py
str 
```

创建元组的另一种方法是使用内建函数`tuple`。如果没有参数，它会创建一个空元组。

```py
t = tuple()
t 
```

```py
() 
```

如果参数是一个序列（字符串、列表或元组），则结果是一个包含序列元素的元组。

```py
t = tuple('lupin')
t 
```

```py
('l', 'u', 'p', 'i', 'n') 
```

因为`tuple`是一个内建函数的名称，所以应该避免将其用作变量名。

大多数列表操作符也适用于元组。例如，方括号操作符可以索引一个元素。

```py
t[0] 
```

```py
'l' 
```

而切片操作符用于选择一系列元素。

```py
t[1:3] 
```

```py
('u', 'p') 
```

`+`操作符用于连接元组。

```py
tuple('lup') + ('i', 'n') 
```

```py
('l', 'u', 'p', 'i', 'n') 
```

`*`操作符将元组重复给定次数。

```py
tuple('spam') * 2 
```

```py
('s', 'p', 'a', 'm', 's', 'p', 'a', 'm') 
```

`sorted`函数也适用于元组——但结果是一个列表，而不是元组。

```py
sorted(t) 
```

```py
['i', 'l', 'n', 'p', 'u'] 
```

`reversed`函数也可以用于元组。

```py
reversed(t) 
```

```py
<reversed at 0x7f23a9a32b60> 
```

结果是一个`reversed`对象，我们可以将其转换为列表或元组。

```py
tuple(reversed(t)) 
```

```py
('n', 'i', 'p', 'u', 'l') 
```

根据目前的例子，元组看起来可能与列表相同。

## 11.2\. 但是元组是不可变的

如果你尝试使用方括号操作符修改元组，会得到一个`TypeError`。

```py
t[0] = 'L' 
```

```py
TypeError: 'tuple' object does not support item assignment 
```

而且元组没有修改列表的任何方法，例如`append`和`remove`。

```py
t.remove('l') 
```

```py
AttributeError: 'tuple' object has no attribute 'remove' 
```

记住，“属性”是与对象相关联的变量或方法——这个错误信息意味着元组没有名为`remove`的方法。

由于元组是不可变的，它们是可哈希的，这意味着它们可以用作字典中的键。例如，下面的字典包含两个作为键的元组，它们映射到整数值。

```py
d = {}
d[1, 2] = 3
d[3, 4] = 7 
```

我们可以像这样在字典中查找元组：

```py
d[1, 2] 
```

```py
3 
```

或者，如果我们有一个指向元组的变量，也可以将其作为键使用。

```py
t = (3, 4)
d[t] 
```

```py
7 
```

元组也可以作为字典中的值出现。

```py
t = tuple('abc')
d = {'key': t}
d 
```

```py
{'key': ('a', 'b', 'c')} 
```

## 11.3\. 元组赋值

你可以在赋值的左边放一个变量元组，在右边放一个值元组。

```py
a, b = 1, 2 
```

值会从左到右赋给变量——在这个例子中，`a`得到值`1`，`b`得到值`2`。我们可以这样展示结果：

```py
a, b 
```

```py
(1, 2) 
```

更一般地说，如果赋值的左边是一个元组，右边可以是任何类型的序列——字符串、列表或元组。例如，要将电子邮件地址拆分成用户名和域名，你可以这样写：

```py
email = 'monty@python.org'
username, domain = email.split('@') 
```

`split`的返回值是一个包含两个元素的列表——第一个元素赋给`username`，第二个赋给`domain`。

```py
username, domain 
```

```py
('monty', 'python.org') 
```

左边的变量数量和右边的值数量必须相同——否则会引发`ValueError`。

```py
a, b = 1, 2, 3 
```

```py
ValueError: too many values to unpack (expected 2) 
```

如果你想交换两个变量的值，元组赋值非常有用。使用常规赋值时，你需要使用临时变量，像这样：

```py
temp = a
a = b
b = temp 
```

这样是可行的，但使用元组赋值我们可以在不使用临时变量的情况下完成相同的操作。

```py
a, b = b, a 
```

之所以可行，是因为右边的所有表达式会在任何赋值操作之前计算。

我们还可以在`for`语句中使用元组赋值。例如，要遍历字典中的项，我们可以使用`items`方法。

```py
d = {'one': 1, 'two': 2}

for item in d.items():
    key, value = item
    print(key, '->', value) 
```

```py
one -> 1
two -> 2 
```

每次循环时，`item`会被赋值为一个包含键和对应值的元组。

我们可以像这样更简洁地写这个循环：

```py
for key, value in d.items():
    print(key, '->', value) 
```

```py
one -> 1
two -> 2 
```

每次循环时，一个键和值会直接赋给`key`和`value`。

## 11.4\. 元组作为返回值

严格来说，一个函数只能返回一个值，但如果这个值是一个元组，效果上就和返回多个值相同。例如，如果你想除以两个整数并计算商和余数，计算`x//y`然后再计算`x%y`效率不高。最好同时计算它们。

内置函数`divmod`接受两个参数，返回一个包含商和余数的元组。

```py
divmod(7, 3) 
```

```py
(2, 1) 
```

我们可以使用元组赋值将元组中的元素存储在两个变量中。

```py
quotient, remainder = divmod(7, 3)
quotient 
```

```py
2 
```

```py
remainder 
```

```py
1 
```

下面是一个返回元组的函数示例。

```py
def min_max(t):
    return min(t), max(t) 
```

`max`和`min`是内置函数，用于找到序列中最大的和最小的元素。`min_max`同时计算并返回一个包含两个值的元组。

```py
min_max([2, 4, 1, 3]) 
```

```py
(1, 4) 
```

我们可以像这样将结果赋给变量：

```py
low, high = min_max([2, 4, 1, 3])
low, high 
```

```py
(1, 4) 
```

## 11.5\. 参数打包

函数可以接受可变数量的参数。以`*`操作符开头的参数名称**打包**参数为元组。例如，下面的函数接受任意数量的参数并计算它们的算术平均值——也就是它们的和除以参数的数量。

```py
def mean(*args):
    return sum(args) / len(args) 
```

参数可以有任何你喜欢的名字，但`args`是惯用的。我们可以像这样调用函数：

```py
mean(1, 2, 3) 
```

```py
2.0 
```

如果你有一个值的序列，并且想将它们作为多个参数传递给一个函数，你可以使用`*`操作符来**解包**元组。例如，`divmod`函数需要两个精确的参数——如果你传递一个元组作为参数，就会报错。

```py
t = (7, 3)
divmod(t) 
```

```py
TypeError: divmod expected 2 arguments, got 1 
```

尽管元组包含两个元素，它仍然被视为一个单独的参数。但如果你解包元组，它会被当作两个参数来处理。

```py
divmod(*t) 
```

```py
(2, 1) 
```

打包和解包可以非常有用，特别是当你想调整一个现有函数的行为时。例如，这个函数接受任意数量的参数，去掉最低和最高的值，然后计算剩余部分的平均值。

```py
def trimmed_mean(*args):
    low, high = min_max(args)
    trimmed = list(args)
    trimmed.remove(low)
    trimmed.remove(high)
    return mean(*trimmed) 
```

首先，它使用`min_max`找到最低和最高的元素。然后，它将`args`转换为列表，这样就可以使用`remove`方法。最后，它解包这个列表，将元素作为单独的参数传递给`mean`，而不是作为一个列表。

这里有一个例子展示了这种影响。

```py
mean(1, 2, 3, 10) 
```

```py
4.0 
```

```py
trimmed_mean(1, 2, 3, 10) 
```

```py
2.5 
```

这种“修剪过的”平均值在一些主观评分的体育项目中使用——比如跳水和体操——用来减少评分偏离其他裁判的影响。

## 11.6\. Zip

元组在遍历两个序列的元素并对对应元素执行操作时非常有用。例如，假设两支队伍进行七场比赛，并且我们将它们的得分记录在两个列表中，每支队伍一个。

```py
scores1 = [1, 2, 4, 5, 1, 5, 2]
scores2 = [5, 5, 2, 2, 5, 2, 3] 
```

让我们看看每个队伍赢了多少场比赛。我们将使用`zip`，这是一个内置函数，它接受两个或多个序列并返回一个**zip 对象**，因为它像拉链的齿一样将序列的元素配对在一起。

```py
zip(scores1, scores2) 
```

```py
<zip at 0x7f23a9a7bdc0> 
```

我们可以使用 zip 对象按对遍历序列中的值。

```py
for pair in zip(scores1, scores2):
     print(pair) 
```

```py
(1, 5)
(2, 5)
(4, 2)
(5, 2)
(1, 5)
(5, 2)
(2, 3) 
```

每次进入循环时，`pair`都会被赋值为一个包含分数的元组。因此，我们可以将分数赋值给变量，并统计第一支队伍的胜利场数，像这样：

```py
wins = 0
for team1, team2 in zip(scores1, scores2):
    if team1 > team2:
        wins += 1

wins 
```

```py
3 
```

可惜的是，第一支队伍只赢了三场比赛并输掉了系列赛。

如果你有两个列表，并且想要一个包含配对元素的列表，可以使用`zip`和`list`。

```py
t = list(zip(scores1, scores2))
t 
```

```py
[(1, 5), (2, 5), (4, 2), (5, 2), (1, 5), (5, 2), (2, 3)] 
```

结果是一个元组列表，因此我们可以像这样获取最后一场比赛的结果：

```py
t[-1] 
```

```py
(2, 3) 
```

如果你有一个键的列表和一个值的列表，可以使用`zip`和`dict`来创建一个字典。例如，下面是我们如何创建一个字典，将每个字母映射到它在字母表中的位置。

```py
letters = 'abcdefghijklmnopqrstuvwxyz'
numbers = range(len(letters))
letter_map = dict(zip(letters, numbers)) 
```

现在我们可以查找一个字母并获取它在字母表中的索引。

```py
letter_map['a'], letter_map['z'] 
```

```py
(0, 25) 
```

在这个映射中，`'a'`的索引是`0`，而`'z'`的索引是`25`。

如果你需要遍历一个序列的元素及其索引，可以使用内置函数`enumerate`。

```py
enumerate('abc') 
```

```py
<enumerate at 0x7f23a808afc0> 
```

结果是一个**enumerate 对象**，它遍历一个由索引（从 0 开始）和给定序列中的元素组成的配对序列。

```py
for index, element in enumerate('abc'):
    print(index, element) 
```

```py
0 a
1 b
2 c 
```

## 11.7\. 比较和排序

关系运算符适用于元组和其他序列。例如，如果你用`<`运算符比较元组，它会先比较每个序列中的第一个元素。如果它们相等，则继续比较第二对元素，以此类推，直到找到一对不同的元素。

```py
(0, 1, 2) < (0, 3, 4) 
```

```py
True 
```

后续的元素不会被考虑——即使它们真的很大。

```py
(0, 1, 2000000) < (0, 3, 4) 
```

```py
True 
```

这种比较元组的方式对于排序元组列表或找到最小值或最大值非常有用。作为示例，让我们找到一个单词中最常见的字母。在前一章中，我们编写了`value_counts`，它接受一个字符串并返回一个字典，该字典将每个字母映射到其出现的次数。

```py
def value_counts(string):
    counter = {}
    for letter in string:
        if letter not in counter:
            counter[letter] = 1
        else:
            counter[letter] += 1
    return counter 
```

这是字符串`'banana'`的结果。

```py
counter = value_counts('banana')
counter 
```

```py
{'b': 1, 'a': 3, 'n': 2} 
```

只有三个项时，我们可以很容易地看到最常见的字母是`'a'`，它出现了三次。但如果有更多项，自动排序将会非常有用。

我们可以像这样从`counter`中获取项。

```py
items = counter.items()
items 
```

```py
dict_items([('b', 1), ('a', 3), ('n', 2)]) 
```

结果是一个`dict_items`对象，它表现得像一个元组列表，因此我们可以像这样对其进行排序。

```py
sorted(items) 
```

```py
[('a', 3), ('b', 1), ('n', 2)] 
```

默认行为是使用每个元组的第一个元素来排序列表，并使用第二个元素来解决相同的情况。

然而，为了找到出现次数最多的项，我们想要使用第二个元素对列表进行排序。我们可以通过编写一个函数来实现，该函数接受一个元组并返回第二个元素。

```py
def second_element(t):
    return t[1] 
```

然后我们可以将该函数作为可选参数`key`传递给`sorted`，该参数表示此函数应用于计算每个项的**排序关键字**。

```py
sorted_items = sorted(items, key=second_element)
sorted_items 
```

```py
[('b', 1), ('n', 2), ('a', 3)] 
```

排序关键字决定了列表中项的顺序。出现次数最少的字母排在前面，出现次数最多的字母排在最后。因此，我们可以像这样找到最常见的字母。

```py
sorted_items[-1] 
```

```py
('a', 3) 
```

如果我们只需要最大值，我们就不必排序列表。我们可以使用`max`，它也接受`key`作为可选参数。

```py
max(items, key=second_element) 
```

```py
('a', 3) 
```

要找到出现次数最少的字母，我们可以用`min`来进行相同的操作。

## 11.8\. 反转字典

假设你想要反转一个字典，以便通过查找一个值来得到对应的键。例如，如果你有一个单词计数器，它将每个单词映射到该单词出现的次数，你可以创建一个字典，将整数映射到出现相应次数的单词。

但是有一个问题——字典中的键必须是唯一的，但值不一定是唯一的。例如，在一个单词计数器中，可能有许多单词的出现次数相同。

所以反转字典的一种方法是创建一个新字典，其中值是原字典中键的列表。作为示例，让我们统计`parrot`中字母的出现次数。

```py
d =  value_counts('parrot')
d 
```

```py
{'p': 1, 'a': 1, 'r': 2, 'o': 1, 't': 1} 
```

如果我们反转这个字典，结果应该是`{1: ['p', 'a', 'o', 't'], 2: ['r']}`，这表示出现一次的字母是`'p'`、`'a'`、`'o'`和`'t'`，出现两次的字母是`'r'`。

以下函数接受一个字典并将其反转为一个新的字典。

```py
def invert_dict(d):
    new = {}
    for key, value in d.items():
        if value not in new:
            new[value] = [key]
        else:
            new[value].append(key)
    return new 
```

`for`语句遍历`d`中的键和值。如果该值尚未在新字典中，则将其添加并与包含单个元素的列表相关联。否则，它将被追加到现有的列表中。

我们可以这样测试它：

```py
invert_dict(d) 
```

```py
{1: ['p', 'a', 'o', 't'], 2: ['r']} 
```

我们得到了预期的结果。

这是我们看到的第一个字典中的值是列表的例子。我们会看到更多类似的例子！

## 11.9\. 调试

列表、字典和元组是**数据结构**。在本章中，我们开始看到复合数据结构，例如元组的列表，或者包含元组作为键和列表作为值的字典。复合数据结构很有用，但容易因数据结构的类型、大小或结构错误而导致错误。例如，如果一个函数期望一个整数列表，而你给它一个普通的整数（不是列表），它可能无法正常工作。

为了帮助调试这些错误，我编写了一个名为`structshape`的模块，它提供了一个同名的函数，可以将任何类型的数据结构作为参数，并返回一个字符串来总结其结构。你可以从[`raw.githubusercontent.com/AllenDowney/ThinkPython/v3/structshape.py`](https://raw.githubusercontent.com/AllenDowney/ThinkPython/v3/structshape.py)下载它。

我们可以这样导入它。

```py
from structshape import structshape 
```

这是一个简单列表的例子。

```py
t = [1, 2, 3]
structshape(t) 
```

```py
'list of 3 int' 
```

这里有一个列表的列表。

```py
t2 = [[1,2], [3,4], [5,6]]
structshape(t2) 
```

```py
'list of 3 list of 2 int' 
```

如果列表中的元素类型不同，`structshape`会按类型将它们分组。

```py
t3 = [1, 2, 3, 4.0, '5', '6', [7], [8], 9]
structshape(t3) 
```

```py
'list of (3 int, float, 2 str, 2 list of int, int)' 
```

这里有一个元组的列表。

```py
s = 'abc'
lt = list(zip(t, s))
structshape(lt) 
```

```py
'list of 3 tuple of (int, str)' 
```

这是一个包含三个项的字典，将整数映射到字符串。

```py
d = dict(lt) 
structshape(d) 
```

```py
'dict of 3 int->str' 
```

如果你在跟踪数据结构时遇到困难，`structshape`可以帮助你。

## 11.10\. 术语表

**打包：** 将多个参数收集到一个元组中。

**解包：** 将元组（或其他序列）视为多个参数。

**zip 对象：** 调用内置函数`zip`的结果，可以用来遍历一系列元组。

**enumerate 对象：** 调用内置函数`enumerate`的结果，可以用来遍历一系列元组。

**排序键：** 用于排序集合元素的值或计算该值的函数。

**数据结构：** 一组有组织的值，用于高效地执行某些操作。

## 11.11\. 练习

```py
# This cell tells Jupyter to provide detailed debugging information
# when a runtime error occurs. Run it before working on the exercises.

%xmode Verbose 
```

```py
Exception reporting mode: Verbose 
```

### 11.11.1\. 向虚拟助手提问

本章中的练习可能比前几章的练习更难，因此我鼓励你向虚拟助手寻求帮助。当你提出更难的问题时，可能会发现答案第一次并不正确，这是一个练习编写良好提示并进行有效跟进的机会。

你可以考虑的一种策略是将一个大问题拆解成可以通过简单函数解决的小问题。让虚拟助手编写这些函数并测试它们。然后，一旦它们工作正常，再请求解决原始问题。

对于下面的一些练习，我会建议使用哪些数据结构和算法。你可能会发现这些建议在解决问题时有用，但它们也是传递给虚拟助手的良好提示。

### 11.11.2\. 练习

在本章中，我提到过元组可以作为字典中的键，因为它们是可哈希的，而它们之所以可哈希，是因为它们是不可变的。但这并不总是正确的。

如果元组包含可变值，例如列表或字典，则该元组不再是可哈希的，因为它包含了不可哈希的元素。举个例子，下面是一个包含两个整数列表的元组。

```py
list0 = [1, 2, 3]
list1 = [4, 5]

t = (list0, list1)
t 
```

```py
([1, 2, 3], [4, 5]) 
```

编写一行代码，将值`6`附加到`t`中第二个列表的末尾。如果你显示`t`，结果应为`([1, 2, 3], [4, 5, 6])`。

尝试创建一个将`t`映射到字符串的字典，并确认你会遇到`TypeError`。

```py
d = {t: 'this tuple contains two lists'} 
```

```py
---------------------------------------------------------------------------
TypeError  Traceback (most recent call last)
Cell In[77], line 1
----> 1 d = {t: 'this tuple contains two lists'}
        d = {1: 'a', 2: 'b', 3: 'c'}
        t = ([1, 2, 3], [4, 5, 6])

TypeError: unhashable type: 'list' 
```

更多关于此主题的内容，可以向虚拟助手询问：“Python 元组总是可哈希的吗？”

### 11.11.3\. 练习

在本章中，我们创建了一个字典，将每个字母映射到它在字母表中的索引。

```py
letters = 'abcdefghijklmnopqrstuvwxyz'
numbers = range(len(letters))
letter_map = dict(zip(letters, numbers)) 
```

例如，`'a'`的索引是`0`。

```py
letter_map['a'] 
```

```py
0 
```

要朝另一个方向移动，我们可以使用列表索引。例如，索引`1`处的字母是`'b'`。

```py
letters[1] 
```

```py
'b' 
```

我们可以使用`letter_map`和`letters`来使用凯撒密码对单词进行编码和解码。

凯撒密码是一种弱加密形式，它通过将每个字母按固定的位移数移动来加密，如果有需要，可以绕回字母表的开头。例如，`'a'`移动 2 位是`'c'`，而`'z'`移动 1 位是`'a'`。

编写一个名为`shift_word`的函数，接受一个字符串和一个整数作为参数，并返回一个新的字符串，其中的字母按给定的位移数移动。

为了测试你的函数，确认“cheer”移动 7 个位置后是“jolly”，而“melon”移动 16 个位置后是“cubed”。

提示：使用模运算符将字母从`'z'`回绕到`'a'`。循环遍历单词中的字母，移动每个字母，并将结果附加到字母列表中。然后使用`join`将字母连接成一个字符串。

### 11.11.4\. 练习

编写一个名为`most_frequent_letters`的函数，该函数接受一个字符串并按频率递减顺序打印字母。

要按递减顺序获取项目，你可以使用`reversed`与`sorted`一起，或者你可以将`reverse=True`作为关键字参数传递给`sorted`。

### 11.11.5\. 练习

在之前的练习中，我们通过对两个单词的字母进行排序并检查排序后的字母是否相同，来判断这两个字符串是否是字谜词。现在让我们让这个问题更具挑战性。

我们将编写一个程序，该程序接受一个单词列表并打印出所有字谜词组。以下是输出可能的示例：

```py
['deltas', 'desalt', 'lasted', 'salted', 'slated', 'staled']
['retainers', 'ternaries']
['generating', 'greatening']
['resmelts', 'smelters', 'termless'] 
```

提示：对于单词列表中的每个单词，先将字母排序，再将其连接回一个字符串。创建一个字典，将这个排序后的字符串映射到与之为字谜词的单词列表。

### 11.11.6\. 练习

编写一个名为`word_distance`的函数，该函数接受两个相同长度的单词，并返回两个单词在多少个位置上有所不同。

提示：使用`zip`函数来遍历单词中字母的对应位置。

### 11.11.7\. 练习

“元音交换”（Metathesis）是指单词中字母的交换。如果你可以通过交换两个字母将一个单词转换成另一个单词，那么这两个单词就是“元音交换对”，例如`converse`和`conserve`。编写一个程序，找出单词列表中的所有元音交换对。

提示：互换对中的单词必须是彼此的字谜词。

致谢：此练习的灵感来源于[`puzzlers.org`](http://puzzlers.org)上的一个示例。

[Think Python: 第三版](https://allendowney.github.io/ThinkPython/index.html)

版权 2024 [Allen B. Downey](https://allendowney.com)

代码许可：[MIT 许可证](https://mit-license.org/)

文本许可：[知识共享署名-非商业性使用-相同方式共享 4.0 国际](https://creativecommons.org/licenses/by-nc-sa/4.0/)
