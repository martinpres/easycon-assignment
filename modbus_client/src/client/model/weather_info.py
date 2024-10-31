from dataclasses import dataclass


@dataclass(frozen=True)
class WeatherInfo:
    temperature_2m: int
    relative_humidity_2m: int
    wind_speed_10m: int

    @staticmethod
    def from_list(given):
        return WeatherInfo(given[0], given[1], given[2])

    def to_dict(self):
        return {
            'temperature_2m': self.temperature_2m,
            'relative_humidity_2m': self.relative_humidity_2m,
            'wind_speed_10m': self.wind_speed_10m
        }
