---
name: daily-hot-fetcher
description: 全平台热门信息获取器。自动抓取每天国内外各平台热门信息：国内（微博热搜、知乎热榜、百度热搜、抖音6榜单、B站热搜、今日头条、虎扑、豆瓣、36氪、少数派等）+
user-invocable: true
---


# 全平台热门信息获取器

## 触发条件

### 获取热门信息

**关键词匹配**（包含以下任意词汇即可触发）：

| 类别 | 关键词 |
|------|--------|
| 通用 | 热点、热搜、热门、热榜、趋势、流行、火、爆款、头条 |
| 时间词 | 今天、今日、最近、目前、现在、这周、本周 |
| 动作词 | 看看、查查、获取、抓取、看看有什么、显示、展示 |
| 组合示例 | 今天有什么热点、看看热搜、今天流行什么、最近什么火、刷刷热榜、今天的头条、现在热门、获取热门信息、看看趋势 |

**平台特定触发**：
- 微博：微博热搜、微博热门、微博热榜、微博上什么
- 知乎：知乎热榜、知乎热门、知乎上什么
- 抖音：抖音热榜、抖音热点、抖音6榜单、抖音综合榜、抖音娱乐榜
- 百度：百度热搜、百度热榜
- B站：B站热门、bilibili热搜
- Hacker News：HN热门、Hacker News今天什么
- GitHub：GitHub Trending、GitHub热门、github趋势
- Reddit：Reddit热门、Reddit热帖

### 实时搜索

**关键词匹配**（包含以下任意词汇即可触发）：

| 类别 | 关键词 |
|------|--------|
| 搜索词 | 搜索、查找、找一找、search、实时搜索、全网搜索 |
| 范围词 | 国内外、全网、全平台、综合、全面 |
| 话题词 | 最新资讯、新闻、动态、tech、技术 |

**自然语言变体**：
```
✓ "搜索 AI 相关新闻"
✓ "实时搜索 科技资讯"
✓ "搜索一下 最新动态"
✓ "全网搜索 人工智能"
✓ "获取最新资讯"
✓ "搜索技术新闻"
```

**模糊匹配示例**：
```
✓ "今天有什么热点"
✓ "热搜看看"
✓ "最近什么比较火"
✓ "今天微博上什么"
✓ "刷刷热搜"
✓ "给我看看今天的热门"
✓ "现在流行什么"
✓ "有什么新闻"
✓ "今天头条"
✓ "获取热搜"
```

### 登录管理

**关键词匹配**（包含以下任意词汇即可触发）：

| 类别 | 关键词 |
|------|--------|
| 动作词 | 登录、登入、登录一下、扫码、认证、授权 |
| 辅助词 | 帮我、帮我一下、需要、要、重新、刷新、更新 |
| 平台词 | 抖音、知乎、微博、所有平台、全部平台 |

**自然语言变体**：
```
✓ "登录抖音" / "抖音登录"
✓ "帮我登录抖音"
✓ "抖音要登录"
✓ "登录一下知乎"
✓ "帮我登录微博"
✓ "重新登录"
✓ "刷新登录"
✓ "更新登录状态"
✓ "Cookie过期了"
✓ "无法获取数据"
✓ "需要登录"
✓ "扫码登录"
✓ "全部登录"
✓ "登录所有平台"
```

### 状态查询

**关键词匹配**（包含以下任意词汇即可触发）：

| 类别 | 关键词 |
|------|--------|
| 状态词 | 状态、怎么样、如何、有效、无效、过期、可用 |
| 检查词 | 检查、查看、看看、查询、显示、展示、确认 |
| Cookie相关 | Cookie、Session、登录状态、认证状态 |

**自然语言变体**：
```
✓ "检查登录状态"
✓ "登录状态怎么样"
✓ "Cookie状态"
✓ "查看登录状态"
✓ "登录有效吗"
✓ "Session状态"
✓ "还能用吗"
✓ "Cookie过期了吗"
✓ "检查一下登录"
✓ "看看登录"
✓ "登录检查"
✓ "状态怎么样"
```

## 支持的平台

### 国内平台

