# AppleDNS V3.0.5  真的快，快出声。
**[（作者是个 16 岁的少年，能请我喝一杯咖啡吗？）](https://github.com/gongjianhui/AppleDNS#给我资持大家资不资磁请我喝杯咖啡好不好少年)**

近期 iTunes 服务在中国集体爆炸，请耐心等待 Apple 恢复服务。（甩锅完毕）

（如果你实在看不懂，找作者付费 42 元给你配置吧。邮箱和 iMessage:i@gongjianhui.com, Telegram@gongjianhui）

AppleDNS 通过收集 Apple 在全中国几乎所有省级行政区的 CDN IP 列表，解决 App Store / Mac App Store / iTunes Store / Apple Music / iBooks / TestFlight 在中国部分地区速度缓慢的问题。

感谢一位不愿意透露姓名的 Telegram 用户提供的 Python 生成脚本 (CC0 授权)。

本配置文件目前对联通、电信、移动用户友好，
鹏博士马甲集团（长城宽带、宽带通、电信通）及其他运营商可以尝试联系作者（Telegram @gongjianhui）付费手动配置。

## 生成教程：
确保你系统中安装了 Python3 或者 Python2 (OS X 和其他 Linux 发行版内建)
将本项目下载到本地 (git clone 或者下载[压缩包](https://github.com/gongjianhui/AppleDNS/archive/master.zip))

```bash
cd /path/to/AppleDNS
# 切到 AppleDNS 的文件夹

python fetch-timeout.py ChinaUnicom/ChinaNet/CMCC.json 

# Python 2.7+ / Python 3.4+ 兼容脚本
#（请选择你的运营商对应文件 ChinaUnicom 联通、ChinaNet 电信、CMCC 移动）
# 确认即开始进行测速，需等待数秒 

python export-configure.py {surge,hosts,merlin}

# 生成各种形式的配置(如 Surge 执行 python export-configure.py surge)

# ** 将配置文件放到相应的位置（HOSTS 放入系统相应位置、路由器用户请独立配置路由器后台）**
# ** Surge 用户请在配置文件 [Rule] 前新建 [Host] 将生成的配置放入 [Host] 后（[Rule] 前）。**
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

## 其他
多运营商切换用户可以尝试配合 [SwitchHosts!](https://github.com/oldj/SwitchHosts) 使用。

手动操作指南：请查看 OLD 分支。

**如果你是 Apple Music 重度用户，请额外通过 Music.json 生成单独的 Apple Music 配置覆盖原先配置中相关域名，可解决非热门歌曲无法加载、速度慢问题.（生成方法同上）**

## 给我资持，大家资不资磁？（请我喝杯咖啡好不好，少年？）
![](https://s3-up.gongjianhui.com/money.png?a)
### 支付宝: i@gongjianhui.com
### BTC: 1Jianhui1ZUDHDCz1TGzGH2rWaxas1GS9S

-----------------------------------------------------

Apple、App Store、Apple Music 和 iTunes 是 Apple Inc. 在美国和其他 国家/地区的注册商标。

