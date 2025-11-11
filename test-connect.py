from ncclient import manager

with manager.connect(
    # Get host from environment variable
    host=__import__('os').environ.get('CISCO_HOST'),
    port=int(__import__('os').environ.get('CISCO_PORT', 830)),
    username="admin",
    password=__import__('os').environ.get('CISCO_PASSWORD'),
    hostkey_verify=False
    ) as m:
    print("Connected OK")
    print("Server capabilities")
    for cap in m.server_capabilities:
        print(cap)
