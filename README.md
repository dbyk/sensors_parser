# Sensors_parser
Parse `lm-sensors` command for Zabbix

# Insallation
* Config Zabbix agent for using UserParameters [Zabbix docs](https://www.zabbix.com/documentation/3.4/manual/config/items/userparameters)
* Put script somewhere and make it executable (`chmod +x parser.py`)
* Add tne next UserParametes: `UserParameter=sensor.get[*],/path/to/parser.py $1 $2 $3`
* Restart Zabix agent

# Configuring into the web
* "Configuration" → "Templates" → "Import" button
* Add template to hosts

# Manual usage
`./parser.py discovery` - print zabbix-friendly discovery json

`./parser.py CORENUMBER WHATTOSHOW`

Where `CORENUMBER` must be one of existing core numbers
`WHATTOSHOW` can be one of `[max,crit,input]`, `input` is default
