from ncclient import manager

with manager.connect(host="<SANDBOX IOS SERVER>", port=830,
                     username="admin", password="<PASSWORD>",
                     hostkey_verify=False, allow_agent=False, look_for_keys=False) as m:
    r = m.get_config(source="running")
    print(r.xml[:4000])  # you should see <interface-configurations>
