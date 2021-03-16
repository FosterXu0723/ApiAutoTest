#coding=utf-8
##################################################
#Copyright(c) 2020
#Environment: python 3.5
#Author By: zhanfei
#Create Date: 2020-07-16
#Scenario:复星地区码校验
#################################################
import requests
import json
import time
import datetime
import random
#import logging
import sys
import os
import unittest
import pickle
from xlwt import *
from xlrd import open_workbook
from xlutils.copy import copy
sys.path.append("../..")
from common.ReadConfig import *
from common.Log import *
from common.IdCardNumber import *





#logging.basicConfig(level=logging.INFO,filename='testcase_log.txt',filemode='w')
log=Log().get_logger()


class fosun_areacode(unittest.TestCase):
	"""复星地区码校验"""

	def test_fosun_areacode(self):
		'''读取excel中的数据'''
		wb=open_workbook('../../test_data/AreaCode.xls')
		tb=wb.sheets()[0]
		data=[]
		for r in range(tb.nrows):
			val=[]
			for c in range(tb.ncols):
				val.append(str(tb.cell_value(r,c)))
			data.append(tuple(val))
		writebook=copy(wb)
		#book=Workbook(encoding='utf-8')
		writesheet=writebook.get_sheet(0)
		"""
		需要参数化的字段
		batchNo,orderNo,effectivedate,applytime,identitycode,birthday,provinceCode,provinceName,cityCode,cityName,areaCode,areaName
		"""
		for index,areas in enumerate(data):
			provincecode=areas[0]
			provincename=areas[1]
			citycode=areas[2]
			cityname=areas[3]
			areacode=areas[4]
			areaname=areas[5]
			batchno="test5020d31e0aa60b4"+str(random.randint(10000,99999))
			orderno="test4261723514"+str(random.randint(10000,99999))
			#生效时间
			effectivedate=str(datetime.date.today() + datetime.timedelta(days=1))+" "+"00:00:00"
			#提交时间
			applytime=str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
			#被保人身份证号码
			identitycode=getRandomIdNumberChild(1)
			#被保人出生年月
			birthday=identitycode[6:10]+"-"+identitycode[10:12]+"-"+identitycode[12:14]
			
				
			#读取报文路径
			file_path='../../test_data/fosun_areacode.json'
			with open(file_path,'r',encoding='UTF-8') as load_f:
				dt0=load_f.read()
				dt1 = dt0 % (batchno,applytime,effectivedate,birthday,identitycode,orderno,areacode,areaname,citycode,cityname,provincecode,provincename,orderno)
				interface_url='https://test.wxb.com.cn/gateway-kunlai/kunlai/message'
				interface_headers={'content-type':"application/json"}
				interface_response=requests.request("POST",interface_url,headers=interface_headers,data=dt1.encode())
				interface_result=json.loads(interface_response.text)
				result_code=interface_result['code']
				result_body=json.loads(interface_result['body'])
				result_msg=result_body['msg']
				result_bodycode=result_body['code']
				print (interface_result)
				if result_code==10000 and result_msg==u'处理成功' and result_bodycode==1:
					writesheet.write(index,6,0)
				else:
					writesheet.write(index,6,1)
			
		writebook.save('../../test_report/AreaCodeResult.xls')


if __name__ == "__main__":
    suite=unittest.TestSuite()
    suite.addTest(fosun_areacode("test_fosun_areacode"))
    unittest.TextTestRunner().run(suite)