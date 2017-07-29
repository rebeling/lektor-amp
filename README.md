# lektor-amp

This plugin creates an [Accelerate Mobile Page (AMP)](https://www.ampproject.org/) subartifact of the original content artifact and links canonical and amphtml. 

## Enabling the Plugin

To enable the plugin run this command:

$ lektor plugins add amp

## Configuring the Plugin

The plugin has a config file to turn off the amp generation. Just create 
a file named `amp.ini` into your `configs/` folder and set the `amp` key.

```ini
generate_amp = false
```

## In Templates

It expects an amp template version, prefixed with **amp-** of the templates.
Basic example for lektors basic blog module templates is in the github repo
(see [repo](https://github.com/rebeling/lektor-amp/example)).
Just copy theses files into a fresh lektor 3.0 templates folder.

Beware that various tags, google ads, etc. behaves different and need 
to be handled in the templates (see [AMP](https://www.ampproject.org/docs/getting-started/)).


Mobile first, AI is coming by itself ;)
