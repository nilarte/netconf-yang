from ncclient import manager

with manager.connect(
    host="<SANDBOX IOS SERVER>",
    port=830,
    username="admin",
    password="<PASSWORD>",
    hostkey_verify=False
    ) as m:
    print("Connected OK")
    print("Server capabilities")
    for cap in m.server_capabilities:
        print(cap)
