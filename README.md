# AutoBuildIOSProject
AutoBuildIOSProject

## 需求：
#### 1.客户（测试）自己上传logo或者将他们放到配置文件中，发布时自动获取。
#### 2.客户（测试）将appDisplayName放到配置文件中，发布时自动获取。
#### 3.自动签名（auto sign),导出archive文件和ipa文件。
#### 4.打包文件夹按照时间创建、排序。
#### 5.将文件上传到fir.im（其他平台根据源码可以很简单的处理）。
#### 6.打包成功、失败发送邮件到配置邮箱中。

## 前置工作：
#### 1.使用python语言，由于MAC OS 预制python2.7所以使用2.7即可，无需安装python3.x
#### 2.xcode尽量使用xcode9.0 +，因为xcode9.0在打包时有thinning选项，*亲测在打包swift项目时缩小近原来的1/10（53M变为5.6M左右）*
#### 3.目前发布到fir使用的是fir-cli插件，这一步可以自己根据fir文档做成自己的代码，由于比较简单就直接使用fir插件,插件安装自行百度，如果有问题请留言。
[fir.im代码发布文档地址](https://fir.im/docs/publish)

## 开始
> 1.logo & appdisplayname 配置
>> a.由于有一些信息需要测试人员发布时手动配置，所以暴露一个txt格式的配置文档;目前使用的自动配置displayname方式是处理国际化文档，用户可以提供多个名字给APP。

> ![配置文档部分内容](https://user-gold-cdn.xitu.io/2018/4/3/16289461bab59025?w=1052&h=777&f=jpeg&s=163537)
>> 处理代码如下
> ![appname处理代码](https://user-gold-cdn.xitu.io/2018/4/3/162894ae918ad3c5?w=772&h=889&f=png&s=190083)
>> b.图片处理方式和displayname相似，代码就不贴了，后面会放出源码地址

> 2.archive project & export ipa file
>> a.这一部分比较重要，也是比较浪费时间的一部分（由于英文不够好，在看官方文档时略痛苦）

>> 这一部分主要使用了两个xcodebuild命令。

>> 第一个是处理为xxx.archive文件:xcodebuild archive -workspace source.xcworkspace -scheme source -configuration Release -archivePath ~/Desktop/source -allowProvisioningUpdates

>> 第二个是导出为ipa文件指令： xcodebuild -exportArchive -archivePath /Users/shanwz/Desktop/source.xcarchive -exportPath ~/Desktop -exportOptionsPlist /Users/shanwz/Desktop/exportOptions.plist -allowProvisioningUpdates

>> 需要注意的是命令中如果需要自动签名最后面的-allowProvisioningUpdates是必须的，两条命令都需要添加。如果不需要这参数可以删除。如果你不清楚上面参数中的-scheme需要的内容，你可以在你项目根目录下执行 xcodebuild list指令查看。其他参数含义比较明显就不多说了，有问题留言。

>> 第二条指令原可以使用xcrun一类的order但是苹果在xcode8.x的时候就不推荐了，并且在之后的xcode中也没有PackageApplication文件，如果还是想用可以直接从网络中下载并安装。

>> 第二条指令中还一个注意点就是-exportOptionsPlist的参数，它需要我们描述我们需要导出何种类型的ipa文件，或者说是以什么方式导出。直接贴图说明：

> ![plistexport file](https://user-gold-cdn.xitu.io/2018/4/3/1628958eb359bfc1?w=513&h=736&f=png&s=108676)

>> 如果是自动签名，需要再signingstyle中添加automatic字段，否则就是MANUAL（这就需要你在自己项目中手动下载配置文件并且选择好）。几个必须的字段在图片中已经描述，如果想直到不同打包方式会需要什么样子的字段，那么我们可以手动打包，然后会在导出的文件夹内包含这个文件名字是：exportOptions.plist。（前期不知道这么搞，去看他官方文档，运行man xcodebuild指令查看，简直崩溃。）

>> 搞清楚这些指令，python就比较简单了。直接贴图。

> ![打包导出iPA](https://user-gold-cdn.xitu.io/2018/4/3/162895f9b5dc11f0?w=1214&h=793&f=png&s=212954)

>> xcodebuild指令直接使用str拼接，直观，方便阅读。

>> 3.发布ipa文件到fir.im

>> 这一步比较简单就不过多解释了，直接贴个图吧。

> ![](https://user-gold-cdn.xitu.io/2018/4/3/1628963b24a51eb0?w=1012&h=772&f=png&s=193681)

>> 由于fir上传时调用upload.communicate()方法返回值error机制不是很清楚，这里直接使用是否含有“publish succeed”字段来判定是否成功，有清楚的留言下。谢谢了。这里上传会重试3次，fir_cli插件在我这里第一次上传多会出现stream closed错误，不过第二次就没问题了。FIR_TIMEOUT=xxx可以设置fir上传时的超时时间。

> 4.发送邮件给指定邮箱

>> 这一部分的python也是很简单的东西，就不多说了，直接上图。 

> ![邮件服务](https://user-gold-cdn.xitu.io/2018/4/3/162896966223b51c?w=1144&h=649&f=png&s=175062)

>> 最后：
cd到源码根目录，执行chmod 777 autoDo.py ; 然后就可以使用./autoDo.py执行脚本命令了。

### 源码会在稍后放出。



