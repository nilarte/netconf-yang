from ncclient import manager

with manager.connect(
    host=__import__('os').environ.get('CISCO_HOST'),
    port=int(__import__('os').environ.get('CISCO_PORT', 830)),
    username="admin",
    password=__import__('os').environ.get('CISCO_PASSWORD'),
    hostkey_verify=False,
    device_params={'name': 'iosxr'},
    allow_agent=False,
    look_for_keys=False
) as m:

    # Proper NETCONF filter wrapped in <filter> with type="subtree"
    filter_xml = """
    <filter xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" type="subtree">
      <interfaces xmlns="http://openconfig.net/yang/interfaces">
        <interface>
          <name>GigabitEthernet0/0/0/0</name>
          <config/>
          <state/>
        </interface>
      </interfaces>
    </filter>
    """

    reply = m.get(filter_xml)
    print(reply.xml)

  # # Parse the returned XML to an Ordered Dictionary
  # netconf_data = xmltodict.parse(reply.xml)["rpc-reply"]["data"]

  # # Create a list of interfaces
  # interfaces = netconf_data["interfaces"]["interface"]

  # print("The interface status of the device is: ")
  # # Loop over interfaces and report status
  # for interface in interfaces:
  #     print("Interface {} enabled status is {}".format(
  #             interface["name"],
  #             interface["enabled"]
  #             )
  #         )
  # print("\n")
 