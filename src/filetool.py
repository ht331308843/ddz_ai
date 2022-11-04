#encoding:utf-8
import sys, os
import pickle
import zipfile
import json
from os.path import join, getsize

def unzip_file(zip_src, dst_dir):
    fz = zipfile.ZipFile(zip_src, 'r')
    for file in fz.namelist():
        fz.extract(file, dst_dir)       
   
def get_all_path(dirname):
    result = []#所有的文件
    for maindir, subdir, file_name_list in os.walk(dirname):
        print("1:",maindir) #当前主目录
        print("2:",subdir) #当前主目录下的所有目录
        print("3:",file_name_list)  #当前主目录下的所有文件

        for filename in file_name_list:
            apath = os.path.join(maindir, filename)#合并成一个完整路径
            result.append(apath)
    return result

def scan_file(dirname, fun, datax, lable, getNum):
	for maindir, subdir, file_name_list in os.walk(dirname):
		#print("1:",maindir) #当前主目录
		#print("2:",subdir) 	#当前主目录下的所有目录
		#print("3:",file_name_list)  #当前主目录下的所有文件

		for filename in file_name_list:
			apath = os.path.join(maindir, filename)#合并成一个完整路径
			if fun(apath, datax, lable, getNum):
				return

def readFile(filename):     #读文件操作
	#f = open(filename,'r',encoding='gb18030',errors='ignore')
	f = open(filename,'r',encoding='UTF-8')
	sread = f.read()    	#文件内容读取 [如果read(n)有值，则读取n个字符，为空则读取全部]
	f.close()
	return sread
 	
#scan_file("./jsondata", testJson)
#unzip_file("./testzip.zip","./jsondata")

#获取数据
def getPickleData(save_file):
	with open(save_file, 'rb') as f:
		dataset = pickle.load(f)	
		return dataset


if __name__ == '__main__':
	allFile = get_all_path('./data_pkl')
	print('allFile ', allFile)