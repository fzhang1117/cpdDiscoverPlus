####   cpdDiscoverPlus ####

本工具集是针对cpdDiscover输出结果的代谢物注释插件，由一系列python脚本构成。主要基于网络编程方法，批量爬取各个代谢物注释信息，减少手动点击鼠标的麻烦。

获取更新：

https://github.com/fzhang1117/cpdDiscoverPlus



##### 说明 #####

1. 在python 3 环境下运行

2. 输入文件必须以utf-8格式编码

3. 依赖包：

   | 依赖模块                                                     | 版本 | 说明         |
   | ------------------------------------------------------------ | ---- | ------------ |
   | re,sys, random, time, urllib.request, urllib.parse, itertools, socket | -    | 自带模块     |
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
cpdName	mass	formula
5,8-Dihydroxy-4-oxo-1,2,3,4-tetrahydro-1-naphthalenyl 6-O-(3,4,5-trihydroxybenzoyl)-β-D-glucopyranoside	508.1216	C23H24O13
7-Hydroxy-2-(4-hydroxyphenyl)-4-oxo-3,4-dihydro-2H-chromen-5-yl β-D-glucopyranoside	434.1214	C21H22O10
Acetophenone	120.0574	C8H8O
Acetophenone	120.0574	C8H8O
Adenosine	267.0964	C10H13N5O4
Betaine	117.0789	C5H11NO2
Cetrimonium	283.3236	C19H41N
Choline	103.0996	C5H13NO
Cyanidin	286.0473	C15H10O6
Cyanidin	286.0474	C15H10O6
Cyanidin	286.0471	C15H10O6
Cytidine	243.0853	C9H13N3O5
Cytidine	243.0853	C9H13N3O5
```

文件第一行为列名，不能省略。

第一列为cpdDiscover所输出的化合物名称。

第二列为该化合物的accurate mass，由cpdDiscover输出，可作为脚本内置的一种查询结果校验方式。此版本还没有实现该功能。

第三列为该化合物的分子式，由cpdDiscover输出，作为脚本内置的查询结果校验方式。由于cpdDiscover输出格式是有空格的。在脚本里做了相应处理，使用者可直接复制结果。也可去除空格后粘贴，对查询结果没有影响。

查询文件用tab分隔，必须使用utf-8格式编码。

由于mzCloud的搜索引擎中无法处理希腊字母，故我们在脚本中做了相应的处理。使用者无需进行另外的处理。



**输出文件格式：**

```
cpdName	mass	formula	mzCloudSearch	InCHI Key	InChI	CAS	PubChem	ChemSpider	KEGG	HMDb	ChEMBL	Other Names
5,8-Dihydroxy-4-oxo-1,2,3,4-tetrahydro-1-naphthalenyl 6-O-(3,4,5-trihydroxybenzoyl)-β-D-glucopyranoside	508.1216	C23H24O13	matched	LWONLPZQFYNCMG-ATSIEDNJSA-N	InChI=1S/C23H24O13/c24-9-1-2-11(26)17-14(4-3-10(25)16(9)17)35-23-21(32)20(31)19(30)15(36-23)7-34-22(33)8-5-12(27)18(29)13(28)6-8/h1-2,5-6,14-15,19-21,23-24,26-32H,3-4,7H2/t14?,15-,19-,20+,21-,23-/m1/s1		60208892	29814794	-	-	-	1(2H)-Naphthalenone, 3,4-dihydro-5,8-dihydroxy-4-{[6-O-(3,4,5-trihydroxybenzoyl)-β-D-glucopyranosyl]oxy}- ;  {(2R,3S,4S,5R,6R)-6-[(5,8-Dihydroxy-4-oxo-1,2,3,4-tetrahydronaphthalen-1-yl)oxy]-3,4,5-trihydroxyoxan-2-yl}methyl 3,4,5-trihydroxybenzoate 
7-Hydroxy-2-(4-hydroxyphenyl)-4-oxo-3,4-dihydro-2H-chromen-5-yl β-D-glucopyranoside	434.1214	C21H22O10	matched	MFQIWHVVFBCURA-LKBAIHPRSA-N	InChI=1S/C21H22O10/c22-8-16-18(26)19(27)20(28)21(31-16)30-15-6-11(24)5-14-17(15)12(25)7-13(29-14)9-1-3-10(23)4-2-9/h1-6,13,16,18-24,26-28H,7-8H2/t13?,16-,18-,19+,20-,21-/m1/s1		5321085	23551150	-	-	-	2-(4-Hydroxyphenyl)-5-(β-D-glucopyranosyloxy)-7-hydroxy-2,3-dihydro-4H-1-benzopyran-4-one;  4H-1-Benzopyran-4-one, 5-(β-D-glucopyranosyloxy)-2,3-dihydro-7-hydroxy-2-(4-hydroxyphenyl)-;  Salipurposid
Acetophenone	120.0574	C8H8O	matched	KWOLFJPFCHCOCG-UHFFFAOYSA-N	InChI=1S/C8H8O/c1-7(9)8-5-3-2-4-6-8/h2-6H,1H3	98862	7410	7132	C07113	HMDB33910	-	Acetofenon;  Acetophenon;  Acetylbenzol;  Dymex;  Hypnone;  1-Phenyl-1-ethanone;  1-Phenyl-ethanone;  Acetylbenzene;  Benzene, acetyl-;  Benzoylmethide;  Ethanone, 1-phenyl-;  Ketone, methyl phenyl-;  Methylphenylketone;  Phenylethanone
Acetophenone	120.0574	C8H8O	matched	KWOLFJPFCHCOCG-UHFFFAOYSA-N	InChI=1S/C8H8O/c1-7(9)8-5-3-2-4-6-8/h2-6H,1H3	98862	7410	7132	C07113	HMDB33910	-	Acetofenon;  Acetophenon;  Acetylbenzol;  Dymex;  Hypnone;  1-Phenyl-1-ethanone;  1-Phenyl-ethanone;  Acetylbenzene;  Benzene, acetyl-;  Benzoylmethide;  Ethanone, 1-phenyl-;  Ketone, methyl phenyl-;  Methylphenylketone;  Phenylethanone
Adenosine	267.0964	C10H13N5O4	matched	OIRDTQYFTABQOQ-KQYNXXCUSA-N	InChI=1S/C10H13N5O4/c11-8-5-9(13-2-12-8)15(3-14-5)10-7(18)6(17)4(1-16)19-10/h2-4,6-7,10,16-18H,1H2,(H2,11,12,13)/t4-,6-,7-,10-/m1/s1	58617	60961	186; 21111796; 21241906	C00212; D00045	HMDB00050	CHEMBL477	6-Amino-9-β-D-ribofuranosyl-9H-purine;  β-D-Ribofuranose, 1-(6-amino-9H-purin-9-yl)-1-deoxy-;  6-Amino-9-β-ribofuranosyl-9H-purine;  (2R,3R,4S,5R)-2-(6-Amino-9H-purin-9-yl)-5-(hydroxymethyl)tetrahydrofuran-3,4-diol;  6-Amino-9β-δ-ribofuranosyl-9H-purine;  1-(6-Amino-9H-purin-9-yl)-1-deoxy-β-δ-ribofuranose;  Adenocard;  Adenoscan;  Adenocor;  Adenosin;  Boniton;  Adenine riboside;  Adenine nucleoside;  Nucleocardyl;  Sandesin;  Myocol;  β-Adenosine;  9H-Purin-6-amine, 9β-D-ribofuranosyl-;  ADN;  β-δ-Adenosine;  9β-δ-Ribofuranosyladenine;  Adenine-9β-δ-ribofuranoside;  9β-δ-Ribofuranosyl-9H-purin-6-amine
Betaine	117.0789	check it manually	Ion	-	-	-	-	-	-	-	-	-
Cetrimonium	283.3236	C19H41N	unmatch	-	-	-	-	-	-	-	-	-
Choline	103.0996	check it manually	Ion	-	-	-	-	-	-	-	-	-
Cyanidin	286.0473	check it manually	Ion	-	-	-	-	-	-	-	-	-
Cyanidin	286.0474	check it manually	Ion	-	-	-	-	-	-	-	-	-
Cyanidin	286.0471	check it manually	Ion	-	-	-	-	-	-	-	-	-
Cytidine	243.0853	C9H13N3O5	matched	UHDGCWIWMRVCDJ-XVFCMESISA-N	InChI=1S/C9H13N3O5/c10-5-1-2-12(9(16)11-5)8-7(15)6(14)4(3-13)17-8/h1-2,4,6-8,13-15H,3H2,(H2,10,11,16)/t4-,6-,7-,8-/m1/s1	65463	6175	5940	C00475; D07769	HMDB00089	CHEMBL95606	4-Amino-1β-D-ribofuranosyl-2(1H)-pyrimidinone;  2(1H)-Pyrimidinone, 4-amino-1β-D-ribofuranosyl-;  4-Amino-1-β-δ-ribofuranosyl-2(1H)-pyrimidinone;  1-(β-D-Ribofuranosyl)-2-oxo-4-amino-1,2-dihydro-1,3-diazine;  1β-Ribofuranosylcytosine;  Cytidin;  β-D-Ribofuranoside, cytosine-1;  Cytosine, 1-β-D-ribofuranosyl-;  CYD;  Cytosine β-D-riboside;  1β-δ-Ribofuranosylcytosine;  Cytosine-1β-δ-ribofuranoside
Cytidine	243.0853	C9H13N3O5	matched	UHDGCWIWMRVCDJ-XVFCMESISA-N	InChI=1S/C9H13N3O5/c10-5-1-2-12(9(16)11-5)8-7(15)6(14)4(3-13)17-8/h1-2,4,6-8,13-15H,3H2,(H2,10,11,16)/t4-,6-,7-,8-/m1/s1	65463	6175	5940	C00475; D07769	HMDB00089	CHEMBL95606	4-Amino-1β-D-ribofuranosyl-2(1H)-pyrimidinone;  2(1H)-Pyrimidinone, 4-amino-1β-D-ribofuranosyl-;  4-Amino-1-β-δ-ribofuranosyl-2(1H)-pyrimidinone;  1-(β-D-Ribofuranosyl)-2-oxo-4-amino-1,2-dihydro-1,3-diazine;  1β-Ribofuranosylcytosine;  Cytidin;  β-D-Ribofuranoside, cytosine-1;  Cytosine, 1-β-D-ribofuranosyl-;  CYD;  Cytosine β-D-riboside;  1β-δ-Ribofuranosylcytosine;  Cytosine-1β-δ-ribofuranoside
```

第四列报告了在mzCloud中的查询状态，目前定义了三种状态: matched, unmatch, Ion

**matched:** 在mzCloud中成功找到匹配项，并通过了结构式检验

**unmatched：**未能成功在在mzCloud中得到匹配项，可能的原因有:

​		mzCloud中未收录该化合物

​        由于网络原因导致的查询失败

​        其他的未知原因

​        当结果为unmatch时，建议使用者进行一次手动检索，确定未匹配的原因。

 **Ion:** 某些代谢物在生物体内以离子形式存在。这种情况下cpdDiscover将无法正确估计分子式，导致检索失败。此时，建议使用者进行一次手动检索，确定该化合物信息。



**其他注意事项**

1. 本脚本基于网络编程原理， 查询速度和稳定性受网络影响。尽管我们采取了一些方法保证脚本的稳定性与健壮性，但爬取失败的原因仍可能出现。
2. 本脚本在完成一项查询后，会随机等待 0.2秒 到 5秒再进行下一项查询。用户可以对这一项进行修改，但查询频率过高可能被网站认为是恶意攻击，导致切断线程，甚至封ip等后果。
3. 目前尚不支持断点续爬功能，故将每次启动程序时, 将新建一个 ./tmp/query_file_prefix_time/的目录， 每次爬取的结构都储存在该目录下。如果程序中途失败，使用者可从该目录下提取已经得到的信息。