| 平台 | 热榜类型 | 数据源 |
|------|----------|--------|
| 微博 | 微博热搜 | weibo.com/hot/search |
| 知乎 | 知乎热榜 | zhihu.com/hot |
| 百度 | 百度热搜 | baidu.com/s?wd=热搜 |
| 抖音 | 抖音热点 | douyin.com/hot |
| B站 | B站热搜 | bilibili.com/v/popular/all |
| 今日头条 | 头条热榜 | toutiao.com/hot-event/hot-board |
| 虎扑 | 虎扑热搜 | hupu.com |
| 豆瓣 | 豆瓣榜单 | douban.com |
| 36氪 | 36氪快讯 | 36kr.com |
| 少数派 | 少数派热门 | sspai.com |
| V2EX | V2EX热门 | v2ex.com |
| SegmentFault | SF热门 | segmentfault.com |
| 掘金 | 掘金热门 | juejin.cn |
| CSDN | CSDN热门 | csdn.net |

### 国外平台

| 平台 | 热榜类型 | 数据源 |
|------|----------|--------|
| Hacker News | 技术热门 | news.ycombinator.com |
| Reddit | 热门帖子 | reddit.com |
| Product Hunt | 产品发现 | producthunt.com |
| Twitter/X | 趋势话题 | twitter.com |
| GitHub | Trending 仓库 | github.com/trending |
| YouTube | 热门视频 | youtube.com |
| The Verge | 科技新闻 | theverge.com |
| TechCrunch | 科技新闻 | techcrunch.com |
| Indie Hackers | 创业者社区 | indiehackers.com |
| Lobsters | 技术新闻 | lobste.rs |
| Hacker News (ALT) | HN 备用 | hn.algolia.com |

## 工作流程

### 自然语言匹配逻辑

当用户输入时，按以下优先级进行匹配：

**优先级 1: 登录管理**
```
包含 "登录" OR "登入" OR "扫码" OR "认证" + 可选平台词
→ 执行对应平台的登录操作

包含 "重新" OR "刷新" OR "更新" + "登录"
→ 执行强制重新登录

包含 "所有" OR "全部" + "登录"
→ 执行全平台登录
```

**优先级 2: 状态查询**
```
包含 "状态" OR "检查" OR "查看" + 可选 "登录"/"Cookie"/"Session"
→ 执行状态查询命令

包含 "有效" OR "过期" OR "可用" OR "怎么样"
→ 执行状态查询命令
```

**优先级 3: 获取热门**
```
包含 "热点" OR "热搜" OR "热门" OR "热榜"
→ 执行获取热门信息

包含平台关键词 (微博/知乎/抖音/百度/B站/HN/Reddit/GitHub)
→ 执行对应平台的热门获取
```

**匹配示例**：
```python
# 伪代码示例
user_input = "帮我看看登录状态怎么样"

if any(word in user_input for word in ["登录", "登入", "扫码"]):
    if any(word in user_input for word in ["抖音", "douyin"]):
        platform = "douyin"
        command = f"auto_login.py {platform}"
elif any(word in user_input for word in ["状态", "检查", "有效", "过期"]):
    command = "auto_login.py --check"
elif any(word in user_input for word in ["热点", "热搜", "热门", "热榜"]):
    command = "fetch.py"
```

### 自然语言命令映射

当用户使用自然语言时，执行对应的命令：

#### 登录管理

| 用户输入示例 | 执行命令 |
|-------------|----------|
| "登录抖音" / "抖音登录" | `python ~/.claude/skills/daily-hot-fetcher/scripts/auto_login.py douyin` |
| "登录知乎" / "知乎登录" | `python ~/.claude/skills/daily-hot-fetcher/scripts/auto_login.py zhihu` |
| "登录微博" / "微博登录" | `python ~/.claude/skills/daily-hot-fetcher/scripts/auto_login.py weibo` |
| "登录X" / "登录Twitter" | `python ~/.claude/skills/daily-hot-fetcher/scripts/auto_login.py x` |
| "登录所有平台" / "全部登录" | `python ~/.claude/skills/daily-hot-fetcher/scripts/auto_login.py all` |
| "重新登录" / "刷新登录" | `python ~/.claude/skills/daily-hot-fetcher/scripts/auto_login.py all --force` |
| "检查登录状态" / "状态检查" | `python ~/.claude/skills/daily-hot-fetcher/scripts/auto_login.py --check` |

