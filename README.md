# SBin
二进制代码相似性检测

环境 python2.7 linux

需要安装的包

pip install futures

pip install fastdtw

pip install gensim

此项目将ACFG特征转换为向量表示以方便后续使用神经网络学习，输入数据为ACFG数据，格式为JSON，在SBin/目录中有测试数据test.json和test1.json

用法为 python src/main.py --input test1.josn --output test1 --num-walks 20 --walk-length 80 --window-size 5 --dimensions 2 --OPT1 True --OPT2 True --OPT3 True --until-layer 6

主要参数为input(输入数据位置），output(输出数据位置），demensions（将图转化为向量时的维度）

结果

输出目录为 test1_output/feature, 输出数据内容也是Json格式，特征储存在数据数据的features中，在features中前7个数据为提取的原始的ACFG，后面的数据为图嵌入后的向量表示（数量取决于生成时的维度）
