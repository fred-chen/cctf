"""
Created on Aug 25, 2018

@author: fred

===============================================================================
"""

import nmap
from .common import Common


class Scanner(Common):
    """Scanner is a class that provides nmap scanning functions."""

    def __init__(self, *args, **kwargs):
        Common.__init__(self, *args, **kwargs)
        self.scanner = nmap.PortScanner()
        self.ports = "22"
        self.hosts = "localhost"
        self.arguments = "-sV -O"

    def scan(self, hosts=None, ports=None, arguments=None) -> dict:
        """scan hosts for open ports

        Args:
            hosts (str, optional): the list of hosts to scan. Format is nmap
            complient, e.g. 192.168.0.*,192.168.1.1-100. Defaults to None.

            ports (str, optional): the list of ports to scan. Format is nmap
            complient, e.g. 22,80,443,50-100. Defaults to None.

            arguments (str, optional): the list of arguments to pass to nmap.
            Defaults to None.

        Returns:
            dict: the nmap scan results in dict format. example:
            {
                "nmap": {
                    "command_line": "nmap -oX - -p 22 -sV -O 127.0.0.1",
                    "scaninfo": { "tcp": { "method": "syn", "services": "22" } },
                    "scanstats": {
                    "timestr": "Sat Aug  5 16:25:43 2023",
                    "elapsed": "3.38",
                    "uphosts": "1",
                    "downhosts": "0",
                    "totalhosts": "1"
                    }
                },
                "scan": {
                    "127.0.0.1": {
                        "hostnames": [{ "name": "ngds-dev.chenp.net", "type": "PTR" }],
                        "addresses": { "ipv4": "127.0.0.1" },
                        "vendor": {},
                        "status": { "state": "up", "reason": "localhost-response" },
                        "uptime": { "seconds": "842607", "lastboot": "Wed Jul 26 22:22:16 2023" },
                        "tcp": {
                            "22": {
                                "state": "open",
                                "reason": "syn-ack",
                                "name": "ssh",
                                "product": "OpenSSH",
                                "version": "8.0",
                                "extrainfo": "protocol 2.0",
                                "conf": "10",
                                "cpe": "cpe:/a:openbsd:openssh:8.0"
                            }
                        },
                        "portused": [
                            { "state": "open", "proto": "tcp", "portid": "22" },
                            { "state": "closed", "proto": "udp", "portid": "41868" }
                        ],
                        "osmatch": [
                            {
                                "name": "Linux 2.6.32",
                                "accuracy": "100",
                                "line": "55543",
                                "osclass": [
                                    {
                                    "type": "general purpose",
                                    "vendor": "Linux",
                                    "osfamily": "Linux",
                                    "osgen": "2.6.X",
                                    "accuracy": "100",
                                    "cpe": ["cpe:/o:linux:linux_kernel:2.6.32"]
                                    }
                                ]
                            }
                        ]
                    }
                }
            }
        """
        if not hosts:
            hosts = self.hosts
        if not ports:
            ports = self.ports
        if not arguments:
            arguments = self.arguments

        return self.scanner.scan(hosts=hosts, ports=ports, arguments=arguments)
