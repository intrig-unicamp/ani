# Abstracted Network Inventory (ANI)

The Abstracted Network Inventory (ANI) component proactively constructs multiple network views over the same network infrastructure, called Logical Network Inventories (LNIs). Each LNI is optimized to a service in terms of its requirements such as CPU, memory, latency, etc. Every new service in a catalog triggers the creation of another LNI that will be part of the optimized network inventory. As such, service requirements are used in the method to guide the right level of abstraction.
