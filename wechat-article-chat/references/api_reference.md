# 微信公众号接口技术参考

## 文章URL格式

```
https://mp.weixin.qq.com/s/{article_id}
https://mp.weixin.qq.com/s?__biz={biz_id}&mid={msg_id}&sn={sn}
```

参数说明：
- `article_id` / `sn`: 文章唯一标识
- `biz`: 公众号唯一标识
- `mid`: 消息ID

## 请求流程

### 1. 直接请求文章URL（公开文章）

```http
GET https://mp.weixin.qq.com/s/xxx
Host: mp.weixin.qq.com
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9
Referer: https://mp.weixin.qq.com/
```

### 2. 携带Cookie请求（受限文章）

```http
GET https://mp.weixin.qq.com/s/xxx
Cookie: key=xxx; pass_ticket=xxx; wxuin=xxx
```

## 响应HTML结构

关键DOM元素：
```html
<!-- 文章标题 -->
<meta property="og:title" content="文章标题" />

<!-- 公众号名称 -->
<meta property="og:site_name" content="公众号名称" />

<!-- 正文内容 -->
<div id="js_content" class="rich_media_content">
  <!-- 文章内容 -->
</div>
```

## 反爬机制

| 机制 | 说明 | 应对方案 |
|------|------|---------|
| Cookie验证 | 需要有效的登录Cookie | 配置Cookie |
| User-Agent检测 | 检查请求头 | 使用真实浏览器UA |
| 请求频率限制 | 高频请求被限制 | 控制请求频率 |
| IP限制 | 同IP请求过多 | 暂无（个人使用足够） |

## 错误类型与处理

### HTML响应判断

```python
# 需要登录
if '请先登录' in html or '账号登录' in html:
    return {"error": "需要配置Cookie"}

# 文章已删除
if '此内容因违规无法查看' in html or '文章已被删除' in html:
    return {"error": "文章已被删除或违规"}

# 链接过期
if '链接已过期' in html or '此链接已失效' in html:
    return {"error": "文章链接已过期，需要Cookie"}
```

## 状态码

| 状态码 | 说明 | 处理方式 |
|-------|------|---------|
| 200 | 成功 | 解析HTML内容 |
| 302 | 重定向 | 检查是否跳转到登录页 |
| 404 | 不存在 | 文章可能被删除 |

## 解析文章内容

使用BeautifulSoup + html2text：

```python
from bs4 import BeautifulSoup
import html2text

soup = BeautifulSoup(html, 'html.parser')

# 获取正文
content_div = soup.find('div', {'id': 'js_content'})

# 转换为Markdown
h = html2text.HTML2Text()
h.ignore_links = False
h.ignore_images = False
content = h.handle(str(content_div))
```

## 接口限速建议

- **最小间隔**: 2秒/请求
- **推荐间隔**: 5秒/请求
- **批量请求**: 每小时不超过100次

个人使用场景下，这些限制已经足够。
