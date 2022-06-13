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
    location: 116.40,39.90 #注意，此处改为了经纬度
    default: 3
```
- 再次重启 Home Assistant
- 依次点击配置 - 设备与服务 - 实体注册表 搜索你刚才填写配置文件里的名字即可
  
- 关于调用接口次数：
  集成每次更新会调用7个接口（新版本新增小时级预报，可以预报24小时的天气，新增格点天气，新增灾害预警），所以你的接口调用次数是每更新一次就是调用4次。
  在老版本的时候，每次更新调用4个接口，我设置了`scan_interval: 600`（直接在`default`参数换行后追加即可，注意缩进），每小时调用次数是24次。
  现在增加了一些功能，等于查询一次等于调用7次接口，这个可以根据你的需求自己调整更新时间，节省请求次数。
```yaml
    scan_interval: 600  #默认是10秒还是30秒我记不清了
```


## 参数释义：

- `name` 实体名字
- `api_key` 和风申请的api key，申请地址：[https://dev.qweather.com/](https://dev.qweather.com/)
- `location` 经纬度，请[参考和风官方的地址列表](https://github.com/qwd/LocationList/blob/master/China-City-List-latest.csv)，搜索你所在的地区
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
- 未来2小时内分钟级预报： 开发者工具-状态-实体名称-属性

```yaml
forecast_minutely:
  - time: '14:10'
    type: rain
    precipitation: 0
  - time: '14:15'
    type: rain
    precipitation: 0
  - time: '14:20'
    type: rain
    precipitation: 0
  - time: '14:25'
    type: rain
    precipitation: 0
  - time: '14:30'
    type: rain
    precipitation: 0
    ……
minutely_summary: 未来两小时无降水 #预报描述
```

- 灾害预警
```yaml
# 无预警
weather_warning: 
  - text: 当前无灾害预警
```
```yaml
# 有预警
weather_warning:
  - time: 2021-10-09T15:46+08:00
    sender: 北京市气象局
    title: 北京市气象台2021年10月09日15时40分发布大风蓝色预警信号
    text: 市气象台2021年10月9日15时40分发布大风蓝色预警信号：预计，9日22时至10日19时，本市大部分地区有4级左右偏北风，阵风6、7级，山区阵风可达8级左右，请注意防范。
    severity: Minor
    severityColor: Blue
    typeName: 大风
```
#
## 版本记录：

- v0.0.4
  - 新增未来2小时分钟级预报。（forecast_minutely, minutely_summary）
  - 新增灾害预警。（weather_warning）
  - 因支持格点天气分钟级别预报，location参数中ID不在使用，使用经纬度作为参数，格式、获取方式一样参考上方。
  - 注：以上2个接口是否需要认证开发者未测试，因为我的账号是认证开发者，默认都是认证开发者。


- v0.0.3
  - 新增当天24小时的小时级预报
  - AQI拆分，便于template调用
  - 生活指数无法拆分，因为是循环出来的信息。
  - 增加当天的小时级预报。（是否需要认证开发者未测试，默认都是认证开发者。）
  - 尝试解决“weather-night-partly-cloudy”，但由于HA官方未适配该字典，暂时无法适配。


- v0.0.2
  - skip this version


- v0.0.1 提交集成
  - 使用和风天气的认证开发者账号，每天16700次调用，非认证的1000次。但是功能上可能会受限。该集成默认用户都是认证开发者，可以调用7天预报之类的接口。



## 鸣谢：
- ### 感谢 [hass-xiaomi-miot](https://github.com/al-one/hass-xiaomi-miot) 作者 [@al-one](https://github.com/al-one) 的帮助。
-  [hass-xiaomi-miot](https://github.com/al-one/hass-xiaomi-miot) 可将小米设备自动接入HomeAssistant，目前已支持大部分小米米家智能设备。且该插件支持HA后台界面集成，无需配置yaml即可轻松将小米设备接入HA。

## 交流
- QQ群：198841186

- 微信群：(添加该机器人，发送“进群”会自动发送邀请链接）
  
![xiaomi miot weixin group](https://user-images.githubusercontent.com/4549099/161735971-0540ce1c-eb49-4aff-8cb3-3bdad15e22f7.png)
