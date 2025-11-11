from ncclient import manager
filter = '''
<filter>
  <interfaces xmlns="urn:ietf:params:xml:ns:netconf:base:1.0"/>
</filter>
'''


with manager.connect(
    host=__import__('os').environ.get('CISCO_HOST'),
    port=int(__import__('os').environ.get('CISCO_PORT', 830)), #use environment variable for port as well
    username="admin",
    password=__import__('os').environ.get('CISCO_PASSWORD'),
    hostkey_verify=False
    ) as m:
    result = m.get(filter=filter)
    print(result.xml)



