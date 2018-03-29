# coding = utf-8
import codecs
from lxml import etree
import re
import random


def nike_shop():
    fi = codecs.open("nike_shop1.htm", "r", "gbk")
    html = fi.read()
    fi.close()
    html="""
      <head>
    <meta charset="gbk" /><meta content="hahah"/>
    <meta name="renderer" content="webkit">
    <meta http-equiv="X-UA-Compatible" content="IE=Edge">
    
    """
    # 匹配页面编码
    match_obj = re.search(r"<meta charset=\"(.+?)\"\s*/>", html)
    if match_obj:
        print(match_obj.group(1))
    print("no!")

    exit()
    selector = etree.HTML(html)
    # 解析页面信息
    # 内容列表
    list_area = selector.xpath("//div[@id='J_ItemList\']/div")
    for item_area in list_area:
        shop=item_area.xpath("div[1]/div[1]/a")[0]
        html = etree.tostring(shop)
        # print(html)
        # 去除html标签
        # https://www.zhihu.com/question/40443483/answer/86721491
        # https://stackoverflow.com/questions/10618016/html-xpath-extracting-text-mixed-in-with-multiple-tags
        # print(shop.xpath("string(.)").replace("\n","".replace(" ","")))
        # 商店名称
        shop_name = str(shop.text)
        # 商店链接地址
        shop_url = shop.get("href")
        # 商店所在地（省、市）
        location_txt = list0_to_str(item_area.xpath("div[1]/div[1]/p[2]/text()"))
        location = location_txt.strip(u"所在地：")
        # 更多商品的链接地址
        more_shop_url = list0_to_str(item_area.xpath("div[2]/p/a/@href"))
        # print(shop_name+" "+location+" "+shop_url+" "+more_shop_url)
    # 获取翻页信息
    page_area = selector.xpath("//a[@class='ui-page-next']")
    if len(page_area)>0:
        next_page_url = page_area[0].get("href")
        # print(next_page_url)


def list0_to_str(input_list):
    if len(input_list) > 0:
        return str(input_list[0])
    return ""


def nike_item():
    fi = codecs.open("nike_item2.htm", "r", "gbk")
    html = fi.read()
    fi.close()
    selector = etree.HTML(html)
    html = etree.tostring(selector)
    # 获取页面信息
    list_area = selector.xpath("//div[@id='J_ItemList\']/div")
    for item_area in list_area:
        price = item_area.xpath("div/p[1]/em/text()")[0]
        item_name = item_area.xpath("div/p[2]/a")[0].get("title")
        deal_num = item_area.xpath("div/p[3]/span[1]/em/text()")[0].strip(u"笔")
        comment_num = item_area.xpath("div/p[3]/span[2]/a/text()")[0]
        print(item_name)
    # 获取翻页信息
    page_area = selector.xpath("//a[@class='ui-page-next']")
    if len(page_area)>0:
        next_page_url = page_area[0].get("href")
        print(next_page_url)


def citic():
    fi=codecs.open("citic.htm","r","utf-8")
    html=fi.read()
    fi.close()
    selector = etree.HTML(html)
    # 获取页面信息
    result = selector.xpath("//div[@class='content-w']/div[@class='content']/div[@class='iteam']")
    for div in result:
        # 卡名称
        card_name = div.xpath("div[1]/a[2]")[0].text
        print(card_name)
        card_cash_type = div.xpath("div[2]/div[1]/span[1]/i")[0].text
        print(card_cash_type)
        card_org = div.xpath("div[2]/div[1]/span[2]/i")[0].text
        print(card_org)
        card_rank = div.xpath("div[2]/div[1]/span[3]/i")[0].text
        print(card_rank)
        cash_amount = div.xpath("div[2]/div[1]/span[4]/i")[0].text
        print(cash_amount.strip())
        free_interest = div.xpath("div[2]/div[1]/span[5]/i")[0].text
        print(free_interest.strip())
        score_rule = div.xpath("div[2]/div[2]/p[1]")[0].text
        print(score_rule.strip())
        free_policy = div.xpath("div[2]/div[2]/p[2]")[0].text
        print(free_policy.strip())
        break
    # 翻页信息
    result = selector.xpath("//div[@class='page-box']/ul/li[@class='next-page']/a")
    if (result is not None) and len(result)>0:
        next_page_href = result[0].get("href")
        print(next_page_href)


def random_ip():
    """随机生成ip"""
    ip1 = random.randint(10, 245)
    ip2 = random.randint(10, 245)
    ip3 = random.randint(10, 245)
    ip4 = random.randint(10, 245)
    return "%d.%d.%d.%d" % (ip1, ip2, ip3, ip4)


if __name__ == '__main__':
    # nike_item()
    nike_shop()
