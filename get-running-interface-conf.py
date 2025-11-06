from ncclient import manager
filter = '''
<filter>
  <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces"/>
</filter>
'''


with manager.connect(
    host="<SANDBOX IOS SERVER>",
    port=830,
    username="admin",
    password="<PASSWORD>",
    hostkey_verify=False
    ) as m:
    result = m.get(filter=filter)
    print(result.xml)



