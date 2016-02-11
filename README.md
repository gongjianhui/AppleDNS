# 配置说明

## 在域名对应的 IP 中选择地理位置相近，配置在 Surge、hosts 文件，或者自有 DNS 上即可。
iOS、OS X 以及 Apple Music 访问、下载速度慢请配置 List.md 中第六项。iTunes Store Movie 配置请见 iTunesMovie 文件。

# 由于数据采集方式的原因，可能会有一部分 IP 无法使用，请测试后再部署

## 提示：本项目对冷门资源无加速效果。

# Surge 配置
在配置文件最下方添加，IP请在 List.md 文件中查找，一组可以使用一个 IP。

```
[Host]

a1.mzstatic.com = 
a2.mzstatic.com = 
a3.mzstatic.com = 
a4.mzstatic.com = 
a5.mzstatic.com = 

is1.mzstatic.com = 
is2.mzstatic.com = 
is3.mzstatic.com = 
is4.mzstatic.com = 
is5.mzstatic.com = 

iosapps.itunes.apple.com = 
streamingaudio.itunes.apple.com = 
aod.itunes.apple.com = 

radio.itunes.apple.com = 
radio-services.itunes.apple.com = 
radio-activity.itunes.apple.com = 

client-api.itunes.apple.com = 
```
另外，如果您的 Surge 代理质量足够好，建议在 Rule 中添加一条
```
IP-CIDR,17.173.66.0/22,Proxy
```

# hosts 配置
例：IP Domain
```
a1.mzstatic.com 
a2.mzstatic.com
a3.mzstatic.com
a4.mzstatic.com
a5.mzstatic.com
is1.mzstatic.com
is2.mzstatic.com
is3.mzstatic.com
is4.mzstatic.com
is5.mzstatic.com
iosapps.itunes.apple.com
streamingaudio.itunes.apple.com
aod.itunes.apple.com
radio.itunes.apple.com
radio-services.itunes.apple.com
radio-activity.itunes.apple.com
client-api.itunes.apple.com
```

## 给我资持，大家资不资磁？
### 支付裱: i@gongjianhui.com
![](https://ooo.0o0.ooo/2016/01/28/56aaef6758139.jpg)
### BTC: 1Jianhui1ZUDHDCz1TGzGH2rWaxas1GS9S



