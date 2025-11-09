from ncclient import manager
filter = '''
<filter>
  <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces"/>
</filter>
'''


with manager.connect(
    host=__import__('os').environ.get('CISCO_HOST'),
    port=830,
    username="admin",
    password=__import__('os').environ.get('CISCO_PASSWORD'),
    hostkey_verify=False
    ) as m:
    result = m.get(filter=filter)
    print(result.xml)



