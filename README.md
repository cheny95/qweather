# 和风天气 Home Assistant 插件

![yaofan](https://user-images.githubusercontent.com/6293952/196037499-17ef6aec-9fe4-4fc2-a4ac-811a12bfb380.jpg)

## 使用方法：

- 下载该集成放入homeassistant安装目录`/config/custom_conponents/`中
- 然后重启Home Assistant服务。
- 启动完成后，在`/config/configuration.yaml`添加以下内容
- **注意：后续版本不支持普通用户，仅支持开发者用户**

```yaml
weather:
  - platform: qweather
    name: hefeng
    api_key: 123456
    location: 116.40,39.90 #注意，此处改为了经纬度
    default: 7
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
- `api_key` 和风申请的api key，申请地址：[https://dev.qweather.com/](https://dev.qweather.com/)，申请后，请认证为个人开发者，新建一个使用web sdk项目，获取key。
- `location` 经纬度，请[参考和风官方的地址列表](https://github.com/qwd/LocationList/blob/master/China-City-List-latest.csv)，搜索你所在的地区
- `default`: 需要`认证开发者`，意为查询未来7天的数据。**取消了非开发者的支持，因为有一些格点天气之类的必须需要开发者**

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
  - pubTime: 2021-10-09T15:46+08:00
    startTime: 2022-06-13T16:14+08:00,
    endTime: 2022-06-14T16:14+08:00,
    sender: 北京市气象局
    title: 北京市气象台2021年10月09日15时40分发布大风蓝色预警信号
    text: 市气象台2021年10月9日15时40分发布大风蓝色预警信号：预计，9日22时至10日19时，本市大部分地区有4级左右偏北风，阵风6、7级，山区阵风可达8级左右，请注意防范。
    severity: Minor
    severityColor: Blue
    level: 黄色,
    typeName: 大风
```
#
## 版本记录：

- v0.0.8
  - 修复实时天气的取值还原为英文，但是在属性中增加了中文字段（condition_desc），因为官方仅支持少量天气图标和解释。（所有偶尔会有图标不对的情况）

- v0.0.7
  - 增加7天预报天气的中文状态
  - 修复默认状态为英文，现在默认状态为中文。（不知是否有问题，待观察）
  - 尝试修复图标问题，但是home assistant官方仅支持部分天气状态。（待观察）
  
- v0.0.6
  - 修复偶尔报错的问题。代码中增加了清除缓存以及连接数的修改。

- v0.0.5
  - 修复灾害预警取值错误导致集成启动失败的问题
  - 增加灾害预警推送时间、开始时间、结束时间、预警等级[官方后期会弃用，到时候同步修改]


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