#### 获取热门信息

| 用户输入示例 | 执行命令 |
|-------------|----------|
| "今天有什么热点" / "获取热搜" | `python ~/.claude/skills/daily-hot-fetcher/scripts/fetch.py` |
| "获取国内热搜" / "国内热门" | `python ~/.claude/skills/daily-hot-fetcher/scripts/fetch.py --platforms domestic` |
| "获取国外热搜" / "国外热门" | `python ~/.claude/skills/daily-hot-fetcher/scripts/fetch.py --platforms international` |
| "微博热搜" | `python ~/.claude/skills/daily-hot-fetcher/scripts/fetch.py --platforms weibo` |
| "知乎热榜" | `python ~/.claude/skills/daily-hot-fetcher/scripts/fetch.py --platforms zhihu` |
| "抖音热榜" / "抖音6榜单" | `python ~/.claude/skills/daily-hot-fetcher/scripts/auto_login.py douyin` (登录后获取) |
| "Hacker News" / "HN热门" | `python ~/.claude/skills/daily-hot-fetcher/scripts/fetch.py --platforms hn` |
| "GitHub Trending" | `python ~/.claude/skills/daily-hot-fetcher/scripts/fetch.py --platforms github` |
| "保存热搜到文件" | `python ~/.claude/skills/daily-hot-fetcher/scripts/fetch.py --output hot.md` |

#### 实时搜索

| 用户输入示例 | 执行命令 |
|-------------|----------|
| "实时搜索" / "全网搜索" | `python ~/.claude/skills/daily-hot-fetcher/scripts/realtime_search.py` |
| "搜索 AI 新闻" / "查找 AI" | `python ~/.claude/skills/daily-hot-fetcher/scripts/realtime_search.py --query AI` |
| "搜索区块链" / "查找区块链" | `python ~/.claude/skills/daily-hot-fetcher/scripts/realtime_search.py --query 区块链` |
| "搜索技术新闻" / "tech 搜索" | `python ~/.claude/skills/daily-hot-fetcher/scripts/realtime_search.py --sources hn,github,techcrunch --limit 10` |
| "中文搜索" / "搜索中文资讯" | `python ~/.claude/skills/daily-hot-fetcher/scripts/realtime_search.py --sources 36kr,sspai,baidu` |
| "搜索并保存" | `python ~/.claude/skills/daily-hot-fetcher/scripts/realtime_search.py --output search.md` |

#### 综合查询

| 用户输入示例 | 执行命令 |
|-------------|----------|
| "获取今天的全部信息" | 先执行 `fetch.py`，再执行 `realtime_search.py` |
| "热搜 + 搜索" | 组合执行两个脚本 |
| "全面获取" | 所有平台 + 所有搜索源 |

#### 命令参数说明

**fetch.py 参数**:
- `--platforms` 平台选择: `all`, `domestic`, `international`, 或 `weibo,zhihu,hn`
- `--limit` 每平台条目数: 默认 10
- `--output` 输出文件路径

**realtime_search.py 参数**:
- `--query` 搜索关键词
- `--sources` 搜索源: `hn`, `reddit`, `github`, `36kr`, `sspai`, `techcrunch`, `verge`, `ddg`, `baidu`, `gnews`
- `--limit` 每源结果数: 默认 10
- `--output` 输出文件路径

**auto_login.py 参数**:
- 平台名称: `zhihu`, `douyin`, `weibo`, `x`, `twitter`, `all`
- `--force` 强制重新登录
- `--check` 检查登录状态

### 自然语言解析逻辑

当用户输入自然语言时，按以下逻辑解析并执行命令：

#### 步骤 1: 判断意图类型

```python
# 伪代码示例
def parse_intent(user_input):
    user_input = user_input.lower()

    # 优先级 1: 登录管理
    if any(word in user_input for word in ["登录", "登入", "扫码", "认证"]):
        return "login"

    # 优先级 2: 状态查询
    if any(word in user_input for word in ["状态", "检查", "有效", "过期", "怎么样"]):
        return "status"

    # 优先级 3: 搜索
    if any(word in user_input for word in ["搜索", "查找", "找一找", "search"]):
        return "search"

    # 优先级 4: 获取热门
    if any(word in user_input for word in ["热点", "热搜", "热门", "热榜", "趋势", "流行"]):
        return "hot"

    return "unknown"
```

