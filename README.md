# 和风天气 Home Assistant插件

## 使用方法：

- 下载该集成放入homeassistant安装目录`/config/custom_conponents/`中
- 在`/config/configuration.yaml`添加以下内容

```yaml
weather:
  - platform: qweather
    name: hefeng
    api_key: 123456
    region: 101010100
    default: 3
```
- 重启homeassistant
  


## 参数释义：

- `name` 实体名字
- `api_key` 和风申请的api key，申请地址：[https://dev.qweather.com/](https://dev.qweather.com/)
- `region` id或经纬度，请[参考和风官方的地址列表](https://github.com/qwd/LocationList/blob/master/China-City-List-latest.csv)，搜索你所在的地区
- `default`: 如果你是`普通用户`请填3，`认证开发者`可选7，意为查询未来3天还是7天的数据

#

## 鸣谢：
- ### 感谢 [hass-xiaomi-miot](https://github.com/al-one/hass-xiaomi-miot) 作者 [@al-one](https://github.com/al-one) 的帮助。
-  [hass-xiaomi-miot](https://github.com/al-one/hass-xiaomi-miot) 可将小米设备自动接入HomeAssistant，目前已支持大部分小米米家智能设备。且该插件支持HA后台界面集成，无需配置yaml即可轻松将小米设备接入HA。

## 交流
- QQ群：198841186

- 微信群：
  
![xiaomi miot weixin group](https://user-images.githubusercontent.com/4549099/152003439-d537fda6-15dd-43df-84cb-2c64c693c013.png))
