# AppleDNS V3.0，真的快，快出声。
（作者是个 16 岁的穷逼，求捐赠，账号见下方。）

感谢一位不愿意透露姓名的 Telegram 用户提供的 Python 生成脚本 (CC0 授权)。

本配置文件目前对联通、电信、移动用户友好，
鹏博士马甲集团（长城宽带、宽带通、电信通）及其他运营商可以尝试联系作者（Telegram @gongjianhui）付费手动配置。

## 生成教程：
确保你系统中安装了 Python3
将本项目下载到本地 (git clone 或者下载[压缩包](https://github.com/gongjianhui/AppleDNS/archive/master.zip))

```
cd /path/to/AppleDNS
// 切到 AppleDNS 的文件夹
python3 fetch-timeout.py —payload ChinaUnicom/ChinaNet/CMCC.json 
//（请选择你的运营商对应文件 ChinaUnicom 联通、ChinaNet 电信、CMCC 移动）
// 测速中，需等待数秒
python3 export-configure.py [-t {surge,hosts,merlin}]
// 生成各种形式的配置(如 Surge 执行 python3 export-configure.py -t surge)

** 将配置文件放到相应的位置（HOSTS 放入系统相应位置、路由器用户请独立配置路由器后台）**
** Surge 用户请在配置文件 [Rule] 前新建 [Host] 将生成的配置放入 [Host] 后（[Rule] 前）。**

// 设置完成后可按需清理 DNS 缓存
// OS X v10.10.4 或更高版本
sudo killall -HUP mDNSResponder
// OS X v10.10 至 v10.10.3
sudo killall -HUP mDNSResponder
// Windoge 系统
ipconfig /flushdns

```

手动操作指南：请查看 OLD 文件夹。

## 给我资持，大家资不资磁？
### 支付裱: i@gongjianhui.com
### BTC: 1Jianhui1ZUDHDCz1TGzGH2rWaxas1GS9S

Apple、App Store、Apple Music 和 iTunes 是 Apple Inc. 在美国和其他 国家/地区的注册商标。