#### 步骤 2: 提取参数

```python
def extract_params(user_input, intent):
    params = {}

    if intent == "login":
        # 提取平台
        platforms = {"抖音": "douyin", "知乎": "zhihu", "微博": "weibo", "x": "x", "twitter": "x"}
        for name, code in platforms.items():
            if name in user_input.lower():
                params["platform"] = code
                break

        # 检测强制重新登录
        if any(word in user_input for word in ["重新", "刷新", "更新", "强制"]):
            params["force"] = True

    elif intent == "search":
        # 提取搜索关键词
        # "搜索 AI 新闻" -> "AI"
        # "查找区块链相关" -> "区块链"
        import re
        match = re.search(r'搜索|查找|找一找|search\s*(["\']?)([^\s"\',.。]+)', user_input)
        if match:
            params["query"] = match.group(2)

        # 检测中文/技术类搜索
        if any(word in user_input for word in ["中文", "国内", "cn"]):
            params["sources"] = "36kr,sspai,baidu"
        elif any(word in user_input for word in ["技术", "tech", "编程"]):
            params["sources"] = "hn,github,reddit"

    elif intent == "hot":
        # 提取平台
        if "国内" in user_input or " domestic" in user_input.lower():
            params["platforms"] = "domestic"
        elif "国外" in user_input or "international" in user_input.lower():
            params["platforms"] = "international"
        # 可以添加更多平台检测...

    return params
```

#### 步骤 3: 构建并执行命令

```python
def execute_command(intent, params):
    base_path = "~/.claude/skills/daily-hot-fetcher/scripts"

    if intent == "login":
        platform = params.get("platform", "all")
        force = " --force" if params.get("force") else ""
        return f"python {base_path}/auto_login.py {platform}{force}"

    elif intent == "status":
        return f"python {base_path}/auto_login.py --check"

    elif intent == "search":
        query = params.get("query", "")
        sources = params.get("sources", "hn,github,sspai")
        return f'python {base_path}/realtime_search.py --query "{query}" --sources {sources}'

    elif intent == "hot":
        platforms = params.get("platforms", "all")
        return f"python {base_path}/fetch.py --platforms {platforms}"

    return ""
```

#### 完整示例

```
用户输入: "搜索 AI 技术新闻"

解析过程:
1. intent = "search" (包含"搜索")
2. params = {query: "AI", sources: "hn,github,reddit"} (检测到"技术")
3. command = 'python ~/.../realtime_search.py --query "AI" --sources hn,github,reddit'
```

### 实时搜索功能

**支持的搜索源**：

| 搜索源 | 说明 | 类型 |
|--------|------|------|
| Hacker News | Algolia 搜索 API | 技术论坛 |
| Reddit | JSON 搜索 | 社区讨论 |
| DuckDuckGo | HTML 搜索 | 综合搜索 |
| 百度 | 中文搜索 | 中文内容 |
| Google News | RSS 新闻 | 新闻聚合 |
| TechCrunch | 科技新闻 | 科技媒体 |
| The Verge | 科技新闻 | 科技媒体 |
| 36氪 | 中文科技 | 科技媒体 |
| 少数派 | 中文科技 | 效率工具 |
| GitHub Trending | 热门仓库 | 开发者 |

**使用方式**：

```bash
# 实时搜索（获取最新资讯，无需关键词）
python ~/.claude/skills/daily-hot-fetcher/scripts/realtime_search.py

# 搜索指定关键词
python ~/.claude/skills/daily-hot-fetcher/scripts/realtime_search.py --query "AI"

# 指定搜索源
python ~/.claude/skills/daily-hot-fetcher/scripts/realtime_search.py --query "区块链" --sources hn,reddit,github

# 保存结果
python ~/.claude/skills/daily-hot-fetcher/scripts/realtime_search.py --output today_search.md

# 组合：热搜 + 实时搜索
python ~/.claude/skills/daily-hot-fetcher/scripts/fetch.py --output hot.md && python ~/.claude/skills/daily-hot-fetcher/scripts/realtime_search.py --output search.md
```

