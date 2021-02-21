import socket
import argparse

# Setting timeout for socket connections
socket.setdefaulttimeout(1)

# Set up command line arguments
argparser = argparse.ArgumentParser(description='Port Scanner')
argparser.add_argument('hosts', metavar='<hosts>', help='Specify hosts to scan')
argparser.add_argument('-f', help='Read hosts from specified file')
argparser.add_argument('-p', '--ports', help='Specify ports to scan')
argparser.add_argument('-t', action='store_true', help='Scan with TCP (Default)')
argparser.add_argument('-u', action='store_true', help='Scan with UDP')
argparser.add_argument('-v', '--verbose', action='store_true', help='Verbose output. Include closed ports in output.')

args = argparser.parse_args()

# Parse hosts to scan
hosts = []
for host_arg in args.hosts.split(','):
  # If an IP range specified in hosts, add each host in range to hosts. Else add host to hosts
  if '-' in host_arg:
    ip_vals = host_arg.split('.')
    if '-' in ip_vals[3]:
      ip_range = ip_vals[3].split('-')
      bottom_ip = int(ip_range[0])
      top_ip = int(ip_range[1])

      for ip in range(bottom_ip, top_ip + 1):
        hosts.append('%s.%s.%s.%d' % (ip_vals[0], ip_vals[1], ip_vals[2], ip))
    else:
      print('Cannot scan this ip range')
      exit()
  else:
    hosts.append(host_arg)

# Set IP protocol(s) to use during scan
protocols = [socket.SOCK_STREAM]
if args.u:
  protocols = [socket.SOCK_DGRAM]
if args.t and args.u:
  protocols = [socket.SOCK_STREAM, socket.SOCK_DGRAM]

# Prints only if verbose (-v) option set
def verbose_print(output):
  if args.verbose:
    print(output)

# Scans port on host
def scan_port(host, port):
  # Scan port with each specified protocol
  for protocol in protocols:
    # If using UDP protocol. Else use TCP protocol
    if protocol == socket.SOCK_DGRAM:
      try:
        s = socket.socket(socket.AF_INET, protocol)
        s.sendto("Test data", (host, port))

        s.recvfrom(255)
      except Exception, e:
        try:
          errno, errtxt = e
        except ValueError:
          print('\t%d/%s\t OPEN' % (port, 'UDP'))
        else:
          verbose_print('\t%d/%s\t CLOSED' % (port, 'UDP'))
    else:
      s = socket.socket(socket.AF_INET, protocol)
      conn = s.connect_ex((host, port))

      # If connection established, port is OPEN 
      if (conn == 0):
        print('\t%d/%s\t OPEN' % (port, 'TCP'))
      else:
        verbose_print('\t%d/%s\t CLOSED' % (port, 'TCP'))

    s.close()

# For each host in specified hosts, scan ports
for host in hosts:
  print('Host: %s' % host)
  print('\tPORT\tSTATUS')

  # If ports to scan are specified, scan only those. Else scan all ports.
  if args.ports:
    for ports_arg in args.ports.split(','):
      # If a port range is given, scan each port in range. Else scan the given port.
      if '-' in ports_arg:
        port_range = ports_arg.split('-')
        bottom_port = int(port_range[0])
        top_port = int(port_range[1])

        for port in range(bottom_port, top_port + 1):
          scan_port(host, port)
      else:
        port = int(ports_arg)
        scan_port(host, port)
  else:
    for port in range(1, 65535):
      scan_port(host, port)

  print
