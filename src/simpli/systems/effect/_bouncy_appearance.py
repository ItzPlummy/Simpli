from math import exp, log, sin, tau

from simpli.components.effect import BouncyAppearanceEffectComponent, ScaleEffectComponent
from simpli.counters import Time
from simpli.spaces import Space
from simpli.systems import TickSystem
from simpli.utils import resolve


class BouncyAppearanceEffectSystem(TickSystem):
    def on_tick(
            self,
            space: Space,
            delta: int | float,
    ) -> None:
        time: Time = space.resources.get(Time)

        for entity in space.entities.by_components(BouncyAppearanceEffectComponent):
            effect: BouncyAppearanceEffectComponent = entity.get(BouncyAppearanceEffectComponent)
            elapsed: int = time.tick - resolve(effect.start_tick)

            if elapsed < 0:
                continue

            scale_effect: ScaleEffectComponent | None = entity.find(ScaleEffectComponent)

            if scale_effect is None:
                scale_effect: ScaleEffectComponent = ScaleEffectComponent()
                entity.add(scale_effect)

            duration: int | float = resolve(effect.duration)

            if elapsed >= duration:
                scale_effect.scale = 1
                entity.remove(BouncyAppearanceEffectComponent)
                continue

            decay: int | float = log(100) / duration
            envelope: int | float = resolve(effect.amplitude) * exp(-decay * elapsed)

            scale_effect.scale = 1 + envelope * sin(tau * resolve(effect.frequency) * elapsed * delta)