**搜索源代码**：
- `hn` - Hacker News (官方 Algolia API)
- `reddit` - Reddit 搜索
- `ddg` - DuckDuckGo 搜索
- `baidu` - 百度搜索
- `gnews` - Google News
- `techcrunch` - TechCrunch 最新
- `verge` - The Verge 最新
- `36kr` - 36氪最新
- `sspai` - 少数派最新
- `github` - GitHub Trending

### 方式一：使用 Python 脚本（推荐）

使用内置的可视化爬虫脚本：

```bash
# 获取所有平台热门（默认前10）
python ~/.claude/skills/daily-hot-fetcher/scripts/fetch.py

# 只获取国内平台
python ~/.claude/skills/daily-hot-fetcher/scripts/fetch.py --platforms domestic

# 只获取国外平台
python ~/.claude/skills/daily-hot-fetcher/scripts/fetch.py --platforms international

# 指定平台
python ~/.claude/skills/daily-hot-fetcher/scripts/fetch.py --platforms weibo,zhihu,hn

# 获取更多条目（每平台20条）
python ~/.claude/skills/daily-hot-fetcher/scripts/fetch.py --limit 20

# 保存到文件
python ~/.claude/skills/daily-hot-fetcher/scripts/fetch.py --output hot.md

# 使用极简主题
python ~/.claude/skills/daily-hot-fetcher/scripts/fetch.py --theme minimal
```

### 方式二：使用 MCP 工具

如果安装了 `multi-platform-content-fetcher` MCP 服务：

```bash
# 调用 MCP 服务获取内容
mcp-client fetch-all-platforms
```

### 方式三：使用 Web Reader MCP

对于单个页面，使用 web_reader MCP 工具：

```
1. 访问平台热榜页面
2. 使用 web_reader webReader 工具提取内容
3. 解析和格式化输出
```

## 数据获取方法

### 1. Hacker News (API)

```python
import requests

def get_hn_top(limit=10):
    # 获取 Top Stories IDs
    url = "https://hacker-news.firebaseio.com/v0/topstories.json"
    ids = requests.get(url).json()[:limit]

    results = []
    for item_id in ids:
        item_url = f"https://hacker-news.firebaseio.com/v0/item/{item_id}.json"
        item = requests.get(item_url).json()
        results.append({
            'title': item.get('title'),
            'url': item.get('url'),
            'score': item.get('score'),
            'comments': item.get('descendants')
        })

    return results
```

### 2. Reddit (JSON)

```python
import requests

def get_reddit_hot(subreddit="programming", limit=10):
    url = f"https://www.reddit.com/r/{subreddit}/hot.json?limit={limit}"
    headers = {'User-Agent': 'Mozilla/5.0'}
    data = requests.get(url, headers=headers).json()

    results = []
    for post in data['data']['children']:
        results.append({
            'title': post['data']['title'],
            'url': f"https://reddit.com{post['data']['permalink']}",
            'score': post['data']['score'],
            'comments': post['data']['num_comments']
        })

    return results
```

### 3. GitHub Trending (HTML解析)

```python
import requests
from bs4 import BeautifulSoup

def get_github_trending(language="", limit=10):
    url = f"https://github.com/trending/{language}"
    headers = {'User-Agent': 'Mozilla/5.0'}
    resp = requests.get(url, headers=headers)
    soup = BeautifulSoup(resp.text, 'html.parser')

    results = []
    for repo in soup.select('article.Box-row')[:limit]:
        results.append({
            'name': repo.select_one('h2 a').text.strip().replace('\n', '').replace(' ', ''),
            'url': "https://github.com" + repo.select_one('h2 a')['href'],
            'stars': repo.select_one('span.d-inline-block').text.strip()
        })

    return results
```

### 4. 微博热搜 (HTML解析)

