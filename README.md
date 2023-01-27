# Presence Simulator


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
