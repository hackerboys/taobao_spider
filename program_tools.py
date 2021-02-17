#encoding:utf-8
"""
淘宝爬虫工具集合
小红书自动化工具集合

"""
import ast
import json
import os
import requests
import win32con
import win32gui
import os
import time
from PIL import Image                                       # 处理图片模块
import os
import shutil
import re


class tools():

    def __init__(self):
        pass

    def zys_text(self,str_text):
        """
        提取中文英文数字
        :return:
        """
        color_name = re.findall('[\u4e00-\u9fa5a-zA-Z0-9]+', str(str_text), re.S)
        new_text = "".join(color_name)
        return new_text
    def wt_file(self,filename,content):
        """
        覆盖写入数据
        """
        with open("%s"%filename,'w',encoding='utf-8') as f:
            f.write(str(content)+"\n")
            f.close()


    def to_file(self,filename,content):
        """
        追加写入数据
        """
        with open("%s"%filename,'a+',encoding='utf-8') as f:
            f.write(str(content)+"\n")
            f.close()


    def re_file(self,filename):
        """
        读取数据，并返回list。
        """
        content = []

        with open("%s"%filename,'r',encoding='utf-8') as f:
            text = str(f.read()).split('\n')
            for t in text:
                if "[" in str(t) and "]" in str(t):
                    if len(t)>1:
                        t_list = ast.literal_eval(t)
                        content.append(t_list)

                else:
                    if t!=[] and t!="":
                        content.append(t)

        return content


    def read_jsonfolder(self,filename):
        """
        读取json 文件夹

        """

        with open('%s'%filename,'r',encoding='utf-8') as f:

            jsondata = f.read()

            return jsondata

    def read_jsonfile(self,filename):
        """
        读取JSON文件

        """

        with open('%s.json'%filename,'r',encoding='utf-8') as f:

            jsondata = str(f.read()).replace("'",'"')

            jd = json.loads(jsondata)

            return jd


    def to_jsonfile(self,filename,content):
        """
        写入json 文件

        """

        new_content = json.dumps(content, ensure_ascii=False,indent=4)
        with open('%s.json'%filename, 'w+',encoding='utf-8') as f:
            f.write(new_content)
            f.close()



    def merge_dict(self,dict1,dict2):
        """
        合并两个字典

        """

        new_dict = {}

        c = {}

        for k, v in dict1.items():
            l = []
            for x, y in dict2.items():
                if k == x:
                    l.append(v)
                    l.append(y)
                    new = {k: l}
                    c.update(new)

        new_dict.update(dict1)
        new_dict.update(dict2)
        new_dict.update(c)
        return new_dict


    def create_folder(self,filepath):
        """
        创建文件夹

        """
        while True:
            if os.path.isdir(filepath):

                break
            else:
                os.makedirs(filepath)

    def downloads(self,url,filename):
        """
        下载功能

        """
        n = 0
        while True:
            try:
                data = requests.get(url)
                with open('%s'%filename,'wb+') as f:
                    f.write(data.content)
                    f.close()
                print(url," ----- 下载成功")
                break

            except:
                n+=1
                if n%5==0:
                    print("10秒后继续下载文件")
                    time.sleep(10)
                if n%20==0:
                    self.to_file('taobao_errror_url.txt',url)



                else:
                    self.downloads(url,filename)

    def formatted_text(self,text):

        new_text = str(text).replace('\n','').replace(' ','')
        return new_text

    def upload_file(self,filepath):
        """
        上传功能

        """
        time.sleep(2)
        dialog = win32gui.FindWindow('#32770', '打开')  # 对话框
        ComboBoxEx32 = win32gui.FindWindowEx(dialog, 0, 'ComboBoxEx32', None)
        ComboBox = win32gui.FindWindowEx(ComboBoxEx32, 0, 'ComboBox', None)
        Edit = win32gui.FindWindowEx(ComboBox, 0, 'Edit', None)  # 上面三句依次寻找对象，直到找到输入框Edit对象的句柄
        button = win32gui.FindWindowEx(dialog, 0, 'Button', None)  # 确定按钮Button
        win32gui.SendMessage(Edit, win32con.WM_SETTEXT, None, filepath)  # 往输入框输入绝对地址
        win32gui.SendMessage(dialog, win32con.WM_COMMAND, 1, button)  # 按button
        time.sleep(2)

    def smaller_img(self,filepath,filename):  # x,y用来传入尺寸，path用来传入路径
        #修改图片尺寸
        old_img = Image.open(filepath)
        img_deal = old_img.resize((800,800), Image.ANTIALIAS)  # 转换图片
        img_deal = img_deal.convert('RGB')  # 保存为jpg格式才需要
        img_deal.save(filename)




class xsh_att_pro():
    """
    匹配小红书商品后台的属性参数


    """


    def __init__(self,u):
        self.u = u

    def formatting_data(self):

        new_u = str(self.u).replace("'", '"')
        jd = json.loads(new_u)

        n = []
        c = {}

        for k, v in jd.items():
            if isinstance(v, list):

                if len(v) > 1:
                    number = v[-1]

                    n.append(int(number))
                    uc = {

                        k: v

                    }
                    c.update(uc)
        return n,c

    def findSmallest(self,arr):
        smallest = arr[0]  # 将第一个元素的值作为最小值赋给smallest
        smallest_index = 0  # 将第一个值的索引作为最小值的索引赋给smallest_index
        for i in range(1, len(arr)):
            if arr[i] < smallest:  # 对列表arr中的元素进行一一对比
                smallest = arr[i]
                smallest_index = i
        return smallest_index

    def selectionSort(self,arr):
        newArr = []
        for i in range(len(arr)):
            smallest = self.findSmallest(arr)  # 一共要调用5次findSmallest
            newArr.append(arr.pop(smallest))  # 每一次都把findSmallest里面的最小值删除并存放在新的数组newArr中
        return newArr

    def dict_data(self):
        n,c = self.formatting_data()

        u = self.selectionSort(n)

        dd = {}

        for x in u:
            for h, j in c.items():

                if str(x) == str(j[-1]):
                    new_d = {
                        h: j

                    }
                    dd.update(new_d)

        return dd



if __name__ == '__main__':
    u = "{'上市季节': ['春', 2], '上市年份': ['2020', 3], '厚薄': ['常规', 4], '图案': ['其他', 11], '工艺处理': ['其他', 12], '性别': ['通用', 5], '材质': ['其他', 13], '材质成分': ['其他', 14], '款式': ['开衫', 6], '款式细节': ['其他', 15], '毛线粗细': ['常规', 16], '版型': ['直筒', 17], '袖型': ['常规', 18], '袖长': ['长袖', 7], '适用场景': ['雨天', 19], '适用季节': ['春', 8], '适用对象': ['青年', 20], '领型': ['门筒领（亨利领）', 9], '风格': ['其他', 10], '面料': '其他', '尺码': 'S【加厚】 M【加厚】 L【加厚】 XL【加厚】 S M L XL', '主要颜色': '咖啡色 经典黑 奶白色 温柔杏 南瓜色 高级灰 雾霾蓝 铁锈红 燕麦色', '面料主材质含量': '71', '': 1}"

    xap = xsh_att_pro(u).dict_data()

