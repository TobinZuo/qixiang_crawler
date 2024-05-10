from scrapy import Selector

html = "<img src='https://www.ainav.cn/qr/?text=https://minigpt-v2.github.io/&size=150&margin=10' width='150'>"

# 创建一个 Selector 对象，用于在给定的 HTML 文本中查找元素
sel = Selector(text=html)

# 使用 CSS 选择器找到 img 标签，并提取其 src 属性
src = sel.css('img::attr(src)').get()

print(src)  # 将输出 'https://www.ainav.cn/qr/?text=https://minigpt-v2.github.io/&size=150&margin=10'