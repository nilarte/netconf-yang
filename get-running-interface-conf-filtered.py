from ncclient import manager

f_xml = """
<filter>
  <interface-configurations xmlns="http://cisco.com/ns/yang/Cisco-IOS-XR-ifmgr-cfg">
    <interface-configuration/>
  </interface-configurations>
</filter>
"""

with manager.connect(host="<SANDBOX IOS SERVER>", port=830,
                     username="admin", password="<PASSWORD>",
                     hostkey_verify=False, allow_agent=False, look_for_keys=False) as m:
    r = m.get_config(source="running", filter=("subtree", f_xml))
    print(r.xml[:4000])
