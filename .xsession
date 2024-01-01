# personal xsession login startup script
# based on examples from man i3

# Disable DPMS turning off the screen
xset -dpms
xset s off

# Disable bell
xset -b

# Enforce correct locales from the beginning:
# LC_ALL is unset since it overwrites everything
# LANG=en_US.UTF-8 is used, except for:
# LC_MESSAGES=C never translates program output
# LC_TIME=en_DK leads to yyyy-mm-dd hh:mm date/time output
unset LC_ALL
export LANG=en_US.UTF-8
export LC_MESSAGES=C
export LC_TIME=en_US.UTF-8

# Use XToolkit in java applications
export AWT_TOOLKIT=XToolkit

# Enable core dumps in case something goes wrong
ulimit -c unlimited

# Enable zapping (C-A-<Bksp> kills X)
setxkbmap -option terminate:ctrl_alt_bksp
# Use alt+shift to switch between keyboard layouts
setxkbmap -layout us,ir -option grp:alt_shift_toggle

# Start i3 and log to ~/.i3/logfile
# echo "Starting at $(date)" >> ~/.i3/logfile
# exec /usr/bin/i3 -V -d all >> ~/.i3/logfile

# Or start XFCE
# /usr/bin/startxfce4
