from ncclient import manager

with manager.connect(host=__import__('os').environ.get('CISCO_HOST'), port=830,
                     username="admin", password=__import__('os').environ.get('CISCO_PASSWORD'),
                     hostkey_verify=False, allow_agent=False, look_for_keys=False) as m:
    r = m.get_config(source="running")
    #print(r.xml[:4000])  # you should see <interface-configurations>
    print(r.xml)  # you should see <interface-configurations>
