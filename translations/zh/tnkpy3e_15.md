# 13\. 文件与数据库

> 原文：[`allendowney.github.io/ThinkPython/chap13.html`](https://allendowney.github.io/ThinkPython/chap13.html)

我们迄今为止看到的大多数程序都是**临时的**，因为它们运行时间很短，生成输出，但当它们结束时，它们的数据会消失。每次运行临时程序时，它都会从一个干净的状态开始。

其他程序是**持久的**：它们运行时间很长（或者一直运行）；它们将至少一部分数据保存在长期存储中；如果它们关闭并重新启动，它们会从上次停止的地方继续。

程序保持数据的一种简单方式是通过读取和写入文本文件。一个更通用的替代方案是将数据存储在数据库中。数据库是专门的文件，比文本文件更高效地读取和写入，并且提供了额外的功能。

在本章中，我们将编写读取和写入文本文件及数据库的程序，并且作为一个练习，你将编写一个程序，搜索照片集中的重复文件。但在你可以操作文件之前，首先要找到它，因此我们将从文件名、路径和目录开始。

## 13.1\. 文件名和路径

文件被组织成**目录**，也叫做“文件夹”。每个正在运行的程序都有一个**当前工作目录**，这是大多数操作的默认目录。例如，当你打开一个文件时，Python 会在当前工作目录中查找它。

`os`模块提供了用于操作文件和目录的函数（`os`代表“操作系统”）。它提供了一个名为`getcwd`的函数，用于获取当前工作目录的名称。

```py
import os

os.getcwd() 
```

```py
'/home/dinsdale' 
```

本例中的结果是一个名为`dinsdale`的用户的主目录。像`'/home/dinsdale'`这样的字符串，它标识了一个文件或目录，称为**路径**。

像`'memo.txt'`这样的简单文件名也被视为路径，但它是一个**相对路径**，因为它指定了相对于当前目录的文件名。在本例中，当前目录是`/home/dinsdale`，所以`'memo.txt'`等同于完整路径`'/home/dinsdale/memo.txt'`。

以`/`开头的路径不依赖于当前目录——它被称为**绝对路径**。要找到文件的绝对路径，可以使用`abspath`。

```py
os.path.abspath('memo.txt') 
```

```py
'/home/dinsdale/memo.txt' 
```

`os`模块还提供了其他用于操作文件名和路径的函数。`listdir`返回给定目录的内容列表，包括文件和其他目录。下面是列出名为`photos`目录内容的示例。

```py
os.listdir('photos') 
```

```py
['digests.dat',
 'digests.dir',
 'notes.txt',
 'new_notes.txt',
 'mar-2023',
 'digests.bak',
 'jan-2023',
 'feb-2023'] 
```

这个目录包含一个名为`notes.txt`的文本文件和三个目录。目录中包含 JPEG 格式的图像文件。

```py
os.listdir('photos/jan-2023') 
```

```py
['photo3.jpg', 'photo2.jpg', 'photo1.jpg'] 
```

要检查文件或目录是否存在，可以使用`os.path.exists`。

```py
os.path.exists('photos') 
```

```py
True 
```

```py
os.path.exists('photos/apr-2023') 
```

```py
False 
```

要检查路径是否指向文件或目录，我们可以使用`isdir`，它返回`True`如果路径指向一个目录。

```py
os.path.isdir('photos') 
```

```py
True 
```

还有`isfile`，如果路径指向一个文件，它返回`True`。

```py
os.path.isfile('photos/notes.txt') 
```

```py
True 
```

处理路径的一个挑战是，不同操作系统上的路径表示不同。在 macOS 和类似 Linux 的 UNIX 系统中，路径中的目录和文件名是由正斜杠`/`分隔的。Windows 使用反斜杠`\`。因此，如果你在 Windows 上运行这些示例，你会看到路径中的反斜杠，并且你需要将示例中的正斜杠替换为反斜杠。

或者，为了编写在两个系统上都能运行的代码，可以使用`os.path.join`，它将目录和文件名连接成一个路径，使用正斜杠或反斜杠，具体取决于你使用的操作系统。

```py
os.path.join('photos', 'jan-2023', 'photo1.jpg') 
```

```py
'photos/jan-2023/photo1.jpg' 
```

在本章稍后，我们将使用这些函数来搜索一组目录并找到所有图像文件。

## 13.2\. f-strings

程序存储数据的一种方式是将其写入文本文件。例如，假设你是一个骆驼观察员，想要记录在一段观察期内看到的骆驼数量。假设在一年半的时间里，你已经观察到`23`只骆驼。你在骆驼观察本中的数据可能看起来是这样的。

```py
num_years = 1.5
num_camels = 23 
```

要将这些数据写入文件，可以使用`write`方法，我们在第八章中见过。`write`的参数必须是一个字符串，因此如果我们想将其他值放入文件中，就必须将它们转换为字符串。最简单的方式是使用内置函数`str`。

这看起来是这样的：

```py
writer = open('camel-spotting-book.txt', 'w')
writer.write(str(num_years))
writer.write(str(num_camels))
writer.close() 
```

这有效，但`write`不会添加空格或换行，除非你明确地包含它。如果我们重新读取文件，会发现两个数字被连在一起。

```py
open('camel-spotting-book.txt').read() 
```

```py
'1.523' 
```

至少，我们应该在数字之间添加空格。顺便提一下，让我们添加一些说明文字。

要编写一个字符串和其他值的组合，可以使用**f-string**，它是一个在开头有字母`f`的字符串，并且包含一个或多个用大括号括起来的 Python 表达式。以下的 f-string 包含一个表达式，即一个变量名。

```py
f'I have spotted {num_camels} camels' 
```

```py
'I have spotted 23 camels' 
```

结果是一个字符串，其中的表达式已被求值并替换为结果。可以有多个表达式。

```py
f'In {num_years} years I have spotted {num_camels} camels' 
```

```py
'In 1.5 years I have spotted 23 camels' 
```

而且这些表达式可以包含运算符和函数调用。

```py
line = f'In {round(num_years  *  12)} months I have spotted {num_camels} camels'
line 
```

```py
'In 18 months I have spotted 23 camels' 
```

所以我们可以像这样将数据写入文本文件。

```py
writer = open('camel-spotting-book.txt', 'w')
writer.write(f'Years of observation: {num_years}\n')
writer.write(f'Camels spotted: {num_camels}\n')
writer.close() 
```

两个 f-string 都以序列`\n`结尾，这会添加一个换行符。

我们可以像这样读取文件：

```py
data = open('camel-spotting-book.txt').read()
print(data) 
```

```py
Years of observation: 1.5
Camels spotted: 23 
```

在 f-string 中，大括号中的表达式会被转换为字符串，因此你可以包含列表、字典和其他类型。

```py
t = [1, 2, 3]
d = {'one': 1}
f'Here is a list {t} and a dictionary {d}' 
```

```py
"Here is a list [1, 2, 3] and a dictionary {'one': 1}" 
```

## 13.3\. YAML

程序读取和写入文件的原因之一是存储**配置信息**，这是一种指定程序应该做什么以及如何做的数据信息。

例如，在一个搜索重复照片的程序中，我们可能有一个名为`config`的字典，它包含了要搜索的目录名称、另一个目录的名称（用于存储结果），以及识别图片文件所用的文件扩展名列表。

这可能看起来像这样：

```py
config = {
    'photo_dir': 'photos',
    'data_dir': 'photo_info',
    'extensions': ['jpg', 'jpeg'],
} 
```

为了将这些数据写入文本文件，我们可以像上一节那样使用 f-string。但使用一个名为`yaml`的模块会更方便，它专为处理这类事情而设计。

`yaml`模块提供了用于处理 YAML 文件的函数，YAML 文件是格式化为便于人类*和*程序阅读和写入的文本文件。

这里有一个示例，使用`dump`函数将`config`字典写入 YAML 文件。

```py
import yaml

config_filename = 'config.yaml'
writer = open(config_filename, 'w')
yaml.dump(config, writer)
writer.close() 
```

如果我们读取文件的内容，我们可以看到 YAML 格式的样子。

```py
readback = open(config_filename).read()
print(readback) 
```

```py
data_dir: photo_info
extensions:
- jpg
- jpeg
photo_dir: photos 
```

现在，我们可以使用`safe_load`来读取回 YAML 文件。

```py
reader = open(config_filename)
config_readback = yaml.safe_load(reader)
config_readback 
```

```py
{'data_dir': 'photo_info',
 'extensions': ['jpg', 'jpeg'],
 'photo_dir': 'photos'} 
```

结果是一个包含与原始字典相同信息的新字典，但它不是同一个字典。

```py
config is config_readback 
```

```py
False 
```

将字典之类的对象转换为字符串称为**序列化**。将字符串转换回对象称为**反序列化**。如果你先序列化再反序列化一个对象，结果应该与原始对象等效。

## 13.4\. Shelve

到目前为止，我们一直在读取和写入文本文件——现在让我们来考虑数据库。**数据库**是一个用于存储数据的组织化文件。有些数据库像表格一样，包含行和列的信息。其他的则像字典一样，通过键映射到值，它们有时被称为**键值存储**。

`shelve`模块提供了创建和更新称为“shelf”的键值存储的功能。作为示例，我们将创建一个 shelf 来存储`photos`目录中图片的标题。我们将使用`config`字典来获取应该放置 shelf 的目录名称。

```py
config['data_dir'] 
```

```py
'photo_info' 
```

如果目录不存在，我们可以使用`os.makedirs`来创建这个目录。

```py
os.makedirs(config['data_dir'], exist_ok=True) 
```

以及使用`os.path.join`来创建一个包含目录名称和 shelf 文件名称`captions`的路径。

```py
db_file = os.path.join(config['data_dir'], 'captions')
db_file 
```

```py
'photo_info/captions' 
```

现在我们可以使用`shelve.open`打开 shelf 文件。参数`c`表示如果文件不存在，则创建该文件。

```py
import shelve

db = shelve.open(db_file, 'c')
db 
```

```py
<shelve.DbfilenameShelf at 0x7fcc902cc430> 
```

返回值官方称为`DbfilenameShelf`对象，更通俗地称为 shelf 对象。

shelf 对象在许多方面像字典。例如，我们可以使用括号操作符添加一个条目，它是一个从键到值的映射。

```py
key = 'jan-2023/photo1.jpg' 
db[key] = 'Cat nose' 
```

在这个示例中，键是图像文件的路径，值是描述图像的字符串。

我们还使用括号操作符来查找一个键并获取对应的值。

```py
value = db[key]
value 
```

```py
'Cat nose' 
```

如果你对现有的键进行重新赋值，`shelve`会替换旧值。

```py
db[key] = 'Close up view of a cat nose'
db[key] 
```

```py
'Close up view of a cat nose' 
```

一些字典方法，如`keys`、`values`和`items`，也适用于 shelf 对象。

```py
list(db.keys()) 
```

```py
['jan-2023/photo1.jpg'] 
```

```py
list(db.values()) 
```

```py
['Close up view of a cat nose'] 
```

我们可以使用`in`操作符检查一个键是否出现在 shelf 中。

```py
key in db 
```

```py
True 
```

我们还可以使用`for`语句来遍历键。

```py
for key in db:
    print(key, ':', db[key]) 
```

```py
jan-2023/photo1.jpg : Close up view of a cat nose 
```

和其他文件一样，使用完数据库后，应该关闭它。

```py
db.close() 
```

现在，如果我们列出数据目录的内容，我们会看到两个文件。

```py
os.listdir(config['data_dir']) 
```

```py
['captions.dir', 'captions.dat'] 
```

`captions.dat`包含我们刚刚存储的数据。`captions.dir`包含有关数据库组织的信息，这使得访问更高效。后缀`dir`代表“目录”，但它与我们之前处理的包含文件的目录无关。

## 13.5\. 存储数据结构

在之前的例子中，架子中的键和值是字符串。但我们也可以使用架子来存储像列表和字典这样的数据结构。

作为例子，让我们重新回顾一下第十一章练习中的字谜例子。回想一下，我们创建了一个字典，它将字母的排序字符串映射到可以用这些字母拼写出来的单词列表。例如，键`'opst'`映射到列表`['opts', 'post', 'pots', 'spot', 'stop', 'tops']`。

我们将使用以下函数来排序一个单词中的字母。

```py
def sort_word(word):
    return ''.join(sorted(word)) 
```

这里有一个例子。

```py
word = 'pots'
key = sort_word(word)
key 
```

```py
'opst' 
```

现在让我们打开一个名为`anagram_map`的架子。参数`'n'`意味着我们应该始终创建一个新的空架子，即使已经存在一个。

```py
db = shelve.open('anagram_map', 'n') 
```

现在我们可以像这样向架子中添加一个项目。

```py
db[key] = [word]
db[key] 
```

```py
['pots'] 
```

在这个条目中，键是一个字符串，值是一个字符串列表。

现在假设我们找到另一个包含相同字母的单词，比如`tops`。

```py
word = 'tops'
key = sort_word(word)
key 
```

```py
'opst' 
```

这个键与之前的例子相同，所以我们想将第二个单词附加到同一个字符串列表中。如果`db`是一个字典，下面就是我们如何做的。

```py
db[key].append(word)          # INCORRECT 
```

但是，如果我们运行它并查看架子中的键，它看起来没有被更新。

```py
db[key] 
```

```py
['pots'] 
```

这里是问题：当我们查找键时，我们得到的是一个字符串列表，但如果我们修改这个字符串列表，它并不会影响架子。如果我们想要更新架子，必须先读取旧值，更新它，然后将新值写回架子。

```py
anagram_list = db[key]
anagram_list.append(word)
db[key] = anagram_list 
```

现在架子中的值已更新。

```py
db[key] 
```

```py
['pots', 'tops'] 
```

作为练习，你可以通过读取单词列表并将所有的字谜存储到一个架子中来完成这个例子。## 13.6\. 检查等效文件

现在让我们回到本章的目标：搜索包含相同数据的不同文件。检查的一种方法是读取两个文件的内容并进行比较。

如果文件包含图像，我们必须以`'rb'`模式打开它们，其中`'r'`表示我们想要读取内容，而`'b'`表示**二进制模式**。在二进制模式下，内容不会被解释为文本，而是作为字节序列处理。

这是一个打开并读取图像文件的例子。

```py
path1 = 'photos/jan-2023/photo1.jpg'
data1 = open(path1, 'rb').read()
type(data1) 
```

```py
bytes 
```

`read`的结果是一个`bytes`对象——顾名思义，它包含一个字节序列。

一般来说，图像文件的内容是不可读的。但如果我们从第二个文件中读取内容，我们可以使用`==`运算符进行比较。

```py
path2 = 'photos/jan-2023/photo2.jpg'
data2 = open(path2, 'rb').read()
data1 == data2 
```

```py
False 
```

这两个文件并不相等。

让我们将目前为止的内容封装成一个函数。

```py
def same_contents(path1, path2):
    data1 = open(path1, 'rb').read()
    data2 = open(path2, 'rb').read()
    return data1 == data2 
```

如果我们只有两个文件，这个函数是一个不错的选择。但假设我们有大量的文件，并且想知道是否有任何两个文件包含相同的数据。逐一比较每对文件将是低效的。

另一种选择是使用**哈希函数**，它接受文件内容并计算一个**摘要**，通常是一个大整数。如果两个文件包含相同的数据，它们将有相同的摘要。如果两个文件不同，它们*几乎总是*会有不同的摘要。

`hashlib`模块提供了几种哈希函数——我们将使用的叫做`md5`。我们将通过使用`hashlib.md5`来创建一个`HASH`对象。

```py
import hashlib

md5_hash = hashlib.md5()
type(md5_hash) 
```

```py
_hashlib.HASH 
```

`HASH`对象提供了一个`update`方法，该方法以文件内容作为参数。

```py
md5_hash.update(data1) 
```

现在我们可以使用`hexdigest`来获取摘要，作为一个十六进制数字的字符串，表示一个基数为 16 的整数。

```py
digest = md5_hash.hexdigest()
digest 
```

```py
'aa1d2fc25b7ae247b2931f5a0882fa37' 
```

以下函数封装了这些步骤。

```py
def md5_digest(filename):
    data = open(filename, 'rb').read()
    md5_hash = hashlib.md5()
    md5_hash.update(data)
    digest = md5_hash.hexdigest()
    return digest 
```

如果我们对不同文件的内容进行哈希处理，我们可以确认我们得到的是不同的摘要。

```py
filename2 = 'photos/feb-2023/photo2.jpg'
md5_digest(filename2) 
```

```py
'6a501b11b01f89af9c3f6591d7f02c49' 
```

现在我们几乎拥有了找到等效文件所需的所有内容。最后一步是搜索一个目录并找到所有的图片文件。 ## 13.7\. 遍历目录

以下函数以我们想要搜索的目录作为参数。它使用`listdir`循环遍历目录的内容。当它找到一个文件时，它打印出完整路径。当它找到一个目录时，它递归调用自己以搜索子目录。

```py
def walk(dirname):
    for name in os.listdir(dirname):
        path = os.path.join(dirname, name)

        if os.path.isfile(path):
            print(path)
        elif os.path.isdir(path):
            walk(path) 
```

我们可以像这样使用它：

```py
walk('photos') 
```

```py
photos/digests.dat
photos/digests.dir
photos/notes.txt
photos/new_notes.txt
photos/mar-2023/photo2.jpg
photos/mar-2023/photo1.jpg
photos/digests.bak
photos/jan-2023/photo3.jpg
photos/jan-2023/photo2.jpg
photos/jan-2023/photo1.jpg
photos/feb-2023/photo2.jpg
photos/feb-2023/photo1.jpg 
```

结果的顺序取决于操作系统的具体细节。

## 13.8\. 调试

当你在读取和写入文件时，可能会遇到空白字符的问题。这些错误可能很难调试，因为空白字符通常是不可见的。例如，这里有一个包含空格、由序列`\t`表示的制表符和由序列`\n`表示的新行的字符串。当我们打印它时，看不见空白字符。

```py
s = '1 2\t 3\n 4'
print(s) 
```

```py
1 2	 3
 4 
```

内置函数`repr`可以提供帮助。它接受任何对象作为参数，并返回该对象的字符串表示。对于字符串，它用反斜杠序列表示空白字符。

```py
print(repr(s)) 
```

```py
'1 2\t 3\n 4' 
```

这对调试很有帮助。

另一个你可能遇到的问题是，不同的系统使用不同的字符来表示行结束。有些系统使用换行符，表示为`\n`。其他系统使用回车符，表示为`\r`。有些系统同时使用这两者。如果你在不同系统之间移动文件，这些不一致可能会导致问题。

文件名大小写是你在处理不同操作系统时可能遇到的另一个问题。在 macOS 和 UNIX 中，文件名可以包含小写字母、大写字母、数字和大多数符号。但是许多 Windows 应用程序忽略大小写字母之间的区别，而且在 macOS 和 UNIX 中允许的几个符号在 Windows 中不允许。

## 13.9\. 术语表

**短暂的：** 短暂程序通常运行一段时间，结束时，其数据会丢失。

**持久的：** 持久程序可以无限期运行，并将至少一部分数据保存在永久存储中。

**目录：** 一组文件和其他目录的集合。

**当前工作目录：** 程序使用的默认目录，除非指定了其他目录。

**路径：** 指定一系列目录的字符串，通常指向一个文件。

**相对路径：** 从当前工作目录或某个其他指定目录开始的路径。

**绝对路径：** 不依赖于当前目录的路径。

**f-string：** 在开头有字母`f`的字符串，其中包含一个或多个用大括号括起来的表达式。

**配置数据：** 通常存储在文件中，指定程序应该做什么以及如何做的数据。

**序列化：** 将对象转换为字符串。

**反序列化：** 将字符串转换为对象。

**数据库：** 一个文件，其内容被组织成能够高效执行特定操作的形式。

**键值存储：** 一种数据库，其内容像字典一样组织，键对应着值。

**二进制模式：** 打开文件的一种方式，使得文件内容被解释为字节序列而不是字符序列。

**哈希函数：** 一个接受对象并计算出整数的函数，这个整数有时被称为摘要。

**摘要：** 哈希函数的结果，尤其是在用来检查两个对象是否相同时。

## 13.10\. 练习

```py
# This cell tells Jupyter to provide detailed debugging information
# when a runtime error occurs. Run it before working on the exercises.

%xmode Verbose 
```

```py
Exception reporting mode: Verbose 
```

### 13.10.1\. 向虚拟助手提问

本章中出现了几个我没有详细解释的主题。以下是一些你可以向虚拟助手提问的问题，获取更多信息。

+   “短暂程序和持久程序有什么区别？”

+   “什么是持久程序的例子？”

+   “相对路径和绝对路径有什么区别？”

+   “为什么`yaml`模块有名为`load`和`safe_load`的函数？”

+   “当我写一个 Python shelf 时，`dat`和`dir`后缀的文件是什么？”

+   “除了键值存储，还有哪些类型的数据库？”

+   “当我读取一个文件时，二进制模式和文本模式有什么区别？”

+   “字节对象和字符串有什么区别？”

+   “什么是哈希函数？”

+   “什么是 MD5 摘要？”

和往常一样，如果你在以下练习中遇到困难，可以考虑向虚拟助手求助。除了提问之外，你可能还想粘贴本章中的相关函数。

### 13.10.2\. 练习

编写一个名为`replace_all`的函数，该函数接受一个模式字符串、一个替换字符串和两个文件名作为参数。它应该读取第一个文件，并将内容写入第二个文件（如果需要，创建它）。如果模式字符串出现在内容中的任何位置，它应被替换为替换字符串。

这是一个函数的概要，帮助你入门。

```py
def replace_all(old, new, source_path, dest_path):
    # read the contents of the source file
    reader = open(source_path)

    # replace the old string with the new

    # write the result into the destination file 
```

为了测试你的函数，读取文件`photos/notes.txt`，将`'photos'`替换为`'images'`，并将结果写入文件`photos/new_notes.txt`。

### 13.10.3\. 练习

在前一节中，我们使用了`shelve`模块创建了一个键值存储，将排序后的字母字符串映射到一个变位词的列表。为了完成示例，编写一个名为`add_word`的函数，该函数接受一个字符串和一个架子对象作为参数。

它应该对单词的字母进行排序以生成一个键，然后检查该键是否已存在于架子中。如果不存在，它应该创建一个包含新单词的列表并将其添加到架子中。如果存在，它应该将新单词附加到现有值的列表中。

### 13.10.4\. 练习

在一个大型文件集合中，可能存在多个相同文件的副本，存储在不同的目录或使用不同的文件名。这个练习的目标是搜索重复文件。作为示例，我们将处理`photos`目录中的图像文件。

下面是它的工作原理：

+   我们将使用来自遍历目录的`walk`函数来搜索该目录中的文件，这些文件扩展名与`config['extensions']`中的某个扩展名匹配。

+   对于每个文件，我们将使用来自检查等效文件的`md5_digest`来计算内容的摘要。

+   使用架子，我们将从每个摘要映射到包含该摘要的路径列表。

+   最后，我们将搜索架子，查找映射到多个文件的任何摘要。

+   如果找到任何匹配项，我们将使用`same_contents`来确认文件是否包含相同的数据。

我将首先建议编写一些函数，然后我们将把所有内容结合在一起。

1.  为了识别图像文件，编写一个名为`is_image`的函数，该函数接受一个路径和一个文件扩展名列表，并在路径以列表中的某个扩展名结尾时返回`True`。提示：使用`os.path.splitext`，或者让虚拟助手为你编写这个函数。

1.  编写一个名为`add_path`的函数，该函数接受一个路径和一个架子作为参数。它应该使用`md5_digest`来计算文件内容的摘要。然后，它应该更新架子，要么创建一个新的项，将摘要映射到包含路径的列表，要么将路径附加到已存在的列表中。

1.  编写一个名为`walk_images`的`walk`函数变体，它接受一个目录并遍历该目录及其子目录中的文件。对于每个文件，它应使用`is_image`来检查它是否是图像文件，并使用`add_path`将其添加到架子中。

当一切正常时，你可以使用以下程序来创建书架，搜索`photos`目录并将路径添加到书架中，然后检查是否有多个文件具有相同的摘要。

```py
db = shelve.open('photos/digests', 'n')
walk_images('photos')

for digest, paths in db.items():
    if len(paths) > 1:
        print(paths) 
```

你应该找到一对具有相同摘要的文件。使用`same_contents`来检查它们是否包含相同的数据。

[Think Python: 第 3 版](https://allendowney.github.io/ThinkPython/index.html)

版权 2024 [Allen B. Downey](https://allendowney.com)

代码许可：[MIT 许可](https://mit-license.org/)

文本许可：[创意共享署名-非商业性使用-相同方式共享 4.0 国际版](https://creativecommons.org/licenses/by-nc-sa/4.0/)
