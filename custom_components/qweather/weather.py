from __future__ import annotations
import logging

import aiohttp

from homeassistant.components.weather import (
    WeatherEntity,
    ATTR_FORECAST_CONDITION,
    ATTR_FORECAST_PRECIPITATION,
    ATTR_FORECAST_TEMP,
    ATTR_FORECAST_TEMP_LOW,
    ATTR_FORECAST_TIME,
    ATTR_FORECAST_WIND_BEARING,
    ATTR_FORECAST_WIND_SPEED,
    ATTR_FORECAST_PRESSURE,
    ATTR_FORECAST_PRECIPITATION_PROBABILITY,
    ATTR_WEATHER_HUMIDITY,
    ATTR_CONDITION_CLOUDY
)
from homeassistant.const import (
    TEMP_CELSIUS,
    CONF_API_KEY,
    CONF_LOCATION,
    CONF_NAME,
    CONF_DEFAULT
)

from .condition import CONDITION_MAP, EXCEPTIONAL

_LOGGER = logging.getLogger(__name__)

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    _LOGGER.info("正在设置和风天气…")
    weather_entity = QWeather(
        config[CONF_API_KEY], config[CONF_LOCATION], config[CONF_NAME], config[CONF_DEFAULT]
    )
    async_add_entities([weather_entity], True)

