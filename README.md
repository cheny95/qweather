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
  
- 关于调用接口次数：
  集成每次更新会调用4个接口（新版本新增一个小时级预报，可以预报24小时的天气），所以你的接口调用次数是每更新一次就是调用4次。
  在老版本的时候，每次更新调用3个接口，我设置了 scan_interval: 600
```yaml
    scan_interval: 600  #默认是10秒还是30秒我记不清了
```
每小时调用次数是24次。这个可以根据你的需求自己调整。


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

- 每日预报： 开发者工具-状态-实体名称-属性
  
```yaml
forecast:
  - datetime: '2022-06-13'
    temperature: 30
    templow: 21
    condition: partlycloudy
    wind_bearing: 135
    wind_speed: 3
    precipitation: 0
    humidity: 85
    precipitation_probability: 85
    pressure: 1000
  - datetime: '2022-06-14'
    temperature: 33
    templow: 20
    condition: partlycloudy
    wind_bearing: 135
    wind_speed: 16
    precipitation: 0
    humidity: 69
    precipitation_probability: 69
    pressure: 1002
    ……
```
- 当天每小时预报： 开发者工具-状态-实体名称-属性
  
```yaml
forecast_hourly:
  - time: '01:00'
    cloudy: '100'
    temperature: 19
    condition: weather-night-partly-cloudy
    text: 多云
    wind_bearing: 111
    wind_speed: 11
    precipitation: 0
    humidity: 94
    precipitation_probability: 7
    pressure: 1003
  - time: '02:00'
    cloudy: '100'
    temperature: 19
    condition: weather-night-partly-cloudy
    text: 多云
    wind_bearing: 110
    wind_speed: 11
    precipitation: 0
    humidity: 96
    precipitation_probability: 7
    pressure: 1003
    ……
```
#

## 鸣谢：
- ### 感谢 [hass-xiaomi-miot](https://github.com/al-one/hass-xiaomi-miot) 作者 [@al-one](https://github.com/al-one) 的帮助。
-  [hass-xiaomi-miot](https://github.com/al-one/hass-xiaomi-miot) 可将小米设备自动接入HomeAssistant，目前已支持大部分小米米家智能设备。且该插件支持HA后台界面集成，无需配置yaml即可轻松将小米设备接入HA。

## 交流
- QQ群：198841186

- 微信群：(添加该机器人，发送“进群”会自动发送邀请链接）
  
![xiaomi miot weixin group](https://user-images.githubusercontent.com/4549099/161735971-0540ce1c-eb49-4aff-8cb3-3bdad15e22f7.png)
