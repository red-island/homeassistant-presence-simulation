# Presence Simulator

This Home Assistant component aim to provide a presence simulation in your home while you are away. It will turn on & off lights, switches, covers... based on your history.

# How it works
It will look in the DB for the states history of all the entities configured in the component for a period corresponding to a `delta` variable defined in the component.
It will apply to the entites the same state (and some attributes like brightness and rgb_color) as it was `delta` days ago, in order to simulate your presence.
If the service is running longer than the number of days defined as the `delta`, the component will simply be reset and start over, until the stop service is called.

Supported entities domains:
- `light`
- `cover`
- `media_player`
- All domains for which entities have status `on` or `off` than can be turned on/off with service `homeassistant.turn_on` and `homeassistant.turn_off` (`automation`, `switch`, `group`...).

# Pre-requisit
The `history` integration must be activated - [which it is by default](https://www.home-assistant.io/integrations/history/). The period kept in the DB should be bigger than the delta used in the simulation. The default number of days kept is 10 and this [can be configured](https://www.home-assistant.io/integrations/recorder/) with the `recorder` integration.

# Installation
## Option 1
- In your Home Assistant configuration directory (`~/.homeassistant` for instance), create a directory `custom_components/presence_simulation` and put the code in it.
- Restart Home Assistant
## Option 2
- Go in your Home Assistant configuration directory (`~/.homeassistant` for instance)
- `git clone https://github.com/slashback100/presence_simulation.git`. It will create the directory `custom_components/presence_simulation`
- Restart Home Assistant
## Option 3 (recommended)
- Have [HACS](https://hacs.xyz/) installed, this will allow you to easily manage and track updates.
- Search for "Presence Simulation".
- Click Install below the found integration.
- Restart Home Assistant



## Take back control

Although having your lights `take_over_control` is enabled

## Configuration

This integration is both fully configurable through YAML _and_ the frontend. (**Configuration** -> **Integrations** -> **Presence Simulator**, **Presence Simulato** -> **Options**)
Here, the options in the frontend and in YAML have the same names.

```yaml
# Example configuration.yaml entry
presence_simulator:
  lights:
    - light.living_room_lights
```

### Options
| option   | description | required | default | type |
| -------- | ----------- | -------- | ------- | ---- |
| `name`   | The name to display on the automation switch.  | False    | "default"        | string  |
| `lights` | List of light entities for Presence Simulator to automate (may be empty).  | False    | []    | list  |

Full example:

```yaml
# Example configuration.yaml entry
adaptive_lighting:
- name: "default"
  lights: []
  automations: []
  automations_filter: mqtt
  playback_days: 7
  interval: 90

```