```python
import requests
from bs4 import BeautifulSoup

def get_weibo_hot(limit=10):
    url = "https://s.weibo.com/top/summary"
    headers = {'User-Agent': 'Mozilla/5.0', 'Referer': 'https://weibo.com'}
    resp = requests.get(url, headers=headers)
    soup = BeautifulSoup(resp.text, 'html.parser')

    results = []
    for item in soup.select('#pl_top_realtimehot table tbody tr')[:limit]:
        link = item.select_one('td:nth-child(2) a')
        if link:
            results.append({
                'title': link.text,
                'url': 'https://s.weibo.com' + link['href'],
                'rank': item.select_one('td:nth-child(1)').text,
                'hot': item.select_one('td:nth-child(3)').text if item.select_one('td:nth-child(3)') else ''
            })

    return results
```

### 5. 知乎热榜 (HTML解析)

```python
import requests
from bs4 import BeautifulSoup

def get_zhihu_hot(limit=10):
    url = "https://www.zhihu.com/hot"
    headers = {'User-Agent': 'Mozilla/5.0'}
    resp = requests.get(url, headers=headers)
    soup = BeautifulSoup(resp.text, 'html.parser')

    results = []
    for item in soup.select('.HotItem')[:limit]:
        title_elem = item.select_one('.HotItem-title')
        if title_elem:
            results.append({
                'title': title_elem.text,
                'url': 'https://zhihu.com' + title_elem.select_one('a')['href'],
                'score': item.select_one('.HotItem-score').text if item.select_one('.HotItem-score') else ''
            })

    return results
```

### 6. Product Hunt (API)

```python
import requests
from datetime import datetime

def get_product_hunt(date=None, limit=10):
    if date is None:
        date = datetime.now().strftime('%Y-%m-%d')

    # Product Hunt API 需要认证，这里使用公开页面解析
    url = f"https://www.producthunt.com/posts/{date}"
    # 需要更复杂的处理，或使用 GraphQL API

    return results
```

### 7. Twitter Trends (API)

```python
# Twitter 需要 API 认证，建议使用第三方服务
# 或通过 web_reader MCP 工具获取页面内容
```

## 输出格式

### Markdown 报告格式

```markdown
# 📊 今日全网热点汇总

**时间**: 2024-01-24 08:00:00
**来源**: 共 25 个平台

---

## 🔥 国内热门

### 微博热搜 Top 10
| 排名 | 热度 | 话题 |
|------|------|------|
| 1 | 520万 | 今日头条事件 |
| 2 | 380万 | 某某明星动态 |
| ... | ... | ... |

### 知乎热榜 Top 10
| 排名 | 热度 | 问题 |
|------|------|------|
| 1 | 520万热 | 如何看待... |
| 2 | 380万热 | 为什么... |
| ... | ... | ... |

### 百度热搜 Top 10
...

---

## 🌍 国外热门

### Hacker News Top 10
| 排名 | 得分 | 标题 | 链接 |
|------|------|------|------|
| 1 | 520 | OpenAI releases... | https://... |
| 2 | 380 | New framework... | https://... |

### Reddit r/programming Top 10
...

### GitHub Trending Top 10
...

---

## 📈 趋势分析

### 今日关键词
- AI/人工智能 (出现 15 次)
- 某某事件 (出现 8 次)
- ...

### 跨平台共同话题
- 话题1: 在 3 个平台都出现
- 话题2: 在 2 个平台都出现

---

*数据由 daily-hot-fetcher skill 自动生成*
```

## 定时任务设置

### 使用 crontab (Linux/Mac)

```bash
# 每天早上 8 点获取热门信息
0 8 * * * python ~/.claude/skills/daily-hot-fetcher/scripts/fetch.py --output ~/daily-hot.md

# 每小时获取一次
0 * * * * python ~/.claude/skills/daily-hot-fetcher/scripts/fetch.py --output ~/hourly-hot.md
```

### 使用 Task Scheduler (Windows)

```powershell
# 创建定时任务
schtasks /create /tn "DailyHotFetcher" /tr "python C:\Users\Administrator\.claude\skills\daily-hot-fetcher\scripts\fetch.py --output C:\Users\Administrator\daily-hot.md" /sc daily /st 08:00
```

## 依赖工具

```bash
# Python 依赖
pip install requests beautifulsoup4 lxml

# 可选：更强大的爬虫框架
pip install scrapy selenium playwright

# 可选：异步请求
pip install aiohttp httpx
```

## 抖音 6 大榜单

### 榜单类型

