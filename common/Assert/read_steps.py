t = {'test1': '22'}
print(t.keys(), t.values())
for i in range(1, 3):
    # i = 1
    print(i)

ll = [{'code': 10000, 'msg': 'Success', 'data': {'infoId': '5f3f7761d31e0a3ab9cc0c76'}, 'success': True}, 200,
      {'code': 10000, 'msg': 'Success',
       'data': {'political': None, 'nation': None, 'education': None, 'workArea': None, 'bank': None, 'pdfPath': [
           {'path': 'https://contract-esign.oss-cn-hangzhou.aliyuncs.com/bd11001c221a474eba732c2ed718921f',
            'name': '《心有灵犀保险代理人协议》'}]}, 'success': True}, 200]
n = 2  # 大列表中几个数据组成一个小列表
print([ll[i:i + n] for i in range(0, len(ll), n)])