class QWeather(WeatherEntity):
    def __init__(self, api_key: str, location: str, name: str, default) -> None:
        super().__init__()
        self.api_key = api_key
        self.location = location
        self.default = default
        self._name = name
        self._current: dict = None
        self._daily_data: list[dict] = None
        self._indices_data: list[dict] = None
        self._hourly_data: list[dict] = None
        self._minutely_data: list[dict] = None
        self._warning_data: list[dict] = None
        self._air_data = None
        self.now_url = f"https://devapi.qweather.com/v7/weather/now?location={self.location}&key={self.api_key}"
        self.daily_url = f"https://devapi.qweather.com/v7/weather/{self.default}d?location={self.location}&key={self.api_key}"
        self.indices_url = f"https://devapi.qweather.com/v7/indices/1d?type=0&location={self.location}&key={self.api_key}"
        self.air_url = f"https://devapi.qweather.com/v7/air/now?location={self.location}&key={self.api_key}"
        self.hourly_url = f"https://devapi.qweather.com/v7/weather/24h?location={self.location}&key={self.api_key}"
        self.minutely_url = f"https://devapi.qweather.com/v7/minutely/5m?location={self.location}&key={self.api_key}"
        self.warning_url = f"https://devapi.qweather.com/v7/warning/now?location={self.location}&key={self.api_key}"
        self.update_time = None
        self.minutely_summary = None


    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def condition(self):
        """Return the current condition."""
        return CONDITION_MAP.get(self._current.get("icon"), EXCEPTIONAL)

    async def async_update(self):
        """获取天气数据"""
        timeout = aiohttp.ClientTimeout(total=30)  # 将超时时间设置为30秒
        connector = aiohttp.TCPConnector(limit=50)  # 将并发数量降低
        async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
            async with session.get(self.now_url) as response:
                json_data = await response.json()
                self._current = json_data["now"]
                self.update_time = json_data["updateTime"]
            async with session.get(self.daily_url) as response:
                self._daily_data = (await response.json() or {}).get("daily")

            async with session.get(self.indices_url) as response:
                self._indices_data = (await response.json() or {}).get("daily")

            async with session.get(self.air_url) as response:
                self._air_data = (await response.json() or {}).get("now")

            async with session.get(self.hourly_url) as response:
                self._hourly_data = (await response.json() or {}).get("hourly")

            async with session.get(self.minutely_url) as response:
                minutely_data = await response.json()
                self.minutely_summary =(await response.json() or None).get("summary")
                self._minutely_data = (await response.json() or {}).get("minutely")

            async with session.get(self.warning_url) as response:
                self._warning_data = (await response.json() or {}).get("warning")

    @property
    def cloud_percent(self):
        """实况云量，百分比数值"""
        return float(self._current["cloud"])

    @property
    def condition_desc(self):
        """天气情况"""
        return self._current["text"]

    @property
    def temperature(self):
        """温度"""
        return float(self._current["temp"])

    @property
    def temperature_feels(self):
        """体感温度"""
        return float(self._current["feelsLike"])

    @property
    def temperature_unit(self):
        """温度单位"""
        return TEMP_CELSIUS

    @property
    def pressure(self):
        """大气压强"""
        return float(self._current["pressure"])

    @property
    def humidity(self):
        """湿度"""
        return float(self._current["humidity"])

    @property
    def wind_speed(self):
        """风速"""
        return float(self._current["windSpeed"])

    @property
    def wind_bearing(self):
        """风的角度"""
        return float(self._current["wind360"])

    @property
    def wind_dir(self):
        """风向"""
        return self._current["windDir"]

    @property
    def wind_sacle(self):
        """风力"""
        return float(self._current["windScale"])

    @property
    def visibility(self):
        """能见度"""
        return self._current["vis"]

    @property
    def suggestion(self):
        """生活指数"""
        indices_str = ""
        for data in self._indices_data:
            indices_str += f"{data['name']}: {data['level']}\n({data['category']}\n{data['text']})\n\n"
        return indices_str

    @property
    def ozone(self):
        """臭氧浓度"""
        return self._air_data["o3"]

    @property
    def aqi(self):
        """aqi"""
        return f"AQI: {self._air_data['aqi']} 等级: {self._air_data['level']} {self._air_data['category']} 主要污染物: {self._air_data['primary']}"

    @property
    def aqi_num(self):
        """aqi_num"""
        return f"{self._air_data['aqi']}"

    @property
    def aqi_level(self):
        """aqi等级1"""
        return f"{self._air_data['level']}"

    @property
    def aqi_category(self):
        """aqi等级2"""
        return f"{self._air_data['category']}"

    @property
    def aqi_primary(self):
        """aqi主要污染物"""
        return f"{self._air_data['primary']}"

    @property
    def pm25(self):
        """pm25，质量浓度值"""
        return self._air_data["pm2p5"]

    @property
    def pm10(self):
        """pm10，质量浓度值"""
        return self._air_data["pm10"]

    @property
    def o3(self):
        """臭氧，质量浓度值"""
        return self._air_data["o3"]

    @property
    def no2(self):
        """二氧化氮，质量浓度值"""
        return self._air_data["no2"]

    @property
    def so2(self):
        """二氧化硫，质量浓度值"""
        return self._air_data["so2"]

    @property
    def co(self):
        """一氧化碳，质量浓度值"""
        return self._air_data["co"]

    @property
    def state_attributes(self):
        """注册自定义的属性"""
        data = super(QWeather, self).state_attributes
        data["condition_desc"] = self.condition_desc
        data["update_time"] = self.update_time
        data["cloud_percent"] = self.cloud_percent
        data["temperature_feels"] = self.temperature_feels
        data["wind_dir"] = self.wind_dir
        data["wind_sacle"] = self.wind_sacle
        data["suggestion"] = self.suggestion
        data["aqi"] = self.aqi
        data["aqi_num"] = self.aqi_num
        data["aqi_level"] = self.aqi_level
        data["aqi_category"] = self.aqi_category
        data["aqi_primary"] = self.aqi_primary
        data["pm25"] = self.pm25
        data["pm10"] = self.pm10
        data["o3"] = self.o3
        data["no2"] = self.no2
        data["so2"] = self.so2
        data["co"] = self.co
        data["forecast_hourly"] = self.forecast_hourly
        data["forecast_minutely"] = self.forecast_minutely
        data["minutely_summary"] = self.minutely_summary
        data["weather_warning"] = self.weather_warning
        return data

    @property
    def forecast(self):
        """天为单位的预报"""
        forecast_list = []
        for daily in self._daily_data:
            forecast_list.append(
                {
                    ATTR_FORECAST_TIME: daily["fxDate"],
                    ATTR_FORECAST_TEMP: float(daily["tempMax"]),
                    ATTR_FORECAST_TEMP_LOW: float(daily["tempMin"]),
                    ATTR_FORECAST_CONDITION: CONDITION_MAP.get(
                        daily["iconDay"], EXCEPTIONAL
                    ),
                    ATTR_FORECAST_WIND_BEARING: float(daily["wind360Day"]),
                    ATTR_FORECAST_WIND_SPEED: float(daily["windSpeedDay"]),
                    ATTR_FORECAST_PRECIPITATION: float(daily["precip"]),
                    "humidity": float(daily["humidity"]),
                    ATTR_FORECAST_PRECIPITATION_PROBABILITY: int(
                        daily["humidity"]
                    ),  # 没有降雨率
                    ATTR_FORECAST_PRESSURE: float(daily["pressure"]),
                }
            )

        return forecast_list

    @property
    def forecast_hourly(self):
        """小时为单位的预报"""
        forecast_hourly_list = []
        for hourly in self._hourly_data:
            forecast_hourly_list.append(
                {
                    "time": hourly["fxTime"][11:16],
                    ATTR_CONDITION_CLOUDY: hourly["cloud"],
                    ATTR_FORECAST_TEMP: float(hourly["temp"]),
                    ATTR_FORECAST_CONDITION: CONDITION_MAP.get(
                        hourly["icon"], EXCEPTIONAL
                    ),
                    "text": hourly["text"],
                    ATTR_FORECAST_WIND_BEARING: float(hourly["wind360"]),
                    ATTR_FORECAST_WIND_SPEED: float(hourly["windSpeed"]),
                    ATTR_FORECAST_PRECIPITATION: float(hourly["precip"]),
                    ATTR_WEATHER_HUMIDITY: float(hourly["humidity"]),
                    ATTR_FORECAST_PRECIPITATION_PROBABILITY: int(
                        hourly["pop"]
                    ),  # 降雨率
                    ATTR_FORECAST_PRESSURE: float(hourly["pressure"]),
                }
            )

        return forecast_hourly_list

    @property
    def forecast_minutely(self):
        """格点天气预报"""
        forecast_minutely_list = []
        for minutely_data in self._minutely_data:
            forecast_minutely_list.append(
                {
                    "time": minutely_data['fxTime'][11:16],
                    "type": minutely_data["type"],
                    ATTR_FORECAST_PRECIPITATION: float(minutely_data["precip"]),
                }
            )

        return forecast_minutely_list

    @property
    def weather_warning(self):
        """灾害预警"""
        weather_warning_list = []
        if len(self._warning_data):
            for warningItem in self._warning_data:
                weather_warning_list.append(
                    {
                        "pubTime": warningItem["pubTime"],
                        "startTime": warningItem["startTime"],
                        "endTime": warningItem["endTime"],
                        "sender": warningItem["sender"],
                        "title": warningItem["title"],
                        "text": warningItem["text"],
                        "severity": warningItem["severity"],
                        "severityColor": warningItem["severityColor"],
                        "level": warningItem["level"],
                        "typeName": warningItem["typeName"],
                    }
                )

        else:
            weather_warning_list.append(
                {
                   'text': '当前无灾害预警'
                }
            )

        return weather_warning_list
