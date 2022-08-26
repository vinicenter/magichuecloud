To install the integration, put the root directory of this repository in the following directory of your home assistant:

```
config/custom-components/magichuecloud
```

Configuration example:

```
light:
  - platform: magichuecloud
    email: "email@example.com"
    password: "password"
    lights: 1
```

(lights is the number of lights in your Magichue account)

Put this config inside your "config/configuration.yaml" file.
