#!/usr/bin/python
# coding=utf8

import sys
import dbus

bus = dbus.SessionBus()
bus_obj = bus.get_object(
    "im.pidgin.purple.PurpleService",
    "/im/pidgin/purple/PurpleObject")
purple = dbus.Interface(bus_obj, "im.pidgin.purple.PurpleInterface")
accounts = {}
for acc_id in purple.PurpleAccountsGetAllActive():
    accounts[acc_id] = {
        'name': purple.PurpleAccountGetUsername(acc_id),
        'proto': purple.PurpleAccountGetProtocolName(acc_id)}

buddies = {}
for acc_id in accounts:
    for buddy_id in purple.PurpleFindBuddies(acc_id, ''):
        if not purple.PurpleBuddyIsOnline(buddy_id):
            continue
        buddy_name = purple.PurpleBuddyGetName(buddy_id)
        buddy_alias = buddy_name[0:buddy_name.find('@')]
        buddies[buddy_alias] = {
            'acc_id': acc_id,
            'name': buddy_name}

if len(sys.argv) == 2:
    if sys.argv[1].startswith('-h'):
        sys.stdout.write(
            'usage: {0} [-h|--help] [buddy-alias]\n'.format(
                sys.argv[0]))
    else:
        buddy = buddies[sys.argv[1]]
        purple.PurpleConversationNew(1, buddy['acc_id'], buddy['name'])
else:
    for buddy_alias in buddies:
        sys.stdout.write('{0}\n'.format(buddy_alias))
