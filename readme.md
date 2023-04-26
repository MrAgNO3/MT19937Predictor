[TOC]



# MT19937 Predictor and Solver

基于项目[https://github.com/JuliaPoo/MT19937-Symbolic-Execution-and-Solver](https://github.com/JuliaPoo/MT19937-Symbolic-Execution-and-Solver)，并做改动与拓展



## MT19937简介

算法内部状态大小为19968bit，以32bit为一个单元进行输出。每输出624个单元后，会进行一次twist。如下图所示：

![flow](readme.assets/flow.png)

## 功能

### 已知完整输出序列

即已知连续的624个输出单元的输出内容。即连续的19968bit的输出

较为简单

可以直接在算法层面进行逆向推导

![image-20230421001439814](readme.assets/tamper.png)

对 tamper 进行逆向，实现随机数输出与内部state的转换。

#### 方法：

参考这篇blog：[浅析MT19937伪随机数生成算法](https://www.anquanke.com/post/id/205861#h2-2)

从下往上逐行分析
```python
y1 = y ^ (y >> 18)
```
这一句对 y 的高18位没有影响，即`y1>>18 == y>>18`，所以可以直接推出 y 的高18位的值，进而得到剩余的低14位的值。

```python
y = y ^ y << 15 & 0xefc60000
```
根据运算符的优先级，可以得到`y1 = y^((y<<15)&4022730752)`，和上一步类似，y1的低15位是y的低15位和mask异或的结果，重复步骤可以得到y的全部信息。

用python表示完整过程的代码：

```python
def untempering(y):
    y ^= (y >> 18)
    y ^= (y << 15) & 0xefc60000
    y ^= ((y <<  7) & 0x9d2c5680) ^ ((y << 14) & 0x94284000) ^ ((y << 21) & 0x14200000) ^ ((y << 28) & 0x10000000)
    y ^= (y >> 11) ^ (y >> 22)
    return y
```




### 不完整输出序列

当需要生成的随机数小于32bit时，PRNG会对一个单元的输出进行截断，保留MSB作为输出。如下图所示，生成的32bit的随机数与16bit的随机数的高位相同。

![image-20230425111955811](readme.assets/msb.png)

如果获取的是连续的经过msb截断的数据，也能实现预测。

算法内部主要有两部分，twist和tamper。其中twist是在算法初始化之后或者生成624个随机数之后，对算法内部state进行旋转的操作。tamper是对一个32bit的state单元，进行操作得到32bit的随机数输出。这两个变换都是线性的变换

其中，twist过程等价于state向量与Twist矩阵相乘。这里的state大小位19968*1，Twist矩阵T大小为19968\*19968，如下

$$
T_1*state=state'
$$

这里的state’代表经过一次旋转的state

tamper过程的对象是32bit的state单元，称为block，则可以有如下关系

$$
T_2*block=R
$$

这里的R代表输出是随机数，为32bit

同时，对于整个state，也有如下关系

$$
\left[\begin{matrix}
T_2 & 0 & 0 & \cdots & 0\\
0 & T_2 & 0 & \cdots & 0\\
0 & 0 & T_2 & \cdots & 0\\
\vdots & \vdots & \vdots & \ddots & \vdots\\
0 & 0 & 0 & \cdots & T_2
\end{matrix}\right]*state=R
$$


$$
\left[\begin{matrix}
 T_2 & & & & \\
 & T_2 & & & \\
 & & T_2 & & \\
 & & & \ddots & \\
 & & & & T_2
\end{matrix}\right]*state=R
$$

这里的每一个 $T_2$ 都是一个32*32的矩阵，组合起来就是一个19968\*19968大矩阵，记大矩阵为$T_2'$

此时，可以将Twist和Tamper过程联合，可以将整个过程抽象为:

$$
(T_1)^n*T_2'*state=R
$$

这里的 $T_1$ 代表Twist矩阵， $T_1^n$ 代表经过了 $n$ 次旋转。 $T_2'$ 代表对角线拼接后的tamper矩阵

$state$为状态向量，大小为19968*1， $R$ 为同样大小的向量，代表算法的输出，即随机数。

可以进一步将 $(T_1)^n*T_2$ 进行结合，定义 $T=(T_1)^n*T_2$，则有

$$
T*state=R
$$

$T$ 为变换矩阵，结合了 Twist 和 tamper 两个过程。

#### 构造T的方法

这里的矩阵 $T$，和随机数序列的输出方式是相关的。比如连续的getrandbits(32)构造的矩阵和连续的getrandbits(16)构造的矩阵，是不一样的

1. 通过修改state的值，一行一行测出来

   随机数生成的序列是已知的，如16bit MSB，则可以修改state的值为 $[1,0,0,0,...,0]^T$ ，此时与 $T$ 相乘后，得到的输出 $R$ 就是 $T$ 矩阵的第一列。

   以此类推，以此将state中的每个元素设为1，其余元素设为0，则可以将每次得到是随机数输出 $R$ 进行拼接，得到完整的 $T$ 矩阵的值。

2. 通过符号执行

   算法内部的状态变化都是位运算。将624个int32中的每个bit拆分开来，可以视作19968个模二有限域下的变元，代表state的每一个bit。
   
   即可以将初始state设为符号 $a_1,a_2,...,a_{19968}$ ，使用变量间的异或来代替算法中的数值bit间的异或过程，将最终得到的随机数输出结果进行记录，结果的每一个bit中，包含的初始state的bit状态即可组成变换矩阵 $T$ .



此时，在已知随机数输出序列 $R$ 的情况下，恢复state可以通过以下方式:

$$
state=T^{-1}*R
$$

#### T的性质

在Twist的过程，在Twist后，原state的1~32bit信息被丢失，导致 $T$ 矩阵的第1~32

#### 对T求逆

有一点需要注意的是，根据twist过程可以知道，state经过twist之后，第1个bit至第32个bit，这些bit没有参与twist的过程，twist后的结果也与这31个bit无关

这导致通过两种方法构造出的T矩阵，都是不满秩的
