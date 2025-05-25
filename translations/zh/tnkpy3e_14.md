# 12\. 文本分析与生成

> 原文：[`allendowney.github.io/ThinkPython/chap12.html`](https://allendowney.github.io/ThinkPython/chap12.html)

此时我们已经涵盖了 Python 的核心数据结构——列表、字典和元组——以及一些使用它们的算法。在本章中，我们将利用它们来探索文本分析和马尔科夫生成：

+   文本分析是一种描述文档中单词之间统计关系的方法，比如一个单词后面跟着另一个单词的概率，以及

+   马尔科夫生成是一种使用与原始文本相似的单词和短语生成新文本的方法。

这些算法类似于大型语言模型（LLM）的部分内容，LLM 是聊天机器人的关键组成部分。

我们将从计算每个单词在书中出现的次数开始。然后我们将查看单词对，并列出每个单词后面可以跟随的单词。我们将制作一个简单版本的马尔科夫生成器，作为练习，你将有机会制作一个更通用的版本。

## 12.1\. 唯一单词

作为文本分析的第一步，让我们阅读一本书——罗伯特·路易斯·史蒂文森的《化身博士》——并统计唯一单词的数量。下载这本书的说明可以在本章的笔记本中找到。

```py
filename = 'dr_jekyll.txt' 
```

我们将使用`for`循环从文件中读取行，并使用`split`将行分割成单词。然后，为了跟踪唯一单词，我们将每个单词作为字典中的一个键进行存储。

```py
unique_words = {}
for line in open(filename):
    seq = line.split()
    for word in seq:
        unique_words[word] = 1

len(unique_words) 
```

```py
6040 
```

字典的长度是唯一单词的数量——按照这种计算方式大约是`6000`。但如果我们检查它们，会发现有些并不是有效的单词。

例如，让我们看看`unique_words`中最长的单词。我们可以使用`sorted`来排序单词，将`len`函数作为关键字参数传入，以便按单词长度排序。

```py
sorted(unique_words, key=len)[-5:] 
```

```py
['chocolate-coloured',
 'superiors—behold!”',
 'coolness—frightened',
 'gentleman—something',
 'pocket-handkerchief.'] 
```

切片索引`[-5:]`选择排序后列表中的最后`5`个元素，即最长的单词。

这个列表包括一些合法的长单词，比如“circumscription”，以及一些带连字符的单词，比如“chocolate-coloured”。但一些最长的“单词”实际上是由连字符分隔的两个单词。而其他单词则包含像句号、感叹号和引号等标点符号。

所以，在我们继续之前，让我们处理一下连字符和其他标点符号。

## 12.2\. 标点符号

为了识别文本中的单词，我们需要解决两个问题：

+   当行中出现连字符时，我们应该将其替换为空格——然后当我们使用`split`时，单词就会被分开。

+   分割单词后，我们可以使用`strip`来移除标点符号。

为了处理第一个问题，我们可以使用以下函数，它接受一个字符串，将连字符替换为空格，分割字符串，并返回结果列表。

```py
def split_line(line):
    return line.replace('—', ' ').split() 
```

注意，`split_line`只会替换连字符，而不会替换破折号。这里有一个例子。

```py
split_line('coolness—frightened') 
```

```py
['coolness', 'frightened'] 
```

现在，为了去除每个单词开头和结尾的标点符号，我们可以使用 `strip`，但是我们需要一个标点符号的字符列表。

Python 字符串中的字符使用 Unicode，这是一个国际标准，用于表示几乎所有字母表中的字母、数字、符号、标点符号等。`unicodedata` 模块提供了一个 `category` 函数，我们可以用它来判断字符是否为标点符号。给定一个字母，它会返回一个字符串，指示该字母属于哪个类别。

```py
import unicodedata

unicodedata.category('A') 
```

```py
'Lu' 
```

字符 `'A'` 的类别字符串是 `'Lu'` —— `'L'` 表示它是一个字母，`'u'` 表示它是大写字母。

字符 `'.'` 的类别字符串是 `'Po'` —— `'P'` 表示它是标点符号，`'o'` 表示它的子类别是“其他”。

```py
unicodedata.category('.') 
```

```py
'Po' 
```

我们可以通过检查类别以 `'P'` 开头的字符，来找出书中的标点符号。下面的循环将唯一的标点符号存储在字典中。

```py
punc_marks = {}
for line in open(filename):
    for char in line:
        category = unicodedata.category(char)
        if category.startswith('P'):
            punc_marks[char] = 1 
```

为了制作一个标点符号的列表，我们可以将字典的键连接成一个字符串。

```py
punctuation = ''.join(punc_marks)
print(punctuation) 
```

```py
.’;,-“”:?—‘!()_ 
```

现在我们知道书中哪些字符是标点符号，我们可以编写一个函数，接受一个单词，去除开头和结尾的标点符号，并将其转换为小写。

```py
def clean_word(word):
    return word.strip(punctuation).lower() 
```

这是一个示例。

```py
clean_word('“Behold!”') 
```

```py
'behold' 
```

因为 `strip` 会删除字符串开头和结尾的字符，所以它不会影响带有连字符的单词。

```py
clean_word('pocket-handkerchief') 
```

```py
'pocket-handkerchief' 
```

现在，这是一个使用 `split_line` 和 `clean_word` 来识别书中唯一单词的循环。

```py
unique_words2 = {}
for line in open(filename):
    for word in split_line(line):
        word = clean_word(word)
        unique_words2[word] = 1

len(unique_words2) 
```

```py
4005 
```

根据对单词定义的严格标准，约有 4000 个唯一单词。我们可以确认最长单词的列表已经清理干净。

```py
sorted(unique_words2, key=len)[-5:] 
```

```py
['circumscription',
 'unimpressionable',
 'fellow-creatures',
 'chocolate-coloured',
 'pocket-handkerchief'] 
```

现在让我们看看每个单词的使用频率。

## 12.3\. 单词频率

以下循环计算每个唯一单词的频率。

```py
word_counter = {}
for line in open(filename):
    for word in split_line(line):
        word = clean_word(word)
        if word not in word_counter:
            word_counter[word] = 1
        else:
            word_counter[word] += 1 
```

每当我们第一次遇到一个单词时，我们将其频率初始化为 `1`。如果之后再遇到相同的单词，我们就将其频率加一。

为了查看哪些单词最常出现，我们可以使用 `items` 从 `word_counter` 获取键值对，并按对中的第二个元素（即频率）进行排序。首先，我们将定义一个函数来选择第二个元素。

```py
def second_element(t):
    return t[1] 
```

现在我们可以使用 `sorted` 和两个关键字参数：

+   `key=second_element` 表示项目将根据单词的频率进行排序。

+   `reverse=True` 表示项目将按反向顺序排序，最频繁的单词排在最前面。

```py
items = sorted(word_counter.items(), key=second_element, reverse=True) 
```

这里是五个最常见的单词。

```py
for word, freq in items[:5]:
    print(freq, word, sep='\t') 
```

```py
1614	the
972	and
941	of
640	to
640	i 
```

在接下来的部分，我们将把这个循环封装在一个函数中。我们还将用它来演示一个新功能——可选参数。

## 12.4\. 可选参数

我们已经使用了带有可选参数的内置函数。例如，`round` 有一个名为 `ndigits` 的可选参数，用于指示保留多少位小数。

```py
round(3.141592653589793, ndigits=3) 
```

```py
3.142 
```

但这不仅仅是内置函数——我们也可以编写带有可选参数的函数。例如，下面的函数接受两个参数，`word_counter` 和 `num`。

```py
def print_most_common(word_counter, num=5):
    items = sorted(word_counter.items(), key=second_element, reverse=True)

    for word, freq in items[:num]:
        print(freq, word, sep='\t') 
```

第二个参数看起来像一个赋值语句，但其实它不是——它是一个可选参数。

如果你用一个参数调用这个函数，`num`将获得**默认值**，即`5`。

```py
print_most_common(word_counter) 
```

```py
1614	the
972	and
941	of
640	to
640	i 
```

如果你用两个参数调用这个函数，第二个参数将被赋值给`num`，而不是默认值。

```py
print_most_common(word_counter, 3) 
```

```py
1614	the
972	and
941	of 
```

在这种情况下，我们可以说可选参数**覆盖**了默认值。

如果一个函数既有必需参数又有可选参数，所有必需的参数必须排在前面，后面跟着可选参数。

## 12.5\. 字典减法

假设我们想进行拼写检查——也就是说，找出可能拼写错误的单词列表。做这个的方法之一是找出书中那些不在有效单词列表中的单词。在之前的章节中，我们使用了一个在类似拼字游戏（如拼字游戏）中被认为有效的单词列表。现在我们将使用这个列表来进行罗伯特·路易斯·史蒂文森的拼写检查。

我们可以将这个问题看作集合减法——也就是说，我们想找出一个集合（书中的单词）中不在另一个集合（列表中的单词）中的所有单词。

正如我们之前做过的，我们可以读取`words.txt`的内容，并将其分割成一个字符串列表。

```py
word_list = open('words.txt').read().split() 
```

然后我们将把单词作为键存储在字典中，以便我们可以使用`in`运算符快速检查一个单词是否有效。

```py
valid_words = {}
for word in word_list:
    valid_words[word] = 1 
```

现在，为了识别书中出现但不在单词列表中的单词，我们将使用`subtract`，它接受两个字典作为参数，并返回一个新的字典，其中包含第一个字典中不在第二个字典中的所有键。

```py
def subtract(d1, d2):
    res = {}
    for key in d1:
        if key not in d2:
            res[key] = d1[key]
    return res 
```

下面是我们如何使用它的方法。

```py
diff = subtract(word_counter, valid_words) 
```

要获取可能拼写错误的单词样本，我们可以打印出`diff`中最常见的单词。

```py
print_most_common(diff) 
```

```py
640	i
628	a
128	utterson
124	mr
98	hyde 
```

最常见的“拼写错误”单词大多是人名和一些单字母的单词（乌特森先生是杰基尔博士的朋友和律师）。

如果我们选择那些只出现一次的单词，它们更有可能是拼写错误。我们可以通过遍历项目，并列出频率为`1`的单词来做到这一点。

```py
singletons = []
for word, freq in diff.items():
    if freq == 1:
        singletons.append(word) 
```

这是列表中的最后几个元素。

```py
singletons[-5:] 
```

```py
['gesticulated', 'abjection', 'circumscription', 'reindue', 'fearstruck'] 
```

它们中的大多数是有效的单词，但不在单词列表中。不过，`'reindue'`似乎是`'reinduce'`的拼写错误，所以至少我们发现了一个真正的错误。

## 12.6\. 随机数

作为迈向马尔科夫文本生成的一步，接下来我们将从`word_counter`中选择一个随机的单词序列。但首先，让我们谈谈随机性。

给定相同的输入，大多数计算机程序是**确定性的**，这意味着它们每次生成相同的输出。确定性通常是好事，因为我们希望相同的计算产生相同的结果。然而，对于某些应用程序，我们希望计算机能够不可预测。游戏就是一个例子，但还有更多。

让程序真正做到非确定性是很困难的，但有一些方法可以伪装成非确定性。一个方法是使用生成**伪随机**数的算法。伪随机数并不是真正的随机数，因为它们是通过确定性计算生成的，但仅凭查看这些数字，几乎无法将它们与真正的随机数区分开。

`random` 模块提供了生成伪随机数的函数——我将在这里简单地称其为“随机数”。我们可以这样导入它。

```py
import random 
```

`random` 模块提供了一个名为 `choice` 的函数，可以从列表中随机选择一个元素，每个元素被选中的概率相同。

```py
t = [1, 2, 3]
random.choice(t) 
```

```py
1 
```

如果你再次调用该函数，你可能会得到相同的元素，或者得到不同的元素。

```py
random.choice(t) 
```

```py
2 
```

从长远来看，我们希望每个元素出现的次数大致相同。

如果你用字典调用 `choice`，你会得到一个 `KeyError`。

```py
random.choice(word_counter) 
```

```py
KeyError: 422 
```

要选择一个随机键，你必须先将键放入列表中，然后调用 `choice`。

```py
words = list(word_counter)
random.choice(words) 
```

```py
'posture' 
```

如果我们生成一个随机的单词序列，它没有太大的意义。

```py
for i in range(6):
    word = random.choice(words)
    print(word, end=' ') 
```

```py
ill-contained written apocryphal nor busy spoke 
```

问题的一部分是我们没有考虑到某些单词比其他单词更常见。如果我们选择具有不同“权重”的单词，结果会更好，这样有些单词会比其他单词更频繁地被选中。

如果我们使用来自 `word_counter` 的值作为权重，每个单词的选择概率将取决于它的频率。

```py
weights = word_counter.values() 
```

`random` 模块还提供了另一个名为 `choices` 的函数，接受权重作为一个可选参数。

```py
random.choices(words, weights=weights) 
```

```py
['than'] 
```

它还接受另一个可选参数 `k`，该参数指定要选择的单词数。

```py
random_words = random.choices(words, weights=weights, k=6)
random_words 
```

```py
['reach', 'streets', 'edward', 'a', 'said', 'to'] 
```

结果是一个字符串的列表，我们可以将其连接成更像句子的东西。

```py
' '.join(random_words) 
```

```py
'reach streets edward a said to' 
```

如果你从书中随机选择单词，你可以感知到词汇量，但一系列随机单词通常没有意义，因为连续单词之间没有关系。例如，在一个真实的句子中，你期望像“the”这样的冠词后面跟着形容词或名词，而可能不是动词或副词。所以，下一步是查看单词之间的这些关系。

## 12.7\. 二元组

我们将不再逐个单词查看，而是查看由两个单词组成的序列，这叫做**二元组**。由三个单词组成的序列叫做**三元组**，由若干个单词组成的序列叫做**n-元组**。

我们来写一个程序，找出书中的所有二元组以及每个二元组出现的次数。为了存储结果，我们将使用一个字典，其中

+   键是表示二元组的大写字母字符串的元组，

+   这些值是表示频率的整数。

我们称之为 `bigram_counter`。

```py
bigram_counter = {} 
```

以下函数接受两个字符串组成的列表作为参数。首先，它将这两个字符串组成一个元组，可以作为字典中的键。然后，如果该键不存在，它会将其添加到 `bigram_counter` 中；如果已经存在，它会增加该键的频率。

```py
def count_bigram(bigram):
    key = tuple(bigram)
    if key not in bigram_counter:
        bigram_counter[key] = 1
    else:
        bigram_counter[key] += 1 
```

在阅读本书的过程中，我们必须跟踪每一对连续的单词。因此，如果我们看到“man is not truly one”这一序列，我们将添加“大词组”：“man is”，“is not”，“not truly”等等。

为了跟踪这些大词组，我们将使用一个名为`window`的列表，因为它就像一本书的窗口，一次只显示两个单词。最初，`window`是空的。

```py
window = [] 
```

我们将使用以下函数逐个处理单词。

```py
def process_word(word):
    window.append(word)

    if len(window) == 2:
        count_bigram(window)
        window.pop(0) 
```

当第一次调用此函数时，它会将给定的单词附加到`window`中。由于窗口中只有一个单词，我们还没有形成一个大词组，因此函数结束。

第二次调用时——以及以后每次调用——它会将第二个单词添加到`window`中。由于窗口中有两个单词，它会调用`count_bigram`来跟踪每个大词组出现的次数。然后，它使用`pop`移除窗口中的第一个单词。

以下程序循环遍历书中的单词并逐一处理它们。

```py
for line in open(filename):
    for word in split_line(line):
        word = clean_word(word)
        process_word(word) 
```

结果是一个字典，将每个大词组映射到它出现的次数。我们可以使用`print_most_common`来查看最常见的大词组。

```py
print_most_common(bigram_counter) 
```

```py
178	('of', 'the')
139	('in', 'the')
94	('it', 'was')
80	('and', 'the')
73	('to', 'the') 
```

看着这些结果，我们可以感知哪些单词对最可能一起出现。我们还可以利用这些结果生成随机文本，像这样。

```py
bigrams = list(bigram_counter)
weights = bigram_counter.values()
random_bigrams = random.choices(bigrams, weights=weights, k=6) 
```

`bigrams`是书中出现的大词组列表。`weights`是它们的频率列表，因此`random_bigrams`是一个样本，其中大词组被选中的概率与它的频率成正比。

这是结果。

```py
for pair in random_bigrams:
    print(' '.join(pair), end=' ') 
```

```py
to suggest this preface to detain fact is above all the laboratory 
```

这种生成文本的方式比选择随机单词要好，但仍然没有太多意义。

## 12.8. 马尔科夫分析

我们可以通过马尔科夫链文本分析做得更好，它为文本中的每个单词计算接下来会出现的单词列表。作为示例，我们将分析《蒙提·派森》歌曲 *Eric, the Half a Bee* 的歌词：

```py
song = """
Half a bee, philosophically,
Must, ipso facto, half not be.
But half the bee has got to be
Vis a vis, its entity. D'you see?
""" 
```

为了存储结果，我们将使用一个字典，它将每个单词映射到跟随它的单词列表。

```py
successor_map = {} 
```

举个例子，让我们从歌曲的前两个单词开始。

```py
first = 'half'
second = 'a' 
```

如果第一个单词不在`successor_map`中，我们必须添加一个新项，将第一个单词映射到包含第二个单词的列表。

```py
successor_map[first] = [second]
successor_map 
```

```py
{'half': ['a']} 
```

如果第一个单词已经在字典中，我们可以查找它，获取我们到目前为止看到的后继单词列表，并附加新的单词。

```py
first = 'half'
second = 'not'

successor_map[first].append(second)
successor_map 
```

```py
{'half': ['a', 'not']} 
```

以下函数封装了这些步骤。

```py
def add_bigram(bigram):
    first, second = bigram

    if first not in successor_map:
        successor_map[first] = [second]
    else:
        successor_map[first].append(second) 
```

如果相同的大词组出现多次，第二个单词会被多次添加到列表中。通过这种方式，`successor_map`会跟踪每个后继单词出现的次数。

正如我们在前一节中所做的，我们将使用一个名为`window`的列表来存储连续单词对。我们将使用以下函数逐个处理单词。

```py
def process_word_bigram(word):
    window.append(word)

    if len(window) == 2:
        add_bigram(window)
        window.pop(0) 
```

这是我们如何用它来处理歌曲中的单词。

```py
successor_map = {}
window = []

for word in song.split():
    word = clean_word(word)
    process_word_bigram(word) 
```

这是结果。

```py
successor_map 
```

```py
{'half': ['a', 'not', 'the'],
 'a': ['bee', 'vis'],
 'bee': ['philosophically', 'has'],
 'philosophically': ['must'],
 'must': ['ipso'],
 'ipso': ['facto'],
 'facto': ['half'],
 'not': ['be'],
 'be': ['but', 'vis'],
 'but': ['half'],
 'the': ['bee'],
 'has': ['got'],
 'got': ['to'],
 'to': ['be'],
 'vis': ['a', 'its'],
 'its': ['entity'],
 'entity': ["d'you"],
 "d'you": ['see']} 
```

单词`'half'`可以跟随`'a'`、`'not'`或`'the'`。单词`'a'`可以跟随`'bee'`或`'vis'`。大多数其他单词只出现一次，因此它们只跟随一个单词。

现在，让我们分析这本书。

```py
successor_map = {}
window = []

for line in open(filename):
    for word in split_line(line):
        word = clean_word(word)
        process_word_bigram(word) 
```

我们可以查找任何单词，并找到可以跟随它的单词。

```py
successor_map['going'] 
```

```py
['east', 'in', 'to', 'to', 'up', 'to', 'of'] 
```

在这个后继列表中，请注意单词`'to'`出现了三次，而其他后继只出现了一次。

## 12.9\. 生成文本

我们可以使用前一部分的结果，生成与原文中连续单词之间关系相同的新文本。它是如何工作的：

+   从文本中出现的任何一个单词开始，我们查找它的可能后继，并随机选择一个。

+   然后，使用选中的单词，我们查找它的可能后继，并随机选择一个。

我们可以重复这个过程，生成我们想要的任意多个单词。举个例子，让我们从单词`'although'`开始。以下是可以跟随它的单词。

```py
word = 'although'
successors = successor_map[word]
successors 
```

```py
['i', 'a', 'it', 'the', 'we', 'they', 'i'] 
```

我们可以使用`choice`从列表中以相等的概率选择。

```py
word = random.choice(successors)
word 
```

```py
'i' 
```

如果同一个单词在列表中出现多次，它被选中的概率更大。

重复这些步骤，我们可以使用以下循环生成更长的序列。

```py
for i in range(10):
    successors = successor_map[word]
    word = random.choice(successors)
    print(word, end=' ') 
```

```py
continue to hesitate and swallowed the smile withered from that 
```

结果听起来更像一个真实的句子，但它仍然没有太大意义。

使用多个单词作为`successor_map`中的键，我们可以做得更好。例如，我们可以创建一个字典，将每个二元组（bigram）或三元组（trigram）映射到后续单词的列表。作为一个练习，你将有机会实现这个分析，并查看结果是什么样的。

## 12.10\. 调试

到这个阶段，我们正在编写更复杂的程序，你可能会发现你花更多时间进行调试。如果你在调试一个难题时卡住了，下面是一些可以尝试的办法：

+   阅读：检查你的代码，自己读一遍，确认它是否表达了你想表达的意思。

+   运行：通过进行更改并运行不同的版本进行实验。通常，如果你在程序中的正确位置显示正确的内容，问题会变得明显，但有时你需要构建一些支架。

+   沉思：花点时间思考一下！这是哪种错误：语法错误、运行时错误，还是语义错误？你能从错误信息或者程序的输出中获取哪些信息？是什么样的错误可能导致你看到的问题？在问题出现之前，你最后修改了什么？

+   橡皮鸭调试：如果你将问题解释给别人听，你有时会在还没问完问题之前就找到答案。通常你不需要另一个人；你可以只和一只橡皮鸭交谈。这就是著名的策略——**橡皮鸭调试**的来源。我不是在编造这个——请看 [`en.wikipedia.org/wiki/Rubber_duck_debugging`](https://en.wikipedia.org/wiki/Rubber_duck_debugging)。

+   后退：在某些时候，最好的做法是后退——撤销最近的更改——直到你回到一个正常工作的程序。然后你可以重新开始构建。

+   休息：如果你给大脑休息，有时候它会自己找到问题所在。

初学者程序员有时会在某个活动上卡住，忘记其他的活动。每个活动都有它自己的失败模式。

例如，读取你的代码如果问题是拼写错误的话是有效的，但如果问题是概念性误解，则无效。如果你不理解你的程序是做什么的，即使你读它 100 遍也看不出错误，因为错误在你的脑海里。

运行实验是有效的，特别是当你运行小的、简单的测试时。但如果你没有思考或阅读代码就去实验，可能会花费很长时间才能搞清楚发生了什么。

你必须抽时间思考。调试就像是实验科学。你应该对问题至少有一个假设。如果有两个或更多的可能性，尝试想出一个可以排除其中一个的测试。

但即使是最好的调试技术，也会因为错误太多，或者你试图修复的代码过于庞大复杂而失败。有时候最好的选择是退一步，简化程序，直到恢复到一个能正常工作的版本。

初学者程序员通常不愿意后退，因为他们无法忍受删除一行代码（即使它是错的）。如果这样能让你感觉好一点，可以在开始简化程序之前，把你的程序复制到另一个文件中。然后你可以逐个复制回来。

找到一个棘手的 bug 需要阅读、运行、沉思、退步，有时候还需要休息。如果你在某个活动中遇到困难，尝试其他的方法。

## 12.11\. 词汇表

**默认值（default value）：** 如果没有提供参数，将赋给参数的值。

**覆盖（override）：** 用一个参数替换默认值。

**确定性（deterministic）：** 一个确定性的程序每次运行时，只要输入相同，就会做相同的事情。

**伪随机（pseudorandom）：** 伪随机数列看起来像是随机的，但它是由一个确定性的程序生成的。

**二元组（bigram）：** 一个包含两个元素的序列，通常是单词。

**三元组（trigram）：** 一个包含三个元素的序列。

**n 元组（n-gram）：** 一个包含不确定数量元素的序列。

**橡皮鸭调试（rubber duck debugging）：** 通过大声向一个无生命物体解释问题来进行调试的一种方法。

## 12.12\. 练习

```py
# This cell tells Jupyter to provide detailed debugging information
# when a runtime error occurs. Run it before working on the exercises.

%xmode Verbose 
```

### 12.12.1\. 向虚拟助手询问

在`add_bigram`中，`if`语句根据字典中是否已存在该键，来创建一个新的列表或将元素添加到现有列表中。

```py
def add_bigram(bigram):
    first, second = bigram

    if first not in successor_map:
        successor_map[first] = [second]
    else:
        successor_map[first].append(second) 
```

字典提供了一种叫做`setdefault`的方法，我们可以用它更简洁地做同样的事情。你可以向虚拟助手询问它是如何工作的，或者把`add_word`复制到虚拟助手中并问：“你能用`setdefault`重写这个吗？”

在本章中，我们实现了马尔科夫链文本分析和生成。如果你感兴趣，可以向虚拟助手询问更多关于该主题的信息。你可能学到的一件事是，虚拟助手使用的算法在许多方面是相似的——但在重要方面也有所不同。问一个虚拟助手：“像 GPT 这样的语言模型和马尔科夫链文本分析有什么区别？”

### 12.12.2\. 练习

编写一个函数，计算每个三元组（由三个单词组成的序列）出现的次数。如果你使用《*化身博士*》的文本来测试你的函数，你应该会发现最常见的三元组是“said the lawyer”。

提示：编写一个名为`count_trigram`的函数，它类似于`count_bigram`。然后编写一个名为`process_word_trigram`的函数，它类似于`process_word_bigram`。

### 12.12.3\. 练习

现在让我们通过从每个二元组映射到可能的后继词列表来实现马尔科夫链文本分析。

从`add_bigram`开始，编写一个名为`add_trigram`的函数，该函数接收一个包含三个单词的列表，并使用前两个单词作为键，第三个单词作为可能的后继词，在`successor_map`中添加或更新一个条目。

这是一个调用`add_trigram`的`process_word_trigram`版本。

```py
def process_word_trigram(word):
    window.append(word)

    if len(window) == 3:
        add_trigram(window)
        window.pop(0) 
```

你可以使用以下循环来测试你的函数，使用来自书本的单词。

```py
successor_map = {}
window = []

for line in open(filename):
    for word in split_line(line):
        word = clean_word(word)
        process_word_trigram(word) 
```

在下一个练习中，你将使用这些结果生成新的随机文本。

### 12.12.4\. 练习

对于这个练习，我们假设`successor_map`是一个字典，它将每个二元组映射到后继词的列表。

为了生成随机文本，我们将从`successor_map`中随机选择一个键。

```py
successors = list(successor_map)
bigram = random.choice(successors)
bigram 
```

```py
('doubted', 'if') 
```

现在编写一个循环，按照这些步骤生成更多的 50 个单词：

1.  在`successor_map`中查找可以跟随`bigram`的单词列表。

1.  随机选择其中一个并打印出来。

1.  对于下一个迭代，创建一个新的二元组，该二元组包含`bigram`中的第二个单词和所选的后继词。

例如，如果我们从二元组`('doubted', 'if')`开始，并选择`'from'`作为其后继词，则下一个二元组是`('if', 'from')`。

如果一切正常，你应该会发现生成的文本在风格上与原文相似，一些短语是有意义的，但文本可能会从一个话题跳到另一个话题。

作为附加练习，修改你对最后两个练习的解决方案，使用三元组作为`successor_map`中的键，看看它对结果产生了什么影响。

[Think Python: 第 3 版](https://allendowney.github.io/ThinkPython/index.html)

版权所有 2024 [Allen B. Downey](https://allendowney.com)

代码许可证：[MIT 许可证](https://mit-license.org/)

文本许可证：[知识共享署名-非商业性使用-相同方式共享 4.0 国际](https://creativecommons.org/licenses/by-nc-sa/4.0/)
