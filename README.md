# Final AppleDNS Pro

AppleDNS 通过收集 Apple 在中国的 CDN 数据，解决 iTunes iCloud 等 Apple 网络服务在中国大陆部分地区加载缓慢的问题。

本配置文件目前对联通、电信、移动用户友好。

使用 [GFW.cat 国际网络优化服务](https://my.gfw.cat/?ghad) 可获取更优质、全面的国际网络优化体验。

## 生成教程：
确保你系统中安装了 Python 3.4+ 或者 Python 2.7+ (macOS 和多数 Linux 发行版内建)
将本项目[下载](https://github.com/gongjianhui/AppleDNS/archive/master.zip)到本地

```bash
cd /path/to/AppleDNS
# 切换到 AppleDNS 的文件夹

python fetch-timeout.py {ChinaUnicom.json/ChinaNet.json/CMCC.json}

# 兼容 Python 2.7+ / Python 3.4+
#（请选择你的运营商对应文件 ChinaUnicom 联通、ChinaNet 电信、CMCC 移动）
# 确认即开始进行测速，需等待数秒

python export-configure.py {surge,hosts,dnsmasq,ros,unbound}

# 生成各种形式的配置(如 Surge 执行 python export-configure.py surge)

# ** 将配置文件放到相应的位置（HOSTS 放入系统相应位置、路由器用户请独立配置路由器后台）**
# ** Surge 用户请在配置文件中新建 [Host] 并将配置复制到下方）。**
```

## 设置完成后可按需清理 DNS 缓存

macOS：[#41](https://github.com/gongjianhui/AppleDNS/issues/41)

Windows：<kbd>ipconfig /flushdns</kbd>

## dnsmasq 配置警告：

请删除配置文件中的

```ini
address=/itunes.apple.com/***
```

该配置在 dnsmasq 中意味着将 `itunes.apple.com` 泛解析，请务必删除。

## 其他
多运营商切换用户可以尝试配合 [SwitchHosts!](https://github.com/oldj/SwitchHosts) 使用。

## 给我资持，大家资不资磁？
### Alipay: i@gongjianhui.com
### BTC: 1Jianhui1ZUDHDCz1TGzGH2rWaxas1GS9S

-----------------------------------------------------

iTunes、iTunes Store、App Store、iBooks Store、Apple Music 以及与服务有关而使用的其他 Apple 商标、服务商标、图形和标识是 Apple Inc. 在美国和世界其他国家 / 地区的商标或注册商标。
AppleDNS 不是由 Apple Inc. 提供的服务。
