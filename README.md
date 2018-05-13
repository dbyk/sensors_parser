# sensors_parser
Parse lm-sensors command for zabbix

# usage
`./parser.py discovery` - print zabbix-friendly discovery json

`./parser.py CORENUMBER WHATTOSHOW`

Where `CORENUMBER` must be one of existing core numbers
`WHATTOSHOW` can be one of `[max,crit,input]`, `input` is default
