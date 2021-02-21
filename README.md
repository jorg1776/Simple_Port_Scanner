## Simple Port Scanner
This is a simple Python TCP and UDP port scanner.

### Usage
port-scanner.py [-h] [-p PORTS] [-t] [-u] [-v] HOSTS

- HOSTS
  - Specify the IP addresses of the hosts to scan. You can specify the hosts individually (127.0.0.1,127.0.0.2) and/or specify an IP range of hosts to scan (127.0.0.1-10).

#### Optional arguments:
- -h, --help            
  - show this help message and exit
- -p PORTS, --ports PORTS
  - Specify ports to scan. You can specify ports individually (-p 22,80) and/or specify a range of ports to scan (-p 1-100)
- -t
  - Scan TCP ports (Default)
  - You can scan both TCP and UDP ports using both -t and -u flags.
- -u
  - Scan UDP ports
  - You can scan both TCP and UDP ports using both -t and -u flags.
- -v, --verbose
  - Verbose output. Include closed ports in output.
