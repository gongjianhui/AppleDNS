# 全新的 AppleDNS，大快所有人心的好项目。真的快，快出声！

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
如添加后 Apple Music 部分歌曲（尤其是冷门歌曲）仍然加载速度慢，请考虑将 streamingaudio.itunes.apple.com 和 aod.itunes.apple.com 加入你的代理黑名单列表（DOMAIN-SUFFIX,****.itunes.apple.com,Proxy,force-remote-dns）

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

