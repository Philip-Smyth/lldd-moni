# lldd-moni
Network monitorization through lldp

Installation of Network Monitor on Linux

-Git Clone https://github.com/Philip-Smyth/lldp-moni.git

-Move monitor and porthole directories to a desired location

-Run pip install -r requirements.txt
(Please ensure pip is installed beforehand)

Running of Network Monitor on Linux

-cd to monitor and run 'sudo python begin.py'
(ensure desired range is define within discover.conf)

-Network Monitor will take the subnet from eth0

-On another terminal cd to porthole directory

-Inside porthole, run 'sudo python __init__.py'

-To view the dashboard, open the browser and enter

'127.0.0.1:5000/' 
