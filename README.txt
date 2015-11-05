What is JUpgrade?

JUpgrade is a program for upgrading a Juniper chassis to a new OS version.

Using JLoad

Prerequisites:
- Host with python and standard PyEZ libraries (pip install junos-eznc)
- Juniper Router(s)
- Account on chassis
- Enable netconf access (set system services netconf ssh port 830)


1. Copy the new OS to the "junos" folder in jupgrade folder
2. Run script file > python jupgrade.py
3. Follow instructions