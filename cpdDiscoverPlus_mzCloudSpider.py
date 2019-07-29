# -*- coding: UTF-8 -*-

'''

@Author       :   zhang fei <zhangfei-123@foxmail.com>

@Created Time :   2019-07-27

@File Name    :   cpdDiscoverPlus_kegg_found.py

@Description  :   using this script to sumamry and search kegg id in batch

'''
import re, sys, random, time, os
from urllib.request import urlopen
from urllib.parse import urlencode, quote
from bs4 import BeautifulSoup
from itertools import islice

fl_query = sys.argv[1]
fl_path_tmp = 'tmp/' + fl_query.split('.txt')[0] + time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime())

if not os.path.exists(fl_path_tmp):
    os.makedirs(fl_path_tmp)
    print("--- new folder {} has been created to store collected data ---".format(fl_path_tmp))


#### function defenition ####
def func_mzcloudSearch(query):
    searchString = quote(query)
    url = 'https://www.mzcloud.org/compound/Search?Query=' + searchString
    with urlopen(url) as f:
        page = f.read().decode('utf-8')
        mzcloudSearch_return = re.findall('ID: Reference[0-9]*', page)
        return_num = len(mzcloudSearch_return)
        print('The compound {} find {} items when searching in mzCloud.'.format(query, return_num))
        if return_num != 0:
            RefID_List = [re.split('Reference', i)[1] for i in mzcloudSearch_return]
            return RefID_List
        else:
            #print(query, 'failed match mzCloud database, please try another database.')
            return 0


def func_mzCloudReference(query, formula, RefID_List):
    if len(RefID_List) == 1:
        RefID = quote(RefID_List[0])
        url = 'https://www.mzcloud.org/compound/Reference/' + RefID
        with urlopen(url) as f:
            page = f.read().decode('utf-8')
            formulaSearch = re.findall('Formula:.*\r', page)[0]
            formulaSearch = re.sub('<SUB>|</SUB>', '', formulaSearch)
            formulaSearch = re.split('<Span>|</Span>', formulaSearch)[1]
            if formula == formulaSearch:
                print('{} matched the mzCloud Reference {}\nmatch successful!'.format(query, RefID))
                soup = BeautifulSoup(page, 'lxml')
                ## Extract all table in the html page
                dic_tmp = {}
                for idx, tr in enumerate(soup.find_all('tr')):
                    tds = tr.find_all('td')
                    tds = [re.sub('\n', '', i.get_text()) for i in tds]
                    dic_tmp[tds[0]] = tds[1]
                return dic_tmp
            else:
                #print(query, 'can not match mzCloud Reference', RefID, '...\n match faild...\n return 0')
                return 0
    elif len(RefID_List) > 1:
        for RefID in RefID_List:
            url = 'https://www.mzcloud.org/compound/Reference/' + RefID
            with urlopen(url) as f:
                page = f.read().decode('utf-8')
                formulaSearch = re.findall('Formula:.*\r', page)[0]
                formulaSearch = re.sub('<SUB>|</SUB>', '', formulaSearch)
                formulaSearch = re.split('<Span>|</Span>', formulaSearch)[1]
                if formula == formulaSearch:
                    print('{} matched the mzCloud Reference {}\nmatch successful!'.format(query, RefID))
                    soup = BeautifulSoup(page, 'lxml')
                    ## Extract all table in the html page
                    dic_tmp = {}
                    for idx, tr in enumerate(soup.find_all('tr')):
                        tds = tr.find_all('td')
                        tds = [re.sub('\n', '', i.get_text()) for i in tds]
                        dic_tmp[tds[0]] = tds[1]
                    return dic_tmp
                else:
                    print(query, 'can not match mzCloud Reference', RefID, '\ngo to the next round search...')
                
                print(query, 'can not match any mzCloud Reference, \nmatch faild, return 0')
                return 0

#### load the query file ####
with open(fl_path_tmp + '\store_tmp.txt', 'a') as fh_path_tmp:
    fh_path_tmp.writelines('\t'.join(['cpdName', 'mass', 'formula', 'mzCloudSearch', 'InCHI Key', 'InChI', 'CAS', 'PubChem', 'ChemSpider', 'KEGG', 'HMDb', 'ChEMBL', 'Other Names']))
    fh_path_tmp.writelines('\n')
    with open(fl_query, 'rb') as fh_query:
        res_merge = []
        res_merge.append(['cpdName', 'mass', 'formula', 'mzCloudSearch', 'InCHI Key', 'InChI', 'CAS', 'PubChem', 'ChemSpider', 'KEGG', 'HMDb', 'ChEMBL', 'Other Names'])
        for line in islice(fh_query, 1, None):
            line = line.decode('utf-8').strip('\r\n').split('\t')
            query, mass = line[0], line[1]
            formula = line[2].replace(' ', '')
            print(query, mass, formula)
            RefID_List = func_mzcloudSearch(query)
            time.sleep(random.uniform(0.2, 5))
            if RefID_List != 0:
                mzSearchRes = func_mzCloudReference(query, formula, RefID_List)
                if mzSearchRes != 0:
                    mzCloudSearch = 'matched'
                    KeySearch = ['InChI Key', 'InChI', 'CAS', 'PubChem', 'ChemSpider', 'KEGG', 'HMDb', 'ChEMBL', 'Other Names']
                    res_query = [query, mass, formula, mzCloudSearch]
                    for key in KeySearch:
                        if mzSearchRes.get(key) is not None:
                            res_query.append(mzSearchRes[key])
                        else:
                            res_query.append('-')
                else:
                    mzCloudSearch = 'unmatched'
                    res_query = [query, mass, formula, mzCloudSearch, '-', '-', '-', '-', '-', '-', '-', '-', '-']
            else:
                mzCloudSearch = 'unmatched'
                res_query = [query, mass, formula, mzCloudSearch, '-', '-', '-', '-', '-', '-', '-', '-', '-']
            fh_path_tmp.writelines('\t'.join(res_query))
            fh_path_tmp.writelines('\n')
            res_merge.append(res_query)

fl_output = fl_query.split('.txt')[0] + '_mzCloudSearch.txt'
with open(fl_output, 'w') as fh_output:
    res_merge = ['\t'.join(i) for i in res_merge]
    write_content = '\n'.join(res_merge)
    fh_output.write(write_content)
