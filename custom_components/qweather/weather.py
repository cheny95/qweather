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
)
from homeassistant.const import (
    TEMP_CELSIUS,
    CONF_API_KEY,
    CONF_REGION,
    CONF_NAME,
    CONF_DEFAULT,
)

from .condition import CONDITION_MAP, EXCEPTIONAL

_LOGGER = logging.getLogger(__name__)

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    _LOGGER.info("正在设置和风天气…")
    weather_entity = QWeather(
        config[CONF_API_KEY], config[CONF_REGION], config[CONF_NAME], config[CONF_DEFAULT],
    )
    async_add_entities([weather_entity], True)

class QWeather(WeatherEntity):
    def __init__(self, api_key: str, location: str, name: str, default) -> None:
        super().__init__()
        self.api_key = api_key
        self.location = location
        self.default = default or 3
        self._name = name
        self._current: dict = None
        self._daily_data: list[dict] = None
        self._indices_data: list[dict] = None
        self._air_data = None
        self.now_url = f"https://devapi.qweather.com/v7/weather/now?location={self.location}&key={self.api_key}"
        self.daily_url = f"https://devapi.qweather.com/v7/weather/{self.default}d?location={self.location}&key={self.api_key}"
        self.indices_url = f"https://devapi.qweather.com/v7/indices/1d?type=0&location={self.location}&key={self.api_key}"
        self.air_url = f"https://devapi.qweather.com/v7/air/now?location={self.location}&key={self.api_key}"
        self.update_time = None

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
        async with aiohttp.ClientSession() as session:
            async with session.get(self.now_url) as response:
                json_data = await response.json()
                self._current = json_data["now"]
                self.update_time = json_data["updateTime"]
            async with session.get(self.daily_url) as response:

                self._daily_data = (await response.json() or {}).get("daily")
                # json_data = await response.json()
                # self._daily_data = json_data["daily"]
            async with session.get(self.indices_url) as response:
                self._indices_data = (await response.json() or {}).get("daily")
                # self._indices_data = (await response.json())["daily"]
            async with session.get(self.air_url) as response:
                self._air_data = (await response.json() or {}).get("now")
                # self._air_data = (await response.json())["now"]

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
            indices_str += f"{data['name']}: {data['level']}({data['category']}\n{data['text']}\n\n)"
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
        data["pm25"] = self.pm25
        data["pm10"] = self.pm10
        data["o3"] = self.o3
        data["no2"] = self.no2
        data["so2"] = self.so2
        data["co"] = self.co
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
