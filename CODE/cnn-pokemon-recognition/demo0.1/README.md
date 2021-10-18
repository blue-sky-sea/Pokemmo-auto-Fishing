利用tensorflow搭建简单的神经网络，训练宝可梦的识别模型

1.本项目的开发环境为python3.6+tensorflow 1.120 GPU版本，以及其他的一些python有关机器学习和图像处理的包。

2.getdata.py为从百度获取训练图片的爬虫脚本。

3.pic中为已经爬取并处理好格式的jpg图片，图片格式均为160×120像素，水平、垂直分辨率均为96dpi，位深度24。

4.test中为处理好的测试图片。

5.record.csv中记录了精灵类别编号、名称、和爬取图片的要求数量，便于后续分类处理

6.model.py用于建立模型，利用tensorflow搭建了一个包含输入层、卷积层-激励层-池化层、卷积层-激励层-池化层、全连接层和输出层的简单的神经网络。
  运行时需要命令行传参，两个参数按顺序分别为训练集文件夹名和模型名，本项目中即 python train.py pic model
  
7.predict.py为预测文件，根据model中的模型进行检测，需要先把处理好的需要识别的文件放入test中，然后用predict进行预测，结果进行了简单的图形化展示。
  运行时同样需要命令行传参，三个参数分别为测试集文件夹名、模型名、记录表格名，此项目中为python predict.py test model record.csv
  
8.本项目的模型比较简单，在本地笔记本上用GTX 950M显卡进行训练只需要很短的几分钟。在Google Play中有一款精度很高的识别pokomen的app--Pokedex，有兴趣的盆友可以去看看。
