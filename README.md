# SATOS Genconf
This python script is in charge of (re)generating  required configuration for multiple services. Currently only the `rauc-hawkbit-updater` is supported.

It pulls information from different sources and uses a jinja2 powered config template to fill in the required data on the device!

Example command for local testing, after installing
```
satos-genconf --env-file mock/.dev.env --mock-run true
```