| 榜单 | board_type | 说明 |
|------|------------|------|
| 综合榜 | 0 | 全平台综合热门 |
| 娱乐榜 | 1 | 娱乐相关内容 |
| 剧情榜 | 2 | 剧情/短剧内容 |
| 音乐榜 | 3 | 音乐相关内容 |
| 品牌榜 | 4 | 品牌活动内容 |
| 直播榜 | 5 | 直播热门内容 |

### 触发词

- "抖音热榜" / "抖音6榜单"
- "抖音综合榜" / "抖音娱乐榜"
- "抖音音乐榜" / "抖音剧情榜"
- "获取抖音榜单"

### 使用方式

#### 方式一：自然语言触发（推荐）

```
用户: 抖音6榜单

Claude: 正在获取抖音 6 大榜单...
[显示所有 6 个榜单的 Top 5]
```

#### 方式二：命令行

```bash
# 自动登录并获取所有榜单
python ~/.claude/skills/daily-hot-fetcher/scripts/auto_login.py douyin

# 查看已保存的榜单数据
python -c "
import json
from pathlib import Path
data = json.load(Path('~/.claude/skills/daily-hot-fetcher/sessions/douyin_boards.json')
for board, items in data.items():
    if items:
        print(f'{board}: {len(items)} 条')
        for item in items[:3]:
            print(f'  - {item.get(\"word\", \"\")}')
"
```

### Cookie 自动管理

```bash
# 登录抖音（会自动打开浏览器扫码）
python ~/.claude/skills/daily-hot-fetcher/scripts/auto_login.py douyin

# 检查 Cookie 状态
python ~/.claude/skills/daily-hot-fetcher/scripts/auto_login.py --check

# 刷新 Cookie（7天后过期自动提示）
python ~/.claude/skills/daily-hot-fetcher/scripts/auto_login.py douyin --force
```

### 数据存储

- Cookie 保存在: `~/.claude/skills/daily-hot-fetcher/sessions/`
- 榜单数据保存在: `~/.claude/skills/daily-hot-fetcher/sessions/douyin_boards.json`
- Cookie 有效期: 7 天

---

## 注意事项

1. **请求频率**: 避免频繁请求，设置合理的请求间隔
2. **User-Agent**: 使用真实的浏览器 User-Agent
3. **缓存**: 对相同数据使用缓存，减少重复请求
4. **错误处理**: 网络错误时重试，超时设置
5. **反爬虫**: 遵守 robots.txt，不过度爬取
6. **数据时效性**: 热门信息更新频繁，注意数据时间戳

## 使用示例

### 1. 获取热门信息

```
用户: 今天有什么热点？

Claude: 正在获取全网热门信息...

══════════════════════════════════════════════════════════════
═════════════════════ 全网热门信息获取 ════════════════════════
══════════════════════════════════════════════════════════════

▶ 📡 获取国内平台热门...
  微博热搜 [████████████████████████████████████] 100%
  知乎热榜 [████████████████████████████████████] 100%
  百度热搜 [████████████████████████████████████] 100%

▶ 🌍 获取国外平台热门...
  Hacker News [████████████████████████████████████] 100%
```

### 2. 平台登录

```
用户: 登录抖音

Claude: 正在启动浏览器自动登录...

==================================================
正在处理: DOUYIN
==================================================

[抖音] 等待扫码登录...
[抖音] 请使用抖音 APP 扫码登录

[抖音] 登录成功!
[抖音] Cookie 已保存 (42 个)

==================================================
登录结果汇总
==================================================
[douyin] ✓ 成功 (42 个 Cookie)
```

### 3. 查询登录状态

```
用户: 检查登录状态

Claude: 正在检查各平台 Cookie 状态...

Cookie 状态检查:
----------------------------------------
  zhihu      [OK] 有效
  douyin     [OK] 有效
  weibo      [X] 无效/过期

提示: 微博 Session 已过期，如需获取微博热搜请运行"登录微博"
```
  Reddit [████████████████████████████████████] 100%
  GitHub Trending [████████████████████████████████████] 100%
  ...

══════════════════════════════════════════════════════════════
           🎉 热门信息获取完成！
══════════════════════════════════════════════════════════════

[输出完整的热门信息报告]
```
