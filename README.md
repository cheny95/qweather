# 和风天气 Home Assistant 插件

## 使用方法：

- 下载该集成放入homeassistant安装目录`/config/custom_conponents/`中
- 然后重启Home Assistant服务。
- 启动完成后，在`/config/configuration.yaml`添加以下内容

```yaml
weather:
  - platform: qweather
    name: hefeng
    api_key: 123456
    region: 101010100
    default: 3
```
- 再次重启 Home Assistant
- 依次点击配置 - 设备与服务 - 实体注册表 搜索你刚才填写配置文件里的名字即可
  


## 参数释义：

- `name` 实体名字
- `api_key` 和风申请的api key，申请地址：[https://dev.qweather.com/](https://dev.qweather.com/)
- `region` id或经纬度，请[参考和风官方的地址列表](https://github.com/qwd/LocationList/blob/master/China-City-List-latest.csv)，搜索你所在的地区
- `default`: 如果你是`普通用户`请填3，`认证开发者`可选7，意为查询未来3天还是7天的数据

## 示例

- 3天：

![3 days](https://github.com/cheny95/qweather/blob/main/3d.png?raw=true)

- 7天：

![7 days](https://github.com/cheny95/qweather/blob/main/7d.png?raw=true)
#

## 鸣谢：
- ### 感谢 [hass-xiaomi-miot](https://github.com/al-one/hass-xiaomi-miot) 作者 [@al-one](https://github.com/al-one) 的帮助。
-  [hass-xiaomi-miot](https://github.com/al-one/hass-xiaomi-miot) 可将小米设备自动接入HomeAssistant，目前已支持大部分小米米家智能设备。且该插件支持HA后台界面集成，无需配置yaml即可轻松将小米设备接入HA。

## 交流
- QQ群：198841186

- 微信群：(添加该机器人，发送“进群”会自动发送邀请链接）
  
![xiaomi miot weixin group](https://user-images.githubusercontent.com/4549099/161735971-0540ce1c-eb49-4aff-8cb3-3bdad15e22f7.png)
