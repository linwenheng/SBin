# SBin
二进制代码相似性检测

本项目用于将ACFG数据转化为向量表示

环境 linux python2.7

必要的包

pip install futures
pip install fastdtw
pip install gensim

基础用法：python src/main.py --input test.json --output test --num-walks 20 --walk-length 80 --window-size 5 --dimensions 2 --OPT1 True --OPT2 True --OPT3 True --until-layer 6

输出目录为output_output(例如指定输入为test，输出目录就是test_output/features), dimensions为图嵌入后向量的维度

输入数据为json格式数据，输出也是json格式数据，转化后的向量存储在features文件夹中

输出数据样例{"src": "firmware_mips_80211stats.ida", "n_num": 5, "succs": [[2], [0, 2], [3, 4], [], [3]], "features": [[0.0, 0.0, 3.0, 0.0, 0.0, 1.0, 0.0, 0.7299725, 0.7375571], [0.0, 2.0, 4.0, 2.0, 0.0, 7.0, 0.0, 0.72906685, 0.67802054], [0.0, 3.0, 2.0, 2.0, 1.0, 10.0, 1.0, 0.64527786, 0.78934866], [0.0, 4.0, 0.0, 3.0, 1.0, 12.0, 2.0, 0.893782, 0.5675593], [0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.98324496, 0.4084944]], "fname": "init_proc"}

features中存储转化后的向量特征，前7个为原始特征，后面是图嵌入后的特征，特征数量与转化时的dimensions参数有关
