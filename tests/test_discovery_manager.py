from discovery.discovery_manager import DiscoveryManager


manager = DiscoveryManager()

snapshot = manager.start_discovery()

print(snapshot)