#vim 的配置

git clone https://github.com/gmarik/Vundle.vim.git ~/.vim/bundle/Vundle.vim #先安装vundle

git clone https://github.com/faalin/my_config #down项目

cp vimrc/.vimrc ~ #把.vimrc复制到user目录

rm -rvf vimrc #删掉git项目

部分依赖参照https://github.com/Shougo/neocomplete.vim#requirements

进入vim :PluginInstall

YouCompleteMe需要编译安装, 可以进入~/.vimrc/bundle/YouCompleteMe目录用./install.py --help查看细节

安装如果出现calledprocesserror错误。先sudo apt-get install cmake

*安装完成之后 pip install pep8*

-----------------------------------------------------------------------------------------------------------------

#linux python 的一些配置

把linux默认bash改成了zsh

sudo apt-get install zsh

然后安装oh-my-zsh配置.zshrc

具体参见< https://github.com/robbyrussell/oh-my-zsh >

我的主题是 ZSH_THEME="afowler"

.zshrc 添加了pyenv 创建虚拟环境和virtualenv 创建虚拟环境的配置。以及调用.pythonrc配置。

安装pyenv 详见< https://github.com/yyuu/pyenv >

安装virtualenv 详见< https://github.com/yyuu/pyenv >
