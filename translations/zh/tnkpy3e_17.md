# 15\. 类与方法

> 原文：[`allendowney.github.io/ThinkPython/chap15.html`](https://allendowney.github.io/ThinkPython/chap15.html)

Python 是一种**面向对象的语言**——也就是说，它提供支持面向对象编程的特性，具有以下这些定义性特征：

+   大部分计算是通过对对象执行操作来表达的。

+   对象通常代表现实世界中的事物，方法通常对应于现实世界中事物之间的交互方式。

+   程序包括类和方法的定义。

例如，在上一章中我们定义了一个`Time`类，它对应了人们记录时间的方式，并且我们定义了对应于人们与时间交互的功能。但`Time`类的定义和接下来的函数定义之间没有明确的联系。我们可以通过将函数重写为**方法**来明确这种联系，方法是在类定义内部定义的。

## 15.1\. 定义方法

在上一章中，我们定义了一个名为`Time`的类，并编写了一个名为`print_time`的函数，用于显示一天中的时间。

```py
class Time:
  """Represents the time of day."""

def print_time(time):
    s = f'{time.hour:02d}:{time.minute:02d}:{time.second:02d}'
    print(s) 
```

为了将`print_time`变成一个方法，我们所需要做的就是将函数定义移到类定义内部。请注意缩进的变化。

同时，我们会将参数名称从`time`改为`self`。这个改变不是必须的，但在方法的第一个参数通常命名为`self`。

```py
class Time:
  """Represents the time of day."""    

    def print_time(self):
        s = f'{self.hour:02d}:{self.minute:02d}:{self.second:02d}'
        print(s) 
```

要调用这个方法，你必须传递一个`Time`对象作为参数。这里是我们用来创建`Time`对象的函数。

```py
def make_time(hour, minute, second):
    time = Time()
    time.hour = hour
    time.minute = minute
    time.second = second
    return time 
```

这里是一个`Time`实例。

```py
start = make_time(9, 40, 0) 
```

现在有两种方式调用`print_time`。第一种（不太常见）是使用函数语法。

```py
Time.print_time(start) 
```

```py
09:40:00 
```

在这个版本中，`Time`是类的名称，`print_time`是方法的名称，`start`作为参数传递。第二种（更符合惯例）是使用方法语法：

```py
start.print_time() 
```

```py
09:40:00 
```

在这个版本中，`start`是调用方法的对象，称为**接收者**，这个术语来源于将方法调用比作向对象发送消息的类比。

不管语法如何，该方法的行为是相同的。接收者被赋值为第一个参数，因此在方法内部，`self`指向与`start`相同的对象。

## 15.2\. 另一种方法

这里是上一章的`time_to_int`函数。

```py
def time_to_int(time):
    minutes = time.hour * 60 + time.minute
    seconds = minutes * 60 + time.second
    return seconds 
```

这里是将其重写为方法的版本。

```py
%%add_method_to Time

    def time_to_int(self):
        minutes = self.hour * 60 + self.minute
        seconds = minutes * 60 + self.second
        return seconds 
```

第一行使用了特殊命令`add_method_to`，它将方法添加到先前定义的类中。此命令在 Jupyter 笔记本中有效，但它不是 Python 的一部分，因此在其他环境中无法使用。通常，类的所有方法都在类定义内部，这样它们与类一起定义。但是为了本书的方便，我们一次定义一个方法。

如同前一个示例，方法定义是缩进的，参数名是`self`。除此之外，方法与函数是相同的。下面是我们如何调用它。

```py
start.time_to_int() 
```

```py
34800 
```

通常我们说“调用”一个函数和“调用”一个方法，但它们的意思是一样的。

## 15.3\. 静态方法

作为另一个示例，假设我们考虑`int_to_time`函数。下面是上一章中的版本。

```py
def int_to_time(seconds):
    minute, second = divmod(seconds, 60)
    hour, minute = divmod(minute, 60)
    return make_time(hour, minute, second) 
```

这个函数接受`seconds`作为参数，并返回一个新的`Time`对象。如果我们将它转换为`Time`类的方法，我们必须在`Time`对象上调用它。但如果我们试图创建一个新的`Time`对象，我们应该在什么上调用它呢？

我们可以通过使用**静态方法**来解决这个鸡生蛋问题，静态方法是一种不需要类的实例即可调用的方法。下面是我们如何将这个函数重写为静态方法。

```py
%%add_method_to Time

    def int_to_time(seconds):
        minute, second = divmod(seconds, 60)
        hour, minute = divmod(minute, 60)
        return make_time(hour, minute, second) 
```

因为它是一个静态方法，所以它没有`self`作为参数。要调用它，我们使用`Time`，即类对象。

```py
start = Time.int_to_time(34800) 
```

结果是一个新对象，表示 9:40。

```py
start.print_time() 
```

```py
09:40:00 
```

既然我们有了`Time.from_seconds`，我们可以利用它将`add_time`写成一个方法。下面是上一章的函数。

```py
def add_time(time, hours, minutes, seconds):
    duration = make_time(hours, minutes, seconds)
    seconds = time_to_int(time) + time_to_int(duration)
    return int_to_time(seconds) 
```

这是重写成方法的版本。

```py
%%add_method_to Time

    def add_time(self, hours, minutes, seconds):
        duration = make_time(hours, minutes, seconds)
        seconds = time_to_int(self) + time_to_int(duration)
        return Time.int_to_time(seconds) 
```

`add_time`有`self`作为参数，因为它不是静态方法。它是一个普通方法——也叫做**实例方法**。要调用它，我们需要一个`Time`实例。

```py
end = start.add_time(1, 32, 0)
print_time(end) 
```

```py
11:12:00 
```

## 15.4\. 比较时间对象

作为另一个示例，假设我们将`is_after`写成一个方法。下面是`is_after`函数，这是上一章练习的一个解答。

```py
def is_after(t1, t2):
    return time_to_int(t1) > time_to_int(t2) 
```

这是作为方法的版本。

```py
%%add_method_to Time

    def is_after(self, other):
        return self.time_to_int() > other.time_to_int() 
```

因为我们在比较两个对象，而第一个参数是`self`，所以我们将第二个参数命名为`other`。要使用这个方法，我们必须在一个对象上调用它，并将另一个对象作为参数传入。

```py
end.is_after(start) 
```

```py
True 
```

这个语法的一个优点是，它几乎像在问一个问题：“`end` 在 `start` 之后吗？”

## 15.5\. `__str__`方法

当你编写方法时，你几乎可以选择任何你想要的名字。然而，某些名字有特殊的含义。例如，如果一个对象有一个名为`__str__`的方法，Python 会使用这个方法将对象转换为字符串。例如，下面是一个时间对象的`__str__`方法。

```py
%%add_method_to Time

    def __str__(self):
        s = f'{self.hour:02d}:{self.minute:02d}:{self.second:02d}'
        return s 
```

这个方法与上一章的`print_time`类似，不同之处在于它返回字符串而不是打印它。

你可以用通常的方式调用这个方法。

```py
end.__str__() 
```

```py
'11:12:00' 
```

但 Python 也可以为你调用它。如果你使用内置函数`str`将一个`Time`对象转换为字符串，Python 会使用`Time`类中的`__str__`方法。

```py
str(end) 
```

```py
'11:12:00' 
```

如果你打印一个`Time`对象，它也会做相同的事情。

```py
print(end) 
```

```py
11:12:00 
```

像`__str__`这样的函数被称为**特殊方法**。你可以通过它们的名字来识别它们，因为它们的名称前后都有两个下划线。

## 15.6\. **init**方法

最特殊的特殊方法是`__init__`，之所以如此称呼，是因为它初始化了新对象的属性。`Time`类的一个`__init__`方法可能是这样的：

```py
%%add_method_to Time

    def __init__(self, hour=0, minute=0, second=0):
        self.hour = hour
        self.minute = minute
        self.second = second 
```

现在，当我们实例化一个`Time`对象时，Python 会调用`__init__`并传递参数。因此，我们可以在创建对象的同时初始化属性。

```py
time = Time(9, 40, 0)
print(time) 
```

```py
09:40:00 
```

在这个例子中，参数是可选的，因此如果你调用`Time`时不传递任何参数，你将获得默认值。

```py
time = Time()
print(time) 
```

```py
00:00:00 
```

如果你提供一个参数，它将覆盖`hour`：

```py
time = Time(9)
print(time) 
```

```py
09:00:00 
```

如果你提供两个参数，它们将覆盖`hour`和`minute`。

```py
time = Time(9, 45)
print(time) 
```

```py
09:45:00 
```

如果你提供三个参数，它们将覆盖所有三个默认值。

当我编写一个新的类时，我几乎总是从编写`__init__`开始，这使得创建对象变得更容易，以及`__str__`，它对于调试非常有用。

## 15.7\. 运算符重载

通过定义其他特殊方法，你可以指定运算符在程序员定义类型上的行为。例如，如果你为`Time`类定义一个名为`__add__`的方法，你就可以在`Time`对象上使用`+`运算符。

这里是一个`__add__`方法。

```py
%%add_method_to Time

    def __add__(self, other):
        seconds = self.time_to_int() + other.time_to_int()
        return Time.int_to_time(seconds) 
```

我们可以像这样使用它。

```py
duration = Time(1, 32)
end = start + duration
print(end) 
```

```py
11:12:00 
```

当我们运行这三行代码时，发生了很多事情：

+   当我们实例化一个`Time`对象时，`__init__`方法被调用。

+   当我们在`Time`对象上使用`+`运算符时，它的`__add__`方法被调用。

+   当我们打印一个`Time`对象时，它的`__str__`方法被调用。

改变运算符的行为，使其与程序员定义的类型一起工作，这被称为**运算符重载**。对于每个运算符，比如`+`，都有一个相应的特殊方法，如`__add__`。

## 15.8\. 调试

如果`minute`和`second`的值在`0`到`60`之间（包括`0`但不包括`60`），并且`hour`是正数，则`Time`对象是有效的。此外，`hour`和`minute`应该是整数，但我们可能允许`second`有小数部分。像这样的要求被称为**不变量**，因为它们应该始终为真。换句话说，如果它们不为真，那就意味着出了问题。

编写代码来检查不变量可以帮助检测错误并找出其原因。例如，你可能有一个名为`is_valid`的方法，它接受一个`Time`对象，如果它违反了不变量，返回`False`。

```py
%%add_method_to Time

    def is_valid(self):
        if self.hour < 0 or self.minute < 0 or self.second < 0:
            return False
        if self.minute >= 60 or self.second >= 60:
            return False
        if not isinstance(self.hour, int):
            return False
        if not isinstance(self.minute, int):
            return False
        return True 
```

然后，在每个方法的开始部分，你可以检查参数，以确保它们是有效的。

```py
%%add_method_to Time

    def is_after(self, other):
        assert self.is_valid(), 'self is not a valid Time'
        assert other.is_valid(), 'self is not a valid Time'
        return self.time_to_int() > other.time_to_int() 
```

`assert`语句会计算后面的表达式。如果结果为`True`，它什么都不做；如果结果为`False`，则会引发`AssertionError`。这里是一个例子。

```py
duration = Time(minute=132)
print(duration) 
```

```py
00:132:00 
```

```py
start.is_after(duration) 
```

```py
AssertionError: self is not a valid Time 
```

`assert`语句很有用，因为它们区分了处理正常情况的代码和检查错误的代码。

## 15.9\. 词汇表

**面向对象语言：** 一种提供支持面向对象编程特性的语言，特别是用户定义类型。

**方法（method）：** 定义在类中的函数，并在该类的实例上调用。

**接收者（receiver）：** 方法所调用的对象。

**静态方法（static method）：** 可以在没有对象作为接收者的情况下调用的方法。

**实例方法（instance method）：** 必须在一个对象上调用的方法。

**特殊方法（special method）：** 改变运算符和某些函数与对象交互方式的方法。

**运算符重载（operator overloading）：** 使用特殊方法改变运算符与用户自定义类型之间的交互方式。

**不变式（invariant）：** 程序执行过程中始终应该为真的条件。

## 15.10\. 练习

```py
# This cell tells Jupyter to provide detailed debugging information
# when a runtime error occurs. Run it before working on the exercises.

%xmode Verbose 
```

### 15.10.1\. 向虚拟助手提问

想了解更多关于静态方法的信息，可以向虚拟助手询问：

+   “实例方法和静态方法有什么区别？”

+   “为什么静态方法被称为静态方法？”

如果你请求虚拟助手生成一个静态方法，结果可能会以`@staticmethod`开头，这是一种“装饰器”，表示这是一个静态方法。本书没有涉及装饰器的内容，但如果你感兴趣，可以向虚拟助手询问更多信息。

在本章中，我们将几个函数重写为方法。虚拟助手通常擅长这种代码转换。举个例子，将以下函数粘贴到虚拟助手中，并询问：“将此函数重写为`Time`类的方法。”

```py
def subtract_time(t1, t2):
    return time_to_int(t1) - time_to_int(t2) 
```

### 15.10.2\. 练习

在上一章中，一系列练习要求你编写一个`Date`类和一些与`Date`对象一起使用的函数。现在，让我们练习将这些函数重写为方法。

1.  编写一个`Date`类的定义，用于表示一个日期——即一个年份、月份和日期。

1.  编写一个`__init__`方法，接受`year`、`month`和`day`作为参数，并将这些参数赋值给属性。创建一个表示 1933 年 6 月 22 日的对象。

1.  编写`__str__`方法，使用 f-string 格式化属性并返回结果。如果你用你创建的`Date`对象进行测试，结果应该是`1933-06-22`。

1.  编写一个名为`is_after`的方法，接受两个`Date`对象，如果第一个对象的日期晚于第二个对象，则返回`True`。创建一个表示 1933 年 9 月 17 日的第二个对象，并检查它是否晚于第一个对象。

提示：你可能会发现编写一个名为`to_tuple`的方法很有用，它返回一个包含`Date`对象属性（以年-月-日顺序）的元组。

[Think Python: 第 3 版](https://allendowney.github.io/ThinkPython/index.html)

版权所有 2024 [Allen B. Downey](https://allendowney.com)

代码许可证：[MIT 许可证](https://mit-license.org/)

文字许可证：[创作共用许可证 署名-非商业性使用-相同方式共享 4.0 国际](https://creativecommons.org/licenses/by-nc-sa/4.0/)
