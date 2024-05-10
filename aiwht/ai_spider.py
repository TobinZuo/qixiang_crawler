import traceback

import scrapy
from scrapy.selector import Selector
from scrapy.http import TextResponse
import requests
from bs4 import BeautifulSoup

# 正式: scrapy runspider ai_spider.py -o aiwht.csv
# 测试: scrapy runspider ai_spider.py -o aiwht_test.csv

class AISpider(scrapy.Spider):
    name = "ai_spider"
    host = "https://www.aiwht.com"
    allowed_domains = [host]
    start_urls = []

    for i in range(9000, 0, -1):
        start_urls.append(host + "/sites/%s.html" % i)

    custom_settings = {
        # 'DOWNLOAD_DELAY': 2,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 32
    }

    # 测试使用
    # start_urls = []
    # test_ids = [8961]
    # for id in test_ids:
    #     start_urls.append(host + "/sites/%s.html" % id)

    def parse(self, response):
        # print("=" * 50)
        # # 用BeautifulSoup解析HTML
        # soup = BeautifulSoup(response.text, "html.parser")
        #
        # # 打印格式化后的HTML内容
        # print(soup.prettify())
        # print("=" * 50)

        # 选取元素并提取内容
        try:
            xpath_str_map = {

                'product_name': '//*[@id="content"]/div[2]/div[2]/div/h1',
                "promotional_image": '//*[@id="content"]/div[2]/div[1]/div/img/@data-src',
                "product_description": '//*[@id="content"]/div[2]/div[2]/div/div/p/text()',
                "product_type": '//*[@id="content"]/div[2]/div[2]/div/a',
                "industry": '//*[@id="content"]/div[2]/div[2]/div/a',
                "ai_tag": '//*[@id="content"]/div[2]/div[2]/div/div/span',
                "product_display_link": '//*[@id="content"]/div[2]/div[2]/div/div/div/span/a/@href',
                "product_display_qr_code": '//*[@id="content"]/div[2]/div[2]/div/div/div/a[1]/@title'

            }

            yield {
                'reptile_source': response.url,
                'product_name': response.xpath(xpath_str_map.get("product_name")).xpath('string()').get().strip(),
                "promotional_image": self.get_img_src(response.xpath(xpath_str_map.get("promotional_image")).extract_first()),
                "product_description": response.xpath(xpath_str_map.get("product_description")).extract_first(),
                'product_type': response.xpath(xpath_str_map.get("product_type")).xpath('string()').get().strip(),
                # 待定。不知道行业是哪个字段。https://www.ainav.cn/sites/1564.html
                'industry': None,
                'ai_tag': self.get_ai_tags(response.xpath(xpath_str_map.get("ai_tag"))),
                'used_model': None,
                'product_display_link': response.xpath(xpath_str_map.get("product_display_link")).extract_first(),
                "product_display_qr_code": self.get_qr_code_url(
                    response.xpath(xpath_str_map.get("product_display_qr_code")).extract_first()),
                "like_num": None,
                "collect_num": None,
                "view_num": None,
            }
        except Exception as ex:
            traceback.print_exc()
            print("执行发生异常, ex=%s" % ex)

    def get_ai_tags(self, spans):
        ai_tags = []
        for span in spans:
            content = span.xpath('string()').get().strip()
            ai_tags.append(content)
        return ai_tags if len(ai_tags) > 0 else None

    def get_qr_code_url(self, html):
        # 创建一个 Selector 对象，用于在给定的 HTML 文本中查找元素
        sel = Selector(text=html)

        # 使用 CSS 选择器找到 img 标签，并提取其 src 属性
        src = sel.css('img::attr(src)').get()

        return src

    def get_img_src(self, raw_src):
        if raw_src.startswith(r'//'):
            return 'https:' + raw_src
        return raw_src
