# 一、如何通过git将项目推送到github远程仓库

```
首先，电脑里需要安装了git，还有自己的github账户。
```

```
第一步：我们需要先创建一个本地的版本库（其实也就是一个文件夹）。然后在里面书写自己的项目
	   mkdir projects
```

```
第二步：初始化:           
		进入这个文件夹， git init 
```

```
配置个人信息：
	# 全局配置个人信息
	git config --global user.name "guokaichong"
	git config --global user.email "email@qq.com"
```

```
查看git设置列表信息
	 git config --list 
```

```
第三步:  1.通过git status查看当前文件的状态，也可以跳过这一步;
		2.通过git add '指定文件'  添加到仓库，
		3.或者通过git add .		 把该目录下的所有文件添加到仓库。
```

```
第四步：提交：
		git commit -m "提交内容-描述"。
```

```
第五步：创建密钥、公钥SSH KEY。先看一下你C盘用户目录下有没有.ssh目录，有的话看下里面有没有id_rsa和			   id_rsa.pub这两个文件，有就跳到下一步，没有就通过下面命令创建：

	   ssh-keygen -t rsa -C "email@qq.com"

 然后一路回车。这时你就会在用户下的.ssh目录里找到id_rsa和id_rsa.pub这两个文件。
```

```
第六步：登录Github,找到右上角的图标，打开点进里面的Settings，再选中里面的SSH and GPG KEYS，
	   1.点击右上角的New SSH key，然后Title里面随便填，
       2.再把刚才id_rsa.pub里面的内容复制到Title下面的Key内容框里面，最后点击Add SSH key，完成钥匙配置
```

```
第七步：在Github上创建一个Git仓库。
```

```
 第八步：仓库进行关联：
 		在Github上创建好Git仓库之后我们就可以和本地仓库进行关联了，根据创建好的Git仓库页面的提示，
 		可以在本地TEST仓库的命令行输入：
 
 	    git remote add origin "远程仓库地址"
```

```
第九步：关联好之后我们就可以把本地库的所有内容推送到远程仓库（也就是Github）上了，通过：
	   $ git push -u origin master

```

```
第十步：由于新建的远程仓库是空的，所以要加上-u这个参数，等远程仓库里面有了内容之后，
	  下次再从本地库上传内容的时候只需下面这样就可以了：
	  $ git push origin master

	这时候你再重新刷新你的Github页面进入刚才新建的那个仓库里面就会发现项目已经成功上传了.
```



# 二、常用远程推送失败等问题 、 解决方案：

问题一： error: failed to push some refs to '远程仓库地址'

```
1.解决方案：git pull --rebase origin master 
2.git push -u origin master               --"这样，就可以重放您的本地提交在新更新的原始/master之上。"
```

问题二：fatal: remote origin already exists.

```
 1、先输入$ git remote rm origin
 2、再输入$ git remote add origin 	'远程仓库地址'
```

问题三：error: failed to push some refs to   '远程仓库地址'

```
1.解决方案：git pull --rebase origin master 
2.git push -u origin master               --"这样，就可以重放您的本地提交在新更新的原始/master之上。"
```

问题四:[Everything up-to-date　但没传上去](https://www.cnblogs.com/wenbinshen/p/9069851.html)

```
1.我犯得第一个简单错误，是忘了git commit前必须先git add .
	将我更新的文件记录下来，否则你写的或者传入的本地文件无法提交到本地仓库当中。

2.我犯得第二个简单错误，是git commit 必须加注释，我提交时用的 git commit ，
	随后跳出来一个让你写提交说明的窗口，我直接按ESC，：wq 回车后，直接调回了命令行，很明显没有加上注释，当我再次git push origin master 时，出现了 Everything up-to-date的提示，以后大家如果出现这类简单的错误，可以检查一下这方面。

最后我用git commit -m '上传项目'  提交至本地仓库，再git push origin master后成功加项目推到了远程仓库
```





# 二、git版本其他 命令

**3.查看历史版本**

```linux
git log
git reflog
```

> git reflog 可以查看所有分支的所有操作记录（包括commit和reset的操作），包括已经被删除的commit记录，git log 不能察看已经删除了的commit记录



#### 4.回退版本

方法一：

- `HEAD`表示当前最新版本
- `HEAD^`表示当前最新版本的前一个版本
- `HEAD^^`表示当前最新版本的前两个版本，**以此类推...**
- `HEAD~1`表示当前最新版本的前一个版本
- `HEAD~10`表示当前最新版本的前10个版本，**以此类推...**

```git
git reset --hard HEAD^
```



方法二：

**当版本非常多时可选择的方案**

```linux
# 通过每个版本的版本号回退到指定版本
git reset --hard 版本号
```

#### 

#### 5.撤销修改

- 只能撤销工作区、暂存区的代码

  - 撤销工作区代码

    ```linux
    git checkout 文件名
    ```

  - 撤销暂存区代码

    ```linux
    # 第一步：将暂存区代码撤销到工作区
    git reset HEAD  文件名
    # 第二步：撤销工作区代码
    git checkout 文件名
    ```

- 撤销仓库区的代码就相当于回退版本操作

#### 6.版本对比

- 对比本地仓库库与工作区
  - 在工作区，修改文件
  - `git diff HEAD -- test1.py`
- 对比本地仓库各版本代码
  - `git diff HEAD HEAD^ -- test1.py`



#### 7.文件删除

- 确定删除处理

  ```linux
  # 删除文件
  rm 文件名
  # git确定删除文件，对比添加文件git add 
  git rm 文件名
  # 删除后记录删除操作版本
  git commit -m '删除描述'
  ```

- 误删处理，撤销修改

  ```linux
  # 删除文件
  rm 文件名
  # git撤销修改
  git checkout -- 文件名
  ```