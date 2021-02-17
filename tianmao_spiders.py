#encoding:utf-8
from Tianmao_Spider.script_settings import *
import requests
import re
import json
from bs4 import BeautifulSoup
import os




class tianmao():
    def __init__(self,id):

        self.id = id # 更换商品 ID [天猫] -- [服装类-鞋帽类-内衣等产品]

        # cookie_value = "cna=L1KgGAEugDQCAXjkE92DOrGi; lgc=%5Cu72C2%5Cu98D9%5Cu7684%5Cu8717%5Cu725Bye; tracknick=%5Cu72C2%5Cu98D9%5Cu7684%5Cu8717%5Cu725Bye; enc=703SyCWUub39CnGN%2Bo7o3R%2BRUu0niBCQY2CL%2F%2B8CpH1UPFRclCrc%2F%2Bnidg1%2BOpfTpG3C4zJlbe7v6WGcDs4njg%3D%3D; thw=cn; hng=CN%7Czh-CN%7CCNY%7C156; t=2ace512e6359bd7015a0b4aa1ccc207d; miid=431151891030665784; cookie2=20f0ab267f8ab43bf3f782e54d5371e3; _tb_token_=f33e76fb8938; xlly_s=1; _m_h5_tk=c2ad0900ae4716736100940e32b3f567_1613505747028; _m_h5_tk_enc=4ffee823f2092738585ce05c06c17057; _samesite_flag_=true; sgcookie=E100kJlo9HlFj4xwYDhoP9tLInmcjNFxjuamsLXGkLF2dhZ8JITQoyMQVy1GLxmPNLsQgSOFmrAPrPQcjZmwrnkvdw%3D%3D; unb=2701589139; uc3=vt3=F8dCuASnGVg6zvmFOtY%3D&nk2=3EWY2QbTAkdb7KWx&lg2=WqG3DMC9VAQiUQ%3D%3D&id2=UU8IPTyRbKU2yw%3D%3D; csg=34052d63; cookie17=UU8IPTyRbKU2yw%3D%3D; dnk=%5Cu72C2%5Cu98D9%5Cu7684%5Cu8717%5Cu725Bye; skt=4b1a9362d949668a; existShop=MTYxMzQ5NTcwMw%3D%3D; uc4=id4=0%40U22PGMm3NWDuPibXLvN1qg0halSG&nk4=0%403jG%2Fc5Qu3r%2B0Ew2RwiFRlrn6iJ8n0cs%3D; _cc_=Vq8l%2BKCLiw%3D%3D; _l_g_=Ug%3D%3D; sg=e90; _nk_=%5Cu72C2%5Cu98D9%5Cu7684%5Cu8717%5Cu725Bye; cookie1=B0EzweA7TLKhu4P1CHazoo1aUxo3HEXdG9jckoF2hK4%3D; mt=ci=77_1; uc1=cookie21=UIHiLt3xSixwH1aenGUFEQ%3D%3D&cookie14=Uoe1gWMDlX%2BSKg%3D%3D&cookie15=UIHiLt3xD8xYTw%3D%3D&cookie16=URm48syIJ1yk0MX2J7mAAEhTuw%3D%3D&existShop=true&pas=0; isg=BHNzJgsJFzFM99tl6NOFjSUXAnedqAdqQ3HdRCUQzxLJJJPGrXiXutG22lTKn19i; l=eBxiHVbVjrVy7dYSBOfanurza77OSIRYYuPzaNbMiOCPOQ1B5MicW6iMUY86C3GVh6E9R38huNTBBeYBqQAonxv9w8VMULkmn; tfstk=ch7GBb4geG-1n_KhVPT1aRi5UhzRwt32EZ7C8wFxMm-E-25myDozxwVHIObxc"

        cookie_value = "" # 请填写自己淘宝登录后的COOKIE [不填写也可也抓取]

        self.headers = {'cookie': cookie_value, 'referer': 'https://s.taobao.com/', 'sec-ch-ua': '"Chromium";v="88", "Google Chrome";v="88", ";Not A Brand";v="99"', 'sec-ch-ua-mobile': '?0', 'sec-fetch-dest': 'document', 'sec-fetch-mode': 'navigate', 'sec-fetch-site': 'same-origin', 'sec-fetch-user': '?1', 'upgrade-insecure-requests': '1', 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36'}
        self.url = "https://detail.tmall.com/item.htm?id={}".format(self.id)
        print(self.url)

        self.baby_title = self.get_title()
        print("#########################################")
        print(f"正在获取 {self.baby_title} 宝贝信息中...")
        print("#########################################")

        self.taobao_data_path = taobao_baby_path
        self.tianmao_baby_file_path = os.path.join(self.taobao_data_path,self.baby_title)
        self.tianmao_baby_sku_path = os.path.join(self.tianmao_baby_file_path, '产品规格图片')  # SKU保存路径
        self.tianmao_baby_slideshow_path = os.path.join(self.tianmao_baby_file_path, "产品轮播推荐图")  # 宝贝轮播图保存位置
        self.tianmao_baby_detail_page_img_path = os.path.join(self.tianmao_baby_file_path,'产品详情页图片')  # 保存宝贝详情页图片位置

        tool.create_folder(self.taobao_data_path)  # 创建 数据保存路径
        tool.create_folder(self.tianmao_baby_file_path)  # 根据宝贝创建路径
        tool.create_folder(self.tianmao_baby_sku_path)  # 创建  SKU 信息文件夹
        tool.create_folder(self.tianmao_baby_slideshow_path)  # 创建轮播图文件夹
        tool.create_folder(self.tianmao_baby_detail_page_img_path)  # 创建详情页文件夹

    def get_title(self):
        """
        获取产品标题

        :return:
        """
        response = requests.get(self.url,headers=self.headers)
        valiteminfo = '{"baby' + str(re.findall(r"ItemInfo(.+)", response.text)[0])
        json_valiteminfo = json.loads(valiteminfo)
        baby_title = tool.zys_text(json_valiteminfo['itemDO']['title'])  # 宝贝标题
        return baby_title


    def get_html(self):
        response = requests.get(self.url,headers=self.headers)

        self.get_attribute(response)
        self.get_parameter(response)

    def get_parameter(self,response):
        """
        获取商品的参数
        :return:
        """
        print("成功获取到 宝贝详情参数")
        parameter = response.text
        parameter_html = BeautifulSoup(parameter,'lxml')
        parameter_text = parameter_html.find_all('ul',id="J_AttrUL")[0].find_all('li')

        parameter_dict = {} # 淘宝宝贝参数信息

        for pt in parameter_text:
            pt_text = str(pt.text).split(':')
            pt_k = str(pt_text[0]).replace('\xa0','')
            pt_v = str(pt_text[-1]).replace('\xa0','')
            pt_info = {pt_k:pt_v}
            parameter_dict.update(pt_info)

        taobao_parameter_info = {self.id:parameter_dict}
        taobao_parameter_info = json.dumps(taobao_parameter_info, indent=4, ensure_ascii=False)
        tool.to_file(f"{self.tianmao_baby_file_path}/{self.baby_title}.json",taobao_parameter_info)

    def get_attribute(self,reponse):
        """
        请求淘宝商品的SKU信息
        :param reponse:
        :return:
        """
        print("成功获取到 宝贝规格参数")
        htmltext =  str(reponse.text)
        valiteminfo =  '{"baby' + str(re.findall(r"ItemInfo(.+)", htmltext)[0])
        json_valiteminfo = json.loads(valiteminfo)

        attribute_name_list = [] # 产品规格名称
        size_name_list = [] # 尺码名称
        skuid_dict = {}

        for jv in json_valiteminfo['baby']['skuList']:# 请求SKU名称
            skuId = jv['skuId']
            size_name_info = str(jv['names']).split(' ') # 尺码名称
            print(size_name_info)

            if len(size_name_info) > 3 :

                size_name = "-".join(size_name_info[0:2])
                size_name_list.append(size_name)
                att_name = tool.zys_text(size_name_info[2:])
                attribute_name_list.append(att_name)
                att_dict = {skuId:att_name}
                skuid_dict.update(att_dict)

            elif len(size_name_info) == 3:

                size_name = "-".join(size_name_info[0:1])
                size_name_list.append(size_name)
                att_name = tool.zys_text(size_name_info[1:])
                attribute_name_list.append(att_name)
                att_dict = {skuId:att_name}
                skuid_dict.update(att_dict)

            else:
                size_name = "-".join(size_name_info[0])
                size_name_list.append(size_name)
                att_name = tool.zys_text(size_name_info[1:])
                attribute_name_list.append(att_name)
                att_dict = {skuId: att_name}
                skuid_dict.update(att_dict)

        self.get_prices(skuid_dict,size_name_list,attribute_name_list)

        details_page_api = "https:" +json_valiteminfo['api']['descUrl'] # 详情页API
        self.get_specifications(json_valiteminfo) # 规格图片[轮播图+规格图]
        self.get_details_page(details_page_api) # 详情页

    def get_prices(self,skuid,size_name_list,attribute_name_list):
        """
        获取真实价格
        :param htmltext:
        :return:

        """
        size_name_list =[x for x in set(size_name_list)]
        attribute_name_list =[x for x in set(attribute_name_list)]
        h5_price_api = "https://detail.m.tmall.com/item.htm?id={}".format(self.id)
        response = requests.get(h5_price_api, headers=self.headers)
        skuCore = '{"baby_price' + str(re.findall(r"addressData(.+) </script>", response.text)[0])
        skucore_json = json.loads(skuCore)
        skucore_json_price = skucore_json['skuCore']['sku2info']
        sku_info_dict = {}
        for sku_k,sku_v in skuid.items():
            sku_price = skucore_json_price[sku_k]['price']['priceText']
            sku_name = {sku_v:sku_price} # SKU 对应真实价格
            sku_info_dict.update(sku_name)

        baby_attribute_info = {"尺码":size_name_list,"规格":attribute_name_list,"价格":sku_info_dict}
        taobao_attribute_info = json.dumps(baby_attribute_info, indent=4, ensure_ascii=False)
        tool.to_file(f"{self.tianmao_baby_file_path}/规格参数.json", taobao_attribute_info)

    def get_specifications(self,response):
        """
        产品左侧轮播图 and 产品规格图片(可能没有)
        :return:
        """
        print('获取到 产品主图 ，马上下载！！！')

        imgInfo = response['propertyPics']

        skuList = response['baby']['skuList']

        names_pvs_list = []
        for sku in skuList:
            names = tool.zys_text(str(sku['names']).split(' ')[1:])
            pvs = str(sku['pvs']).split(';')[-1]
            names_pvs = names + "=" + pvs
            names_pvs_list.append(names_pvs)

        set_names_pvs_list = set(names_pvs_list)

        set_picture_dict = {}
        for set_name in set_names_pvs_list:
            set_name_list = set_name.split('=')
            set_names = set_name_list[0]
            set_par = set_name_list[-1]

            set_picture = {set_par:set_names}
            set_picture_dict.update(set_picture)


        for img in imgInfo:
            new_img = str(img).replace(';','')

            if img == "default":    #产品左侧轮播图片
                # print('产品左侧轮播图片')
                default_shuffling_figure_img = imgInfo[img]
                n = 1
                for default_img in default_shuffling_figure_img:
                    default_img_url = "https:" + default_img # 下载地址
                    tool.downloads(default_img_url, f"{self.tianmao_baby_slideshow_path}/{n}.jpg")
                    n+=1

            else: #产品右侧规格图片
                # print("产品右侧规格图片")
                shuffling_figure_name = set_picture_dict[new_img]
                shuffling_figure_img = "https:" + imgInfo[img][0] # 下载地址

                at_suffix_name = shuffling_figure_img.split('.')[-1]
                sava_file_path1 = os.path.join(self.tianmao_baby_sku_path, shuffling_figure_name + "." + at_suffix_name)
                tool.downloads(shuffling_figure_img, sava_file_path1)

    def get_details_page(self,details_page_api):
        """
        请求商品详情页图片

        :param details_page_api:
        :return:
        """
        print('成功获取到 产品详情页图片 下载中')

        response = requests.get(details_page_api, headers=self.headers)

        details_img = re.findall(r"desc='(.+)</p>", response.text)[0]
        details_img_html = BeautifulSoup(details_img,'lxml')
        details_img_ptag = details_img_html.find_all('p')[0].find_all('img')
        n = 1
        for dip in details_img_ptag:
            details_img_url = dip['src'] # 天猫详情页下载地址
            tool.downloads(details_img_url, f"{self.tianmao_baby_detail_page_img_path}/{n}.jpg")
            n+=1

    def taobao_run(self):

        try:
            self.get_html()
        except:
            print("无法获取到数据，请更换其他商品ID")



if __name__ == '__main__':
    shop_id = "602760047198"  # 更换商品 ID [天猫] -- [服装类-鞋帽类-内衣等产品]，有些商品标签不一样会获取失败

    tianmao(shop_id).taobao_run()
