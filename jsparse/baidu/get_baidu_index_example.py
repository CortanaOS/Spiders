import time
import json
import requests


def get_response(area_code, area_name, app_name, start_date, end_date):
    """

    :param area_code:代表地区的编号
    :param area_name: 地区名字
    :param app_name: 软件名称
    :param start_date:开始时间
    :param end_date:结束时间
    :return:
    """
    url = 'http://index.baidu.com/api/SearchApi/index'
    params = {
        "area": area_code,
        "word": json.dumps([[{"name": app_name, "wordType": 1}]]),
        "startDate": start_date,
        "endDate": end_date,
    }
    headers = {
        'Cookie': 'CHKFORREG=219d5ea754b55f8cedf6c5fd67703d07; BAIDUID=707DD6A62950E1EDE431695D90FE4619:FG=1; PSTM=1595502970; BIDUPSID=743881BBBF10A75AAB1FC9F0475E9C4C; MCITY=-%3A; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; H_PS_PSSID=32606_1467_32694_31253_32046_32116; BDSFRCVID=1J-OJeC62rkF_SJrE6uIh7kUWm3roSQTH6f342hIyupKirtz5gz3EG0PSM8g0Ku-F_2QogKK0mOTHvDF_2uxOjjg8UtVJeC6EG0Ptf8g0f5; H_BDCLCKID_SF=tR4HVILatC-3J4PkjjDBDTQLDHLX5-RLfb6Zsl7F5l8-h4ocQln6yRDkjloAaTbWQGvLo-oOLMjxOKQIDT8KMMF-5q3iaRjJMJTMXDON3KJmVpC9bT3v5DuzBN5I2-biWbRL2MbdbqbP_IoG2Mn8M4bb3qOpBtQmJeTxoUJ25DnJhbLGe4bK-Tr0DG0DJM5; delPer=0; ZD_ENTRY=baidu; BDRCVFR[feWj1Vr5u3D]=I67x6TjHwwYf0; Hm_lvt_d101ea4d2a5c67dab98251f0b5de24dc=1599020433; bdindexid=pbi9on0svb7n3sdceu7d0bdqc1; PSINO=1; CHKFORREG=0c86260b4dfedc1ece4e023ba315aff2; BDUSS=xzSVA4UkJITUF2dkVUbXQ3elFhV2lqNGkwM3lXfmRuS2l1NFZTaUc0eUUyblpmRVFBQUFBJCQAAAAAAAAAAAEAAAC31XECbGlwamJkAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAIRNT1-ETU9fT0; Hm_lpvt_d101ea4d2a5c67dab98251f0b5de24dc=1599032722; RT="z=1&dm=baidu.com&si=misz4t5bu78&ss=kel1nms4&sl=s&tt=jec&bcn=https%3A%2F%2Ffclog.baidu.com%2Flog%2Fweirwood%3Ftype%3Dperf',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36',
        'Referer': 'http://index.baidu.com/v2/main/index.html',
        'Host': 'index.baidu.com'
    }
    response = requests.get(url=url, params=params, headers=headers)
    content = response.content.decode()
    json_result = json.loads(content)  # 把byte类型转换为字典类型
    if json_result["status"] != 0:
        raise ValueError(f"返回值错误：{json_result}")
    result_data = str(json_result['data']['generalRatio'][0]['pc']['avg'])
    with open('result_7.csv', 'a+') as f:
        value = ",".join([app_name, start_date, area_name, result_data])
        f.write(value)
        f.write("\n")
    return json_result


