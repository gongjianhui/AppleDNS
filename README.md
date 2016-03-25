# 全新的 AppleDNS，大快所有人心的好项目。真的快，快出声！


感谢 @raptium 和 @xjbeta 提供的自动生成脚本[（Apache License 2.0)](https://gist.github.com/raptium/5a9675667b05529857d4)

将 autogen.py 和 List.md 下载到本地后在终端中执行


```
cd /path/to/AppleDNS
// Surge 配置
python autogen.py -f surge List.md
// Hosts 文件
python autogen.py -f hosts List.md
// Merlin 固件配置
python autogen.py -f merlin List.md

// 设置完成后需要清理 DNS 缓存
// OS X v10.10.4 或更高版本
sudo killall -HUP mDNSResponder
// OS X v10.10 至 v10.10.3
sudo killall -HUP mDNSResponder
// Windoge 系统
ipconfig /flushdns

```



手动操作指南：

在 List.md 中选择与您物理位置相对近的 IP 并按照规则填入 Hosts 文件、私有 DNS 配置文件、Surge 配置文件中即可。
建议移动用户尽量使用移动 IP。

iOS Surge 配置，在 [Rule] 前加入以下内容，等号右侧为您在 List.md 中选择的 IP，每组可使用一个 IP（共 5 组）。（您可以参考或可以直接编辑项目中的 surge.conf 文件）
```
[Host]
iosapps.itunes.apple.com = 
streamingaudio.itunes.apple.com = 
aod.itunes.apple.com = 

radio.itunes.apple.com = 
radio-services.itunes.apple.com = 
radio-activity.itunes.apple.com = 

search.itunes.apple.com = 

init.itunes.apple.com = 
itunes.apple.com = 

play.itunes.apple.com = 
upp.itunes.apple.com = 
client-api.itunes.apple.com = 
su.itunes.apple.com = 
se.itunes.apple.com = 

```
## 请 Apple Music 用户额外留意项目中 Music.md 文件

# Hosts 配置 您需要按照 [IP 空格 域名] 一行一个的形式配置，每组可使用同样的 IP（共 5 组）
```
iosapps.itunes.apple.com
osxapps.itunes.apple.com
streamingaudio.itunes.apple.com
aod.itunes.apple.com

radio.itunes.apple.com
radio-services.itunes.apple.com
radio-activity.itunes.apple.com

search.itunes.apple.com

init.itunes.apple.com
itunes.apple.com

play.itunes.apple.com
upp.itunes.apple.com
client-api.itunes.apple.com
su.itunes.apple.com
se.itunes.apple.com
```

## 给我资持，大家资不资磁？
### 支付裱: i@gongjianhui.com
### BTC: 1Jianhui1ZUDHDCz1TGzGH2rWaxas1GS9S

Apple、App Store、Apple Music 和 iTunes 是 Apple Inc. 在美国和其他 国家/地区的注册商标。

