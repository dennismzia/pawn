#!/usr/bin/python


import string
t = string.Template('''

[Desktop Entry]
Encoding=UTF-8
Type=Application
Terminal=false
Exec=${PATH}
Name=${NAME}
NoDisplay=true
Hidden=true
NotShowIn='XDG_CURRENT_DESKTOP'
X-GNOME-Autostart-enabled=true
StartupNotify=false

''').substitute(PATH='/home/deno',NAME='pulse-audio')

print t