if __name__ == '__main__':
    app_list = [
        '芒果TV',
        '爱奇艺',
        '汽车之家',
        '易车',
        '房天下',
        '安居客',
        '携程旅行',
        '去哪儿旅行',
        '搜狐新闻',
        '网易新闻',
        '微博',
        '豆瓣',
        '知乎',
        '起点读书',
        '宝宝树孕育',
        '妈妈网孕育',
        '丁香医生',
        '好大夫在线',
    ]
    area_dict_need = {
        "北京市": 911,
        "广州市": 95,
        "上海市": 910,
        "深圳市": 94,
        "长春市": 154,
        "常州市": 162,
        "大连市": 29,
        "佛山市": 196,
        "福州市": 50,
        "贵阳市": 2,
        "哈尔滨市": 152,
        "合肥市": 189,
        "惠州市": 199,
        "济南市": 1,
        "嘉兴市": 304,
        "金华市": 135,
        "昆明市": 117,
        "兰州市": 166,
        "南昌市": 5,
        "南宁市": 90,
        "南通市": 163,
        "泉州市": 55,
        "绍兴市": 303,
        "石家庄市": 141,
        "台州市": 287,
        "太原市": 231,
        "温州市": 149,
        "厦门市": 54,
        "徐州市": 161,
        "烟台市": 78,
        "中山市": 207,
        "海口市": 239,
        "扬州市": 158,
        "珠海市": 200,
        "长沙市": 43,
        "成都市": 97,
        "东莞市": 133,
        "杭州市": 138,
        "南京市": 125,
        "宁波市": 289,
        "青岛市": 77,
        "沈阳市": 150,
        "苏州市": 126,
        "天津市": 923,
        "无锡市": 127,
        "武汉市": 28,
        "西安市": 165,
        "郑州市": 168,
        "重庆市": 904,
    }
    area_dict_all = {'广州': '95', '深圳': '94', '东莞': '133', '云浮': '195', '佛山': '196', '湛江': '197', '江门': '198',
                     '惠州': '199', '珠海': '200', '韶关': '201', '阳江': '202', '茂名': '203', '潮州': '204', '揭阳': '205',
                     '中山': '207', '清远': '208', '肇庆': '209', '河源': '210', '梅州': '211', '汕头': '212', '汕尾': '213',
                     '郑州': '168', '南阳': '262', '新乡': '263', '开封': '264', '焦作': '265', '平顶山': '266', '许昌': '268',
                     '安阳': '370', '驻马店': '371', '信阳': '373', '鹤壁': '374', '周口': '375', '商丘': '376', '洛阳': '378',
                     '漯河': '379', '濮阳': '380', '三门峡': '381', '济源': '667', '成都': '97', '宜宾': '96', '绵阳': '98',
                     '广元': '99', '遂宁': '100', '巴中': '101', '内江': '102', '泸州': '103', '南充': '104', '德阳': '106',
                     '乐山': '107', '广安': '108', '资阳': '109', '自贡': '111', '攀枝花': '112', '达州': '113', '雅安': '114',
                     '眉山': '291', '甘孜': '417', '阿坝': '457', '凉山': '479', '南京': '125', '苏州': '126', '无锡': '127',
                     '连云港': '156', '淮安': '157', '扬州': '158', '泰州': '159', '盐城': '160', '徐州': '161', '常州': '162',
                     '南通': '163', '镇江': '169', '宿迁': '172', '武汉': '28', '黄石': '30', '荆州': '31', '襄阳': '32', '黄冈': '33',
                     '荆门': '34', '宜昌': '35', '十堰': '36', '随州': '37', '恩施': '38', '鄂州': '39', '咸宁': '40', '孝感': '41',
                     '仙桃': '42', '天门': '73', '潜江': '74', '神农架': '687', '杭州': '138', '丽水': '134', '金华': '135',
                     '温州': '149', '台州': '287', '衢州': '288', '宁波': '289', '绍兴': '303', '嘉兴': '304', '湖州': '305',
                     '舟山': '306', '福州': '50', '莆田': '51', '三明': '52', '龙岩': '53', '厦门': '54', '泉州': '55', '漳州': '56',
                     '宁德': '87', '南平': '253', '哈尔滨': '152', '大庆': '153', '伊春': '295', '大兴安岭': '297', '黑河': '300',
                     '鹤岗': '301', '七台河': '302', '齐齐哈尔': '319', '佳木斯': '320', '牡丹江': '322', '鸡西': '323', '绥化': '324',
                     '双鸭山': '359', '济南': '1', '滨州': '76', '青岛': '77', '烟台': '78', '临沂': '79', '潍坊': '80', '淄博': '81',
                     '东营': '82', '聊城': '83', '菏泽': '84', '枣庄': '85', '德州': '86', '威海': '88', '济宁': '352', '泰安': '353',
                     '莱芜': '356', '日照': '366', '西安': '165', '铜川': '271', '安康': '272', '宝鸡': '273', '商洛': '274',
                     '渭南': '275', '汉中': '276', '咸阳': '277', '榆林': '278', '延安': '401', '石家庄': '141', '衡水': '143',
                     '张家口': '144', '承德': '145', '秦皇岛': '146', '廊坊': '147', '沧州': '148', '保定': '259', '唐山': '261',
                     '邯郸': '292', '邢台': '293', '沈阳': '150', '大连': '29', '盘锦': '151', '鞍山': '215', '朝阳': '216',
                     '锦州': '217', '铁岭': '218', '丹东': '219', '本溪': '220', '营口': '221', '抚顺': '222', '阜新': '223',
                     '辽阳': '224', '葫芦岛': '225', '长春': '154', '四平': '155', '辽源': '191', '松原': '194', '吉林': '270',
                     '通化': '407', '白山': '408', '白城': '410', '延边': '525', '昆明': '117', '玉溪': '123', '楚雄': '124',
                     '大理': '334', '昭通': '335', '红河': '337', '曲靖': '339', '丽江': '342', '临沧': '350', '文山': '437',
                     '保山': '438', '普洱': '666', '西双版纳': '668', '德宏': '669', '怒江': '671', '迪庆': '672', '乌鲁木齐': '467',
                     '石河子': '280', '吐鲁番': '310', '昌吉': '311', '哈密': '312', '阿克苏': '315', '克拉玛依': '317', '博尔塔拉': '318',
                     '阿勒泰': '383', '喀什': '384', '和田': '386', '巴音郭楞': '499', '伊犁': '520', '塔城': '563', '克孜勒苏柯尔克孜': '653',
                     '五家渠': '661', '阿拉尔': '692', '图木舒克': '693', '南宁': '90', '柳州': '89', '桂林': '91', '贺州': '92',
                     '贵港': '93', '玉林': '118', '河池': '119', '北海': '128', '钦州': '129', '防城港': '130', '百色': '131',
                     '梧州': '132', '来宾': '506', '崇左': '665', '太原': '231', '大同': '227', '长治': '228', '忻州': '229',
                     '晋中': '230', '临汾': '232', '运城': '233', '晋城': '234', '朔州': '235', '阳泉': '236', '吕梁': '237',
                     '长沙': '43', '岳阳': '44', '衡阳': '45', '株洲': '46', '湘潭': '47', '益阳': '48', '郴州': '49', '湘西': '65',
                     '娄底': '66', '怀化': '67', '常德': '68', '张家界': '226', '永州': '269', '邵阳': '405', '南昌': '5', '九江': '6',
                     '鹰潭': '7', '抚州': '8', '上饶': '9', '赣州': '10', '吉安': '115', '萍乡': '136', '景德镇': '137', '新余': '246',
                     '宜春': '256', '合肥': '189', '铜陵': '173', '黄山': '174', '池州': '175', '宣城': '176', '巢湖': '177',
                     '淮南': '178', '宿州': '179', '六安': '181', '滁州': '182', '淮北': '183', '阜阳': '184', '马鞍山': '185',
                     '安庆': '186', '蚌埠': '187', '芜湖': '188', '亳州': '391', '呼和浩特': '20', '包头': '13', '鄂尔多斯': '14',
                     '巴彦淖尔': '15', '乌海': '16', '阿拉善盟': '17', '锡林郭勒盟': '19', '赤峰': '21', '通辽': '22', '呼伦贝尔': '25',
                     '乌兰察布': '331', '兴安盟': '333', '兰州': '166', '庆阳': '281', '定西': '282', '武威': '283', '酒泉': '284',
                     '张掖': '285', '嘉峪关': '286', '平凉': '307', '天水': '308', '白银': '309', '金昌': '343', '陇南': '344',
                     '临夏': '346', '甘南': '673', '海口': '239', '万宁': '241', '琼海': '242', '三亚': '243', '儋州': '244',
                     '东方': '456', '五指山': '582', '文昌': '670', '陵水': '674', '澄迈': '675', '乐东': '679', '临高': '680',
                     '定安': '681', '昌江': '683', '屯昌': '684', '保亭': '686', '白沙': '689', '琼中': '690', '贵阳': '2', '黔南': '3',
                     '六盘水': '4', '遵义': '59', '黔东南': '61', '铜仁': '422', '安顺': '424', '毕节': '426', '黔西南': '588',
                     '银川': '140', '吴忠': '395', '固原': '396', '石嘴山': '472', '中卫': '480', '西宁': '139', '海西': '608',
                     '海东': '652', '玉树': '659', '海南': '676', '海北': '682', '黄南': '685', '果洛': '688', '拉萨': '466',
                     '日喀则': '516', '那曲': '655', '林芝': '656', '山南': '677', '昌都': '678', '阿里': '691', '上海': '910',
                     '北京': '911', '天津': '923', '重庆': '904'}
    date_list = [
        # ("2019-07-01", "2019-07-31"),
        # ("2020-01-01", "2020-01-31"),
        ("2020-07-01", "2020-07-31")
    ]
    for app_name in app_list:
        for area_code in area_dict_need.items():
            for date_info in date_list:
                try:
                    print(app_name, area_code[0], area_code[1], date_info[0], date_info[1])
                    time.sleep(1)
                    get_response(area_code[1], area_code[0], app_name, date_info[0], date_info[1])
                except ValueError as e:
                    print("error:", e)
                    # exit("end:{}".format("程序异常终止"))