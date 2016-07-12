# AppleDNS V4

AppleDNS 通过收集 Apple 在全中国几乎所有省级行政区的 CDN IP 列表，解决 App Store / Mac App Store / iTunes Store / Apple Music / iBooks / TestFlight 在中国部分地区速度缓慢的问题。

感谢一位不愿意透露姓名的 Telegram 用户提供的 Python 生成脚本 (CC0 授权)。

## 生成教程：
确保你系统中安装了 Python3 或者 Python2 (OS X 和其他 Linux 发行版内建)

```bash
cd /path/to/AppleDNS
# 切到 AppleDNS 的文件夹

python domain-lookup.py -d Apple-Domains.json -s ChinaUnicomDNS.json > res.json

python fetch-timeout.py res.json

# Python 2.7 脚本
#（请选择你的运营商对应文件 ChinaUnicom 联通、ChinaNet 电信、CMCC 移动）
# 确认即开始进行测速，需等待数秒

python export-configure.py {surge,hosts,merlin,ros}

# 生成各种形式的配置(如 Surge 执行 python export-configure.py surge)

# 将配置文件放到相应的位置（HOSTS 放入系统相应位置、路由器用户请独立配置路由器后台）
# Surge 用户请在配置文件 [Rule] 前新建 [Host] 将生成的配置放入 [Host] 后（[Rule] 前）。
```

## 设置完成后可按需清理 DNS 缓存

OS X：[#41](../../issues/41)

Windows：<kbd>ipconfig /flushdns</kbd>

## DNSMASQ 用户和 MERLIN 用户警告：

请删除配置文件中的

```ini
address=/itunes.apple.com/***
```

该配置在 DNSMASQ 中意味着将 `itunes.apple.com` 泛解析！

-----------------------------------------------------

Apple、App Store、Apple Music 和 iTunes 是 Apple Inc. 在美国和其他 国家/地区的注册商标。

