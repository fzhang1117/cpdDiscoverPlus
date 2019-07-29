####  #### cpdDiscoverPlus ####

本工具集是针对cpdDiscover输出结果的代谢物注释插件，由一系列python脚本构成。主要基于网络编程方法，批量爬取各个代谢物注释信息，减少手动点击鼠标的麻烦。

获取更新：

https://github.com/fzhang1117/cpdDiscoverPlus



##### 说明 #####

1. 在python 3 环境下运行

2. 输入文件必须以utf-8格式编码

3. 依赖包：

   | 依赖模块                                                     | 版本 | 说明         |
   | ------------------------------------------------------------ | ---- | ------------ |
   | re,sys, random, time, urllib.request, urllib.parse, itertools | -    | 自带模块     |
   | bs4                                                          |      | 解析网页数据 |

4. to be continue..

   

##### 脚本说明 

###### cpdDiscoverPlus_mzCloudSpider.py

本脚本首先以化合物名称为键值查询mzCloud网站，解析网页内容。判断该化合物是否被mzCloud收录。若被收录，则提取其在mzCloud 中的 Reference ID 作为键值，继续查询，解析网页内容。最终输出结果包含该代谢物在mzCloud中的查询状态，以及InChI Key, InChI, CAS号, PubChem号, ChemSpider号，KEGG编号，HMDb编号，ChEMBL编号, mzCloud中收录的同义代谢物等信息。 



**使用方法:**

```
python cpdDiscoverPlus_mzCloudSpider.py query_tst.txt
```

**查询文件格式:**

```	
cpdName	mass	Formula
(+)-Syringaresinol	418.1626	C22 H26 O8
(+)-Syringaresinol	418.1628	C22 H26 O8
(1S)-1,5-Anhydro-2-O-(6-deoxy-α-L-mannopyranosyl)-1-[5,7-dihydroxy-2-(4-hydroxyphenyl)-4-oxo-4H-chromen-6-yl]-D-glucitol	578.1629	C27 H30 O14
(1S)-1,5-Anhydro-2-O-(6-deoxy-α-L-mannopyranosyl)-1-[5,7-dihydroxy-2-(4-hydroxyphenyl)-4-oxo-4H-chromen-6-yl]-D-glucitol	578.1631	C27 H30 O14
```

文件第一行为列名，不能省略。

第一列为cpdDiscover所输出的化合物名称。

第二列为该化合物的accurate mass，由cpdDiscover输出，可作为脚本内置的一种查询结果校验方式。此版本还没有实现该功能。

第三列为该化合物的分子式，由cpdDiscover输出，作为脚本内置的查询结果校验方式。由于cpdDiscover输出格式是有空格的。在脚本里做了相应处理，使用者可直接复制结果。也可去除空格后粘贴，对查询结果没有影响。

查询文件用tab分隔，必须使用utf-8格式编码。



**输出文件格式：**

```
cpdName	mass	formula	mzCloudSearch	InCHI Key	InChI	CAS	PubChem	ChemSpider	KEGG	HMDb	ChEMBL	Other Names
(+)-Syringaresinol	418.1626	C22H26O8	matched	KOWMJRJXZMEZLD-HCIHMXRSSA-N	InChI=1S/C22H26O8/c1-25-15-5-11(6-16(26-2)19(15)23)21-13-9-30-22(14(13)10-29-21)12-7-17(27-3)20(24)18(8-12)28-4/h5-8,13-14,21-24H,9-10H2,1-4H3/t13-,14-,21+,22+/m0/s1		443023	391324	C10889	-	CHEMBL361362	Syringaresinol;  (7α,7'α,8α,8'α)-3,3',5,5'-Tetramethoxy-7,9':7',9-diepoxylignane-4,4'-diol
(+)-Syringaresinol	418.1628	C22H26O8	matched	KOWMJRJXZMEZLD-HCIHMXRSSA-N	InChI=1S/C22H26O8/c1-25-15-5-11(6-16(26-2)19(15)23)21-13-9-30-22(14(13)10-29-21)12-7-17(27-3)20(24)18(8-12)28-4/h5-8,13-14,21-24H,9-10H2,1-4H3/t13-,14-,21+,22+/m0/s1		443023	391324	C10889	-	CHEMBL361362	Syringaresinol;  (7α,7'α,8α,8'α)-3,3',5,5'-Tetramethoxy-7,9':7',9-diepoxylignane-4,4'-diol
(1S)-1,5-Anhydro-2-O-(6-deoxy-α-L-mannopyranosyl)-1-[5,7-dihydroxy-2-(4-hydroxyphenyl)-4-oxo-4H-chromen-6-yl]-D-glucitol	578.1629	C27H30O14	unmatched	-	-	-	-	-	-	-	-	-
(1S)-1,5-Anhydro-2-O-(6-deoxy-α-L-mannopyranosyl)-1-[5,7-dihydroxy-2-(4-hydroxyphenyl)-4-oxo-4H-chromen-6-yl]-D-glucitol	578.1631	C27H30O14	unmatched	-	-	-	-	-	-	-	-	-

```

**其他注意事项** 

1. 本脚本基于网络编程原理， 查询速度和稳定性受网络影响。
2. 本脚本在完成一项查询后，会随机等待 0.2秒 到 5秒再进行下一项查询。用户可以对这一项进行修改，但查询频率过高可能被网站认为是恶意攻击，导致切断线程，甚至封ip等后果。
3. 目前尚不支持断点续爬功能，假如查询由于网络原因或网站原因中止，先前查询的结果将无法获得。因此，暂不建议用户一次查询过多内容（2019.07.29）。

