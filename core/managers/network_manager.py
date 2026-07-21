import socket
import psutil


class NetworkManager:

    def __init__(self):

        pass

    def get_hostname(self):

        return socket.gethostname()

    def get_ip_addresses(self):

        addresses = []

        adapters = psutil.net_if_addrs()

        for adapter_name, adapter_addresses in adapters.items():

            for address in adapter_addresses:

                if address.family == 2:

                    addresses.append(

                        {

                            "adapter":
                                adapter_name,

                            "ip_address":
                                address.address,

                            "subnet_mask":
                                address.netmask,

                        }

                    )

        return addresses

    def get_information(self):

        adapters = self.get_ip_addresses()

        warnings = []

        status = "SUCCESS"

        if len(adapters) == 0:

            status = "WARNING"

            warnings.append(

                "No active network adapters found."

            )

        return {

            "success": True,

            "status": status,

            "warnings": warnings,

            "errors": [],

            "data": {

                "hostname":

                    self.get_hostname(),

                "network_adapters":

                    adapters,

            }

        }