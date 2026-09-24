from pydantic.dataclasses import dataclass

from simpli.resources import Resource


@dataclass
class Time(Resource):
    tick: int
    delta: int | float
    alpha: int | float
    simulation_time: int | float

    @classmethod
    def tag(cls) -> str:
        return "time"
