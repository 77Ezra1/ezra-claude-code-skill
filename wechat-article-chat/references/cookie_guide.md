# Cookie配置详细指南

## 为什么需要Cookie？

部分微信公众号文章存在以下访问限制：

| 限制类型 | 说明 | 是否需要Cookie |
|---------|------|---------------|
| 公开文章 | 任何人都可以访问 | ❌ 不需要 |
| 仅关注者可见 | 需要关注公众号才能查看 | ✅ 需要 |
| 链接过期 | 文章链接已失效 | ✅ 需要 |
| 历史文章限制 | 部分账号限制历史文章访问 | ✅ 需要 |

## 获取Cookie详细步骤

### 方法一：Chrome/Edge浏览器

1. **登录微信公众号平台**
   ```
   访问 https://mp.weixin.qq.com/
   使用微信扫码登录
   ```

2. **打开开发者工具**
   - Windows: 按 `F12`
   - Mac: 按 `Cmd + Option + I`

3. **找到Cookie面板**
   - 切换到 `Application` (应用) 标签
   - 左侧展开 `Storage` → `Cookies`
   - 点击 `https://mp.weixin.qq.com`

4. **复制关键Cookie**
   必须包含的Cookie字段：
   - `key` - 登录密钥
   - `pass_ticket` - 票据
   `wxuin` - 用户标识

   可选但推荐的Cookie：
   - `pgv_pvi` / `pgv_pvid` - 访问统计
   - `mm_lang` - 语言设置
   - `noticeLoginFlag` - 登录标识

5. **填写到配置文件**
   ```json
   {
     "cookies": [
       {"name": "key", "value": "复制的值", "domain": "mp.weixin.qq.com"},
       {"name": "pass_ticket", "value": "复制的值", "domain": "mp.weixin.qq.com"},
       {"name": "wxuin", "value": "复制的值", "domain": "mp.weixin.qq.com"}
     ],
     "last_updated": "2025-01-26T10:30:00Z"
   }
   ```

### 方法二：使用浏览器插件

推荐插件：
- **EditThisCookie** (Chrome/Edge)
- **Cookie-Editor** (Firefox)

步骤：
1. 安装插件
2. 登录 mp.weixin.qq.com
3. 点击插件图标
4. 导出当前域名的所有Cookie
5. 粘贴到配置文件

## Cookie有效期

| Cookie类型 | 大小有效期 | 说明 |
|-----------|-----------|------|
| key | 几小时到几天 | 核心认证Cookie |
| pass_ticket | 几小时 | 会话票据 |
| wxuin | 长期 | 用户标识 |

**建议**：当获取失败时，重新获取Cookie即可。

## 检查Cookie是否有效

使用内置检查脚本：
```bash
python scripts/check_cookie.py --cookie assets/cookie_config.json
```

输出示例：
```
✓ Cookie有效 (最后更新: 2025-01-26T10:30:00Z)
```

或：
```
✗ Cookie已失效
💡 请重新登录 mp.weixin.qq.com 获取最新Cookie
```

## Cookie安全注意事项

1. **不要分享Cookie** - Cookie相当于你的登录凭证
2. **定期更新** - Cookie会过期，需要定期重新获取
3. **仅用于个人使用** - 不要用于商业爬虫
4. **遵守平台规则** - 合理使用，避免频繁请求

## 常见问题

### Q: Cookie多久需要更新一次？
A: 通常几天到一周。当脚本提示Cookie失效时更新即可。

### Q: 能否用自动化方式获取Cookie？
A: 可以使用Selenium，但需要处理扫码登录，复杂度较高。建议手动获取。

### Q: 为什么有时候不需要Cookie也能获取文章？
A: 因为部分文章是公开的，不需要登录就能访问。脚本会自动判断。

### Q: 可以使用多个账号的Cookie吗？
A: 可以轮换使用，避免单个账号请求过于频繁被限制。
