1.首先升级服务器的Python版本	
	下载压缩包：wget http://www.python.org/ftp/python/2.7.6/Python-2.7.6.tar.xz
	解压Python2.7.6：tar -xvf Python-2.7.6.tar.xz
	进入Python2.7.6目录：cd Python-2.7.6
	编译安装Python2.7.6：./configure
				make && make altinstall
	服务器原生版本2.6.6是默认的。将老版本备份：mv /usr/bin/python /usr/bin/python2.6.6
	建立新的Python链接：ln -s /usr/local/bin/python2.7 /usr/bin/python

2.解决yum不支持Python2.7的问题
	修改/usr/bin/yum文件：vim /usr/bin/yum
	将第一行的 #!/usr/bin/python 改为 #!/usr/bin/python2.6.6
　　　
3.安装setuptools
	下载压缩包：wget https://pypi.python.org/packages/source/s/setuptools/setuptools-18.3.1.tar.gz#md5=748187b93152fa60287dfb896837fd7c
	解压setuptools：：tar -zxvf setuptools-18.3.1.tar.gz
	进入setuptools-18.3.1：cd setuptools-18.3.1
	安装：Python setup.py install

4.直接:easy_install pip

5.安装libxslt-devel支持lxml
 	yum install libxslt-devel

6.安装scrapy
	pip install scrapy

7.安装scrapyd
	pip install scrapyd
8.安装scrapyd-client
	pip install scrapyd-client
9.安装Python egg
	pip install python egg
