# Simpli

A small entity-component-system (ECS) engine for 2D simulations in Python, rendered with pyglet. You describe a simulation as entities with components and a list of systems; Simpli runs the loop, rendering and input.

Early and experimental: the core works, the API will change.

## Example

```python
from simpli import Simpli
from simpli.systems import MouseClickSystem
from simpli.systems.motion import AirResistanceSystem, VelocitySystem, GravitySystem
from simpli.structures import Circle


class SpawnCircle(MouseClickSystem):
    def on_mouse_click(self, space, position, screen_position, mouse_button):
        space.entities.place(Circle(position, 30, is_dynamic=True))


class Example(Simpli):
    SYSTEMS = [SpawnCircle(), GravitySystem(), AirResistanceSystem(), VelocitySystem()]


Example().start()
```

More in [examples/](examples): gravity and repulsion between bodies.

## What's inside

- Entities, components, systems and resources, each in its own registry
- Motion systems: velocity, gravity, attraction, repulsion, air resistance
- Tick, frame, start and mouse-click systems as extension points
- Bindings with memoization for values that change at runtime
- Appearance effects and shape rendering on pyglet

Requires Python 3.12+. Install with `uv sync`, then run `uv run examples/gravity.py`.
