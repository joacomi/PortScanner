import socket
import sys

def usage(error = 0):
    print("Usage: scanner.py -v -p <ports> <ip>")
    sys.exit(error)

def process_arguments():
    verbose = False
    aux_ports = []
    max_number_of_arguments = 5
    min_number_of_arguments = 2

    if len( sys.argv ) < min_number_of_arguments or len( sys.argv ) > max_number_of_arguments :
        usage(1)

    for pos in range(len(sys.argv)):
        if sys.argv[pos] == "-h" or sys.argv[pos] == "--help":
            usage(0)
        if sys.argv[pos] == "-p" or sys.argv[pos] == "--ports":
            if len(sys.argv) < pos + 3 :
                usage(1)
            aux_ports = sys.argv[pos + 1].split(',')
        if sys.argv[pos] == "-v":
            verbose = True

    ip = sys.argv[-1]
    if not isinstance(ip, str):
        usage(1)

    ports = []
    for p in aux_ports:

        port = p.split('-')
        if not str.isdigit( port[0] ) :
            usage(1)

        if len(port) > 1  and str.isdigit( port[1] ):
            ports.extend( range( int(port[0]), int(port[1]) + 1 ) )
        else:
            ports.append( int(port[0]) )

    return ports, ip, verbose

def scan_port(ip, port, verbose):
    if verbose:
        print("Trying to connect to port: " + str(port))

    try:
        s = socket.socket( socket.AF_INET, socket.SOCK_STREAM )

        res = s.connect_ex(( ip, port ))
        if res == 0 :
            print("Port " + str(port) + " is open")
        s.close()

    except socket.gaierror:
        print("Can't resolve hostname")
        sys.exit()
    except OSError:
        print("An error ocurred")
        sys.exit()
    except KeyboardInterrupt:
        print("")
        sys.exit()

ports, ip, verbose = process_arguments()

# Default ports to scan
if not ports:
    ports = [21, 22, 80, 443]

for p in ports:
    scan_port(ip, p, verbose)
