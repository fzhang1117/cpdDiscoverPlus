# -*- coding: UTF-8 -*-

'''

@Author       :   zhang fei <zhangfei-123@foxmail.com>

@Created Time :   2019-07-27

@File Name    :   cpdDiscoverPlus_mzCloudSpider.py

@Description  :   search mzCloudSpider by compound name and double checked by formula, expand the compound information in batch

'''
import re, sys, random, time, os
from urllib.request import urlopen
from urllib.parse import urlencode, quote
from urllib import error
from bs4 import BeautifulSoup
from itertools import islice
import socket

## wait the response in socket level as 20 seconds
socket.setdefaulttimeout(20)

fl_query = sys.argv[1]
fl_path_tmp = 'tmp/' + fl_query.split('.txt')[0] + time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime())

if not os.path.exists(fl_path_tmp):
    os.makedirs(fl_path_tmp)
    print("--- new folder {} has been created to store collected data ---".format(fl_path_tmp))


#### function defenition ####

def func_mzcloudSearch(query):
    greek_letterz = [chr(code) for code in range(945, 970)]
    query = re.sub('[' + ''.join(greek_letterz) + ']', '', query)
    searchString = quote(query)
    url = 'https://www.mzcloud.org/compound/Search?Query=' + searchString
    try:
        with urlopen(url) as f:
            page = f.read().decode('utf-8')
            mzcloudSearch_return = re.findall('ID: Reference[0-9]*', page)
            return_num = len(mzcloudSearch_return)
            print('The compound {} find {} items when searching in mzCloud.'.format(query, return_num))
            if return_num != 0:
                RefID_List = [re.split('Reference', i)[1] for i in mzcloudSearch_return]
                return RefID_List
            else:
                print('{} failed match mzCloud database, please try another database.'.format(query))
                return 0

    except socket.timeout as e:
        print("----socket timeout:", url)
        return 0

    except error.HTTPError as e:
        print('HTTPError : {}'.format(e.code))
        return 0

    except error.URLError as e:
        print('URLError : {}'.format(e.reason))
        return 0


def func_mzCloudReference(query, formula, RefID_List):
    for RefID in RefID_List:
        RefID = quote(RefID)
        url = 'https://www.mzcloud.org/compound/Reference/' + RefID
        try:
            with urlopen(url) as f:
                page = f.read().decode('utf-8')
                formulaSearch = re.findall('Formula:.*\r', page)[0]
                formulaSearch = re.sub('<SUB>|</SUB>', '', formulaSearch, flags = re.I)
                formulaSearch = re.split('<Span>|</Span>', formulaSearch)[1]
                if len(formulaSearch.split('&nbsp')) > 1:
                    formulaSearch = formulaSearch.split('&nbsp')[0]
                    return -1
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
                    print('{} can not match any mzCloud Reference {} \nmatch faild'.format(query, RefID))
        
        except socket.timeout as e:
            print("----socket timeout:", url)
            return 0

        except error.HTTPError as e:
            print('HTTPError : {}'.format(e.code))
            return 0

        except error.URLError as e:
            print('URLError : {}'.format(e.reason))
            return 0
    
    print('{} can not match any mzCloud Reference\nmatch failed return 0'.format(query))
    return 0

#### load the query file ####
with open(fl_query, 'rb') as fh_query:
    res_merge = []
    res_merge.append(['cpdName', 'mass', 'formula', 'mzCloudSearch', 'InCHI Key', 'InChI', 'CAS', 'PubChem', 'ChemSpider', 'KEGG', 'HMDb', 'ChEMBL', 'Other Names'])
    for idx, line in enumerate(islice(fh_query, 1, None)):
        line = line.decode('utf-8').strip('\r\n').split('\t')
        query, mass = line[0], line[1]
        formula = line[2].replace(' ', '')
        print(query, mass, formula)
        RefID_List = func_mzcloudSearch(query)
        time.sleep(random.uniform(0.2, 5))
        if RefID_List != 0:
            mzSearchRes = func_mzCloudReference(query, formula, RefID_List)
            if mzSearchRes != 0 and mzSearchRes != -1:
                mzCloudSearch = 'matched'
                KeySearch = ['InChI Key', 'InChI', 'CAS', 'PubChem', 'ChemSpider', 'KEGG', 'HMDb', 'ChEMBL', 'Other Names']
                res_query = [query, mass, formula, mzCloudSearch]
                for key in KeySearch:
                    if mzSearchRes.get(key) is not None:
                        res_query.append(mzSearchRes[key])
                    else:
                        res_query.append('-')
            elif mzSearchRes == -1:
                mzCloudSearch = 'Ion'
                print('{} exist as Ion format in vivo, please fill the information manually'.format(query))
                res_query = [query, mass, 'check it manually', mzCloudSearch, '-', '-', '-', '-', '-', '-', '-', '-', '-']
            else:
                mzCloudSearch = 'unmatch'
                res_query = [query, mass, formula, mzCloudSearch, '-', '-', '-', '-', '-', '-', '-', '-', '-']

        else:
            mzCloudSearch = 'unmatch'
            res_query = [query, mass, formula, mzCloudSearch, '-', '-', '-', '-', '-', '-', '-', '-', '-']
        with open(fl_path_tmp + '/{}.idx.txt'.format(idx), 'wb') as fh_tmp:
            fh_tmp.write('\t'.join(res_query).encode('utf-8'))
        res_merge.append(res_query)

fl_output = fl_query.split('.txt')[0] + '_mzCloudSearch.txt'
with open(fl_output, 'wb') as fh_output:
    res_merge = ['\t'.join(i) for i in res_merge]
    write_content = '\n'.join(res_merge).encode('utf-8')
    fh_output.write(write_content)
