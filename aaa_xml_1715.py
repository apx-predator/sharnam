# aaa_features_1715.py
# Modular AAA XML bodies for Cisco-IOS-XE-aaa (IOS XE 17.15, rev 2024-07-01, v7.0.0).
# Same conventions as interface_attrs_1715.py:
#   * Bare interface/native-scoped fragments, NO <config>/<native> wrapper
#   * One LABEL_1715 string per feature + a matching LABEL_REMOVE_1715 twin
#   * $placeholders via string.Template
#   * Caller wraps: <config><native>$anchor>…</$anchor></native></config>
#   * Anchor name is documented in each section banner; the AAAA node is
#     inserted with xmlns="$AAA" on its first element by the caller's wrapper.

# ============================================================
# NAMESPACES (carried by the caller's NS dict)
# ============================================================
# $N    = http://cisco.com/ns/yang/Cisco-IOS-XE-native
# $NC   = urn:ietf:params:xml:ns:netconf:base:1.0
# $AAA  = http://cisco.com/ns/yang/Cisco-IOS-XE-aaa


# ============================================================
# 1. aaa  — general  (anchor: aaa)
# ============================================================
AAA_NEW_MODEL_1715        = "<new-model/>"
AAA_NEW_MODEL_REMOVE_1715 = '<new-model nc:operation="remove"/>'

AAA_SESSION_MIB_DISCONNECT_1715 = (
    "<session-mib><disconnect/></session-mib>"
)
AAA_SESSION_MIB_DISCONNECT_REMOVE_1715 = (
    '<session-mib><disconnect nc:operation="remove"/></session-mib>'
)

AAA_SESSION_MIB_POPULATE_SETUP_1715 = (
    "<session-mib><populate><setup/></populate></session-mib>"
)
AAA_SESSION_MIB_POPULATE_SETUP_REMOVE_1715 = (
    '<session-mib><populate><setup nc:operation="remove"/></populate></session-mib>'
)

AAA_SESSION_MIB_POPULATE_START_1715 = (
    "<session-mib><populate><start/></populate></session-mib>"
)
AAA_SESSION_MIB_POPULATE_START_REMOVE_1715 = (
    '<session-mib><populate><start nc:operation="remove"/></populate></session-mib>'
)

AAA_SESSION_ID_1715        = "<session-id>$mode</session-id>"
AAA_SESSION_ID_REMOVE_1715 = '<session-id nc:operation="remove"/>'

AAA_LOGIN_DISPLAY_1715        = "<login><display>$disp</display></login>"
AAA_LOGIN_DISPLAY_REMOVE_1715 = '<login><display nc:operation="remove"/></login>'

AAA_LOGIN_SUCCESS_TRACK_CONF_TIME_1715 = (
    "<login><success-track-conf-time>$hours</success-track-conf-time></login>"
)
AAA_LOGIN_SUCCESS_TRACK_CONF_TIME_REMOVE_1715 = (
    '<login><success-track-conf-time nc:operation="remove"/></login>'
)

AAA_MAX_SESSIONS_1715        = "<max-sessions>$max</max-sessions>"
AAA_MAX_SESSIONS_REMOVE_1715 = '<max-sessions nc:operation="remove"/>'

AAA_MEMORY_THRESHOLD_ACCOUNTING_DISABLE_1715 = (
    "<memory><threshold><accounting><disable>$pct</disable></accounting></threshold></memory>"
)
AAA_MEMORY_THRESHOLD_ACCOUNTING_DISABLE_REMOVE_1715 = (
    '<memory><threshold><accounting><disable nc:operation="remove"/></accounting></threshold></memory>'
)

AAA_MEMORY_THRESHOLD_AUTHENTICATION_REJECT_1715 = (
    "<memory><threshold><authentication><reject>$pct</reject></authentication></threshold></memory>"
)
AAA_MEMORY_THRESHOLD_AUTHENTICATION_REJECT_REMOVE_1715 = (
    '<memory><threshold><authentication><reject nc:operation="remove"/></authentication></threshold></memory>'
)

AAA_PASSWORD_RESTRICTION_1715        = "<password>restriction</password>"
AAA_PASSWORD_RESTRICTION_REMOVE_1715 = '<password nc:operation="remove"/>'

AAA_POLICY_INTERFACE_CONFIG_1715 = (
    "<policy><interface-config>allow-subinterface</interface-config></policy>"
)
AAA_POLICY_INTERFACE_CONFIG_REMOVE_1715 = (
    '<policy><interface-config nc:operation="remove"/></policy>'
)

AAA_ROUTE_DOWNLOAD_UPDATE_PERIOD_1715 = (
    "<route><download><update-period>$minutes</update-period></download></route>"
)
AAA_ROUTE_DOWNLOAD_UPDATE_PERIOD_REMOVE_1715 = (
    '<route><download><update-period nc:operation="remove"/></download></route>'
)

AAA_ROUTE_DOWNLOAD_AUTHORIZATION_1715 = (
    "<route><download><authorization>$mlist</authorization></download></route>"
)
AAA_ROUTE_DOWNLOAD_AUTHORIZATION_REMOVE_1715 = (
    '<route><download><authorization nc:operation="remove"/></download></route>'
)

AAA_TRACEBACK_RECORDING_1715        = "<traceback>recording</traceback>"
AAA_TRACEBACK_RECORDING_REMOVE_1715 = '<traceback nc:operation="remove"/>'

AAA_REMOTE_USERNAME_1715        = "<remote><username>$remote_user</username></remote>"
AAA_REMOTE_USERNAME_REMOVE_1715 = '<remote><username nc:operation="remove"/></remote>'


# ============================================================
# 2. aaa cache profiles  (anchor: aaa)
# ============================================================
AAA_CACHE_PROFILE_CREATE_1715 = (
    "<cache><cache-profile><name>$profile</name></cache-profile></cache>"
)
AAA_CACHE_PROFILE_CREATE_REMOVE_1715 = (
    '<cache><cache-profile><name>$profile</name></cache-profile></cache>'
)

AAA_CACHE_PROFILE_ALL_1715 = (
    "<cache><cache-profile><name>$profile</name><all/></cache-profile></cache>"
)
AAA_CACHE_PROFILE_ALL_REMOVE_1715 = (
    '<cache><cache-profile><name>$profile</name><all nc:operation="remove"/></cache-profile></cache>'
)

AAA_CACHE_PROFILE_ALL_NO_AUTH_1715 = (
    "<cache><cache-profile><name>$profile</name><all><no-auth/></all></cache-profile></cache>"
)
AAA_CACHE_PROFILE_ALL_NO_AUTH_REMOVE_1715 = (
    '<cache><cache-profile><name>$profile</name><all><no-auth nc:operation="remove"/></all></cache-profile></cache>'
)

AAA_CACHE_PROFILE_REGEXP_ANY_1715 = (
    "<cache><cache-profile><name>$profile</name>"
    "<regexp><name>$regex</name><any/></regexp></cache-profile></cache>"
)
AAA_CACHE_PROFILE_REGEXP_ANY_REMOVE_1715 = (
    '<cache><cache-profile><name>$profile</name>'
    '<regexp><name>$regex</name><any nc:operation="remove"/></regexp></cache-profile></cache>'
)

AAA_CACHE_PROFILE_REGEXP_ONLY_1715 = (
    "<cache><cache-profile><name>$profile</name>"
    "<regexp><name>$regex</name><only/></regexp></cache-profile></cache>"
)
AAA_CACHE_PROFILE_REGEXP_ONLY_REMOVE_1715 = (
    '<cache><cache-profile><name>$profile</name>'
    '<regexp><name>$regex</name><only nc:operation="remove"/></regexp></cache-profile></cache>'
)

AAA_CACHE_PROFILE_REGEXP_NO_AUTH_1715 = (
    "<cache><cache-profile><name>$profile</name>"
    "<regexp><name>$regex</name><no-auth/></regexp></cache-profile></cache>"
)
AAA_CACHE_PROFILE_REGEXP_NO_AUTH_REMOVE_1715 = (
    '<cache><cache-profile><name>$profile</name>'
    '<regexp><name>$regex</name><no-auth nc:operation="remove"/></regexp></cache-profile></cache>'
)

AAA_CACHE_PROFILE_PROFILE_1715 = (
    "<cache><cache-profile><name>$profile</name>"
    "<profile><name>$match</name></profile></cache-profile></cache>"
)
AAA_CACHE_PROFILE_PROFILE_REMOVE_1715 = (
    '<cache><cache-profile><name>$profile</name>'
    '<profile><name>$match</name></profile></cache-profile></cache>'
)

AAA_CACHE_PROFILE_PROFILE_NO_AUTH_1715 = (
    "<cache><cache-profile><name>$profile</name>"
    "<profile><name>$match</name><no-auth/></profile></cache-profile></cache>"
)
AAA_CACHE_PROFILE_PROFILE_NO_AUTH_REMOVE_1715 = (
    '<cache><cache-profile><name>$profile</name>'
    '<profile><name>$match</name><no-auth nc:operation="remove"/></profile></cache-profile></cache>'
)

AAA_CACHE_PROFILE_DEFAULT_ALL_1715 = (
    "<cache><cache-profile><name>$profile</name><default><all/></default></cache-profile></cache>"
)
AAA_CACHE_PROFILE_DEFAULT_ALL_REMOVE_1715 = (
    '<cache><cache-profile><name>$profile</name><default><all nc:operation="remove"/></default></cache-profile></cache>'
)

AAA_CACHE_PROFILE_DEFAULT_REGEXP_ANY_1715 = (
    "<cache><cache-profile><name>$profile</name>"
    "<default><regexp><name>$regex</name><any/></regexp></default></cache-profile></cache>"
)
AAA_CACHE_PROFILE_DEFAULT_REGEXP_ANY_REMOVE_1715 = (
    '<cache><cache-profile><name>$profile</name>'
    '<default><regexp><name>$regex</name><any nc:operation="remove"/></regexp></default></cache-profile></cache>'
)

AAA_CACHE_PROFILE_DEFAULT_REGEXP_ONLY_1715 = (
    "<cache><cache-profile><name>$profile</name>"
    "<default><regexp><name>$regex</name><only/></regexp></default></cache-profile></cache>"
)
AAA_CACHE_PROFILE_DEFAULT_REGEXP_ONLY_REMOVE_1715 = (
    '<cache><cache-profile><name>$profile</name>'
    '<default><regexp><name>$regex</name><only nc:operation="remove"/></regexp></default></cache-profile></cache>'
)

AAA_CACHE_PROFILE_DEFAULT_PROFILE_1715 = (
    "<cache><cache-profile><name>$profile</name>"
    "<default><profile><name>$match</name></profile></default></cache-profile></cache>"
)
AAA_CACHE_PROFILE_DEFAULT_PROFILE_REMOVE_1715 = (
    '<cache><cache-profile><name>$profile</name>'
    '<default><profile><name>$match</name></profile></default></cache-profile></cache>'
)


# ============================================================
# 3. aaa group server tacacsplus[name]  (anchor: aaa)
# ============================================================
AAA_GRP_TACACS_CREATE_1715 = (
    "<group><server><tacacsplus><name>$grp</name></tacacsplus></server></group>"
)
AAA_GRP_TACACS_CREATE_REMOVE_1715 = (
    '<group><server><tacacsplus nc:operation="remove"><name>$grp</name></tacacsplus></server></group>'
)

AAA_GRP_TACACS_LEGACY_CREATE_1715 = (
    "<group><server><tacacs><name>$grp</name></tacacs></server></group>"
)
AAA_GRP_TACACS_LEGACY_CREATE_REMOVE_1715 = (
    '<group><server><tacacs nc:operation="remove"><name>$grp</name></tacacs></server></group>'
)

AAA_GRP_TACACS_SERVER_NAME_1715 = (
    "<group><server><tacacsplus><name>$grp</name>"
    "<server><name><name>$srv</name></name></server>"
    "</tacacsplus></server></group>"
)
AAA_GRP_TACACS_SERVER_NAME_REMOVE_1715 = (
    '<group><server><tacacsplus><name>$grp</name>'
    '<server><name nc:operation="remove"><name>$srv</name></name></server>'
    '</tacacsplus></server></group>'
)

AAA_GRP_TACACS_SERVER_IP_1715 = (
    "<group><server><tacacsplus><name>$grp</name>"
    "<server><server-ip><name>$host</name></server-ip></server>"
    "</tacacsplus></server></group>"
)
AAA_GRP_TACACS_SERVER_IP_REMOVE_1715 = (
    '<group><server><tacacsplus><name>$grp</name>'
    '<server><server-ip nc:operation="remove"><name>$host</name></server-ip></server>'
    '</tacacsplus></server></group>'
)

AAA_GRP_TACACS_SERVER_PRIVATE_1715 = (
    "<group><server><tacacsplus><name>$grp</name>"
    "<server-private><name>$host</name>$opt_extra</server-private>"
    "</tacacsplus></server></group>"
)
AAA_GRP_TACACS_SERVER_PRIVATE_REMOVE_1715 = (
    '<group><server><tacacsplus><name>$grp</name>'
    '<server-private nc:operation="remove"><name>$host</name></server-private>'
    '</tacacsplus></server></group>'
)

AAA_GRP_TACACS_SERVER_PRIVATE_PORT_1715 = (
    "<group><server><tacacsplus><name>$grp</name>"
    "<server-private><name>$host</name><port>$port</port></server-private>"
    "</tacacsplus></server></group>"
)
AAA_GRP_TACACS_SERVER_PRIVATE_PORT_REMOVE_1715 = (
    '<group><server><tacacsplus><name>$grp</name>'
    '<server-private><name>$host</name><port nc:operation="remove"/></server-private>'
    '</tacacsplus></server></group>'
)

AAA_GRP_TACACS_SERVER_PRIVATE_TIMEOUT_1715 = (
    "<group><server><tacacsplus><name>$grp</name>"
    "<server-private><name>$host</name><timeout>$secs</timeout></server-private>"
    "</tacacsplus></server></group>"
)
AAA_GRP_TACACS_SERVER_PRIVATE_TIMEOUT_REMOVE_1715 = (
    '<group><server><tacacsplus><name>$grp</name>'
    '<server-private><name>$host</name><timeout nc:operation="remove"/></server-private>'
    '</tacacsplus></server></group>'
)

AAA_GRP_TACACS_SERVER_PRIVATE_KEY_1715 = (
    "<group><server><tacacsplus><name>$grp</name>"
    "<server-private><name>$host</name>"
    "<key><encryption>$enc</encryption><key>$key</key></key>"
    "</server-private></tacacsplus></server></group>"
)
AAA_GRP_TACACS_SERVER_PRIVATE_KEY_REMOVE_1715 = (
    '<group><server><tacacsplus><name>$grp</name>'
    '<server-private><name>$host</name><key nc:operation="remove"/></server-private>'
    '</tacacsplus></server></group>'
)

AAA_GRP_TACACS_IP_TACACS_SOURCE_INTERFACE_1715 = (
    "<group><server><tacacsplus><name>$grp</name>"
    "<ip><tacacs><source-interface<$if_type>$if_num</$if_type></source-interface></tacacs></ip>"
    "</tacacsplus></server></group>"
)
AAA_GRP_TACACS_IP_TACACS_SOURCE_INTERFACE_REMOVE_1715 = (
    '<group><server><tacacsplus><name>$grp</name>'
    '<ip><tacacs><source-interface nc:operation="remove"/></tacacs></ip>'
    '</tacacsplus></server></group>'
)

AAA_GRP_TACACS_IP_VRF_1715 = (
    "<group><server><tacacsplus><name>$grp</name>"
    "<ip><vrf><forwarding>$vrf</forwarding></vrf></ip>"
    "</tacacsplus></server></group>"
)
AAA_GRP_TACACS_IP_VRF_REMOVE_1715 = (
    '<group><server><tacacsplus><name>$grp</name>'
    '<ip><vrf><forwarding nc:operation="remove"/></vrf></ip>'
    '</tacacsplus></server></group>'
)

AAA_GRP_TACACS_IPV6_TACACS_SOURCE_INTERFACE_1715 = (
    "<group><server><tacacsplus><name>$grp</name>"
    "<ipv6><tacacs><source-interface><$if_type>$if_num</$if_type></source-interface></tacacs></ipv6>"
    "</tacacsplus></server></group>"
)
AAA_GRP_TACACS_IPV6_TACACS_SOURCE_INTERFACE_REMOVE_1715 = (
    '<group><server><tacacsplus><name>$grp</name>'
    '<ipv6><tacacs><source-interface nc:operation="remove"/></tacacs></ipv6>'
    '</tacacsplus></server></group>'
)

AAA_GRP_TACACS_IPV6_VRF_1715 = (
    "<group><server><tacacsplus><name>$grp</name>"
    "<ipv6><vrf><forwarding>$vrf</forwarding></vrf></ipv6>"
    "</tacacsplus></server></group>"
)
AAA_GRP_TACACS_IPV6_VRF_REMOVE_1715 = (
    '<group><server><tacacsplus><name>$grp</name>'
    '<ipv6><vrf><forwarding nc:operation="remove"/></vrf></ipv6>'
    '</tacacsplus></server></group>'
)

AAA_GRP_TACACS_ACCOUNTING_ACK_BROADCAST_1715 = (
    "<group><server><tacacsplus><name>$grp</name>"
    "<accounting><acknowledge><broadcast/></acknowledge></accounting>"
    "</tacacsplus></server></group>"
)
AAA_GRP_TACACS_ACCOUNTING_ACK_BROADCAST_REMOVE_1715 = (
    '<group><server><tacacsplus><name>$grp</name>'
    '<accounting><acknowledge><broadcast nc:operation="remove"/></acknowledge></accounting>'
    '</tacacsplus></server></group>'
)

AAA_GRP_TACACS_CACHE_AUTHENTICATION_PROFILE_1715 = (
    "<group><server><tacacsplus><name>$grp</name>"
    "<cache><authentication><profile>$profile</profile></authentication></cache>"
    "</tacacsplus></server></group>"
)
AAA_GRP_TACACS_CACHE_AUTHENTICATION_PROFILE_REMOVE_1715 = (
    '<group><server><tacacsplus><name>$grp</name>'
    '<cache><authentication><profile nc:operation="remove"/></authentication></cache>'
    '</tacacsplus></server></group>'
)

AAA_GRP_TACACS_CACHE_AUTHORIZATION_PROFILE_1715 = (
    "<group><server><tacacsplus><name>$grp</name>"
    "<cache><authorization><profile>$profile</profile></authorization></cache>"
    "</tacacsplus></server></group>"
)
AAA_GRP_TACACS_CACHE_AUTHORIZATION_PROFILE_REMOVE_1715 = (
    '<group><server><tacacsplus><name>$grp</name>'
    '<cache><authorization><profile nc:operation="remove"/></authorization></cache>'
    '</tacacsplus></server></group>'
)

AAA_GRP_TACACS_CACHE_EXPIRY_1715 = (
    "<group><server><tacacsplus><name>$grp</name>"
    "<cache><expiry>$expiry</expiry></cache>"
    "</tacacsplus></server></group>"
)
AAA_GRP_TACACS_CACHE_EXPIRY_REMOVE_1715 = (
    '<group><server><tacacsplus><name>$grp</name>'
    '<cache><expiry nc:operation="remove"/></cache>'
    '</tacacsplus></server></group>'
)

AAA_GRP_TACACS_DNS_ALIAS_LOOKUP_1715 = (
    "<group><server><tacacsplus><name>$grp</name>"
    "<dns-alias-lookup/>"
    "</tacacsplus></server></group>"
)
AAA_GRP_TACACS_DNS_ALIAS_LOOKUP_REMOVE_1715 = (
    '<group><server><tacacsplus><name>$grp</name>'
    '<dns-alias-lookup nc:operation="remove"/>'
    '</tacacsplus></server></group>'
)

AAA_GRP_TACACS_HOST_1715 = (
    "<group><server><tacacsplus><name>$grp</name>"
    "<host><ip-address>$host</ip-address></host>"
    "</tacacsplus></server></group>"
)
AAA_GRP_TACACS_HOST_REMOVE_1715 = (
    '<group><server><tacacsplus><name>$grp</name>'
    '<host nc:operation="remove"><ip-address>$host</ip-address></host>'
    '</tacacsplus></server></group>'
)

AAA_GRP_TACACS_PICK_METHOD_1715 = (
    "<group><server><tacacsplus><name>$grp</name>"
    "<pick-method>$method</pick-method>"
    "</tacacsplus></server></group>"
)
AAA_GRP_TACACS_PICK_METHOD_REMOVE_1715 = (
    '<group><server><tacacsplus><name>$grp</name>'
    '<pick-method nc:operation="remove"/>'
    '</tacacsplus></server></group>'
)

AAA_GRP_TACACS_TIMEOUT_1715 = (
    "<group><server><tacacsplus><name>$grp</name>"
    "<timeout>$secs</timeout>"
    "</tacacsplus></server></group>"
)
AAA_GRP_TACACS_TIMEOUT_REMOVE_1715 = (
    '<group><server><tacacsplus><name>$grp</name>'
    '<timeout nc:operation="remove"/>'
    '</tacacsplus></server></group>'
)

# ============================================================
# 4. aaa group server radius[name]  (anchor: aaa)
# ============================================================
AAA_GRP_RADIUS_CREATE_1715 = (
    "<group><server><radius><name>$grp</name></radius></server></group>"
)
AAA_GRP_RADIUS_CREATE_REMOVE_1715 = (
    '<group><server><radius nc:operation="remove"><name>$grp</name></radius></server></group>'
)

AAA_GRP_RADIUS_SERVER_NAME_1715 = (
    "<group><server><radius><name>$grp</name>"
    "<server><name><name>$srv</name></name></server>"
    "</radius></server></group>"
)
AAA_GRP_RADIUS_SERVER_NAME_REMOVE_1715 = (
    '<group><server><radius><name>$grp</name>'
    '<server><name nc:operation="remove"><name>$srv</name></name></server>'
    '</radius></server></group>'
)

AAA_GRP_RADIUS_SERVER_DIRECT_1715 = (
    "<group><server><radius><name>$grp</name>"
    "<server><direct><name>$host</name>$opt_extra</direct></server>"
    "</radius></server></group>"
)
AAA_GRP_RADIUS_SERVER_DIRECT_REMOVE_1715 = (
    '<group><server><radius><name>$grp</name>'
    '<server><direct nc:operation="remove"><name>$host</name></direct></server>'
    '</radius></server></group>'
)

AAA_GRP_RADIUS_SERVER_DIRECT_PORTS_1715 = (
    "<group><server><radius><name>$grp</name>"
    "<server><direct><name>$host</name>"
    "<auth-port>$aport</auth-port><acct-port>$cport</acct-port>"
    "</direct></server>"
    "</radius></server></group>"
)
AAA_GRP_RADIUS_SERVER_DIRECT_PORTS_REMOVE_1715 = (
    '<group><server><radius><name>$grp</name>'
    '<server><direct nc:operation="remove"><name>$host</name></direct></server>'
    '</radius></server></group>'
)

AAA_GRP_RADIUS_SUBSCRIBER_MAC_FILTERING_1715 = (
    "<group><server><radius><name>$grp</name>"
    "<subscriber><mac-filtering><security-mode>$mode</security-mode></mac-filtering></subscriber>"
    "</radius></server></group>"
)
AAA_GRP_RADIUS_SUBSCRIBER_MAC_FILTERING_REMOVE_1715 = (
    '<group><server><radius><name>$grp</name>'
    '<subscriber><mac-filtering nc:operation="remove"/></subscriber>'
    '</radius></server></group>'
)

AAA_GRP_RADIUS_MAC_DELIMITER_1715 = (
    "<group><server><radius><name>$grp</name>"
    "<mac-delimiter>$delim</mac-delimiter>"
    "</radius></server></group>"
)
AAA_GRP_RADIUS_MAC_DELIMITER_REMOVE_1715 = (
    '<group><server><radius><name>$grp</name>'
    '<mac-delimiter nc:operation="remove"/>'
    '</radius></server></group>'
)

AAA_GRP_RADIUS_SERVER_PRIVATE_1715 = (
    "<group><server><radius><name>$grp</name>"
    "<server-private><name>$host</name>$opt_extra</server-private>"
    "</radius></server></group>"
)
AAA_GRP_RADIUS_SERVER_PRIVATE_REMOVE_1715 = (
    '<group><server><radius><name>$grp</name>'
    '<server-private nc:operation="remove"><name>$host</name></server-private>'
    '</radius></server></group>'
)

AAA_GRP_RADIUS_SERVER_PRIVATE_PORTS_1715 = (
    "<group><server><radius><name>$grp</name>"
    "<server-private><name>$host</name>"
    "<auth-port>$aport</auth-port><acct-port>$cport</acct-port>"
    "</server-private>"
    "</radius></server></group>"
)
AAA_GRP_RADIUS_SERVER_PRIVATE_PORTS_REMOVE_1715 = (
    '<group><server><radius><name>$grp</name>'
    '<server-private nc:operation="remove"><name>$host</name></server-private>'
    '</radius></server></group>'
)

AAA_GRP_RADIUS_SERVER_PRIVATE_TIMEOUT_1715 = (
    "<group><server><radius><name>$grp</name>"
    "<server-private><name>$host</name><timeout>$secs</timeout></server-private>"
    "</radius></server></group>"
)
AAA_GRP_RADIUS_SERVER_PRIVATE_TIMEOUT_REMOVE_1715 = (
    '<group><server><radius><name>$grp</name>'
    '<server-private><name>$host</name><timeout nc:operation="remove"/></server-private>'
    '</radius></server></group>'
)

AAA_GRP_RADIUS_SERVER_PRIVATE_RETRANSMIT_1715 = (
    "<group><server><radius><name>$grp</name>"
    "<server-private><name>$host</name><retransmit>$retries</retransmit></server-private>"
    "</radius></server></group>"
)
AAA_GRP_RADIUS_SERVER_PRIVATE_RETRANSMIT_REMOVE_1715 = (
    '<group><server><radius><name>$grp</name>'
    '<server-private><name>$host</name><retransmit nc:operation="remove"/></server-private>'
    '</radius></server></group>'
)

AAA_GRP_RADIUS_SERVER_PRIVATE_PAC_1715 = (
    "<group><server><radius><name>$grp</name>"
    "<server-private><name>$host</name><pac/></server-private>"
    "</radius></server></group>"
)
AAA_GRP_RADIUS_SERVER_PRIVATE_PAC_REMOVE_1715 = (
    '<group><server><radius><name>$grp</name>'
    '<server-private><name>$host</name><pac nc:operation="remove"/></server-private>'
    '</radius></server></group>'
)

AAA_GRP_RADIUS_SERVER_PRIVATE_KEY_1715 = (
    "<group><server><radius><name>$grp</name>"
    "<server-private><name>$host</name>"
    "<key><encryption>$enc</encryption><key>$key</key></key>"
    "</server-private>"
    "</radius></server></group>"
)
AAA_GRP_RADIUS_SERVER_PRIVATE_KEY_REMOVE_1715 = (
    '<group><server><radius><name>$grp</name>'
    '<server-private><name>$host</name><key nc:operation="remove"/></server-private>'
    '</radius></server></group>'
)

AAA_GRP_RADIUS_DEADTIME_1715 = (
    "<group><server><radius><name>$grp</name>"
    "<deadtime>$minutes</deadtime>"
    "</radius></server></group>"
)
AAA_GRP_RADIUS_DEADTIME_REMOVE_1715 = (
    '<group><server><radius><name>$grp</name>'
    '<deadtime nc:operation="remove"/>'
    '</radius></server></group>'
)

AAA_GRP_RADIUS_IP_RADIUS_SOURCE_INTERFACE_1715 = (
    "<group><server><radius><name>$grp</name>"
    "<ip><radius><source-interface><$if_type>$if_num</$if_type></source-interface></radius></ip>"
    "</radius></server></group>"
)
AAA_GRP_RADIUS_IP_RADIUS_SOURCE_INTERFACE_REMOVE_1715 = (
    '<group><server><radius><name>$grp</name>'
    '<ip><radius><source-interface nc:operation="remove"/></radius></ip>'
    '</radius></server></group>'
)

AAA_GRP_RADIUS_IP_VRF_1715 = (
    "<group><server><radius><name>$grp</name>"
    "<ip><vrf><forwarding>$vrf</forwarding></vrf></ip>"
    "</radius></server></group>"
)
AAA_GRP_RADIUS_IP_VRF_REMOVE_1715 = (
    '<group><server><radius><name>$grp</name>'
    '<ip><vrf><forwarding nc:operation="remove"/></vrf></ip>'
    '</radius></server></group>'
)

AAA_GRP_RADIUS_IPV6_RADIUS_SOURCE_INTERFACE_1715 = (
    "<group><server><radius><name>$grp</name>"
    "<ipv6><radius><source-interface><$if_type>$if_num</$if_type></source-interface></radius></ipv6>"
    "</radius></server></group>"
)
AAA_GRP_RADIUS_IPV6_RADIUS_SOURCE_INTERFACE_REMOVE_1715 = (
    '<group><server><radius><name>$grp</name>'
    '<ipv6><radius><source-interface nc:operation="remove"/></radius></ipv6>'
    '</radius></server></group>'
)

AAA_GRP_RADIUS_IPV6_VRF_1715 = (
    "<group><server><radius><name>$grp</name>"
    "<ipv6><vrf><forwarding>$vrf</forwarding></vrf></ipv6>"
    "</radius></server></group>"
)
AAA_GRP_RADIUS_IPV6_VRF_REMOVE_1715 = (
    '<group><server><radius><name>$grp</name>'
    '<ipv6><vrf><forwarding nc:operation="remove"/></vrf></ipv6>'
    '</radius></server></group>'
)

AAA_GRP_RADIUS_ACCOUNTING_REQUEST_REJECT_1715 = (
    "<group><server><radius><name>$grp</name>"
    "<accounting><request><reject>$attrs</reject></request></accounting>"
    "</radius></server></group>"
)
AAA_GRP_RADIUS_ACCOUNTING_REQUEST_REJECT_REMOVE_1715 = (
    '<group><server><radius><name>$grp</name>'
    '<accounting><request nc:operation="remove"/></accounting>'
    '</radius></server></group>'
)

AAA_GRP_RADIUS_CACHE_AUTHENTICATION_PROFILE_1715 = (
    "<group><server><radius><name>$grp</name>"
    "<cache><authentication><profile>$profile</profile></authentication></cache>"
    "</radius></server></group>"
)
AAA_GRP_RADIUS_CACHE_AUTHENTICATION_PROFILE_REMOVE_1715 = (
    '<group><server><radius><name>$grp</name>'
    '<cache><authentication><profile nc:operation="remove"/></authentication></cache>'
    '</radius></server></group>'
)

AAA_GRP_RADIUS_CACHE_AUTHORIZATION_PROFILE_1715 = (
    "<group><server><radius><name>$grp</name>"
    "<cache><authorization><profile>$profile</profile></authorization></cache>"
    "</radius></server></group>"
)
AAA_GRP_RADIUS_CACHE_AUTHORIZATION_PROFILE_REMOVE_1715 = (
    '<group><server><radius><name>$grp</name>'
    '<cache><authorization><profile nc:operation="remove"/></authorization></cache>'
    '</radius></server></group>'
)

AAA_GRP_RADIUS_CACHE_EXPIRY_1715 = (
    "<group><server><radius><name>$grp</name>"
    "<cache><expiry-time><expiry>$hours</expiry></expiry-time></cache>"
    "</radius></server></group>"
)
AAA_GRP_RADIUS_CACHE_EXPIRY_REMOVE_1715 = (
    '<group><server><radius><name>$grp</name>'
    '<cache><expiry-time nc:operation="remove"/></cache>'
    '</radius></server></group>'
)

AAA_GRP_RADIUS_DSCP_1715 = (
    "<group><server><radius><name>$grp</name>"
    "<dscp><auth>$auth</auth><acct>$acct</acct></dscp>"
    "</radius></server></group>"
)
AAA_GRP_RADIUS_DSCP_REMOVE_1715 = (
    '<group><server><radius><name>$grp</name>'
    '<dscp nc:operation="remove"/>'
    '</radius></server></group>'
)

AAA_GRP_RADIUS_LOAD_BALANCE_LEAST_OUTSTANDING_1715 = (
    "<group><server><radius><name>$grp</name>"
    "<load-balance><method><least-outstanding/></method></load-balance>"
    "</radius></server></group>"
)
AAA_GRP_RADIUS_LOAD_BALANCE_LEAST_OUTSTANDING_REMOVE_1715 = (
    '<group><server><radius><name>$grp</name>'
    '<load-balance nc:operation="remove"/>'
    '</radius></server></group>'
)

AAA_GRP_RADIUS_LOAD_BALANCE_BATCH_SIZE_1715 = (
    "<group><server><radius><name>$grp</name>"
    "<load-balance><method><least-outstanding><batch-size>$size</batch-size></least-outstanding></method></load-balance>"
    "</radius></server></group>"
)
AAA_GRP_RADIUS_LOAD_BALANCE_BATCH_SIZE_REMOVE_1715 = (
    '<group><server><radius><name>$grp</name>'
    '<load-balance><method><least-outstanding><batch-size nc:operation="remove"/></least-outstanding></method></load-balance>'
    '</radius></server></group>'
)


# ============================================================
# 5. aaa group server ldap[name]  (anchor: aaa)
# ============================================================
AAA_GRP_LDAP_CREATE_1715 = (
    "<group><server><ldap><name>$grp</name></ldap></server></group>"
)
AAA_GRP_LDAP_CREATE_REMOVE_1715 = (
    '<group><server><ldap nc:operation="remove"><name>$grp</name></ldap></server></group>'
)

AAA_GRP_LDAP_SERVER_NAME_1715 = (
    "<group><server><ldap><name>$grp</name>"
    "<server><name><name>$srv</name></name></server>"
    "</ldap></server></group>"
)
AAA_GRP_LDAP_SERVER_NAME_REMOVE_1715 = (
    '<group><server><ldap><name>$grp</name>'
    '<server><name nc:operation="remove"><name>$srv</name></name></server>'
    '</ldap></server></group>'
)


# ============================================================
# 6. aaa attribute list  (anchor: aaa)
# ============================================================
AAA_ATTR_LIST_CREATE_1715 = (
    "<attribute><list><name>$alist</name></list></attribute>"
)
AAA_ATTR_LIST_CREATE_REMOVE_1715 = (
    '<attribute><list nc:operation="remove"><name>$alist</name></list></attribute>'
)

AAA_ATTR_LIST_TYPE_1715 = (
    "<attribute><list><name>$alist</name>"
    "<attribute><type>"
    "<attr-name>$aname</attr-name><attr-value>$aval</attr-value>"
    "$opt_extra"
    "</type></attribute>"
    "</list></attribute>"
)
AAA_ATTR_LIST_TYPE_REMOVE_1715 = (
    '<attribute><list><name>$alist</name>'
    '<attribute><type nc:operation="remove">'
    '<attr-name>$aname</attr-name><attr-value>$aval</attr-value>'
    '</type></attribute>'
    '</list></attribute>'
)

AAA_ATTR_LIST_TYPE_MANDATORY_1715 = (
    "<attribute><list><name>$alist</name>"
    "<attribute><type>"
    "<attr-name>$aname</attr-name><attr-value>$aval</attr-value><mandatory/>"
    "</type></attribute>"
    "</list></attribute>"
)
AAA_ATTR_LIST_TYPE_MANDATORY_REMOVE_1715 = (
    '<attribute><list><name>$alist</name>'
    '<attribute><type><mandatory nc:operation="remove"/></type></attribute>'
    '</list></attribute>'
)

AAA_ATTR_LIST_TYPE_TAG_1715 = (
    "<attribute><list><name>$alist</name>"
    "<attribute><type>"
    "<attr-name>$aname</attr-name><attr-value>$aval</attr-value><tag>$tag</tag>"
    "</type></attribute>"
    "</list></attribute>"
)
AAA_ATTR_LIST_TYPE_TAG_REMOVE_1715 = (
    '<attribute><list><name>$alist</name>'
    '<attribute><type><tag nc:operation="remove"/></type></attribute>'
    '</list></attribute>'
)


# ============================================================
# 7. aaa authentication  (anchor: aaa)
# ============================================================
AAA_AUTHN_BANNER_1715 = (
    "<authentication><banner><banner-value>$banner</banner-value></banner></authentication>"
)
AAA_AUTHN_BANNER_REMOVE_1715 = (
    '<authentication><banner nc:operation="remove"/></authentication>'
)

AAA_AUTHN_FAIL_MESSAGE_1715 = (
    "<authentication><fail-message><message-value>$message</message-value></fail-message></authentication>"
)
AAA_AUTHN_FAIL_MESSAGE_REMOVE_1715 = (
    '<authentication><fail-message nc:operation="remove"/></authentication>'
)

AAA_AUTHN_ATTEMPTS_LOGIN_1715 = (
    "<authentication><attempts><login>$attempts</login></attempts></authentication>"
)
AAA_AUTHN_ATTEMPTS_LOGIN_REMOVE_1715 = (
    '<authentication><attempts nc:operation="remove"/></authentication>'
)

AAA_AUTHN_SUPPRESS_NULL_USERNAME_1715 = (
    "<authentication><suppress><null-username/></suppress></authentication>"
)
AAA_AUTHN_SUPPRESS_NULL_USERNAME_REMOVE_1715 = (
    '<authentication><suppress nc:operation="remove"/></authentication>'
)

AAA_AUTHN_DOT1X_DEFAULT_1715 = (
    "<authentication><dot1x><default>$methods</default></dot1x></authentication>"
)
AAA_AUTHN_DOT1X_DEFAULT_REMOVE_1715 = (
    '<authentication><dot1x><default nc:operation="remove"/></dot1x></authentication>'
)

AAA_AUTHN_DOT1X_LIST_1715 = (
    "<authentication><dot1x><dot1x-list><name>$list</name>$methods</dot1x-list></dot1x></authentication>"
)
AAA_AUTHN_DOT1X_LIST_REMOVE_1715 = (
    '<authentication><dot1x><dot1x-list nc:operation="remove"><name>$list</name></dot1x-list></dot1x></authentication>'
)

AAA_AUTHN_ENABLE_DEFAULT_1715 = (
    "<authentication><enable><default>$methods</default></enable></authentication>"
)
AAA_AUTHN_ENABLE_DEFAULT_REMOVE_1715 = (
    '<authentication><enable><default nc:operation="remove"/></enable></authentication>'
)

AAA_AUTHN_EOU_DEFAULT_RADIUS_1715 = (
    "<authentication><eou><default><group><radius/></group></default></eou></authentication>"
)
AAA_AUTHN_EOU_DEFAULT_RADIUS_REMOVE_1715 = (
    '<authentication><eou nc:operation="remove"/></authentication>'
)

AAA_AUTHN_LOGIN_1715 = (
    "<authentication><login><name>$list</name>$methods</login></authentication>"
)
AAA_AUTHN_LOGIN_REMOVE_1715 = (
    '<authentication><login nc:operation="remove"><name>$list</name></login></authentication>'
)

AAA_AUTHN_ONEP_DEFAULT_LOCAL_1715 = (
    "<authentication><onep><default><local/></default></onep></authentication>"
)
AAA_AUTHN_ONEP_DEFAULT_LOCAL_REMOVE_1715 = (
    '<authentication><onep nc:operation="remove"/></authentication>'
)

AAA_AUTHN_PPP_1715 = (
    "<authentication><ppp><id>$list</id>$methods</ppp></authentication>"
)
AAA_AUTHN_PPP_REMOVE_1715 = (
    '<authentication><ppp nc:operation="remove"><id>$list</id></ppp></authentication>'
)

AAA_AUTHN_PASSWORD_PROMPT_1715 = (
    "<authentication><password-prompt>$text</password-prompt></authentication>"
)
AAA_AUTHN_PASSWORD_PROMPT_REMOVE_1715 = (
    '<authentication><password-prompt nc:operation="remove"/></authentication>'
)

AAA_AUTHN_USERNAME_PROMPT_1715 = (
    "<authentication><username-prompt>$text</username-prompt></authentication>"
)
AAA_AUTHN_USERNAME_PROMPT_REMOVE_1715 = (
    '<authentication><username-prompt nc:operation="remove"/></authentication>'
)

AAA_AUTHN_WEBAUTH_DEFAULT_1715 = (
    "<authentication><webauth><default>$methods</default></webauth></authentication>"
)
AAA_AUTHN_WEBAUTH_DEFAULT_REMOVE_1715 = (
    '<authentication><webauth><default nc:operation="remove"/></webauth></authentication>'
)

AAA_LOCAL_AUTHN_AUTHORIZATION_1715 = (
    "<local><authentication><authorization>"
    "<authen-type>$authn</authen-type>"
    "<authorization>$authz</authorization>"
    "</authorization></authentication></local>"
)
AAA_LOCAL_AUTHN_AUTHORIZATION_REMOVE_1715 = (
    '<local><authentication><authorization nc:operation="remove"/></authentication></local>'
)

AAA_LOCAL_AUTHN_ATTEMPTS_MAX_FAIL_1715 = (
    "<local><authentication><attempts><max-fail>$max</max-fail></attempts></authentication></local>"
)
AAA_LOCAL_AUTHN_ATTEMPTS_MAX_FAIL_REMOVE_1715 = (
    '<local><authentication><attempts nc:operation="remove"/></authentication></local>'
)


# ============================================================
# 8. aaa authorization  (anchor: aaa)
# ============================================================
AAA_AUTHZ_AUTH_TYPE_DEFAULT_GROUP_RADIUS_1715 = (
    "<authorization><auth-type><default><group>radius</group></default></auth-type></authorization>"
)
AAA_AUTHZ_AUTH_TYPE_DEFAULT_GROUP_RADIUS_REMOVE_1715 = (
    '<authorization><auth-type nc:operation="remove"/></authorization>'
)

AAA_AUTHZ_COMMANDS_1715 = (
    "<authorization><commands>"
    "<level>$level</level><list-name>$list</list-name>"
    "$methods"
    "</commands></authorization>"
)
AAA_AUTHZ_COMMANDS_REMOVE_1715 = (
    '<authorization><commands nc:operation="remove">'
    '<level>$level</level><list-name>$list</list-name>'
    '</commands></authorization>'
)

AAA_AUTHZ_CONFIG_COMMANDS_1715 = (
    "<authorization><config-commands/></authorization>"
)
AAA_AUTHZ_CONFIG_COMMANDS_REMOVE_1715 = (
    '<authorization><config-commands nc:operation="remove"/></authorization>'
)

AAA_AUTHZ_CONFIGURATION_LIST_1715 = (
    "<authorization><configuration>"
    "<config-list><name>$list</name>$methods</config-list>"
    "</configuration></authorization>"
)
AAA_AUTHZ_CONFIGURATION_LIST_REMOVE_1715 = (
    '<authorization><configuration>'
    '<config-list nc:operation="remove"><name>$list</name></config-list>'
    '</configuration></authorization>'
)

AAA_AUTHZ_CONFIGURATION_DEFAULT_GROUP_1715 = (
    "<authorization><configuration><default>"
    "<group><group-name><group-name>$grp</group-name></group-name></group>"
    "</default></configuration></authorization>"
)
AAA_AUTHZ_CONFIGURATION_DEFAULT_GROUP_REMOVE_1715 = (
    '<authorization><configuration><default nc:operation="remove"/></configuration></authorization>'
)

AAA_AUTHZ_CONFIGURATION_DEFAULT_CACHE_1715 = (
    "<authorization><configuration><default>"
    "<cache>$cache</cache>"
    "</default></configuration></authorization>"
)
AAA_AUTHZ_CONFIGURATION_DEFAULT_CACHE_REMOVE_1715 = (
    '<authorization><configuration><default><cache nc:operation="remove"/></default></configuration></authorization>'
)

AAA_AUTHZ_CONSOLE_1715 = (
    "<authorization><console/></authorization>"
)
AAA_AUTHZ_CONSOLE_REMOVE_1715 = (
    '<authorization><console nc:operation="remove"/></authorization>'
)

AAA_AUTHZ_CREDENTIAL_DOWNLOAD_DEFAULT_1715 = (
    "<authorization><credential-download><default>$methods</default></credential-download></authorization>"
)
AAA_AUTHZ_CREDENTIAL_DOWNLOAD_DEFAULT_REMOVE_1715 = (
    '<authorization><credential-download><default nc:operation="remove"/></credential-download></authorization>'
)

AAA_AUTHZ_CREDENTIAL_DOWNLOAD_LIST_1715 = (
    "<authorization><credential-download>"
    "<authorization-list><name>$list</name>$methods</authorization-list>"
    "</credential-download></authorization>"
)
AAA_AUTHZ_CREDENTIAL_DOWNLOAD_LIST_REMOVE_1715 = (
    '<authorization><credential-download>'
    '<authorization-list nc:operation="remove"><name>$list</name></authorization-list>'
    '</credential-download></authorization>'
)

AAA_AUTHZ_RADIUS_PROXY_DEFAULT_1715 = (
    "<authorization><radius-proxy><default>$methods</default></radius-proxy></authorization>"
)
AAA_AUTHZ_RADIUS_PROXY_DEFAULT_REMOVE_1715 = (
    '<authorization><radius-proxy><default nc:operation="remove"/></radius-proxy></authorization>'
)

AAA_AUTHZ_RADIUS_PROXY_LIST_1715 = (
    "<authorization><radius-proxy>"
    "<authorization-list><name>$list</name>$methods</authorization-list>"
    "</radius-proxy></authorization>"
)
AAA_AUTHZ_RADIUS_PROXY_LIST_REMOVE_1715 = (
    '<authorization><radius-proxy>'
    '<authorization-list nc:operation="remove"><name>$list</name></authorization-list>'
    '</radius-proxy></authorization>'
)

AAA_AUTHZ_EXEC_1715 = (
    "<authorization><exec><name>$list</name>$methods</exec></authorization>"
)
AAA_AUTHZ_EXEC_REMOVE_1715 = (
    '<authorization><exec nc:operation="remove"><name>$list</name></exec></authorization>'
)

AAA_AUTHZ_EVENTMANAGER_GROUP_1715 = (
    "<authorization><eventmanager><name>$list</name><group>$grp</group></eventmanager></authorization>"
)
AAA_AUTHZ_EVENTMANAGER_GROUP_REMOVE_1715 = (
    '<authorization><eventmanager nc:operation="remove"><name>$list</name></eventmanager></authorization>'
)

AAA_AUTHZ_EVENTMANAGER_LOCAL_1715 = (
    "<authorization><eventmanager><name>$list</name><local/></eventmanager></authorization>"
)
AAA_AUTHZ_EVENTMANAGER_LOCAL_REMOVE_1715 = (
    '<authorization><eventmanager nc:operation="remove"><name>$list</name></eventmanager></authorization>'
)

AAA_AUTHZ_EVENTMANAGER_NONE_1715 = (
    "<authorization><eventmanager><name>$list</name><none/></eventmanager></authorization>"
)
AAA_AUTHZ_EVENTMANAGER_NONE_REMOVE_1715 = (
    '<authorization><eventmanager nc:operation="remove"><name>$list</name></eventmanager></authorization>'
)

AAA_AUTHZ_NETWORK_1715 = (
    "<authorization><network><id>$list</id>$methods</network></authorization>"
)
AAA_AUTHZ_NETWORK_REMOVE_1715 = (
    '<authorization><network nc:operation="remove"><id>$list</id></network></authorization>'
)

AAA_AUTHZ_AUTH_PROXY_DEFAULT_LOCAL_1715 = (
    "<authorization><auth-proxy><default><local/></default></auth-proxy></authorization>"
)
AAA_AUTHZ_AUTH_PROXY_DEFAULT_LOCAL_REMOVE_1715 = (
    '<authorization><auth-proxy nc:operation="remove"/></authorization>'
)

AAA_AUTHZ_AUTH_PROXY_DEFAULT_GROUP_1715 = (
    "<authorization><auth-proxy><default><group>radius</group></default></auth-proxy></authorization>"
)
AAA_AUTHZ_AUTH_PROXY_DEFAULT_GROUP_REMOVE_1715 = (
    '<authorization><auth-proxy nc:operation="remove"/></authorization>'
)

AAA_AUTHZ_ONEP_DEFAULT_GROUP_1715 = (
    "<authorization><onep><default>"
    "<group><group-word><group-word>$grp</group-word></group-word></group>"
    "</default></onep></authorization>"
)
AAA_AUTHZ_ONEP_DEFAULT_GROUP_REMOVE_1715 = (
    '<authorization><onep nc:operation="remove"/></authorization>'
)


# ============================================================
# 9. aaa accounting  (anchor: aaa)
# ============================================================
AAA_ACCT_NESTED_1715 = (
    "<accounting><acct-nested><nested/></acct-nested></accounting>"
)
AAA_ACCT_NESTED_REMOVE_1715 = (
    '<accounting><acct-nested nc:operation="remove"/></accounting>'
)

AAA_ACCT_COMMANDS_LOCAL_1715 = (
    "<accounting><commands-local><commands><local/></commands></commands-local></accounting>"
)
AAA_ACCT_COMMANDS_LOCAL_REMOVE_1715 = (
    '<accounting><commands-local nc:operation="remove"/></accounting>'
)

AAA_ACCT_COMMANDS_NONE_1715 = (
    "<accounting><commands>"
    "<level>$level</level><list-name>$list</list-name>"
    "<commands-config><none/></commands-config>"
    "</commands></accounting>"
)
AAA_ACCT_COMMANDS_NONE_REMOVE_1715 = (
    '<accounting><commands nc:operation="remove"><level>$level</level><list-name>$list</list-name></commands></accounting>'
)

AAA_ACCT_COMMANDS_1715 = (
    "<accounting><commands>"
    "<level>$level</level><list-name>$list</list-name>"
    "<commands-config>"
      "<action-type>$atype</action-type>"
      "$opt_extra"
      "<group-config>$opt_gc$groups</group-config>"
    "</commands-config>"
    "</commands></accounting>"
)
AAA_ACCT_COMMANDS_REMOVE_1715 = (
    '<accounting><commands nc:operation="remove"><level>$level</level><list-name>$list</list-name></commands></accounting>'
)

AAA_ACCT_CONNECTION_NONE_1715 = (
    "<accounting><connection><name>$list</name><none/></connection></accounting>"
)
AAA_ACCT_CONNECTION_NONE_REMOVE_1715 = (
    '<accounting><connection nc:operation="remove"><name>$list</name></connection></accounting>'
)

AAA_ACCT_CONNECTION_1715 = (
    "<accounting><connection><name>$list</name>"
    "<$mode>$opt_extra$groups</$mode>"
    "</connection></accounting>"
)
AAA_ACCT_CONNECTION_REMOVE_1715 = (
    '<accounting><connection nc:operation="remove"><name>$list</name></connection></accounting>'
)

AAA_ACCT_DELAY_START_1715 = (
    "<accounting><delay-start><delay-start/></delay-start></accounting>"
)
AAA_ACCT_DELAY_START_REMOVE_1715 = (
    '<accounting><delay-start nc:operation="remove"/></accounting>'
)

AAA_ACCT_DELAY_START_ALL_1715 = (
    "<accounting><delay-start><all/></delay-start></accounting>"
)
AAA_ACCT_DELAY_START_ALL_REMOVE_1715 = (
    '<accounting><delay-start nc:operation="remove"/></accounting>'
)

AAA_ACCT_DELAY_START_EXTENDED_1715 = (
    "<accounting><delay-start><extended-delay>$n</extended-delay></delay-start></accounting>"
)
AAA_ACCT_DELAY_START_EXTENDED_REMOVE_1715 = (
    '<accounting><delay-start nc:operation="remove"/></accounting>'
)

AAA_ACCT_DOT1X_DEFAULT_1715 = (
    "<accounting><dot1x><default>"
    "<start-stop><group-config>$opt_gc$groups</group-config>$opt_extra</start-stop>"
    "</default></dot1x></accounting>"
)
AAA_ACCT_DOT1X_DEFAULT_REMOVE_1715 = (
    '<accounting><dot1x><default nc:operation="remove"/></dot1x></accounting>'
)

AAA_ACCT_DOT1X_LIST_1715 = (
    "<accounting><dot1x><accounting-list><name>$list</name>"
    "<start-stop><group-config>$opt_gc$groups</group-config>$opt_extra</start-stop>"
    "</accounting-list></dot1x></accounting>"
)
AAA_ACCT_DOT1X_LIST_REMOVE_1715 = (
    '<accounting><dot1x><accounting-list nc:operation="remove"><name>$list</name></accounting-list></dot1x></accounting>'
)

AAA_ACCT_IDENTITY_DEFAULT_1715 = (
    "<accounting><identity><default>"
    "<start-stop><group-config>$opt_gc$groups</group-config>$opt_extra</start-stop>"
    "</default></identity></accounting>"
)

# 9. aaa accounting  (continuation from AAA_ACCT_IDENTITY_DEFAULT_REMOVE_1715)
# ============================================================
AAA_ACCT_IDENTITY_DEFAULT_REMOVE_1715 = (
    '<accounting><identity><default nc:operation="remove"/></identity></accounting>'
)

AAA_ACCT_IDENTITY_LIST_1715 = (
    "<accounting><identity><accounting-list><name>$list</name>"
    "<start-stop><group-config>$opt_gc$groups</group-config>$opt_extra</start-stop>"
    "</accounting-list></identity></accounting>"
)
AAA_ACCT_IDENTITY_LIST_REMOVE_1715 = (
    '<accounting><identity><accounting-list nc:operation="remove"><name>$list</name></accounting-list></identity></accounting>'
)

AAA_ACCT_ONEP_DEFAULT_NONE_1715 = (
    "<accounting><onep><default><none/></default></onep></accounting>"
)
AAA_ACCT_ONEP_DEFAULT_NONE_REMOVE_1715 = (
    '<accounting><onep nc:operation="remove"/></accounting>'
)

AAA_ACCT_ONEP_DEFAULT_1715 = (
    "<accounting><onep><default><$mode>$opt_extra$groups</$mode></default></onep></accounting>"
)
AAA_ACCT_ONEP_DEFAULT_REMOVE_1715 = (
    '<accounting><onep nc:operation="remove"/></accounting>'
)

AAA_ACCT_EXEC_NONE_1715 = (
    "<accounting><exec><name>$list</name><none/></exec></accounting>"
)
AAA_ACCT_EXEC_NONE_REMOVE_1715 = (
    '<accounting><exec nc:operation="remove"><name>$list</name></exec></accounting>'
)

AAA_ACCT_EXEC_1715 = (
    "<accounting><exec><name>$list</name>"
    "<$mode>$opt_extra$groups</$mode>"
    "</exec></accounting>"
)
AAA_ACCT_EXEC_REMOVE_1715 = (
    '<accounting><exec nc:operation="remove"><name>$list</name></exec></accounting>'
)

AAA_ACCT_EXEC_SUBMODE_NONE_1715 = (
    "<accounting><exec-submode><exec><name>$list</name>"
    "<actiontype><none/></actiontype>"
    "</exec></exec-submode></accounting>"
)
AAA_ACCT_EXEC_SUBMODE_NONE_REMOVE_1715 = (
    '<accounting><exec-submode nc:operation="remove"/></accounting>'
)

AAA_ACCT_EXEC_SUBMODE_1715 = (
    "<accounting><exec-submode><exec><name>$list</name>"
    "<actiontype><$mode/></actiontype>"
    "<aaa-accounting-exec-grouping>$exec_groups$opt_extra</aaa-accounting-exec-grouping>"
    "</exec></exec-submode></accounting>"
)
AAA_ACCT_EXEC_SUBMODE_REMOVE_1715 = (
    '<accounting><exec-submode nc:operation="remove"/></accounting>'
)

AAA_ACCT_NETWORK_NONE_1715 = (
    "<accounting><network><id>$list</id><none/></network></accounting>"
)
AAA_ACCT_NETWORK_NONE_REMOVE_1715 = (
    '<accounting><network nc:operation="remove"><id>$list</id></network></accounting>'
)

AAA_ACCT_NETWORK_1715 = (
    "<accounting><network><id>$list</id>"
    "<mode>$mode</mode>$opt_extra$methods"
    "</network></accounting>"
)
AAA_ACCT_NETWORK_REMOVE_1715 = (
    '<accounting><network nc:operation="remove"><id>$list</id></network></accounting>'
)

AAA_ACCT_SEND_COUNTERS_IPV6_1715 = (
    "<accounting><send><counters><ipv6/></counters></send></accounting>"
)
AAA_ACCT_SEND_COUNTERS_IPV6_REMOVE_1715 = (
    '<accounting><send><counters><ipv6 nc:operation="remove"/></counters></send></accounting>'
)

AAA_ACCT_SEND_STOP_RECORD_ALWAYS_1715 = (
    "<accounting><send><stop-record><always/></stop-record></send></accounting>"
)
AAA_ACCT_SEND_STOP_RECORD_ALWAYS_REMOVE_1715 = (
    '<accounting><send><stop-record><always nc:operation="remove"/></stop-record></send></accounting>'
)

AAA_ACCT_SEND_STOP_RECORD_AUTH_FAILURE_1715 = (
    "<accounting><send><stop-record><authentication><failure/></authentication></stop-record></send></accounting>"
)
AAA_ACCT_SEND_STOP_RECORD_AUTH_FAILURE_REMOVE_1715 = (
    '<accounting><send><stop-record><authentication><failure nc:operation="remove"/></authentication></stop-record></send></accounting>'
)

AAA_ACCT_SEND_STOP_RECORD_AUTH_FAILURE_VRF_1715 = (
    "<accounting><send><stop-record><authentication><failure><vrf>$vrf</vrf></failure></authentication></stop-record></send></accounting>"
)
AAA_ACCT_SEND_STOP_RECORD_AUTH_FAILURE_VRF_REMOVE_1715 = (
    '<accounting><send><stop-record><authentication><failure><vrf nc:operation="remove"/></failure></authentication></stop-record></send></accounting>'
)

AAA_ACCT_SEND_STOP_RECORD_AUTH_SUCCESS_REMOTE_1715 = (
    "<accounting><send><stop-record><authentication><success><remote-server/></success></authentication></stop-record></send></accounting>"
)
AAA_ACCT_SEND_STOP_RECORD_AUTH_SUCCESS_REMOTE_REMOVE_1715 = (
    '<accounting><send><stop-record><authentication><success><remote-server nc:operation="remove"/></success></authentication></stop-record></send></accounting>'
)

AAA_ACCT_SEND_STOP_RECORD_AUTH_SUCCESS_REMOTE_VRF_1715 = (
    "<accounting><send><stop-record><authentication><success><remote-server><vrf>$vrf</vrf></remote-server></success></authentication></stop-record></send></accounting>"
)
AAA_ACCT_SEND_STOP_RECORD_AUTH_SUCCESS_REMOTE_VRF_REMOVE_1715 = (
    '<accounting><send><stop-record><authentication><success><remote-server><vrf nc:operation="remove"/></remote-server></success></authentication></stop-record></send></accounting>'
)

AAA_ACCT_SUPPRESS_NULL_USERNAME_1715 = (
    "<accounting><suppress><null-username/></suppress></accounting>"
)
AAA_ACCT_SUPPRESS_NULL_USERNAME_REMOVE_1715 = (
    '<accounting><suppress nc:operation="remove"/></accounting>'
)

AAA_ACCT_SYSTEM_DEFAULT_NONE_1715 = (
    "<accounting><system><default><none/></default></system></accounting>"
)
AAA_ACCT_SYSTEM_DEFAULT_NONE_REMOVE_1715 = (
    '<accounting><system nc:operation="remove"/></accounting>'
)

AAA_ACCT_SYSTEM_DEFAULT_START_STOP_1715 = (
    "<accounting><system><default>"
    "<start-stop>$opt_extra<group-config>$opt_gc$groups</group-config></start-stop>"
    "</default></system></accounting>"
)
AAA_ACCT_SYSTEM_DEFAULT_START_STOP_REMOVE_1715 = (
    '<accounting><system nc:operation="remove"/></accounting>'
)

AAA_ACCT_SYSTEM_DEFAULT_VRF_1715 = (
    "<accounting><system><default><vrf>$vrf</vrf></default></system></accounting>"
)
AAA_ACCT_SYSTEM_DEFAULT_VRF_REMOVE_1715 = (
    '<accounting><system><default><vrf nc:operation="remove"/></default></system></accounting>'
)

AAA_ACCT_SYSTEM_GUARANTEE_FIRST_1715 = (
    "<accounting><system><guarantee-first>$flag</guarantee-first></system></accounting>"
)
AAA_ACCT_SYSTEM_GUARANTEE_FIRST_REMOVE_1715 = (
    '<accounting><system><guarantee-first nc:operation="remove"/></system></accounting>'
)

AAA_ACCT_UPDATE_PERIODIC_1715 = (
    "<accounting><update><periodic>$minutes</periodic></update></accounting>"
)
AAA_ACCT_UPDATE_PERIODIC_REMOVE_1715 = (
    '<accounting><update nc:operation="remove"/></accounting>'
)

AAA_ACCT_UPDATE_NEWINFO_1715 = (
    "<accounting><update><newinfo/></update></accounting>"
)
AAA_ACCT_UPDATE_NEWINFO_REMOVE_1715 = (
    '<accounting><update><newinfo nc:operation="remove"/></update></accounting>'
)

AAA_ACCT_UPDATE_NEWINFO_PERIODIC_1715 = (
    "<accounting><update><newinfo><periodic>$minutes</periodic></newinfo></update></accounting>"
)
AAA_ACCT_UPDATE_NEWINFO_PERIODIC_REMOVE_1715 = (
    '<accounting><update><newinfo><periodic nc:operation="remove"/></newinfo></update></accounting>'
)

AAA_ACCT_AUTH_PROXY_DEFAULT_START_STOP_GROUP_1715 = (
    "<accounting><auth-proxy><default>"
    "<start-stop><group>$grp</group></start-stop>"
    "</default></auth-proxy></accounting>"
)
AAA_ACCT_AUTH_PROXY_DEFAULT_START_STOP_GROUP_REMOVE_1715 = (
    '<accounting><auth-proxy nc:operation="remove"/></accounting>'
)

AAA_ACCT_JITTER_MAXIMUM_1715 = (
    "<accounting><jitter><maximum>$secs</maximum></jitter></accounting>"
)
AAA_ACCT_JITTER_MAXIMUM_REMOVE_1715 = (
    '<accounting><jitter nc:operation="remove"/></accounting>'
)


# ============================================================
# 10. aaa common-criteria[policy]  (anchor: aaa)
# ============================================================
AAA_CC_POLICY_CREATE_1715 = (
    "<common-criteria><policy>$policy</policy></common-criteria>"
)
AAA_CC_POLICY_CREATE_REMOVE_1715 = (
    '<common-criteria nc:operation="remove"><policy>$policy</policy></common-criteria>'
)

AAA_CC_CHAR_CHANGES_1715 = (
    "<common-criteria><policy>$policy</policy>"
    "<char-changes>$n</char-changes>"
    "</common-criteria>"
)
AAA_CC_CHAR_CHANGES_REMOVE_1715 = (
    '<common-criteria><policy>$policy</policy><char-changes nc:operation="remove"/></common-criteria>'
)

AAA_CC_LIFETIME_1715 = (
    "<common-criteria><policy>$policy</policy>"
    "<lifetime>"
      "<year>$years</year><month>$months</month><day>$days</day>"
      "<hours>$hours</hours><minutes>$minutes</minutes><seconds>$seconds</seconds>"
    "</lifetime>"
    "</common-criteria>"
)
AAA_CC_LIFETIME_REMOVE_1715 = (
    '<common-criteria><policy>$policy</policy><lifetime nc:operation="remove"/></common-criteria>'
)

AAA_CC_LOWER_CASE_1715 = (
    "<common-criteria><policy>$policy</policy>"
    "<lower-case>$n</lower-case>"
    "</common-criteria>"
)
AAA_CC_LOWER_CASE_REMOVE_1715 = (
    '<common-criteria><policy>$policy</policy><lower-case nc:operation="remove"/></common-criteria>'
)

AAA_CC_MAX_LENGTH_1715 = (
    "<common-criteria><policy>$policy</policy>"
    "<max-length>$n</max-length>"
    "</common-criteria>"
)
AAA_CC_MAX_LENGTH_REMOVE_1715 = (
    '<common-criteria><policy>$policy</policy><max-length nc:operation="remove"/></common-criteria>'
)

AAA_CC_MIN_LENGTH_1715 = (
    "<common-criteria><policy>$policy</policy>"
    "<min-length>$n</min-length>"
    "</common-criteria>"
)
AAA_CC_MIN_LENGTH_REMOVE_1715 = (
    '<common-criteria><policy>$policy</policy><min-length nc:operation="remove"/></common-criteria>'
)

AAA_CC_NUMERIC_COUNT_1715 = (
    "<common-criteria><policy>$policy</policy>"
    "<numeric-count>$n</numeric-count>"
    "</common-criteria>"
)
AAA_CC_NUMERIC_COUNT_REMOVE_1715 = (
    '<common-criteria><policy>$policy</policy><numeric-count nc:operation="remove"/></common-criteria>'
)

AAA_CC_SPECIAL_CASE_1715 = (
    "<common-criteria><policy>$policy</policy>"
    "<special-case>$n</special-case>"
    "</common-criteria>"
)
AAA_CC_SPECIAL_CASE_REMOVE_1715 = (
    '<common-criteria><policy>$policy</policy><special-case nc:operation="remove"/></common-criteria>'
)

AAA_CC_UPPER_CASE_1715 = (
    "<common-criteria><policy>$policy</policy>"
    "<upper-case>$n</upper-case>"
    "</common-criteria>"
)
AAA_CC_UPPER_CASE_REMOVE_1715 = (
    '<common-criteria><policy>$policy</policy><upper-case nc:operation="remove"/></common-criteria>'
)

AAA_CC_CHARACTER_REPETITION_1715 = (
    "<common-criteria><policy>$policy</policy>"
    "<character-repetition>$n</character-repetition>"
    "</common-criteria>"
)
AAA_CC_CHARACTER_REPETITION_REMOVE_1715 = (
    '<common-criteria><policy>$policy</policy><character-repetition nc:operation="remove"/></common-criteria>'
)

AAA_CC_RESTRICT_CONSECUTIVE_LETTERS_1715 = (
    "<common-criteria><policy>$policy</policy>"
    "<restrict-consecutive-letters/>"
    "</common-criteria>"
)
AAA_CC_RESTRICT_CONSECUTIVE_LETTERS_REMOVE_1715 = (
    '<common-criteria><policy>$policy</policy><restrict-consecutive-letters nc:operation="remove"/></common-criteria>'
)

# ============================================================
# 11. aaa server radius  (anchor: aaa)  — local RADIUS server
# ============================================================
AAA_SRV_RADIUS_DYNAMIC_AUTHOR_1715 = (
    "<server><radius><dynamic-author/></radius></server>"
)
AAA_SRV_RADIUS_DYNAMIC_AUTHOR_REMOVE_1715 = (
    '<server><radius><dynamic-author nc:operation="remove"/></radius></server>'
)

AAA_SRV_RADIUS_DYNAMIC_AUTHOR_PORT_1715 = (
    "<server><radius><dynamic-author><port>$port</port></dynamic-author></radius></server>"
)
AAA_SRV_RADIUS_DYNAMIC_AUTHOR_PORT_REMOVE_1715 = (
    '<server><radius><dynamic-author><port nc:operation="remove"/></dynamic-author></radius></server>'
)

AAA_SRV_RADIUS_DYNAMIC_AUTHOR_CLIENT_1715 = (
    "<server><radius><dynamic-author>"
    "<client><ip>$cip</ip>$opt_extra</client>"
    "</dynamic-author></radius></server>"
)
AAA_SRV_RADIUS_DYNAMIC_AUTHOR_CLIENT_REMOVE_1715 = (
    '<server><radius><dynamic-author><client nc:operation="remove"><ip>$cip</ip></client></dynamic-author></radius></server>'
)

AAA_SRV_RADIUS_DYNAMIC_AUTHOR_CLIENT_DTLS_1715 = (
    "<server><radius><dynamic-author>"
    "<client><ip>$cip</ip><dtls/></client>"
    "</dynamic-author></radius></server>"
)
AAA_SRV_RADIUS_DYNAMIC_AUTHOR_CLIENT_DTLS_REMOVE_1715 = (
    '<server><radius><dynamic-author><client><ip>$cip</ip><dtls nc:operation="remove"/></client></dynamic-author></radius></server>'
)

AAA_SRV_RADIUS_DYNAMIC_AUTHOR_CLIENT_SERVER_KEY_1715 = (
    "<server><radius><dynamic-author>"
    "<client><ip>$cip</ip>"
    "<server-key><key>$ktype</key><string>$key</string></server-key>"
    "</client>"
    "</dynamic-author></radius></server>"
)
AAA_SRV_RADIUS_DYNAMIC_AUTHOR_CLIENT_SERVER_KEY_REMOVE_1715 = (
    '<server><radius><dynamic-author><client><ip>$cip</ip><server-key nc:operation="remove"/></client></dynamic-author></radius></server>'
)

AAA_SRV_RADIUS_DYNAMIC_AUTHOR_CLIENT_VRF_1715 = (
    "<server><radius><dynamic-author>"
    "<client><ip>$cip</ip><vrf><name>$vrf</name>$opt_extra</vrf></client>"
    "</dynamic-author></radius></server>"
)
AAA_SRV_RADIUS_DYNAMIC_AUTHOR_CLIENT_VRF_REMOVE_1715 = (
    '<server><radius><dynamic-author><client><ip>$cip</ip><vrf nc:operation="remove"/></client></dynamic-author></radius></server>'
)

AAA_SRV_RADIUS_DYNAMIC_AUTHOR_CLIENT_VRF_SERVER_KEY_1715 = (
    "<server><radius><dynamic-author>"
    "<client><ip>$cip</ip>"
    "<vrf><name>$vrf</name>"
    "<server-key><key>$ktype</key><string>$key</string></server-key>"
    "</vrf></client>"
    "</dynamic-author></radius></server>"
)
AAA_SRV_RADIUS_DYNAMIC_AUTHOR_CLIENT_VRF_SERVER_KEY_REMOVE_1715 = (
    '<server><radius><dynamic-author><client><ip>$cip</ip><vrf><name>$vrf</name><server-key nc:operation="remove"/></vrf></client></dynamic-author></radius></server>'
)

AAA_SRV_RADIUS_DYNAMIC_AUTHOR_TLS_1715 = (
    "<server><radius><dynamic-author><tls/></dynamic-author></radius></server>"
)
AAA_SRV_RADIUS_DYNAMIC_AUTHOR_TLS_REMOVE_1715 = (
    '<server><radius><dynamic-author><tls nc:operation="remove"/></dynamic-author></radius></server>'
)

AAA_SRV_RADIUS_DYNAMIC_AUTHOR_TLS_PORT_1715 = (
    "<server><radius><dynamic-author><tls><port>$port</port></tls></dynamic-author></radius></server>"
)
AAA_SRV_RADIUS_DYNAMIC_AUTHOR_TLS_PORT_REMOVE_1715 = (
    '<server><radius><dynamic-author><tls><port nc:operation="remove"/></tls></dynamic-author></radius></server>'
)

AAA_SRV_RADIUS_DYNAMIC_AUTHOR_SERVER_KEY_1715 = (
    "<server><radius><dynamic-author>"
    "<server-key><key>$ktype</key><string>$key</string></server-key>"
    "</dynamic-author></radius></server>"
)
AAA_SRV_RADIUS_DYNAMIC_AUTHOR_SERVER_KEY_REMOVE_1715 = (
    '<server><radius><dynamic-author><server-key nc:operation="remove"/></dynamic-author></radius></server>'
)

AAA_SRV_RADIUS_DYNAMIC_AUTHOR_DOMAIN_STRIPPING_1715 = (
    "<server><radius><dynamic-author>"
    "<domain><stripping/></domain>"
    "</dynamic-author></radius></server>"
)
AAA_SRV_RADIUS_DYNAMIC_AUTHOR_DOMAIN_STRIPPING_REMOVE_1715 = (
    '<server><radius><dynamic-author><domain><stripping nc:operation="remove"/></domain></dynamic-author></radius></server>'
)

AAA_SRV_RADIUS_DYNAMIC_AUTHOR_DOMAIN_STRIPPING_R2L_1715 = (
    "<server><radius><dynamic-author>"
    "<domain><stripping><right-to-left/></stripping></domain>"
    "</dynamic-author></radius></server>"
)
AAA_SRV_RADIUS_DYNAMIC_AUTHOR_DOMAIN_STRIPPING_R2L_REMOVE_1715 = (
    '<server><radius><dynamic-author><domain><stripping><right-to-left nc:operation="remove"/></stripping></domain></dynamic-author></radius></server>'
)

AAA_SRV_RADIUS_DYNAMIC_AUTHOR_DOMAIN_DELIMITER_1715 = (
    "<server><radius><dynamic-author>"
    "<domain><delimiter>$delim</delimiter><stripping/></domain>"
    "</dynamic-author></radius></server>"
)
AAA_SRV_RADIUS_DYNAMIC_AUTHOR_DOMAIN_DELIMITER_REMOVE_1715 = (
    '<server><radius><dynamic-author><domain><delimiter nc:operation="remove"/></domain></dynamic-author></radius></server>'
)

AAA_SRV_RADIUS_DYNAMIC_AUTHOR_AUTH_TYPE_1715 = (
    "<server><radius><dynamic-author><auth-type>$atype</auth-type></dynamic-author></radius></server>"
)
AAA_SRV_RADIUS_DYNAMIC_AUTHOR_AUTH_TYPE_REMOVE_1715 = (
    '<server><radius><dynamic-author><auth-type nc:operation="remove"/></dynamic-author></radius></server>'
)

AAA_SRV_RADIUS_DYNAMIC_AUTHOR_IGNORE_RETRANSMISSION_1715 = (
    "<server><radius><dynamic-author>"
    "<ignore><retransmission/></ignore>"
    "</dynamic-author></radius></server>"
)
AAA_SRV_RADIUS_DYNAMIC_AUTHOR_IGNORE_RETRANSMISSION_REMOVE_1715 = (
    '<server><radius><dynamic-author><ignore><retransmission nc:operation="remove"/></ignore></dynamic-author></radius></server>'
)

AAA_SRV_RADIUS_DYNAMIC_AUTHOR_IGNORE_SERVER_KEY_1715 = (
    "<server><radius><dynamic-author>"
    "<ignore><server-key/></ignore>"
    "</dynamic-author></radius></server>"
)
AAA_SRV_RADIUS_DYNAMIC_AUTHOR_IGNORE_SERVER_KEY_REMOVE_1715 = (
    '<server><radius><dynamic-author><ignore><server-key nc:operation="remove"/></ignore></dynamic-author></radius></server>'
)

AAA_SRV_RADIUS_DYNAMIC_AUTHOR_IGNORE_SESSION_KEY_1715 = (
    "<server><radius><dynamic-author>"
    "<ignore><session-key/></ignore>"
    "</dynamic-author></radius></server>"
)
AAA_SRV_RADIUS_DYNAMIC_AUTHOR_IGNORE_SESSION_KEY_REMOVE_1715 = (
    '<server><radius><dynamic-author><ignore><session-key nc:operation="remove"/></ignore></dynamic-author></radius></server>'
)

# --- policy-device ---
AAA_SRV_RADIUS_POLICY_DEVICE_1715 = (
    "<server><radius><policy-device/></radius></server>"
)
AAA_SRV_RADIUS_POLICY_DEVICE_REMOVE_1715 = (
    '<server><radius><policy-device nc:operation="remove"/></radius></server>'
)

AAA_SRV_RADIUS_POLICY_DEVICE_ACCOUNTING_PORT_1715 = (
    "<server><radius><policy-device><accounting><port>$port</port></accounting></policy-device></radius></server>"
)
AAA_SRV_RADIUS_POLICY_DEVICE_ACCOUNTING_PORT_REMOVE_1715 = (
    '<server><radius><policy-device><accounting nc:operation="remove"/></policy-device></radius></server>'
)

AAA_SRV_RADIUS_POLICY_DEVICE_AUTHENTICATION_PORT_1715 = (
    "<server><radius><policy-device><authentication><port>$port</port></authentication></policy-device></radius></server>"
)
AAA_SRV_RADIUS_POLICY_DEVICE_AUTHENTICATION_PORT_REMOVE_1715 = (
    '<server><radius><policy-device><authentication nc:operation="remove"/></policy-device></radius></server>'
)

AAA_SRV_RADIUS_POLICY_DEVICE_CLIENT_1715 = (
    "<server><radius><policy-device>"
    "<client><ip>$cip</ip>$opt_extra</client>"
    "</policy-device></radius></server>"
)
AAA_SRV_RADIUS_POLICY_DEVICE_CLIENT_REMOVE_1715 = (
    '<server><radius><policy-device><client nc:operation="remove"><ip>$cip</ip></client></policy-device></radius></server>'
)

AAA_SRV_RADIUS_POLICY_DEVICE_CLIENT_PORT_1715 = (
    "<server><radius><policy-device>"
    "<client><ip>$cip</ip><port>$port</port></client>"
    "</policy-device></radius></server>"
)
AAA_SRV_RADIUS_POLICY_DEVICE_CLIENT_PORT_REMOVE_1715 = (
    '<server><radius><policy-device><client><ip>$cip</ip><port nc:operation="remove"/></client></policy-device></radius></server>'
)

AAA_SRV_RADIUS_POLICY_DEVICE_CLIENT_KEY_1715 = (
    "<server><radius><policy-device>"
    "<client><ip>$cip</ip>"
    "<key><key>$ktype</key><string>$key</string></key>"
    "</client>"
    "</policy-device></radius></server>"
)
AAA_SRV_RADIUS_POLICY_DEVICE_CLIENT_KEY_REMOVE_1715 = (
    '<server><radius><policy-device><client><ip>$cip</ip><key nc:operation="remove"/></client></policy-device></radius></server>'
)

AAA_SRV_RADIUS_POLICY_DEVICE_CLIENT_VRF_1715 = (
    "<server><radius><policy-device>"
    "<client><ip>$cip</ip><vrf><name>$vrf</name>$opt_extra</vrf></client>"
    "</policy-device></radius></server>"
)
AAA_SRV_RADIUS_POLICY_DEVICE_CLIENT_VRF_REMOVE_1715 = (
    '<server><radius><policy-device><client><ip>$cip</ip><vrf nc:operation="remove"/></client></policy-device></radius></server>'
)

AAA_SRV_RADIUS_POLICY_DEVICE_KEY_1715 = (
    "<server><radius><policy-device>"
    "<key><key>$ktype</key><string>$key</string></key>"
    "</policy-device></radius></server>"
)
AAA_SRV_RADIUS_POLICY_DEVICE_KEY_REMOVE_1715 = (
    '<server><radius><policy-device><key nc:operation="remove"/></policy-device></radius></server>'
)

AAA_SRV_RADIUS_POLICY_DEVICE_MESSAGE_AUTHENTICATOR_IGNORE_1715 = (
    "<server><radius><policy-device>"
    "<message-authenticator><ignore/></message-authenticator>"
    "</policy-device></radius></server>"
)
AAA_SRV_RADIUS_POLICY_DEVICE_MESSAGE_AUTHENTICATOR_IGNORE_REMOVE_1715 = (
    '<server><radius><policy-device><message-authenticator nc:operation="remove"/></policy-device></radius></server>'
)


# ============================================================
# 12. native/radius  (anchor: radius)  — radius filter + radius server[id]
# ============================================================
RADIUS_FILTER_1715 = (
    "<filter><id>$fid</id><match>$match</match></filter>"
)
RADIUS_FILTER_REMOVE_1715 = (
    '<filter nc:operation="remove"><id>$fid</id></filter>'
)

RADIUS_SERVER_CREATE_1715 = (
    "<server><id>$rs</id></server>"
)
RADIUS_SERVER_CREATE_REMOVE_1715 = (
    '<server nc:operation="remove"><id>$rs</id></server>'
)

RADIUS_SERVER_ADDRESS_IPV4_1715 = (
    "<server><id>$rs</id><address><ipv4>$addr</ipv4>$opt_extra</address></server>"
)
RADIUS_SERVER_ADDRESS_IPV4_REMOVE_1715 = (
    '<server><id>$rs</id><address><ipv4 nc:operation="remove"/></address></server>'
)

RADIUS_SERVER_ADDRESS_IPV6_1715 = (
    "<server><id>$rs</id><address><ipv6>$addr</ipv6>$opt_extra</address></server>"
)
RADIUS_SERVER_ADDRESS_IPV6_REMOVE_1715 = (
    '<server><id>$rs</id><address><ipv6 nc:operation="remove"/></address></server>'
)

RADIUS_SERVER_ADDRESS_FQDN_1715 = (
    "<server><id>$rs</id><address><fqdn>$addr</fqdn>$opt_extra</address></server>"
)
RADIUS_SERVER_ADDRESS_FQDN_REMOVE_1715 = (
    '<server><id>$rs</id><address><fqdn nc:operation="remove"/></address></server>'
)

RADIUS_SERVER_ADDRESS_PORTS_1715 = (
    "<server><id>$rs</id>"
    "<address><auth-port>$aport</auth-port><acct-port>$cport</acct-port></address>"
    "</server>"
)
RADIUS_SERVER_ADDRESS_PORTS_REMOVE_1715 = (
    '<server><id>$rs</id><address nc:operation="remove"/></server>'
)

RADIUS_SERVER_TIMEOUT_1715 = (
    "<server><id>$rs</id><timeout>$secs</timeout></server>"
)
RADIUS_SERVER_TIMEOUT_REMOVE_1715 = (
    '<server><id>$rs</id><timeout nc:operation="remove"/></server>'
)

RADIUS_SERVER_TLS_PORT_1715 = (
    "<server><id>$rs</id><tls><port>$port</port></tls></server>"
)
RADIUS_SERVER_TLS_PORT_REMOVE_1715 = (
    '<server><id>$rs</id><tls><port nc:operation="remove"/></tls></server>'
)

RADIUS_SERVER_TLS_TRUSTPOINT_CLIENT_1715 = (
    "<server><id>$rs</id><tls><trustpoint><client>$tp</client></trustpoint></tls></server>"
)
RADIUS_SERVER_TLS_TRUSTPOINT_CLIENT_REMOVE_1715 = (
    '<server><id>$rs</id><tls><trustpoint><client nc:operation="remove"/></trustpoint></tls></server>'
)

RADIUS_SERVER_TLS_TRUSTPOINT_SERVER_1715 = (
    "<server><id>$rs</id><tls><trustpoint><server>$tp</server></trustpoint></tls></server>"
)
RADIUS_SERVER_TLS_TRUSTPOINT_SERVER_REMOVE_1715 = (
    '<server><id>$rs</id><tls><trustpoint><server nc:operation="remove"/></trustpoint></tls></server>'
)

RADIUS_SERVER_TLS_MATCH_SERVER_IDENTITY_HOSTNAME_1715 = (
    "<server><id>$rs</id><tls>"
    "<match-server-identity><hostname>$host</hostname></match-server-identity>"
    "</tls></server>"
)
RADIUS_SERVER_TLS_MATCH_SERVER_IDENTITY_HOSTNAME_REMOVE_1715 = (
    '<server><id>$rs</id><tls><match-server-identity nc:operation="remove"/></tls></server>'
)

RADIUS_SERVER_AUTOMATE_TESTER_1715 = (
    "<server><id>$rs</id>"
    "<automate-tester><username>$tuser</username>$opt_extra</automate-tester>"
    "</server>"
)
RADIUS_SERVER_AUTOMATE_TESTER_REMOVE_1715 = (
    '<server><id>$rs</id><automate-tester nc:operation="remove"/></server>'
)

RADIUS_SERVER_AUTOMATE_TESTER_PROBE_ON_CONFIG_1715 = (
    "<server><id>$rs</id>"
    "<automate-tester><username>$tuser</username><probe-on-config/></automate-tester>"
    "</server>"
)
RADIUS_SERVER_AUTOMATE_TESTER_PROBE_ON_CONFIG_REMOVE_1715 = (
    '<server><id>$rs</id><automate-tester><probe-on-config nc:operation="remove"/></automate-tester></server>'
)

RADIUS_SERVER_AUTOMATE_TESTER_IDLE_TIME_1715 = (
    "<server><id>$rs</id>"
    "<automate-tester><username>$tuser</username><idle-time-config>$minutes</idle-time-config></automate-tester>"
    "</server>"
)
RADIUS_SERVER_AUTOMATE_TESTER_IDLE_TIME_REMOVE_1715 = (
    '<server><id>$rs</id><automate-tester><idle-time-config nc:operation="remove"/></automate-tester></server>'
)

RADIUS_SERVER_AUTOMATE_TESTER_IGNORE_AUTH_PORT_1715 = (
    "<server><id>$rs</id>"
    "<automate-tester><username>$tuser</username><ignore-auth-port/></automate-tester>"
    "</server>"
)
RADIUS_SERVER_AUTOMATE_TESTER_IGNORE_AUTH_PORT_REMOVE_1715 = (
    '<server><id>$rs</id><automate-tester><ignore-auth-port nc:operation="remove"/></automate-tester></server>'
)

RADIUS_SERVER_AUTOMATE_TESTER_IGNORE_ACCT_PORT_1715 = (
    "<server><id>$rs</id>"
    "<automate-tester><username>$tuser</username><ignore-acct-port/></automate-tester>"
    "</server>"
)
RADIUS_SERVER_AUTOMATE_TESTER_IGNORE_ACCT_PORT_REMOVE_1715 = (
    '<server><id>$rs</id><automate-tester><ignore-acct-port nc:operation="remove"/></automate-tester></server>'
)

RADIUS_SERVER_AUTOMATE_TESTER_VRF_1715 = (
    "<server><id>$rs</id>"
    "<automate-tester><username>$tuser</username><vrf>$vrf</vrf></automate-tester>"
    "</server>"
)
RADIUS_SERVER_AUTOMATE_TESTER_VRF_REMOVE_1715 = (
    '<server><id>$rs</id><automate-tester><vrf nc:operation="remove"/></automate-tester></server>'
)

RADIUS_SERVER_BACKOFF_EXPONENTIAL_1715 = (
    "<server><id>$rs</id>"
    "<backoff><exponential>"
      "<max-delay>$delay</max-delay><backoff-retry>$retry</backoff-retry>"
    "</exponential></backoff>"
    "</server>"
)
RADIUS_SERVER_BACKOFF_EXPONENTIAL_REMOVE_1715 = (
    '<server><id>$rs</id><backoff nc:operation="remove"/></server>'
)

RADIUS_SERVER_PAC_KEY_1715 = (
    "<server><id>$rs</id>"
    "<pac><key><encryption>$enc</encryption><key>$key</key></key></pac>"
    "</server>"
)
RADIUS_SERVER_PAC_KEY_REMOVE_1715 = (
    '<server><id>$rs</id><pac nc:operation="remove"/></server>'
)

RADIUS_SERVER_KEY_1715 = (
    "<server><id>$rs</id>"
    "<key><encryption>$enc</encryption><key>$key</key></key>"
    "</server>"
)
RADIUS_SERVER_KEY_REMOVE_1715 = (
    '<server><id>$rs</id><key nc:operation="remove"/></server>'
)

RADIUS_SERVER_RETRANSMIT_1715 = (
    "<server><id>$rs</id><retransmit>$retries</retransmit></server>"
)
RADIUS_SERVER_RETRANSMIT_REMOVE_1715 = (
    '<server><id>$rs</id><retransmit nc:operation="remove"/></server>'
)

RADIUS_SERVER_DSCP_1715 = (
    "<server><id>$rs</id><dscp><auth>$auth</auth><acct>$acct</acct></dscp></server>"
)
RADIUS_SERVER_DSCP_REMOVE_1715 = (
    '<server><id>$rs</id><dscp nc:operation="remove"/></server>'
)


# ============================================================
# 13. native/ldap  (anchor: ldap)  — ldap server[id]
# ============================================================
LDAP_SERVER_CREATE_1715 = (
    "<server><id>$ls</id></server>"
)
LDAP_SERVER_CREATE_REMOVE_1715 = (
    '<server nc:operation="remove"><id>$ls</id></server>'
)

LDAP_SERVER_IPV4_1715 = (
    "<server><id>$ls</id><ipv4>$addr</ipv4></server>"
)
LDAP_SERVER_IPV4_REMOVE_1715 = (
    '<server><id>$ls</id><ipv4 nc:operation="remove"/></server>'
)

LDAP_SERVER_IPV6_1715 = (
    "<server><id>$ls</id><ipv6>$addr</ipv6></server>"
)
LDAP_SERVER_IPV6_REMOVE_1715 = (
    '<server><id>$ls</id><ipv6 nc:operation="remove"/></server>'
)

LDAP_SERVER_FQDN_1715 = (
    "<server><id>$ls</id><fqdn>$addr</fqdn></server>"
)
LDAP_SERVER_FQDN_REMOVE_1715 = (
    '<server><id>$ls</id><fqdn nc:operation="remove"/></server>'
)

LDAP_SERVER_AUTHENTICATION_BIND_FIRST_1715 = (
    "<server><id>$ls</id><authentication><bind-first/></authentication></server>"
)
LDAP_SERVER_AUTHENTICATION_BIND_FIRST_REMOVE_1715 = (
    '<server><id>$ls</id><authentication nc:operation="remove"/></server>'
)

LDAP_SERVER_AUTHENTICATION_BIND_FIRST_NO_AUTHZ_1715 = (
    "<server><id>$ls</id><authentication>"
    "<bind-first><no-authorization/></bind-first>"
    "</authentication></server>"
)
LDAP_SERVER_AUTHENTICATION_BIND_FIRST_NO_AUTHZ_REMOVE_1715 = (
    '<server><id>$ls</id><authentication><bind-first><no-authorization nc:operation="remove"/></bind-first></authentication></server>'
)

LDAP_SERVER_AUTHENTICATION_COMPARE_1715 = (
    "<server><id>$ls</id><authentication><compare/></authentication></server>"
)
LDAP_SERVER_AUTHENTICATION_COMPARE_REMOVE_1715 = (
    '<server><id>$ls</id><authentication><compare nc:operation="remove"/></authentication></server>'
)

LDAP_SERVER_AUTOMATE_TESTER_1715 = (
    "<server><id>$ls</id>"
    "<automate-tester><username>$tuser</username><probe-on/></automate-tester>"
    "</server>"
)
LDAP_SERVER_AUTOMATE_TESTER_REMOVE_1715 = (
    '<server><id>$ls</id><automate-tester nc:operation="remove"/></server>'
)

LDAP_SERVER_BASE_DN_1715 = (
    "<server><id>$ls</id><base-dn>$dn</base-dn></server>"
)
LDAP_SERVER_BASE_DN_REMOVE_1715 = (
    '<server><id>$ls</id><base-dn nc:operation="remove"/></server>'
)

LDAP_SERVER_DEADTIME_1715 = (
    "<server><id>$ls</id><deadtime>$minutes</deadtime></server>"
)
LDAP_SERVER_DEADTIME_REMOVE_1715 = (
    '<server><id>$ls</id><deadtime nc:operation="remove"/></server>'
)

LDAP_SERVER_TIMEOUT_RETRANSMIT_1715 = (
    "<server><id>$ls</id><timeout><retransmit>$secs</retransmit></timeout></server>"
)
LDAP_SERVER_TIMEOUT_RETRANSMIT_REMOVE_1715 = (
    '<server><id>$ls</id><timeout nc:operation="remove"/></server>'
)

LDAP_SERVER_BIND_AUTHENTICATE_1715 = (
    "<server><id>$ls</id><bind><authenticate/></bind></server>"
)
LDAP_SERVER_BIND_AUTHENTICATE_REMOVE_1715 = (
    '<server><id>$ls</id><bind nc:operation="remove"/></server>'
)

LDAP_SERVER_BIND_ROOT_DN_1715 = (
    "<server><id>$ls</id><bind><root-dn/></bind></server>"
)
LDAP_SERVER_BIND_ROOT_DN_REMOVE_1715 = (
    '<server><id>$ls</id><bind><root-dn nc:operation="remove"/></bind></server>'
)

LDAP_SERVER_BIND_USERNAME_1715 = (
    "<server><id>$ls</id><bind><username>$buser</username></bind></server>"
)
LDAP_SERVER_BIND_USERNAME_REMOVE_1715 = (
    '<server><id>$ls</id><bind><username nc:operation="remove"/></bind></server>'
)

LDAP_SERVER_BIND_PASSWORD_1715 = (
    "<server><id>$ls</id><bind>"
    "<password/><pass-type>$ptype</pass-type><pass-str>$pass</pass-str>"
    "</bind></server>"
)
LDAP_SERVER_BIND_PASSWORD_REMOVE_1715 = (
    '<server><id>$ls</id><bind><password nc:operation="remove"/></bind></server>'
)

LDAP_SERVER_MODE_SECURE_1715 = (
    "<server><id>$ls</id><mode><secure/></mode></server>"
)
LDAP_SERVER_MODE_SECURE_REMOVE_1715 = (
    '<server><id>$ls</id><mode nc:operation="remove"/></server>'
)

LDAP_SERVER_MODE_SECURE_NO_NEGOTIATION_1715 = (
    "<server><id>$ls</id><mode><secure><no-negotiation/></secure></mode></server>"
)
LDAP_SERVER_MODE_SECURE_NO_NEGOTIATION_REMOVE_1715 = (
    '<server><id>$ls</id><mode><secure><no-negotiation nc:operation="remove"/></secure></mode></server>'
)

LDAP_SERVER_SEARCH_TYPE_NESTED_1715 = (
    "<server><id>$ls</id><search-type><nested/></search-type></server>"
)
LDAP_SERVER_SEARCH_TYPE_NESTED_REMOVE_1715 = (
    '<server><id>$ls</id><search-type nc:operation="remove"/></server>'
)

LDAP_SERVER_SEARCH_FILTER_USER_OBJECT_TYPE_1715 = (
    "<server><id>$ls</id>"
    "<search-filter><user-object-type><name>$oc</name></user-object-type></search-filter>"
    "</server>"
)
LDAP_SERVER_SEARCH_FILTER_USER_OBJECT_TYPE_REMOVE_1715 = (
    '<server><id>$ls</id><search-filter nc:operation="remove"/></server>'
)

LDAP_SERVER_SECURE_CIPHER_1715 = (
    "<server><id>$ls</id><secure><cipher><$cipher/></cipher></secure></server>"
)
LDAP_SERVER_SECURE_CIPHER_REMOVE_1715 = (
    '<server><id>$ls</id><secure><cipher nc:operation="remove"/></secure></server>'
)

LDAP_SERVER_SECURE_TRUSTPOINT_1715 = (
    "<server><id>$ls</id><secure><trustpoint>$tp</trustpoint></secure></server>"
)
LDAP_SERVER_SECURE_TRUSTPOINT_REMOVE_1715 = (
    '<server><id>$ls</id><secure><trustpoint nc:operation="remove"/></secure></server>'
)

LDAP_SERVER_TRANSPORT_PORT_1715 = (
    "<server><id>$ls</id><transport><port>$port</port></transport></server>"
)
LDAP_SERVER_TRANSPORT_PORT_REMOVE_1715 = (
    '<server><id>$ls</id><transport><port nc:operation="remove"/></transport></server>'
)


# ============================================================
# 14. native/radius-server  (anchor: radius-server)
# ============================================================
RS_ATTRIBUTE_4_1715 = (
    "<attribute><number>4</number><attri4>$ip</attri4></attribute>"
)
RS_ATTRIBUTE_4_REMOVE_1715 = (
    '<attribute nc:operation="remove"><number>4</number></attribute>'
)

RS_ATTRIBUTE_SEND_1715 = (
    "<attribute><number>$num</number><send-attribute>$sattr</send-attribute></attribute>"
)
RS_ATTRIBUTE_SEND_REMOVE_1715 = (
    '<attribute nc:operation="remove"><number>$num</number></attribute>'
)

RS_ATTRIBUTE_25_ACCESS_REQUEST_INCLUDE_1715 = (
    "<attribute><number>25</number><access-request><include/></access-request></attribute>"
)
RS_ATTRIBUTE_25_ACCESS_REQUEST_INCLUDE_REMOVE_1715 = (
    '<attribute nc:operation="remove"><number>25</number></attribute>'
)

RS_ATTRIBUTE_31_MAC_1715 = (
    "<attribute><number>31</number><attri31><attri31-list>"
    "<calling-station-id>mac</calling-station-id>"
    "<id-mac><format>ietf</format><lu-case>$case</lu-case></id-mac>"
    "</attri31-list></attri31></attribute>"
)
RS_ATTRIBUTE_31_MAC_REMOVE_1715 = (
    '<attribute nc:operation="remove"><number>31</number></attribute>'
)

RS_ATTRIBUTE_31_SEND_1715 = (
    "<attribute><number>31</number><attri31><attri31-list>"
    "<calling-station-id>send</calling-station-id>"
    "<id-send><nas-port-detail/><mac-only/></id-send>"
    "</attri31-list></attri31></attribute>"
)
RS_ATTRIBUTE_31_SEND_REMOVE_1715 = (
    '<attribute nc:operation="remove"><number>31</number></attribute>'
)

RS_ATTRIBUTE_11_DEFAULT_DIRECTION_1715 = (
    "<attribute><number>11</number><attri11><attri11-list>"
    "<filter-id-defaults>default</filter-id-defaults>"
    "<default><direction>$dir</direction></default>"
    "</attri11-list></attri11></attribute>"
)
RS_ATTRIBUTE_11_DEFAULT_DIRECTION_REMOVE_1715 = (
    '<attribute nc:operation="remove"><number>11</number></attribute>'
)

RS_ATTRIBUTE_11_OPTIONAL_1715 = (
    "<attribute><number>11</number><attri11><attri11-list>"
    "<filter-id-defaults>optional</filter-id-defaults>"
    "</attri11-list></attri11></attribute>"
)
RS_ATTRIBUTE_11_OPTIONAL_REMOVE_1715 = (
    '<attribute nc:operation="remove"><number>11</number></attribute>'
)

RS_WIRELESS_ACCOUNTING_NAS_PORT_ID_EXCLUDE_1715 = (
    "<attribute><number>wireless</number><wireless><accounting>"
    "<nas-port-id><exclude/></nas-port-id>"
    "</accounting></wireless></attribute>"
)
RS_WIRELESS_ACCOUNTING_NAS_PORT_ID_EXCLUDE_REMOVE_1715 = (
    '<attribute nc:operation="remove"><number>wireless</number></attribute>'
)

RS_WIRELESS_ACCOUNTING_USERNAME_CASE_1715 = (
    "<attribute><number>wireless</number><wireless><accounting>"
    "<username-case>$case</username-case>"
    "</accounting></wireless></attribute>"
)
RS_WIRELESS_ACCOUNTING_USERNAME_CASE_REMOVE_1715 = (
    '<attribute nc:operation="remove"><number>wireless</number></attribute>'
)

RS_WIRELESS_ACCOUNTING_USERNAME_DELIMITER_1715 = (
    "<attribute><number>wireless</number><wireless><accounting>"
    "<username-delimiter>$delim</username-delimiter>"
    "</accounting></wireless></attribute>"
)

RS_WIRELESS_ACCOUNTING_USERNAME_DELIMITER_REMOVE_1715 = (
    '<attribute nc:operation="remove"><number>wireless</number></attribute>'
)

RS_WIRELESS_ACCOUNTING_CALL_STATION_ID_1715 = (
    "<attribute><number>wireless</number><wireless><accounting>"
    "<call-station-id>$csid</call-station-id>"
    "</accounting></wireless></attribute>"
)
RS_WIRELESS_ACCOUNTING_CALL_STATION_ID_REMOVE_1715 = (
    '<attribute nc:operation="remove"><number>wireless</number></attribute>'
)

RS_WIRELESS_ACCOUNTING_CALL_STATION_ID_CASE_1715 = (
    "<attribute><number>wireless</number><wireless><accounting>"
    "<callStationIdCase>$case</callStationIdCase>"
    "</accounting></wireless></attribute>"
)
RS_WIRELESS_ACCOUNTING_CALL_STATION_ID_CASE_REMOVE_1715 = (
    '<attribute nc:operation="remove"><number>wireless</number></attribute>'
)

RS_WIRELESS_ACCOUNTING_MAC_DELIMITER_1715 = (
    "<attribute><number>wireless</number><wireless><accounting>"
    "<mac-delimiter>$delim</mac-delimiter>"
    "</accounting></wireless></attribute>"
)
RS_WIRELESS_ACCOUNTING_MAC_DELIMITER_REMOVE_1715 = (
    '<attribute nc:operation="remove"><number>wireless</number></attribute>'
)

RS_WIRELESS_AUTHENTICATION_CALL_STATION_ID_1715 = (
    "<attribute><number>wireless</number><wireless><authentication>"
    "<call-station-id>$csid</call-station-id>"
    "</authentication></wireless></attribute>"
)
RS_WIRELESS_AUTHENTICATION_CALL_STATION_ID_REMOVE_1715 = (
    '<attribute nc:operation="remove"><number>wireless</number></attribute>'
)

RS_WIRELESS_AUTHENTICATION_CALL_STATION_ID_CASE_1715 = (
    "<attribute><number>wireless</number><wireless><authentication>"
    "<callStationIdCase>$case</callStationIdCase>"
    "</authentication></wireless></attribute>"
)
RS_WIRELESS_AUTHENTICATION_CALL_STATION_ID_CASE_REMOVE_1715 = (
    '<attribute nc:operation="remove"><number>wireless</number></attribute>'
)

RS_WIRELESS_AUTHENTICATION_MAC_DELIMITER_1715 = (
    "<attribute><number>wireless</number><wireless><authentication>"
    "<mac-delimiter>$delim</mac-delimiter>"
    "</authentication></wireless></attribute>"
)
RS_WIRELESS_AUTHENTICATION_MAC_DELIMITER_REMOVE_1715 = (
    '<attribute nc:operation="remove"><number>wireless</number></attribute>'
)

RS_WIRELESS_ATTR44_1715 = (
    "<attribute><number>wireless</number><wireless>"
    "<attr44><attr44val>44</attr44val>$opt_extra</attr44>"
    "</wireless></attribute>"
)
RS_WIRELESS_ATTR44_REMOVE_1715 = (
    '<attribute nc:operation="remove"><number>wireless</number></attribute>'
)

RS_WIRELESS_ATTR44_INCLUDE_IN_ACCESS_REQ_1715 = (
    "<attribute><number>wireless</number><wireless>"
    "<attr44><include-in-access-req/></attr44>"
    "</wireless></attribute>"
)
RS_WIRELESS_ATTR44_INCLUDE_IN_ACCESS_REQ_REMOVE_1715 = (
    '<attribute nc:operation="remove"><number>wireless</number></attribute>'
)

RS_WIRELESS_ATTR44_EXTEND_WITH_MAC_1715 = (
    "<attribute><number>wireless</number><wireless>"
    "<attr44><extend-with-mac-addr/></attr44>"
    "</wireless></attribute>"
)
RS_WIRELESS_ATTR44_EXTEND_WITH_MAC_REMOVE_1715 = (
    '<attribute nc:operation="remove"><number>wireless</number></attribute>'
)

RS_WIRELESS_LOCATION_DELIVERY_OUT_OF_BAND_1715 = (
    "<attribute><number>wireless</number><wireless>"
    "<location><delivery><out-of-band/></delivery></location>"
    "</wireless></attribute>"
)
RS_WIRELESS_LOCATION_DELIVERY_OUT_OF_BAND_REMOVE_1715 = (
    '<attribute nc:operation="remove"><number>wireless</number></attribute>'
)

RS_WIRELESS_LOCATION_DELIVERY_INCLUDE_LOCATION_CAPABLE_1715 = (
    "<attribute><number>wireless</number><wireless>"
    "<location><delivery><include-location-capable/></delivery></location>"
    "</wireless></attribute>"
)
RS_WIRELESS_LOCATION_DELIVERY_INCLUDE_LOCATION_CAPABLE_REMOVE_1715 = (
    '<attribute nc:operation="remove"><number>wireless</number></attribute>'
)

RS_WIRELESS_LOCATION_CIVIC_LOCATION_ID_1715 = (
    "<attribute><number>wireless</number><wireless>"
    "<location><civic-location-id>$id</civic-location-id></location>"
    "</wireless></attribute>"
)
RS_WIRELESS_LOCATION_CIVIC_LOCATION_ID_REMOVE_1715 = (
    '<attribute nc:operation="remove"><number>wireless</number></attribute>'
)

RS_WIRELESS_LOCATION_GEO_LOCATION_ID_1715 = (
    "<attribute><number>wireless</number><wireless>"
    "<location><geo-location-id>$id</geo-location-id></location>"
    "</wireless></attribute>"
)
RS_WIRELESS_LOCATION_GEO_LOCATION_ID_REMOVE_1715 = (
    '<attribute nc:operation="remove"><number>wireless</number></attribute>'
)

RS_WIRELESS_LOCATION_OPERATOR_ID_1715 = (
    "<attribute><number>wireless</number><wireless>"
    "<location><operator-id>$id</operator-id></location>"
    "</wireless></attribute>"
)
RS_WIRELESS_LOCATION_OPERATOR_ID_REMOVE_1715 = (
    '<attribute nc:operation="remove"><number>wireless</number></attribute>'
)

RS_CACHE_AUTHENTICATION_PROFILE_1715 = (
    "<cache><authentication><profile>$profile</profile></authentication></cache>"
)
RS_CACHE_AUTHENTICATION_PROFILE_REMOVE_1715 = (
    '<cache><authentication><profile nc:operation="remove"/></authentication></cache>'
)

RS_CACHE_AUTHORIZATION_PROFILE_1715 = (
    "<cache><authorization><profile>$profile</profile></authorization></cache>"
)
RS_CACHE_AUTHORIZATION_PROFILE_REMOVE_1715 = (
    '<cache><authorization><profile nc:operation="remove"/></authorization></cache>'
)

RS_CACHE_EXPIRY_1715 = (
    "<cache><expiry-time><expiry>$hours</expiry></expiry-time></cache>"
)
RS_CACHE_EXPIRY_REMOVE_1715 = (
    '<cache><expiry-time nc:operation="remove"/></cache>'
)

RS_CACHE_EXPIRY_OPTIONS_1715 = (
    "<cache><expiry-time><options-value>"
    "<rules-value>$rule</rules-value><time-value>$unit</time-value>"
    "</options-value></expiry-time></cache>"
)
RS_CACHE_EXPIRY_OPTIONS_REMOVE_1715 = (
    '<cache><expiry-time><options-value nc:operation="remove"/></expiry-time></cache>'
)

RS_DEAD_CRITERIA_1715 = (
    "<dead-criteria><time>$secs</time><tries>$tries</tries></dead-criteria>"
)
RS_DEAD_CRITERIA_REMOVE_1715 = (
    '<dead-criteria nc:operation="remove"/>'
)

RS_DEADTIME_1715 = (
    "<deadtime>$minutes</deadtime>"
)
RS_DEADTIME_REMOVE_1715 = (
    '<deadtime nc:operation="remove"/>'
)

RS_DIRECTED_REQUEST_1715 = (
    "<directed-request-value><directed-request/></directed-request-value>"
)
RS_DIRECTED_REQUEST_REMOVE_1715 = (
    '<directed-request-value nc:operation="remove"/>'
)

RS_HOST_CREATE_1715 = (
    "<host><id>$host</id></host>"
)
RS_HOST_CREATE_REMOVE_1715 = (
    '<host nc:operation="remove"><id>$host</id></host>'
)

RS_HOST_PORTS_1715 = (
    "<host><id>$host</id>"
    "<auth-port>$aport</auth-port><acct-port>$cport</acct-port>"
    "</host>"
)
RS_HOST_PORTS_REMOVE_1715 = (
    '<host><id>$host</id><auth-port nc:operation="remove"/><acct-port nc:operation="remove"/></host>'
)

RS_HOST_RETRANSMIT_1715 = (
    "<host><id>$host</id><retransmit>$retries</retransmit></host>"
)
RS_HOST_RETRANSMIT_REMOVE_1715 = (
    '<host><id>$host</id><retransmit nc:operation="remove"/></host>'
)

RS_HOST_TIMEOUT_1715 = (
    "<host><id>$host</id><timeout>$secs</timeout></host>"
)
RS_HOST_TIMEOUT_REMOVE_1715 = (
    '<host><id>$host</id><timeout nc:operation="remove"/></host>'
)

RS_HOST_KEY_1715 = (
    "<host><id>$host</id><key>$ktype</key><clear-key>$key</clear-key></host>"
)
RS_HOST_KEY_REMOVE_1715 = (
    '<host><id>$host</id><key nc:operation="remove"/><clear-key nc:operation="remove"/></host>'
)

RS_HOST_TEST_USERNAME_1715 = (
    "<host><id>$host</id>"
    "<test><username><name>$tuser</name></username></test>"
    "</host>"
)
RS_HOST_TEST_USERNAME_REMOVE_1715 = (
    '<host><id>$host</id><test nc:operation="remove"/></host>'
)

RS_HOST_TEST_USERNAME_KEY_1715 = (
    "<host><id>$host</id>"
    "<test><username><name>$tuser</name>"
    "<key><encryption>$enc</encryption><clear-key>$key</clear-key></key>"
    "</username></test>"
    "</host>"
)
RS_HOST_TEST_USERNAME_KEY_REMOVE_1715 = (
    '<host><id>$host</id><test><username><key nc:operation="remove"/></username></test></host>'
)

RS_KEY_1715 = (
    "<key><encryption>$enc</encryption><clear-key>$key</clear-key></key>"
)
RS_KEY_REMOVE_1715 = (
    '<key nc:operation="remove"/>'
)

RS_LOAD_BALANCE_LEAST_OUTSTANDING_1715 = (
    "<load-balance><method><least-outstanding/></method></load-balance>"
)
RS_LOAD_BALANCE_LEAST_OUTSTANDING_REMOVE_1715 = (
    '<load-balance nc:operation="remove"/>'
)

RS_LOAD_BALANCE_BATCH_SIZE_1715 = (
    "<load-balance><method><least-outstanding><batch-size>$size</batch-size></least-outstanding></method></load-balance>"
)
RS_LOAD_BALANCE_BATCH_SIZE_REMOVE_1715 = (
    '<load-balance><method><least-outstanding><batch-size nc:operation="remove"/></least-outstanding></method></load-balance>'
)

RS_LOAD_BALANCE_IGNORE_PREFERRED_SERVER_1715 = (
    "<load-balance><method><least-outstanding><ignore-preferred-server/></least-outstanding></method></load-balance>"
)
RS_LOAD_BALANCE_IGNORE_PREFERRED_SERVER_REMOVE_1715 = (
    '<load-balance><method><least-outstanding><ignore-preferred-server nc:operation="remove"/></least-outstanding></method></load-balance>'
)

RS_RETRANSMIT_1715 = (
    "<retransmit>$retries</retransmit>"
)
RS_RETRANSMIT_REMOVE_1715 = (
    '<retransmit nc:operation="remove"/>'
)

RS_SOURCE_PORTS_EXTENDED_1715 = (
    "<source-ports><extended/></source-ports>"
)
RS_SOURCE_PORTS_EXTENDED_REMOVE_1715 = (
    '<source-ports nc:operation="remove"/>'
)

RS_TIMEOUT_1715 = (
    "<timeout>$secs</timeout>"
)
RS_TIMEOUT_REMOVE_1715 = (
    '<timeout nc:operation="remove"/>'
)

RS_VSA_DISALLOW_UNKNOWN_1715 = (
    "<vsa><disallow><unknown/></disallow></vsa>"
)
RS_VSA_DISALLOW_UNKNOWN_REMOVE_1715 = (
    '<vsa><disallow nc:operation="remove"/></vsa>'
)

RS_VSA_SEND_1715 = (
    "<vsa><send/></vsa>"
)
RS_VSA_SEND_REMOVE_1715 = (
    '<vsa><send nc:operation="remove"/></vsa>'
)

RS_VSA_SEND_ACCOUNTING_ONLY_1715 = (
    "<vsa><send><accounting-only>$flag</accounting-only></send></vsa>"
)
RS_VSA_SEND_ACCOUNTING_ONLY_REMOVE_1715 = (
    '<vsa><send><accounting-only nc:operation="remove"/></send></vsa>'
)

RS_VSA_SEND_AUTHENTICATION_ONLY_1715 = (
    "<vsa><send><authentication-only>$flag</authentication-only></send></vsa>"
)
RS_VSA_SEND_AUTHENTICATION_ONLY_REMOVE_1715 = (
    '<vsa><send><authentication-only nc:operation="remove"/></send></vsa>'
)

RS_VSA_SEND_ACCOUNTING_THREEGPP2_1715 = (
    "<vsa><send><accounting-settings><threegpp2/></accounting-settings></send></vsa>"
)
RS_VSA_SEND_ACCOUNTING_THREEGPP2_REMOVE_1715 = (
    '<vsa><send><accounting-settings nc:operation="remove"/></send></vsa>'
)

RS_VSA_SEND_AUTHENTICATION_THREEGPP2_1715 = (
    "<vsa><send><authentication-settings><threegpp2/></authentication-settings></send></vsa>"
)
RS_VSA_SEND_AUTHENTICATION_THREEGPP2_REMOVE_1715 = (
    '<vsa><send><authentication-settings nc:operation="remove"/></send></vsa>'
)

RS_VSA_SEND_CISCO_NAS_PORT_1715 = (
    "<vsa><send><cisco-nas-port/></send></vsa>"
)
RS_VSA_SEND_CISCO_NAS_PORT_REMOVE_1715 = (
    '<vsa><send><cisco-nas-port nc:operation="remove"/></send></vsa>'
)

RS_VSA_SEND_CISCO_NAS_PORT_THREEGPP2_1715 = (
    "<vsa><send><cisco-nas-port><threegpp2/></cisco-nas-port></send></vsa>"
)
RS_VSA_SEND_CISCO_NAS_PORT_THREEGPP2_REMOVE_1715 = (
    '<vsa><send><cisco-nas-port><threegpp2 nc:operation="remove"/></cisco-nas-port></send></vsa>'
)

RS_DSCP_1715 = (
    "<dscp><auth>$auth</auth><acct>$acct</acct></dscp>"
)
RS_DSCP_REMOVE_1715 = (
    '<dscp nc:operation="remove"/>'
)


# ============================================================
# 15. source-interface under ip / ipv6  (anchors: ip, ipv6)
# ============================================================
IP_RADIUS_SOURCE_INTERFACE_1715 = (
    "<radius><source-interface>$src_if_xml$opt_extra</source-interface></radius>"
)
IP_RADIUS_SOURCE_INTERFACE_REMOVE_1715 = (
    '<radius><source-interface nc:operation="remove"/></radius>'
)

IP_RADIUS_SOURCE_INTERFACE_VRF_1715 = (
    "<radius><source-interface>$src_if_xml<vrf>$vrf</vrf></source-interface></radius>"
)
IP_RADIUS_SOURCE_INTERFACE_VRF_REMOVE_1715 = (
    '<radius><source-interface><vrf nc:operation="remove"/></source-interface></radius>'
)

IPV6_RADIUS_SOURCE_INTERFACE_1715 = (
    "<radius><source-interface>$src_if_xml$opt_extra</source-interface></radius>"
)
IPV6_RADIUS_SOURCE_INTERFACE_REMOVE_1715 = (
    '<radius><source-interface nc:operation="remove"/></radius>'
)

IPV6_RADIUS_SOURCE_INTERFACE_VRF_1715 = (
    "<radius><source-interface>$src_if_xml<vrf>$vrf</vrf></source-interface></radius>"
)
IPV6_RADIUS_SOURCE_INTERFACE_VRF_REMOVE_1715 = (
    '<radius><source-interface><vrf nc:operation="remove"/></source-interface></radius>'
)

IP_TACACS_SOURCE_INTERFACE_1715 = (
    "<tacacs><source-interface>$src_if_xml$opt_extra</source-interface></tacacs>"
)
IP_TACACS_SOURCE_INTERFACE_REMOVE_1715 = (
    '<tacacs><source-interface nc:operation="remove"/></tacacs>'
)

IP_TACACS_SOURCE_INTERFACE_VRF_1715 = (
    "<tacacs><source-interface>$src_if_xml<vrf>$vrf</vrf></source-interface></tacacs>"
)
IP_TACACS_SOURCE_INTERFACE_VRF_REMOVE_1715 = (
    '<tacacs><source-interface><vrf nc:operation="remove"/></source-interface></tacacs>'
)

IPV6_TACACS_SOURCE_INTERFACE_1715 = (
    "<tacacs><source-interface>$src_if_xml$opt_extra</source-interface></tacacs>"
)
IPV6_TACACS_SOURCE_INTERFACE_REMOVE_1715 = (
    '<tacacs><source-interface nc:operation="remove"/></tacacs>'
)

IPV6_TACACS_SOURCE_INTERFACE_VRF_1715 = (
    "<tacacs><source-interface>$src_if_xml<vrf>$vrf</vrf></source-interface></tacacs>"
)
IPV6_TACACS_SOURCE_INTERFACE_VRF_REMOVE_1715 = (
    '<tacacs><source-interface><vrf nc:operation="remove"/></source-interface></tacacs>'
)


# ============================================================
# 16. native/tacacs  (anchor: tacacs)  — tacacs server[name]
# ============================================================
TACACS_SERVER_CREATE_1715 = (
    "<server><name>$ts</name></server>"
)
TACACS_SERVER_CREATE_REMOVE_1715 = (
    '<server nc:operation="remove"><name>$ts</name></server>'
)

TACACS_SERVER_ADDRESS_IPV4_1715 = (
    "<server><name>$ts</name><address><ipv4>$addr</ipv4></address></server>"
)
TACACS_SERVER_ADDRESS_IPV4_REMOVE_1715 = (
    '<server><name>$ts</name><address><ipv4 nc:operation="remove"/></address></server>'
)

TACACS_SERVER_ADDRESS_IPV6_1715 = (
    "<server><name>$ts</name><address><ipv6>$addr</ipv6></address></server>"
)
TACACS_SERVER_ADDRESS_IPV6_REMOVE_1715 = (
    '<server><name>$ts</name><address><ipv6 nc:operation="remove"/></address></server>'
)

TACACS_SERVER_ADDRESS_FQDN_1715 = (
    "<server><name>$ts</name><address><fqdn>$addr</fqdn></address></server>"
)
TACACS_SERVER_ADDRESS_FQDN_REMOVE_1715 = (
    '<server><name>$ts</name><address><fqdn nc:operation="remove"/></address></server>'
)

TACACS_SERVER_PORT_1715 = (
    "<server><name>$ts</name><port>$port</port></server>"
)
TACACS_SERVER_PORT_REMOVE_1715 = (
    '<server><name>$ts</name><port nc:operation="remove"/></server>'
)

TACACS_SERVER_TIMEOUT_1715 = (
    "<server><name>$ts</name><timeout>$secs</timeout></server>"
)
TACACS_SERVER_TIMEOUT_REMOVE_1715 = (
    '<server><name>$ts</name><timeout nc:operation="remove"/></server>'
)

TACACS_SERVER_KEY_1715 = (
    "<server><name>$ts</name>"
    "<key><encryption>$enc</encryption><key>$key</key></key>"
    "</server>"
)
TACACS_SERVER_KEY_REMOVE_1715 = (
    '<server><name>$ts</name><key nc:operation="remove"/></server>'
)


# ============================================================
# 17. native/tacacs-server  (anchor: tacacs-server)
# ============================================================
TS_TIMEOUT_1715 = (
    "<timeout>$secs</timeout>"
)
TS_TIMEOUT_REMOVE_1715 = (
    '<timeout nc:operation="remove"/>'
)

TS_DIRECTED_REQUEST_1715 = (
    "<directed-request/>"
)
TS_DIRECTED_REQUEST_REMOVE_1715 = (
    '<directed-request nc:operation="remove"/>'
)

TS_DIRECTED_REQUEST_RESTRICTED_1715 = (
    "<directed-request><restricted/></directed-request>"
)
TS_DIRECTED_REQUEST_RESTRICTED_REMOVE_1715 = (
    '<directed-request><restricted nc:operation="remove"/></directed-request>'
)

TS_DIRECTED_REQUEST_NO_TRUNCATE_1715 = (
    "<directed-request><no-truncate/></directed-request>"
)
TS_DIRECTED_REQUEST_NO_TRUNCATE_REMOVE_1715 = (
    '<directed-request><no-truncate nc:operation="remove"/></directed-request>'
)

TS_KEY_1715 = (
    "<key><encryption>$enc</encryption><key>$key</key></key>"
)
TS_KEY_REMOVE_1715 = (
    '<key nc:operation="remove"/>'
)

TS_ATTRIBUTE_ALLOW_UNKNOWN_1715 = (
    "<attribute><allow><unknown/></allow></attribute>"
)
TS_ATTRIBUTE_ALLOW_UNKNOWN_REMOVE_1715 = (
    '<attribute><allow nc:operation="remove"/></attribute>'
)


# ============================================================
# 18. username[name]  (anchor: username)
# ============================================================
USER_COMMON_CRITERIA_POLICY_1715 = (
    "<common-criteria-policy>"
    "<common-criteria-policy>$policy</common-criteria-policy>"
    "</common-criteria-policy>"
)
USER_COMMON_CRITERIA_POLICY_REMOVE_1715 = (
    '<common-criteria-policy nc:operation="remove"/>'
)

USER_COMMON_CRITERIA_PASSWORD_1715 = (
    "<common-criteria-policy>"
    "<common-criteria-policy>$policy</common-criteria-policy>"
    "<password><encryption>$enc</encryption><password>$pw</password></password>"
    "</common-criteria-policy>"
)
USER_COMMON_CRITERIA_PASSWORD_REMOVE_1715 = (
    '<common-criteria-policy><password nc:operation="remove"/></common-criteria-policy>'
)

USER_AAA_ATTRIBUTE_LIST_1715 = (
    "<aaa><attribute><list>$alist</list></attribute></aaa>"
)
USER_AAA_ATTRIBUTE_LIST_REMOVE_1715 = (
    '<aaa><attribute nc:operation="remove"/></aaa>'
)


# ============================================================
# 19. native/security  (anchor: native)
# ============================================================
SEC_AUTHENTICATION_FAILURE_RATE_1715 = (
    "<security><authentication><failure>"
    "<rate><threshold>$threshold</threshold><log/></rate>"
    "</failure></authentication></security>"
)
SEC_AUTHENTICATION_FAILURE_RATE_REMOVE_1715 = (
    '<security><authentication nc:operation="remove"/></security>'
)

SEC_PASSWORDS_MIN_LENGTH_1715 = (
    "<security><passwords><min-length>$n</min-length></passwords></security>"
)
SEC_PASSWORDS_MIN_LENGTH_REMOVE_1715 = (
    '<security><passwords nc:operation="remove"/></security>'
)

# ================================================================
# TEMPLATE REGISTRY  (base label -> {train: template})
# ================================================================
_TRAINS = ("1715",)

def _t(**kw):
    return {v: kw.get(v) for v in _TRAINS}


TEMPLATES = {
    # §1. aaa — general
    "AAA_NEW_MODEL":                                _t(**{"1715": AAA_NEW_MODEL_1715}),
    "AAA_NEW_MODEL_REMOVE":                         _t(**{"1715": AAA_NEW_MODEL_REMOVE_1715}),
    "AAA_SESSION_MIB_DISCONNECT":                   _t(**{"1715": AAA_SESSION_MIB_DISCONNECT_1715}),
    "AAA_SESSION_MIB_DISCONNECT_REMOVE":            _t(**{"1715": AAA_SESSION_MIB_DISCONNECT_REMOVE_1715}),
    "AAA_SESSION_MIB_POPULATE_SETUP":               _t(**{"1715": AAA_SESSION_MIB_POPULATE_SETUP_1715}),
    "AAA_SESSION_MIB_POPULATE_SETUP_REMOVE":        _t(**{"1715": AAA_SESSION_MIB_POPULATE_SETUP_REMOVE_1715}),
    "AAA_SESSION_MIB_POPULATE_START":               _t(**{"1715": AAA_SESSION_MIB_POPULATE_START_1715}),
    "AAA_SESSION_MIB_POPULATE_START_REMOVE":        _t(**{"1715": AAA_SESSION_MIB_POPULATE_START_REMOVE_1715}),
    "AAA_SESSION_ID":                               _t(**{"1715": AAA_SESSION_ID_1715}),
    "AAA_SESSION_ID_REMOVE":                        _t(**{"1715": AAA_SESSION_ID_REMOVE_1715}),
    "AAA_LOGIN_DISPLAY":                            _t(**{"1715": AAA_LOGIN_DISPLAY_1715}),
    "AAA_LOGIN_DISPLAY_REMOVE":                     _t(**{"1715": AAA_LOGIN_DISPLAY_REMOVE_1715}),
    "AAA_LOGIN_SUCCESS_TRACK_CONF_TIME":            _t(**{"1715": AAA_LOGIN_SUCCESS_TRACK_CONF_TIME_1715}),
    "AAA_LOGIN_SUCCESS_TRACK_CONF_TIME_REMOVE":     _t(**{"1715": AAA_LOGIN_SUCCESS_TRACK_CONF_TIME_REMOVE_1715}),
    "AAA_MAX_SESSIONS":                             _t(**{"1715": AAA_MAX_SESSIONS_1715}),
    "AAA_MAX_SESSIONS_REMOVE":                      _t(**{"1715": AAA_MAX_SESSIONS_REMOVE_1715}),
    "AAA_MEMORY_THRESHOLD_ACCOUNTING_DISABLE":      _t(**{"1715": AAA_MEMORY_THRESHOLD_ACCOUNTING_DISABLE_1715}),
    "AAA_MEMORY_THRESHOLD_ACCOUNTING_DISABLE_REMOVE": _t(**{"1715": AAA_MEMORY_THRESHOLD_ACCOUNTING_DISABLE_REMOVE_1715}),
    "AAA_MEMORY_THRESHOLD_AUTHENTICATION_REJECT":   _t(**{"1715": AAA_MEMORY_THRESHOLD_AUTHENTICATION_REJECT_1715}),
    "AAA_MEMORY_THRESHOLD_AUTHENTICATION_REJECT_REMOVE": _t(**{"1715": AAA_MEMORY_THRESHOLD_AUTHENTICATION_REJECT_REMOVE_1715}),
    "AAA_PASSWORD_RESTRICTION":                     _t(**{"1715": AAA_PASSWORD_RESTRICTION_1715}),
    "AAA_PASSWORD_RESTRICTION_REMOVE":              _t(**{"1715": AAA_PASSWORD_RESTRICTION_REMOVE_1715}),
    "AAA_POLICY_INTERFACE_CONFIG":                  _t(**{"1715": AAA_POLICY_INTERFACE_CONFIG_1715}),
    "AAA_POLICY_INTERFACE_CONFIG_REMOVE":           _t(**{"1715": AAA_POLICY_INTERFACE_CONFIG_REMOVE_1715}),
    "AAA_ROUTE_DOWNLOAD_UPDATE_PERIOD":             _t(**{"1715": AAA_ROUTE_DOWNLOAD_UPDATE_PERIOD_1715}),
    "AAA_ROUTE_DOWNLOAD_UPDATE_PERIOD_REMOVE":      _t(**{"1715": AAA_ROUTE_DOWNLOAD_UPDATE_PERIOD_REMOVE_1715}),
    "AAA_ROUTE_DOWNLOAD_AUTHORIZATION":             _t(**{"1715": AAA_ROUTE_DOWNLOAD_AUTHORIZATION_1715}),
    "AAA_ROUTE_DOWNLOAD_AUTHORIZATION_REMOVE":      _t(**{"1715": AAA_ROUTE_DOWNLOAD_AUTHORIZATION_REMOVE_1715}),
    "AAA_TRACEBACK_RECORDING":                      _t(**{"1715": AAA_TRACEBACK_RECORDING_1715}),
    "AAA_TRACEBACK_RECORDING_REMOVE":               _t(**{"1715": AAA_TRACEBACK_RECORDING_REMOVE_1715}),
    "AAA_REMOTE_USERNAME":                          _t(**{"1715": AAA_REMOTE_USERNAME_1715}),
    "AAA_REMOTE_USERNAME_REMOVE":                   _t(**{"1715": AAA_REMOTE_USERNAME_REMOVE_1715}),

    # §2. aaa cache profiles
    "AAA_CACHE_PROFILE_CREATE":                     _t(**{"1715": AAA_CACHE_PROFILE_CREATE_1715}),
    "AAA_CACHE_PROFILE_CREATE_REMOVE":              _t(**{"1715": AAA_CACHE_PROFILE_CREATE_REMOVE_1715}),
    "AAA_CACHE_PROFILE_ALL":                        _t(**{"1715": AAA_CACHE_PROFILE_ALL_1715}),
    "AAA_CACHE_PROFILE_ALL_REMOVE":                 _t(**{"1715": AAA_CACHE_PROFILE_ALL_REMOVE_1715}),
    "AAA_CACHE_PROFILE_ALL_NO_AUTH":                _t(**{"1715": AAA_CACHE_PROFILE_ALL_NO_AUTH_1715}),
    "AAA_CACHE_PROFILE_ALL_NO_AUTH_REMOVE":         _t(**{"1715": AAA_CACHE_PROFILE_ALL_NO_AUTH_REMOVE_1715}),
    "AAA_CACHE_PROFILE_REGEXP_ANY":                 _t(**{"1715": AAA_CACHE_PROFILE_REGEXP_ANY_1715}),
    "AAA_CACHE_PROFILE_REGEXP_ANY_REMOVE":          _t(**{"1715": AAA_CACHE_PROFILE_REGEXP_ANY_REMOVE_1715}),
    "AAA_CACHE_PROFILE_REGEXP_ONLY":                _t(**{"1715": AAA_CACHE_PROFILE_REGEXP_ONLY_1715}),
    "AAA_CACHE_PROFILE_REGEXP_ONLY_REMOVE":         _t(**{"1715": AAA_CACHE_PROFILE_REGEXP_ONLY_REMOVE_1715}),
    "AAA_CACHE_PROFILE_REGEXP_NO_AUTH":             _t(**{"1715": AAA_CACHE_PROFILE_REGEXP_NO_AUTH_1715}),
    "AAA_CACHE_PROFILE_REGEXP_NO_AUTH_REMOVE":      _t(**{"1715": AAA_CACHE_PROFILE_REGEXP_NO_AUTH_REMOVE_1715}),
    "AAA_CACHE_PROFILE_PROFILE":                    _t(**{"1715": AAA_CACHE_PROFILE_PROFILE_1715}),
    "AAA_CACHE_PROFILE_PROFILE_REMOVE":             _t(**{"1715": AAA_CACHE_PROFILE_PROFILE_REMOVE_1715}),
    "AAA_CACHE_PROFILE_PROFILE_NO_AUTH":            _t(**{"1715": AAA_CACHE_PROFILE_PROFILE_NO_AUTH_1715}),
    "AAA_CACHE_PROFILE_PROFILE_NO_AUTH_REMOVE":     _t(**{"1715": AAA_CACHE_PROFILE_PROFILE_NO_AUTH_REMOVE_1715}),
    "AAA_CACHE_PROFILE_DEFAULT_ALL":                _t(**{"1715": AAA_CACHE_PROFILE_DEFAULT_ALL_1715}),
    "AAA_CACHE_PROFILE_DEFAULT_ALL_REMOVE":         _t(**{"1715": AAA_CACHE_PROFILE_DEFAULT_ALL_REMOVE_1715}),
    "AAA_CACHE_PROFILE_DEFAULT_REGEXP_ANY":         _t(**{"1715": AAA_CACHE_PROFILE_DEFAULT_REGEXP_ANY_1715}),
    "AAA_CACHE_PROFILE_DEFAULT_REGEXP_ANY_REMOVE":  _t(**{"1715": AAA_CACHE_PROFILE_DEFAULT_REGEXP_ANY_REMOVE_1715}),
    "AAA_CACHE_PROFILE_DEFAULT_REGEXP_ONLY":        _t(**{"1715": AAA_CACHE_PROFILE_DEFAULT_REGEXP_ONLY_1715}),
    "AAA_CACHE_PROFILE_DEFAULT_REGEXP_ONLY_REMOVE": _t(**{"1715": AAA_CACHE_PROFILE_DEFAULT_REGEXP_ONLY_REMOVE_1715}),
    "AAA_CACHE_PROFILE_DEFAULT_PROFILE":            _t(**{"1715": AAA_CACHE_PROFILE_DEFAULT_PROFILE_1715}),
    "AAA_CACHE_PROFILE_DEFAULT_PROFILE_REMOVE":     _t(**{"1715": AAA_CACHE_PROFILE_DEFAULT_PROFILE_REMOVE_1715}),

    # §3. aaa group server tacacsplus
    "AAA_GRP_TACACS_CREATE":                        _t(**{"1715": AAA_GRP_TACACS_CREATE_1715}),
    "AAA_GRP_TACACS_CREATE_REMOVE":                 _t(**{"1715": AAA_GRP_TACACS_CREATE_REMOVE_1715}),
    "AAA_GRP_TACACS_LEGACY_CREATE":                 _t(**{"1715": AAA_GRP_TACACS_LEGACY_CREATE_1715}),
    "AAA_GRP_TACACS_LEGACY_CREATE_REMOVE":          _t(**{"1715": AAA_GRP_TACACS_LEGACY_CREATE_REMOVE_1715}),
    "AAA_GRP_TACACS_SERVER_NAME":                   _t(**{"1715": AAA_GRP_TACACS_SERVER_NAME_1715}),
    "AAA_GRP_TACACS_SERVER_NAME_REMOVE":            _t(**{"1715": AAA_GRP_TACACS_SERVER_NAME_REMOVE_1715}),
    "AAA_GRP_TACACS_SERVER_IP":                     _t(**{"1715": AAA_GRP_TACACS_SERVER_IP_1715}),
    "AAA_GRP_TACACS_SERVER_IP_REMOVE":              _t(**{"1715": AAA_GRP_TACACS_SERVER_IP_REMOVE_1715}),
    "AAA_GRP_TACACS_SERVER_PRIVATE":                _t(**{"1715": AAA_GRP_TACACS_SERVER_PRIVATE_1715}),
    "AAA_GRP_TACACS_SERVER_PRIVATE_REMOVE":         _t(**{"1715": AAA_GRP_TACACS_SERVER_PRIVATE_REMOVE_1715}),
    "AAA_GRP_TACACS_SERVER_PRIVATE_PORT":           _t(**{"1715": AAA_GRP_TACACS_SERVER_PRIVATE_PORT_1715}),
    "AAA_GRP_TACACS_SERVER_PRIVATE_PORT_REMOVE":    _t(**{"1715": AAA_GRP_TACACS_SERVER_PRIVATE_PORT_REMOVE_1715}),
    "AAA_GRP_TACACS_SERVER_PRIVATE_TIMEOUT":        _t(**{"1715": AAA_GRP_TACACS_SERVER_PRIVATE_TIMEOUT_1715}),
    "AAA_GRP_TACACS_SERVER_PRIVATE_TIMEOUT_REMOVE": _t(**{"1715": AAA_GRP_TACACS_SERVER_PRIVATE_TIMEOUT_REMOVE_1715}),
    "AAA_GRP_TACACS_SERVER_PRIVATE_KEY":            _t(**{"1715": AAA_GRP_TACACS_SERVER_PRIVATE_KEY_1715}),
    "AAA_GRP_TACACS_SERVER_PRIVATE_KEY_REMOVE":     _t(**{"1715": AAA_GRP_TACACS_SERVER_PRIVATE_KEY_REMOVE_1715}),
    "AAA_GRP_TACACS_IP_TACACS_SOURCE_INTERFACE":    _t(**{"1715": AAA_GRP_TACACS_IP_TACACS_SOURCE_INTERFACE_1715}),
    "AAA_GRP_TACACS_IP_TACACS_SOURCE_INTERFACE_REMOVE": _t(**{"1715": AAA_GRP_TACACS_IP_TACACS_SOURCE_INTERFACE_REMOVE_1715}),
    "AAA_GRP_TACACS_IP_VRF":                        _t(**{"1715": AAA_GRP_TACACS_IP_VRF_1715}),
    "AAA_GRP_TACACS_IP_VRF_REMOVE":                 _t(**{"1715": AAA_GRP_TACACS_IP_VRF_REMOVE_1715}),
    "AAA_GRP_TACACS_IPV6_TACACS_SOURCE_INTERFACE":  _t(**{"1715": AAA_GRP_TACACS_IPV6_TACACS_SOURCE_INTERFACE_1715}),
    "AAA_GRP_TACACS_IPV6_TACACS_SOURCE_INTERFACE_REMOVE": _t(**{"1715": AAA_GRP_TACACS_IPV6_TACACS_SOURCE_INTERFACE_REMOVE_1715}),
    "AAA_GRP_TACACS_IPV6_VRF":                      _t(**{"1715": AAA_GRP_TACACS_IPV6_VRF_1715}),
    "AAA_GRP_TACACS_IPV6_VRF_REMOVE":               _t(**{"1715": AAA_GRP_TACACS_IPV6_VRF_REMOVE_1715}),
    "AAA_GRP_TACACS_ACCOUNTING_ACK_BROADCAST":      _t(**{"1715": AAA_GRP_TACACS_ACCOUNTING_ACK_BROADCAST_1715}),
    "AAA_GRP_TACACS_ACCOUNTING_ACK_BROADCAST_REMOVE": _t(**{"1715": AAA_GRP_TACACS_ACCOUNTING_ACK_BROADCAST_REMOVE_1715}),
    "AAA_GRP_TACACS_CACHE_AUTHENTICATION_PROFILE":  _t(**{"1715": AAA_GRP_TACACS_CACHE_AUTHENTICATION_PROFILE_1715}),
    "AAA_GRP_TACACS_CACHE_AUTHENTICATION_PROFILE_REMOVE": _t(**{"1715": AAA_GRP_TACACS_CACHE_AUTHENTICATION_PROFILE_REMOVE_1715}),
    "AAA_GRP_TACACS_CACHE_AUTHORIZATION_PROFILE":   _t(**{"1715": AAA_GRP_TACACS_CACHE_AUTHORIZATION_PROFILE_1715}),
    "AAA_GRP_TACACS_CACHE_AUTHORIZATION_PROFILE_REMOVE": _t(**{"1715": AAA_GRP_TACACS_CACHE_AUTHORIZATION_PROFILE_REMOVE_1715}),
    "AAA_GRP_TACACS_CACHE_EXPIRY":                  _t(**{"1715": AAA_GRP_TACACS_CACHE_EXPIRY_1715}),
    "AAA_GRP_TACACS_CACHE_EXPIRY_REMOVE":           _t(**{"1715": AAA_GRP_TACACS_CACHE_EXPIRY_REMOVE_1715}),
    "AAA_GRP_TACACS_DNS_ALIAS_LOOKUP":              _t(**{"1715": AAA_GRP_TACACS_DNS_ALIAS_LOOKUP_1715}),
    "AAA_GRP_TACACS_DNS_ALIAS_LOOKUP_REMOVE":       _t(**{"1715": AAA_GRP_TACACS_DNS_ALIAS_LOOKUP_REMOVE_1715}),
    "AAA_GRP_TACACS_HOST":                          _t(**{"1715": AAA_GRP_TACACS_HOST_1715}),
    "AAA_GRP_TACACS_HOST_REMOVE":                   _t(**{"1715": AAA_GRP_TACACS_HOST_REMOVE_1715}),
    "AAA_GRP_TACACS_PICK_METHOD":                   _t(**{"1715": AAA_GRP_TACACS_PICK_METHOD_1715}),
    "AAA_GRP_TACACS_PICK_METHOD_REMOVE":            _t(**{"1715": AAA_GRP_TACACS_PICK_METHOD_REMOVE_1715}),
    "AAA_GRP_TACACS_TIMEOUT":                       _t(**{"1715": AAA_GRP_TACACS_TIMEOUT_1715}),
    "AAA_GRP_TACACS_TIMEOUT_REMOVE":                _t(**{"1715": AAA_GRP_TACACS_TIMEOUT_REMOVE_1715}),

    # §4. aaa group server radius
    "AAA_GRP_RADIUS_CREATE":                        _t(**{"1715": AAA_GRP_RADIUS_CREATE_1715}),
    "AAA_GRP_RADIUS_CREATE_REMOVE":                 _t(**{"1715": AAA_GRP_RADIUS_CREATE_REMOVE_1715}),
    "AAA_GRP_RADIUS_SERVER_NAME":                   _t(**{"1715": AAA_GRP_RADIUS_SERVER_NAME_1715}),
    "AAA_GRP_RADIUS_SERVER_NAME_REMOVE":            _t(**{"1715": AAA_GRP_RADIUS_SERVER_NAME_REMOVE_1715}),
    "AAA_GRP_RADIUS_SERVER_DIRECT":                 _t(**{"1715": AAA_GRP_RADIUS_SERVER_DIRECT_1715}),
    "AAA_GRP_RADIUS_SERVER_DIRECT_REMOVE":          _t(**{"1715": AAA_GRP_RADIUS_SERVER_DIRECT_REMOVE_1715}),
    "AAA_GRP_RADIUS_SERVER_DIRECT_PORTS":           _t(**{"1715": AAA_GRP_RADIUS_SERVER_DIRECT_PORTS_1715}),
    "AAA_GRP_RADIUS_SERVER_DIRECT_PORTS_REMOVE":    _t(**{"1715": AAA_GRP_RADIUS_SERVER_DIRECT_PORTS_REMOVE_1715}),
    "AAA_GRP_RADIUS_SUBSCRIBER_MAC_FILTERING":      _t(**{"1715": AAA_GRP_RADIUS_SUBSCRIBER_MAC_FILTERING_1715}),
    "AAA_GRP_RADIUS_SUBSCRIBER_MAC_FILTERING_REMOVE": _t(**{"1715": AAA_GRP_RADIUS_SUBSCRIBER_MAC_FILTERING_REMOVE_1715}),
    "AAA_GRP_RADIUS_MAC_DELIMITER":                 _t(**{"1715": AAA_GRP_RADIUS_MAC_DELIMITER_1715}),
    "AAA_GRP_RADIUS_MAC_DELIMITER_REMOVE":          _t(**{"1715": AAA_GRP_RADIUS_MAC_DELIMITER_REMOVE_1715}),
    "AAA_GRP_RADIUS_SERVER_PRIVATE":                _t(**{"1715": AAA_GRP_RADIUS_SERVER_PRIVATE_1715}),
    "AAA_GRP_RADIUS_SERVER_PRIVATE_REMOVE":         _t(**{"1715": AAA_GRP_RADIUS_SERVER_PRIVATE_REMOVE_1715}),
    "AAA_GRP_RADIUS_SERVER_PRIVATE_PORTS":          _t(**{"1715": AAA_GRP_RADIUS_SERVER_PRIVATE_PORTS_1715}),
    "AAA_GRP_RADIUS_SERVER_PRIVATE_PORTS_REMOVE":   _t(**{"1715": AAA_GRP_RADIUS_SERVER_PRIVATE_PORTS_REMOVE_1715}),
    "AAA_GRP_RADIUS_SERVER_PRIVATE_TIMEOUT":        _t(**{"1715": AAA_GRP_RADIUS_SERVER_PRIVATE_TIMEOUT_1715}),
    "AAA_GRP_RADIUS_SERVER_PRIVATE_TIMEOUT_REMOVE": _t(**{"1715": AAA_GRP_RADIUS_SERVER_PRIVATE_TIMEOUT_REMOVE_1715}),
    "AAA_GRP_RADIUS_SERVER_PRIVATE_RETRANSMIT":     _t(**{"1715": AAA_GRP_RADIUS_SERVER_PRIVATE_RETRANSMIT_1715}),
    "AAA_GRP_RADIUS_SERVER_PRIVATE_RETRANSMIT_REMOVE": _t(**{"1715": AAA_GRP_RADIUS_SERVER_PRIVATE_RETRANSMIT_REMOVE_1715}),
    "AAA_GRP_RADIUS_SERVER_PRIVATE_PAC":            _t(**{"1715": AAA_GRP_RADIUS_SERVER_PRIVATE_PAC_1715}),
    "AAA_GRP_RADIUS_SERVER_PRIVATE_PAC_REMOVE":     _t(**{"1715": AAA_GRP_RADIUS_SERVER_PRIVATE_PAC_REMOVE_1715}),
    "AAA_GRP_RADIUS_SERVER_PRIVATE_KEY":            _t(**{"1715": AAA_GRP_RADIUS_SERVER_PRIVATE_KEY_1715}),
    "AAA_GRP_RADIUS_SERVER_PRIVATE_KEY_REMOVE":     _t(**{"1715": AAA_GRP_RADIUS_SERVER_PRIVATE_KEY_REMOVE_1715}),
    "AAA_GRP_RADIUS_DEADTIME":                      _t(**{"1715": AAA_GRP_RADIUS_DEADTIME_1715}),
    "AAA_GRP_RADIUS_DEADTIME_REMOVE":               _t(**{"1715": AAA_GRP_RADIUS_DEADTIME_REMOVE_1715}),
    "AAA_GRP_RADIUS_IP_RADIUS_SOURCE_INTERFACE":    _t(**{"1715": AAA_GRP_RADIUS_IP_RADIUS_SOURCE_INTERFACE_1715}),
    "AAA_GRP_RADIUS_IP_RADIUS_SOURCE_INTERFACE_REMOVE": _t(**{"1715": AAA_GRP_RADIUS_IP_RADIUS_SOURCE_INTERFACE_REMOVE_1715}),
    "AAA_GRP_RADIUS_IP_VRF":                        _t(**{"1715": AAA_GRP_RADIUS_IP_VRF_1715}),
    "AAA_GRP_RADIUS_IP_VRF_REMOVE":                 _t(**{"1715": AAA_GRP_RADIUS_IP_VRF_REMOVE_1715}),
    "AAA_GRP_RADIUS_IPV6_RADIUS_SOURCE_INTERFACE":  _t(**{"1715": AAA_GRP_RADIUS_IPV6_RADIUS_SOURCE_INTERFACE_1715}),
    "AAA_GRP_RADIUS_IPV6_RADIUS_SOURCE_INTERFACE_REMOVE": _t(**{"1715": AAA_GRP_RADIUS_IPV6_RADIUS_SOURCE_INTERFACE_REMOVE_1715}),
    "AAA_GRP_RADIUS_IPV6_VRF":                      _t(**{"1715": AAA_GRP_RADIUS_IPV6_VRF_1715}),
    "AAA_GRP_RADIUS_IPV6_VRF_REMOVE":               _t(**{"1715": AAA_GRP_RADIUS_IPV6_VRF_REMOVE_1715}),
    "AAA_GRP_RADIUS_ACCOUNTING_REQUEST_REJECT":     _t(**{"1715": AAA_GRP_RADIUS_ACCOUNTING_REQUEST_REJECT_1715}),
    "AAA_GRP_RADIUS_ACCOUNTING_REQUEST_REJECT_REMOVE": _t(**{"1715": AAA_GRP_RADIUS_ACCOUNTING_REQUEST_REJECT_REMOVE_1715}),
    "AAA_GRP_RADIUS_CACHE_AUTHENTICATION_PROFILE":  _t(**{"1715": AAA_GRP_RADIUS_CACHE_AUTHENTICATION_PROFILE_1715}),
    "AAA_GRP_RADIUS_CACHE_AUTHENTICATION_PROFILE_REMOVE": _t(**{"1715": AAA_GRP_RADIUS_CACHE_AUTHENTICATION_PROFILE_REMOVE_1715}),
    "AAA_GRP_RADIUS_CACHE_AUTHORIZATION_PROFILE":   _t(**{"1715": AAA_GRP_RADIUS_CACHE_AUTHORIZATION_PROFILE_1715}),
    "AAA_GRP_RADIUS_CACHE_AUTHORIZATION_PROFILE_REMOVE": _t(**{"1715": AAA_GRP_RADIUS_CACHE_AUTHORIZATION_PROFILE_REMOVE_1715}),
    "AAA_GRP_RADIUS_CACHE_EXPIRY":                  _t(**{"1715": AAA_GRP_RADIUS_CACHE_EXPIRY_1715}),
    "AAA_GRP_RADIUS_CACHE_EXPIRY_REMOVE":           _t(**{"1715": AAA_GRP_RADIUS_CACHE_EXPIRY_REMOVE_1715}),
    "AAA_GRP_RADIUS_DSCP":                          _t(**{"1715": AAA_GRP_RADIUS_DSCP_1715}),
    "AAA_GRP_RADIUS_DSCP_REMOVE":                   _t(**{"1715": AAA_GRP_RADIUS_DSCP_REMOVE_1715}),
    "AAA_GRP_RADIUS_LOAD_BALANCE_LEAST_OUTSTANDING": _t(**{"1715": AAA_GRP_RADIUS_LOAD_BALANCE_LEAST_OUTSTANDING_1715}),
    "AAA_GRP_RADIUS_LOAD_BALANCE_LEAST_OUTSTANDING_REMOVE": _t(**{"1715": AAA_GRP_RADIUS_LOAD_BALANCE_LEAST_OUTSTANDING_REMOVE_1715}),
    "AAA_GRP_RADIUS_LOAD_BALANCE_BATCH_SIZE":       _t(**{"1715": AAA_GRP_RADIUS_LOAD_BALANCE_BATCH_SIZE_1715}),
    "AAA_GRP_RADIUS_LOAD_BALANCE_BATCH_SIZE_REMOVE": _t(**{"1715": AAA_GRP_RADIUS_LOAD_BALANCE_BATCH_SIZE_REMOVE_1715}),

    # §5. aaa group server ldap
    "AAA_GRP_LDAP_CREATE":                          _t(**{"1715": AAA_GRP_LDAP_CREATE_1715}),
    "AAA_GRP_LDAP_CREATE_REMOVE":                   _t(**{"1715": AAA_GRP_LDAP_CREATE_REMOVE_1715}),
    "AAA_GRP_LDAP_SERVER_NAME":                     _t(**{"1715": AAA_GRP_LDAP_SERVER_NAME_1715}),
    "AAA_GRP_LDAP_SERVER_NAME_REMOVE":              _t(**{"1715": AAA_GRP_LDAP_SERVER_NAME_REMOVE_1715}),

    # §6. aaa attribute list
    "AAA_ATTR_LIST_CREATE":                         _t(**{"1715": AAA_ATTR_LIST_CREATE_1715}),
    "AAA_ATTR_LIST_CREATE_REMOVE":                  _t(**{"1715": AAA_ATTR_LIST_CREATE_REMOVE_1715}),
    "AAA_ATTR_LIST_TYPE":                           _t(**{"1715": AAA_ATTR_LIST_TYPE_1715}),
    "AAA_ATTR_LIST_TYPE_REMOVE":                    _t(**{"1715": AAA_ATTR_LIST_TYPE_REMOVE_1715}),
    "AAA_ATTR_LIST_TYPE_MANDATORY":                 _t(**{"1715": AAA_ATTR_LIST_TYPE_MANDATORY_1715}),
    "AAA_ATTR_LIST_TYPE_MANDATORY_REMOVE":          _t(**{"1715": AAA_ATTR_LIST_TYPE_MANDATORY_REMOVE_1715}),
    "AAA_ATTR_LIST_TYPE_TAG":                       _t(**{"1715": AAA_ATTR_LIST_TYPE_TAG_1715}),
    "AAA_ATTR_LIST_TYPE_TAG_REMOVE":                _t(**{"1715": AAA_ATTR_LIST_TYPE_TAG_REMOVE_1715}),

    # §7. aaa authentication + local
    "AAA_AUTHN_BANNER":                             _t(**{"1715": AAA_AUTHN_BANNER_1715}),
    "AAA_AUTHN_BANNER_REMOVE":                      _t(**{"1715": AAA_AUTHN_BANNER_REMOVE_1715}),
    "AAA_AUTHN_FAIL_MESSAGE":                       _t(**{"1715": AAA_AUTHN_FAIL_MESSAGE_1715}),
    "AAA_AUTHN_FAIL_MESSAGE_REMOVE":                _t(**{"1715": AAA_AUTHN_FAIL_MESSAGE_REMOVE_1715}),
    "AAA_AUTHN_ATTEMPTS_LOGIN":                     _t(**{"1715": AAA_AUTHN_ATTEMPTS_LOGIN_1715}),
    "AAA_AUTHN_ATTEMPTS_LOGIN_REMOVE":              _t(**{"1715": AAA_AUTHN_ATTEMPTS_LOGIN_REMOVE_1715}),
    "AAA_AUTHN_SUPPRESS_NULL_USERNAME":             _t(**{"1715": AAA_AUTHN_SUPPRESS_NULL_USERNAME_1715}),
    "AAA_AUTHN_SUPPRESS_NULL_USERNAME_REMOVE":      _t(**{"1715": AAA_AUTHN_SUPPRESS_NULL_USERNAME_REMOVE_1715}),
    "AAA_AUTHN_DOT1X_DEFAULT":                      _t(**{"1715": AAA_AUTHN_DOT1X_DEFAULT_1715}),
    "AAA_AUTHN_DOT1X_DEFAULT_REMOVE":               _t(**{"1715": AAA_AUTHN_DOT1X_DEFAULT_REMOVE_1715}),
    "AAA_AUTHN_DOT1X_LIST":                         _t(**{"1715": AAA_AUTHN_DOT1X_LIST_1715}),
    "AAA_AUTHN_DOT1X_LIST_REMOVE":                  _t(**{"1715": AAA_AUTHN_DOT1X_LIST_REMOVE_1715}),
    "AAA_AUTHN_ENABLE_DEFAULT":                     _t(**{"1715": AAA_AUTHN_ENABLE_DEFAULT_1715}),
    "AAA_AUTHN_ENABLE_DEFAULT_REMOVE":              _t(**{"1715": AAA_AUTHN_ENABLE_DEFAULT_REMOVE_1715}),
    "AAA_AUTHN_EOU_DEFAULT_RADIUS":                 _t(**{"1715": AAA_AUTHN_EOU_DEFAULT_RADIUS_1715}),
    "AAA_AUTHN_EOU_DEFAULT_RADIUS_REMOVE":          _t(**{"1715": AAA_AUTHN_EOU_DEFAULT_RADIUS_REMOVE_1715}),
    "AAA_AUTHN_LOGIN":                              _t(**{"1715": AAA_AUTHN_LOGIN_1715}),
    "AAA_AUTHN_LOGIN_REMOVE":                       _t(**{"1715": AAA_AUTHN_LOGIN_REMOVE_1715}),
    "AAA_AUTHN_ONEP_DEFAULT_LOCAL":                 _t(**{"1715": AAA_AUTHN_ONEP_DEFAULT_LOCAL_1715}),
    "AAA_AUTHN_ONEP_DEFAULT_LOCAL_REMOVE":          _t(**{"1715": AAA_AUTHN_ONEP_DEFAULT_LOCAL_REMOVE_1715}),
    "AAA_AUTHN_PPP":                                _t(**{"1715": AAA_AUTHN_PPP_1715}),
    "AAA_AUTHN_PPP_REMOVE":                         _t(**{"1715": AAA_AUTHN_PPP_REMOVE_1715}),
    "AAA_AUTHN_PASSWORD_PROMPT":                    _t(**{"1715": AAA_AUTHN_PASSWORD_PROMPT_1715}),
    "AAA_AUTHN_PASSWORD_PROMPT_REMOVE":             _t(**{"1715": AAA_AUTHN_PASSWORD_PROMPT_REMOVE_1715}),
    "AAA_AUTHN_USERNAME_PROMPT":                    _t(**{"1715": AAA_AUTHN_USERNAME_PROMPT_1715}),
    "AAA_AUTHN_USERNAME_PROMPT_REMOVE":             _t(**{"1715": AAA_AUTHN_USERNAME_PROMPT_REMOVE_1715}),
    "AAA_AUTHN_WEBAUTH_DEFAULT":                    _t(**{"1715": AAA_AUTHN_WEBAUTH_DEFAULT_1715}),
    "AAA_AUTHN_WEBAUTH_DEFAULT_REMOVE":             _t(**{"1715": AAA_AUTHN_WEBAUTH_DEFAULT_REMOVE_1715}),
    "AAA_LOCAL_AUTHN_AUTHORIZATION":                _t(**{"1715": AAA_LOCAL_AUTHN_AUTHORIZATION_1715}),
    "AAA_LOCAL_AUTHN_AUTHORIZATION_REMOVE":         _t(**{"1715": AAA_LOCAL_AUTHN_AUTHORIZATION_REMOVE_1715}),
        "AAA_LOCAL_AUTHN_ATTEMPTS_MAX_FAIL":            _t(**{"1715": AAA_LOCAL_AUTHN_ATTEMPTS_MAX_FAIL_1715}),
    "AAA_LOCAL_AUTHN_ATTEMPTS_MAX_FAIL_REMOVE":     _t(**{"1715": AAA_LOCAL_AUTHN_ATTEMPTS_MAX_FAIL_REMOVE_1715}),

    # §8. aaa authorization
    "AAA_AUTHZ_AUTH_TYPE_DEFAULT_GROUP_RADIUS":     _t(**{"1715": AAA_AUTHZ_AUTH_TYPE_DEFAULT_GROUP_RADIUS_1715}),
    "AAA_AUTHZ_AUTH_TYPE_DEFAULT_GROUP_RADIUS_REMOVE": _t(**{"1715": AAA_AUTHZ_AUTH_TYPE_DEFAULT_GROUP_RADIUS_REMOVE_1715}),
    "AAA_AUTHZ_COMMANDS":                           _t(**{"1715": AAA_AUTHZ_COMMANDS_1715}),
    "AAA_AUTHZ_COMMANDS_REMOVE":                    _t(**{"1715": AAA_AUTHZ_COMMANDS_REMOVE_1715}),
    "AAA_AUTHZ_CONFIG_COMMANDS":                    _t(**{"1715": AAA_AUTHZ_CONFIG_COMMANDS_1715}),
    "AAA_AUTHZ_CONFIG_COMMANDS_REMOVE":             _t(**{"1715": AAA_AUTHZ_CONFIG_COMMANDS_REMOVE_1715}),
    "AAA_AUTHZ_CONFIGURATION_LIST":                 _t(**{"1715": AAA_AUTHZ_CONFIGURATION_LIST_1715}),
    "AAA_AUTHZ_CONFIGURATION_LIST_REMOVE":          _t(**{"1715": AAA_AUTHZ_CONFIGURATION_LIST_REMOVE_1715}),
    "AAA_AUTHZ_CONFIGURATION_DEFAULT_GROUP":        _t(**{"1715": AAA_AUTHZ_CONFIGURATION_DEFAULT_GROUP_1715}),
    "AAA_AUTHZ_CONFIGURATION_DEFAULT_GROUP_REMOVE": _t(**{"1715": AAA_AUTHZ_CONFIGURATION_DEFAULT_GROUP_REMOVE_1715}),
    "AAA_AUTHZ_CONFIGURATION_DEFAULT_CACHE":        _t(**{"1715": AAA_AUTHZ_CONFIGURATION_DEFAULT_CACHE_1715}),
    "AAA_AUTHZ_CONFIGURATION_DEFAULT_CACHE_REMOVE": _t(**{"1715": AAA_AUTHZ_CONFIGURATION_DEFAULT_CACHE_REMOVE_1715}),
    "AAA_AUTHZ_CONSOLE":                            _t(**{"1715": AAA_AUTHZ_CONSOLE_1715}),
    "AAA_AUTHZ_CONSOLE_REMOVE":                     _t(**{"1715": AAA_AUTHZ_CONSOLE_REMOVE_1715}),
    "AAA_AUTHZ_CREDENTIAL_DOWNLOAD_DEFAULT":        _t(**{"1715": AAA_AUTHZ_CREDENTIAL_DOWNLOAD_DEFAULT_1715}),
    "AAA_AUTHZ_CREDENTIAL_DOWNLOAD_DEFAULT_REMOVE": _t(**{"1715": AAA_AUTHZ_CREDENTIAL_DOWNLOAD_DEFAULT_REMOVE_1715}),
    "AAA_AUTHZ_CREDENTIAL_DOWNLOAD_LIST":           _t(**{"1715": AAA_AUTHZ_CREDENTIAL_DOWNLOAD_LIST_1715}),
    "AAA_AUTHZ_CREDENTIAL_DOWNLOAD_LIST_REMOVE":    _t(**{"1715": AAA_AUTHZ_CREDENTIAL_DOWNLOAD_LIST_REMOVE_1715}),
    "AAA_AUTHZ_RADIUS_PROXY_DEFAULT":               _t(**{"1715": AAA_AUTHZ_RADIUS_PROXY_DEFAULT_1715}),
    "AAA_AUTHZ_RADIUS_PROXY_DEFAULT_REMOVE":        _t(**{"1715": AAA_AUTHZ_RADIUS_PROXY_DEFAULT_REMOVE_1715}),
    "AAA_AUTHZ_RADIUS_PROXY_LIST":                  _t(**{"1715": AAA_AUTHZ_RADIUS_PROXY_LIST_1715}),
    "AAA_AUTHZ_RADIUS_PROXY_LIST_REMOVE":           _t(**{"1715": AAA_AUTHZ_RADIUS_PROXY_LIST_REMOVE_1715}),
    "AAA_AUTHZ_EXEC":                               _t(**{"1715": AAA_AUTHZ_EXEC_1715}),
    "AAA_AUTHZ_EXEC_REMOVE":                        _t(**{"1715": AAA_AUTHZ_EXEC_REMOVE_1715}),
    "AAA_AUTHZ_EVENTMANAGER_GROUP":                 _t(**{"1715": AAA_AUTHZ_EVENTMANAGER_GROUP_1715}),
    "AAA_AUTHZ_EVENTMANAGER_GROUP_REMOVE":          _t(**{"1715": AAA_AUTHZ_EVENTMANAGER_GROUP_REMOVE_1715}),
    "AAA_AUTHZ_EVENTMANAGER_LOCAL":                 _t(**{"1715": AAA_AUTHZ_EVENTMANAGER_LOCAL_1715}),
    "AAA_AUTHZ_EVENTMANAGER_LOCAL_REMOVE":          _t(**{"1715": AAA_AUTHZ_EVENTMANAGER_LOCAL_REMOVE_1715}),
    "AAA_AUTHZ_EVENTMANAGER_NONE":                  _t(**{"1715": AAA_AUTHZ_EVENTMANAGER_NONE_1715}),
    "AAA_AUTHZ_EVENTMANAGER_NONE_REMOVE":           _t(**{"1715": AAA_AUTHZ_EVENTMANAGER_NONE_REMOVE_1715}),
    "AAA_AUTHZ_NETWORK":                            _t(**{"1715": AAA_AUTHZ_NETWORK_1715}),
    "AAA_AUTHZ_NETWORK_REMOVE":                     _t(**{"1715": AAA_AUTHZ_NETWORK_REMOVE_1715}),
    "AAA_AUTHZ_AUTH_PROXY_DEFAULT_LOCAL":           _t(**{"1715": AAA_AUTHZ_AUTH_PROXY_DEFAULT_LOCAL_1715}),
    "AAA_AUTHZ_AUTH_PROXY_DEFAULT_LOCAL_REMOVE":    _t(**{"1715": AAA_AUTHZ_AUTH_PROXY_DEFAULT_LOCAL_REMOVE_1715}),
    "AAA_AUTHZ_AUTH_PROXY_DEFAULT_GROUP":           _t(**{"1715": AAA_AUTHZ_AUTH_PROXY_DEFAULT_GROUP_1715}),
    "AAA_AUTHZ_AUTH_PROXY_DEFAULT_GROUP_REMOVE":    _t(**{"1715": AAA_AUTHZ_AUTH_PROXY_DEFAULT_GROUP_REMOVE_1715}),
    "AAA_AUTHZ_ONEP_DEFAULT_GROUP":                 _t(**{"1715": AAA_AUTHZ_ONEP_DEFAULT_GROUP_1715}),
    "AAA_AUTHZ_ONEP_DEFAULT_GROUP_REMOVE":          _t(**{"1715": AAA_AUTHZ_ONEP_DEFAULT_GROUP_REMOVE_1715}),

    # §9. aaa accounting
    "AAA_ACCT_NESTED":                              _t(**{"1715": AAA_ACCT_NESTED_1715}),
    "AAA_ACCT_NESTED_REMOVE":                       _t(**{"1715": AAA_ACCT_NESTED_REMOVE_1715}),
    "AAA_ACCT_COMMANDS_LOCAL":                      _t(**{"1715": AAA_ACCT_COMMANDS_LOCAL_1715}),
    "AAA_ACCT_COMMANDS_LOCAL_REMOVE":               _t(**{"1715": AAA_ACCT_COMMANDS_LOCAL_REMOVE_1715}),
    "AAA_ACCT_COMMANDS_NONE":                       _t(**{"1715": AAA_ACCT_COMMANDS_NONE_1715}),
    "AAA_ACCT_COMMANDS_NONE_REMOVE":                _t(**{"1715": AAA_ACCT_COMMANDS_NONE_REMOVE_1715}),
    "AAA_ACCT_COMMANDS":                            _t(**{"1715": AAA_ACCT_COMMANDS_1715}),
    "AAA_ACCT_COMMANDS_REMOVE":                     _t(**{"1715": AAA_ACCT_COMMANDS_REMOVE_1715}),
    "AAA_ACCT_CONNECTION_NONE":                     _t(**{"1715": AAA_ACCT_CONNECTION_NONE_1715}),
    "AAA_ACCT_CONNECTION_NONE_REMOVE":              _t(**{"1715": AAA_ACCT_CONNECTION_NONE_REMOVE_1715}),
    "AAA_ACCT_CONNECTION":                          _t(**{"1715": AAA_ACCT_CONNECTION_1715}),
    "AAA_ACCT_CONNECTION_REMOVE":                   _t(**{"1715": AAA_ACCT_CONNECTION_REMOVE_1715}),
    "AAA_ACCT_DELAY_START":                         _t(**{"1715": AAA_ACCT_DELAY_START_1715}),
    "AAA_ACCT_DELAY_START_REMOVE":                  _t(**{"1715": AAA_ACCT_DELAY_START_REMOVE_1715}),
    "AAA_ACCT_DELAY_START_ALL":                     _t(**{"1715": AAA_ACCT_DELAY_START_ALL_1715}),
    "AAA_ACCT_DELAY_START_ALL_REMOVE":              _t(**{"1715": AAA_ACCT_DELAY_START_ALL_REMOVE_1715}),
    "AAA_ACCT_DELAY_START_EXTENDED":                _t(**{"1715": AAA_ACCT_DELAY_START_EXTENDED_1715}),
    "AAA_ACCT_DELAY_START_EXTENDED_REMOVE":         _t(**{"1715": AAA_ACCT_DELAY_START_EXTENDED_REMOVE_1715}),
    "AAA_ACCT_DOT1X_DEFAULT":                       _t(**{"1715": AAA_ACCT_DOT1X_DEFAULT_1715}),
    "AAA_ACCT_DOT1X_DEFAULT_REMOVE":                _t(**{"1715": AAA_ACCT_DOT1X_DEFAULT_REMOVE_1715}),
    "AAA_ACCT_DOT1X_LIST":                          _t(**{"1715": AAA_ACCT_DOT1X_LIST_1715}),
    "AAA_ACCT_DOT1X_LIST_REMOVE":                   _t(**{"1715": AAA_ACCT_DOT1X_LIST_REMOVE_1715}),
    "AAA_ACCT_IDENTITY_DEFAULT":                    _t(**{"1715": AAA_ACCT_IDENTITY_DEFAULT_1715}),
    "AAA_ACCT_IDENTITY_DEFAULT_REMOVE":             _t(**{"1715": AAA_ACCT_IDENTITY_DEFAULT_REMOVE_1715}),
    "AAA_ACCT_IDENTITY_LIST":                       _t(**{"1715": AAA_ACCT_IDENTITY_LIST_1715}),
    "AAA_ACCT_IDENTITY_LIST_REMOVE":                _t(**{"1715": AAA_ACCT_IDENTITY_LIST_REMOVE_1715}),
    "AAA_ACCT_ONEP_DEFAULT_NONE":                   _t(**{"1715": AAA_ACCT_ONEP_DEFAULT_NONE_1715}),
    "AAA_ACCT_ONEP_DEFAULT_NONE_REMOVE":            _t(**{"1715": AAA_ACCT_ONEP_DEFAULT_NONE_REMOVE_1715}),
    "AAA_ACCT_ONEP_DEFAULT":                        _t(**{"1715": AAA_ACCT_ONEP_DEFAULT_1715}),
    "AAA_ACCT_ONEP_DEFAULT_REMOVE":                 _t(**{"1715": AAA_ACCT_ONEP_DEFAULT_REMOVE_1715}),
    "AAA_ACCT_EXEC_NONE":                           _t(**{"1715": AAA_ACCT_EXEC_NONE_1715}),
    "AAA_ACCT_EXEC_NONE_REMOVE":                    _t(**{"1715": AAA_ACCT_EXEC_NONE_REMOVE_1715}),
    "AAA_ACCT_EXEC":                                _t(**{"1715": AAA_ACCT_EXEC_1715}),
    "AAA_ACCT_EXEC_REMOVE":                         _t(**{"1715": AAA_ACCT_EXEC_REMOVE_1715}),
    "AAA_ACCT_EXEC_SUBMODE_NONE":                   _t(**{"1715": AAA_ACCT_EXEC_SUBMODE_NONE_1715}),
    "AAA_ACCT_EXEC_SUBMODE_NONE_REMOVE":            _t(**{"1715": AAA_ACCT_EXEC_SUBMODE_NONE_REMOVE_1715}),
    "AAA_ACCT_EXEC_SUBMODE":                        _t(**{"1715": AAA_ACCT_EXEC_SUBMODE_1715}),
    "AAA_ACCT_EXEC_SUBMODE_REMOVE":                 _t(**{"1715": AAA_ACCT_EXEC_SUBMODE_REMOVE_1715}),
    "AAA_ACCT_NETWORK_NONE":                        _t(**{"1715": AAA_ACCT_NETWORK_NONE_1715}),
    "AAA_ACCT_NETWORK_NONE_REMOVE":                 _t(**{"1715": AAA_ACCT_NETWORK_NONE_REMOVE_1715}),
    "AAA_ACCT_NETWORK":                             _t(**{"1715": AAA_ACCT_NETWORK_1715}),
    "AAA_ACCT_NETWORK_REMOVE":                      _t(**{"1715": AAA_ACCT_NETWORK_REMOVE_1715}),
    "AAA_ACCT_SEND_COUNTERS_IPV6":                  _t(**{"1715": AAA_ACCT_SEND_COUNTERS_IPV6_1715}),
    "AAA_ACCT_SEND_COUNTERS_IPV6_REMOVE":           _t(**{"1715": AAA_ACCT_SEND_COUNTERS_IPV6_REMOVE_1715}),
    "AAA_ACCT_SEND_STOP_RECORD_ALWAYS":             _t(**{"1715": AAA_ACCT_SEND_STOP_RECORD_ALWAYS_1715}),
    "AAA_ACCT_SEND_STOP_RECORD_ALWAYS_REMOVE":      _t(**{"1715": AAA_ACCT_SEND_STOP_RECORD_ALWAYS_REMOVE_1715}),
    "AAA_ACCT_SEND_STOP_RECORD_AUTH_FAILURE":       _t(**{"1715": AAA_ACCT_SEND_STOP_RECORD_AUTH_FAILURE_1715}),
    "AAA_ACCT_SEND_STOP_RECORD_AUTH_FAILURE_REMOVE":_t(**{"1715": AAA_ACCT_SEND_STOP_RECORD_AUTH_FAILURE_REMOVE_1715}),
    "AAA_ACCT_SEND_STOP_RECORD_AUTH_FAILURE_VRF":   _t(**{"1715": AAA_ACCT_SEND_STOP_RECORD_AUTH_FAILURE_VRF_1715}),
    "AAA_ACCT_SEND_STOP_RECORD_AUTH_FAILURE_VRF_REMOVE": _t(**{"1715": AAA_ACCT_SEND_STOP_RECORD_AUTH_FAILURE_VRF_REMOVE_1715}),
    "AAA_ACCT_SEND_STOP_RECORD_AUTH_SUCCESS_REMOTE": _t(**{"1715": AAA_ACCT_SEND_STOP_RECORD_AUTH_SUCCESS_REMOTE_1715}),
    "AAA_ACCT_SEND_STOP_RECORD_AUTH_SUCCESS_REMOTE_REMOVE": _t(**{"1715": AAA_ACCT_SEND_STOP_RECORD_AUTH_SUCCESS_REMOTE_REMOVE_1715}),
    "AAA_ACCT_SEND_STOP_RECORD_AUTH_SUCCESS_REMOTE_VRF": _t(**{"1715": AAA_ACCT_SEND_STOP_RECORD_AUTH_SUCCESS_REMOTE_VRF_1715}),
    "AAA_ACCT_SEND_STOP_RECORD_AUTH_SUCCESS_REMOTE_VRF_REMOVE": _t(**{"1715": AAA_ACCT_SEND_STOP_RECORD_AUTH_SUCCESS_REMOTE_VRF_REMOVE_1715}),
    "AAA_ACCT_SUPPRESS_NULL_USERNAME":              _t(**{"1715": AAA_ACCT_SUPPRESS_NULL_USERNAME_1715}),
    "AAA_ACCT_SUPPRESS_NULL_USERNAME_REMOVE":       _t(**{"1715": AAA_ACCT_SUPPRESS_NULL_USERNAME_REMOVE_1715}),
    "AAA_ACCT_SYSTEM_DEFAULT_NONE":                 _t(**{"1715": AAA_ACCT_SYSTEM_DEFAULT_NONE_1715}),
    "AAA_ACCT_SYSTEM_DEFAULT_NONE_REMOVE":          _t(**{"1715": AAA_ACCT_SYSTEM_DEFAULT_NONE_REMOVE_1715}),
    "AAA_ACCT_SYSTEM_DEFAULT_START_STOP":           _t(**{"1715": AAA_ACCT_SYSTEM_DEFAULT_START_STOP_1715}),
    "AAA_ACCT_SYSTEM_DEFAULT_START_STOP_REMOVE":    _t(**{"1715": AAA_ACCT_SYSTEM_DEFAULT_START_STOP_REMOVE_1715}),
    "AAA_ACCT_SYSTEM_DEFAULT_VRF":                  _t(**{"1715": AAA_ACCT_SYSTEM_DEFAULT_VRF_1715}),
    "AAA_ACCT_SYSTEM_DEFAULT_VRF_REMOVE":           _t(**{"1715": AAA_ACCT_SYSTEM_DEFAULT_VRF_REMOVE_1715}),
    "AAA_ACCT_SYSTEM_GUARANTEE_FIRST":              _t(**{"1715": AAA_ACCT_SYSTEM_GUARANTEE_FIRST_1715}),
    "AAA_ACCT_SYSTEM_GUARANTEE_FIRST_REMOVE":       _t(**{"1715": AAA_ACCT_SYSTEM_GUARANTEE_FIRST_REMOVE_1715}),
    "AAA_ACCT_UPDATE_PERIODIC":                     _t(**{"1715": AAA_ACCT_UPDATE_PERIODIC_1715}),
    "AAA_ACCT_UPDATE_PERIODIC_REMOVE":              _t(**{"1715": AAA_ACCT_UPDATE_PERIODIC_REMOVE_1715}),
    "AAA_ACCT_UPDATE_NEWINFO":                      _t(**{"1715": AAA_ACCT_UPDATE_NEWINFO_1715}),
    "AAA_ACCT_UPDATE_NEWINFO_REMOVE":               _t(**{"1715": AAA_ACCT_UPDATE_NEWINFO_REMOVE_1715}),
    "AAA_ACCT_UPDATE_NEWINFO_PERIODIC":             _t(**{"1715": AAA_ACCT_UPDATE_NEWINFO_PERIODIC_1715}),
    "AAA_ACCT_UPDATE_NEWINFO_PERIODIC_REMOVE":      _t(**{"1715": AAA_ACCT_UPDATE_NEWINFO_PERIODIC_REMOVE_1715}),
    "AAA_ACCT_AUTH_PROXY_DEFAULT_START_STOP_GROUP": _t(**{"1715": AAA_ACCT_AUTH_PROXY_DEFAULT_START_STOP_GROUP_1715}),
    "AAA_ACCT_AUTH_PROXY_DEFAULT_START_STOP_GROUP_REMOVE": _t(**{"1715": AAA_ACCT_AUTH_PROXY_DEFAULT_START_STOP_GROUP_REMOVE_1715}),
    "AAA_ACCT_JITTER_MAXIMUM":                      _t(**{"1715": AAA_ACCT_JITTER_MAXIMUM_1715}),
    "AAA_ACCT_JITTER_MAXIMUM_REMOVE":               _t(**{"1715": AAA_ACCT_JITTER_MAXIMUM_REMOVE_1715}),

    # §10. aaa common-criteria
    "AAA_CC_POLICY_CREATE":                         _t(**{"1715": AAA_CC_POLICY_CREATE_1715}),
    "AAA_CC_POLICY_CREATE_REMOVE":                  _t(**{"1715": AAA_CC_POLICY_CREATE_REMOVE_1715}),
    "AAA_CC_CHAR_CHANGES":                          _t(**{"1715": AAA_CC_CHAR_CHANGES_1715}),
    "AAA_CC_CHAR_CHANGES_REMOVE":                   _t(**{"1715": AAA_CC_CHAR_CHANGES_REMOVE_1715}),
    "AAA_CC_LIFETIME":                              _t(**{"1715": AAA_CC_LIFETIME_1715}),
    "AAA_CC_LIFETIME_REMOVE":                       _t(**{"1715": AAA_CC_LIFETIME_REMOVE_1715}),
    "AAA_CC_LOWER_CASE":                            _t(**{"1715": AAA_CC_LOWER_CASE_1715}),
    "AAA_CC_LOWER_CASE_REMOVE":                     _t(**{"1715": AAA_CC_LOWER_CASE_REMOVE_1715}),
    "AAA_CC_MAX_LENGTH":                            _t(**{"1715": AAA_CC_MAX_LENGTH_1715}),
    "AAA_CC_MAX_LENGTH_REMOVE":                     _t(**{"1715": AAA_CC_MAX_LENGTH_REMOVE_1715}),
    "AAA_CC_MIN_LENGTH":                            _t(**{"1715": AAA_CC_MIN_LENGTH_1715}),
    "AAA_CC_MIN_LENGTH_REMOVE":                     _t(**{"1715": AAA_CC_MIN_LENGTH_REMOVE_1715}),
    "AAA_CC_NUMERIC_COUNT":                         _t(**{"1715": AAA_CC_NUMERIC_COUNT_1715}),
    "AAA_CC_NUMERIC_COUNT_REMOVE":                  _t(**{"1715": AAA_CC_NUMERIC_COUNT_REMOVE_1715}),
    "AAA_CC_SPECIAL_CASE":                          _t(**{"1715": AAA_CC_SPECIAL_CASE_1715}),
    "AAA_CC_SPECIAL_CASE_REMOVE":                   _t(**{"1715": AAA_CC_SPECIAL_CASE_REMOVE_1715}),
    "AAA_CC_UPPER_CASE":                            _t(**{"1715": AAA_CC_UPPER_CASE_1715}),
    "AAA_CC_UPPER_CASE_REMOVE":                     _t(**{"1715": AAA_CC_UPPER_CASE_REMOVE_1715}),
    "AAA_CC_CHARACTER_REPETITION":                  _t(**{"1715": AAA_CC_CHARACTER_REPETITION_1715}),
    "AAA_CC_CHARACTER_REPETITION_REMOVE":           _t(**{"1715": AAA_CC_CHARACTER_REPETITION_REMOVE_1715}),
    "AAA_CC_RESTRICT_CONSECUTIVE_LETTERS":          _t(**{"1715": AAA_CC_RESTRICT_CONSECUTIVE_LETTERS_1715}),
    "AAA_CC_RESTRICT_CONSECUTIVE_LETTERS_REMOVE":   _t(**{"1715": AAA_CC_RESTRICT_CONSECUTIVE_LETTERS_REMOVE_1715}),

    # §11. aaa server radius
    "AAA_SRV_RADIUS_DYNAMIC_AUTHOR":                _t(**{"1715": AAA_SRV_RADIUS_DYNAMIC_AUTHOR_1715}),
    "AAA_SRV_RADIUS_DYNAMIC_AUTHOR_REMOVE":         _t(**{"1715": AAA_SRV_RADIUS_DYNAMIC_AUTHOR_REMOVE_1715}),
    "AAA_SRV_RADIUS_DYNAMIC_AUTHOR_PORT":           _t(**{"1715": AAA_SRV_RADIUS_DYNAMIC_AUTHOR_PORT_1715}),
    "AAA_SRV_RADIUS_DYNAMIC_AUTHOR_PORT_REMOVE":    _t(**{"1715": AAA_SRV_RADIUS_DYNAMIC_AUTHOR_PORT_REMOVE_1715}),
    "AAA_SRV_RADIUS_DYNAMIC_AUTHOR_CLIENT":         _t(**{"1715": AAA_SRV_RADIUS_DYNAMIC_AUTHOR_CLIENT_1715}),
    "AAA_SRV_RADIUS_DYNAMIC_AUTHOR_CLIENT_REMOVE":  _t(**{"1715": AAA_SRV_RADIUS_DYNAMIC_AUTHOR_CLIENT_REMOVE_1715}),
    "AAA_SRV_RADIUS_DYNAMIC_AUTHOR_CLIENT_DTLS":    _t(**{"1715": AAA_SRV_RADIUS_DYNAMIC_AUTHOR_CLIENT_DTLS_1715}),
    "AAA_SRV_RADIUS_DYNAMIC_AUTHOR_CLIENT_DTLS_REMOVE": _t(**{"1715": AAA_SRV_RADIUS_DYNAMIC_AUTHOR_CLIENT_DTLS_REMOVE_1715}),
    "AAA_SRV_RADIUS_DYNAMIC_AUTHOR_CLIENT_SERVER_KEY": _t(**{"1715": AAA_SRV_RADIUS_DYNAMIC_AUTHOR_CLIENT_SERVER_KEY_1715}),
    "AAA_SRV_RADIUS_DYNAMIC_AUTHOR_CLIENT_SERVER_KEY_REMOVE": _t(**{"1715": AAA_SRV_RADIUS_DYNAMIC_AUTHOR_CLIENT_SERVER_KEY_REMOVE_1715}),
    "AAA_SRV_RADIUS_DYNAMIC_AUTHOR_CLIENT_VRF":     _t(**{"1715": AAA_SRV_RADIUS_DYNAMIC_AUTHOR_CLIENT_VRF_1715}),
    "AAA_SRV_RADIUS_DYNAMIC_AUTHOR_CLIENT_VRF_REMOVE": _t(**{"1715": AAA_SRV_RADIUS_DYNAMIC_AUTHOR_CLIENT_VRF_REMOVE_1715}),
    "AAA_SRV_RADIUS_DYNAMIC_AUTHOR_CLIENT_VRF_SERVER_KEY": _t(**{"1715": AAA_SRV_RADIUS_DYNAMIC_AUTHOR_CLIENT_VRF_SERVER_KEY_1715}),
    "AAA_SRV_RADIUS_DYNAMIC_AUTHOR_CLIENT_VRF_SERVER_KEY_REMOVE": _t(**{"1715": AAA_SRV_RADIUS_DYNAMIC_AUTHOR_CLIENT_VRF_SERVER_KEY_REMOVE_1715}),
    "AAA_SRV_RADIUS_DYNAMIC_AUTHOR_TLS":            _t(**{"1715": AAA_SRV_RADIUS_DYNAMIC_AUTHOR_TLS_1715}),
    "AAA_SRV_RADIUS_DYNAMIC_AUTHOR_TLS_REMOVE":     _t(**{"1715": AAA_SRV_RADIUS_DYNAMIC_AUTHOR_TLS_REMOVE_1715}),
    "AAA_SRV_RADIUS_DYNAMIC_AUTHOR_TLS_PORT":       _t(**{"1715": AAA_SRV_RADIUS_DYNAMIC_AUTHOR_TLS_PORT_1715}),
    "AAA_SRV_RADIUS_DYNAMIC_AUTHOR_TLS_PORT_REMOVE":_t(**{"1715": AAA_SRV_RADIUS_DYNAMIC_AUTHOR_TLS_PORT_REMOVE_1715}),
    "AAA_SRV_RADIUS_DYNAMIC_AUTHOR_SERVER_KEY":     _t(**{"1715": AAA_SRV_RADIUS_DYNAMIC_AUTHOR_SERVER_KEY_1715}),
    "AAA_SRV_RADIUS_DYNAMIC_AUTHOR_SERVER_KEY_REMOVE": _t(**{"1715": AAA_SRV_RADIUS_DYNAMIC_AUTHOR_SERVER_KEY_REMOVE_1715}),
    "AAA_SRV_RADIUS_DYNAMIC_AUTHOR_DOMAIN_STRIPPING": _t(**{"1715": AAA_SRV_RADIUS_DYNAMIC_AUTHOR_DOMAIN_STRIPPING_1715}),
    "AAA_SRV_RADIUS_DYNAMIC_AUTHOR_DOMAIN_STRIPPING_REMOVE": _t(**{"1715": AAA_SRV_RADIUS_DYNAMIC_AUTHOR_DOMAIN_STRIPPING_REMOVE_1715}),
    "AAA_SRV_RADIUS_DYNAMIC_AUTHOR_DOMAIN_STRIPPING_R2L": _t(**{"1715": AAA_SRV_RADIUS_DYNAMIC_AUTHOR_DOMAIN_STRIPPING_R2L_1715}),
    "AAA_SRV_RADIUS_DYNAMIC_AUTHOR_DOMAIN_STRIPPING_R2L_REMOVE": _t(**{"1715": AAA_SRV_RADIUS_DYNAMIC_AUTHOR_DOMAIN_STRIPPING_R2L_REMOVE_1715}),
    "AAA_SRV_RADIUS_DYNAMIC_AUTHOR_DOMAIN_DELIMITER": _t(**{"1715": AAA_SRV_RADIUS_DYNAMIC_AUTHOR_DOMAIN_DELIMITER_1715}),
    "AAA_SRV_RADIUS_DYNAMIC_AUTHOR_DOMAIN_DELIMITER_REMOVE": _t(**{"1715": AAA_SRV_RADIUS_DYNAMIC_AUTHOR_DOMAIN_DELIMITER_REMOVE_1715}),
    "AAA_SRV_RADIUS_DYNAMIC_AUTHOR_AUTH_TYPE":      _t(**{"1715": AAA_SRV_RADIUS_DYNAMIC_AUTHOR_AUTH_TYPE_1715}),
    "AAA_SRV_RADIUS_DYNAMIC_AUTHOR_AUTH_TYPE_REMOVE": _t(**{"1715": AAA_SRV_RADIUS_DYNAMIC_AUTHOR_AUTH_TYPE_REMOVE_1715}),
    "AAA_SRV_RADIUS_DYNAMIC_AUTHOR_IGNORE_RETRANSMISSION": _t(**{"1715": AAA_SRV_RADIUS_DYNAMIC_AUTHOR_IGNORE_RETRANSMISSION_1715}),
    "AAA_SRV_RADIUS_DYNAMIC_AUTHOR_IGNORE_RETRANSMISSION_REMOVE": _t(**{"1715": AAA_SRV_RADIUS_DYNAMIC_AUTHOR_IGNORE_RETRANSMISSION_REMOVE_1715}),
    "AAA_SRV_RADIUS_DYNAMIC_AUTHOR_IGNORE_SERVER_KEY": _t(**{"1715": AAA_SRV_RADIUS_DYNAMIC_AUTHOR_IGNORE_SERVER_KEY_1715}),
    "AAA_SRV_RADIUS_DYNAMIC_AUTHOR_IGNORE_SERVER_KEY_REMOVE": _t(**{"1715": AAA_SRV_RADIUS_DYNAMIC_AUTHOR_IGNORE_SERVER_KEY_REMOVE_1715}),
    "AAA_SRV_RADIUS_DYNAMIC_AUTHOR_IGNORE_SESSION_KEY": _t(**{"1715": AAA_SRV_RADIUS_DYNAMIC_AUTHOR_IGNORE_SESSION_KEY_1715}),
    "AAA_SRV_RADIUS_DYNAMIC_AUTHOR_IGNORE_SESSION_KEY_REMOVE": _t(**{"1715": AAA_SRV_RADIUS_DYNAMIC_AUTHOR_IGNORE_SESSION_KEY_REMOVE_1715}),

    "AAA_SRV_RADIUS_POLICY_DEVICE":                 _t(**{"1715": AAA_SRV_RADIUS_POLICY_DEVICE_1715}),
    "AAA_SRV_RADIUS_POLICY_DEVICE_REMOVE":          _t(**{"1715": AAA_SRV_RADIUS_POLICY_DEVICE_REMOVE_1715}),
    "AAA_SRV_RADIUS_POLICY_DEVICE_ACCOUNTING_PORT": _t(**{"1715": AAA_SRV_RADIUS_POLICY_DEVICE_ACCOUNTING_PORT_1715}),
    "AAA_SRV_RADIUS_POLICY_DEVICE_ACCOUNTING_PORT_REMOVE": _t(**{"1715": AAA_SRV_RADIUS_POLICY_DEVICE_ACCOUNTING_PORT_REMOVE_1715}),
    "AAA_SRV_RADIUS_POLICY_DEVICE_AUTHENTICATION_PORT": _t(**{"1715": AAA_SRV_RADIUS_POLICY_DEVICE_AUTHENTICATION_PORT_1715}),
    "AAA_SRV_RADIUS_POLICY_DEVICE_AUTHENTICATION_PORT_REMOVE": _t(**{"1715": AAA_SRV_RADIUS_POLICY_DEVICE_AUTHENTICATION_PORT_REMOVE_1715}),
    "AAA_SRV_RADIUS_POLICY_DEVICE_CLIENT":          _t(**{"1715": AAA_SRV_RADIUS_POLICY_DEVICE_CLIENT_1715}),
    "AAA_SRV_RADIUS_POLICY_DEVICE_CLIENT_REMOVE":   _t(**{"1715": AAA_SRV_RADIUS_POLICY_DEVICE_CLIENT_REMOVE_1715}),
    "AAA_SRV_RADIUS_POLICY_DEVICE_CLIENT_PORT":     _t(**{"1715": AAA_SRV_RADIUS_POLICY_DEVICE_CLIENT_PORT_1715}),
    "AAA_SRV_RADIUS_POLICY_DEVICE_CLIENT_PORT_REMOVE": _t(**{"1715": AAA_SRV_RADIUS_POLICY_DEVICE_CLIENT_PORT_REMOVE_1715}),
    "AAA_SRV_RADIUS_POLICY_DEVICE_CLIENT_KEY":      _t(**{"1715": AAA_SRV_RADIUS_POLICY_DEVICE_CLIENT_KEY_1715}),
    "AAA_SRV_RADIUS_POLICY_DEVICE_CLIENT_KEY_REMOVE": _t(**{"1715": AAA_SRV_RADIUS_POLICY_DEVICE_CLIENT_KEY_REMOVE_1715}),
    "AAA_SRV_RADIUS_POLICY_DEVICE_CLIENT_VRF":      _t(**{"1715": AAA_SRV_RADIUS_POLICY_DEVICE_CLIENT_VRF_1715}),
    "AAA_SRV_RADIUS_POLICY_DEVICE_CLIENT_VRF_REMOVE": _t(**{"1715": AAA_SRV_RADIUS_POLICY_DEVICE_CLIENT_VRF_REMOVE_1715}),
    "AAA_SRV_RADIUS_POLICY_DEVICE_KEY":             _t(**{"1715": AAA_SRV_RADIUS_POLICY_DEVICE_KEY_1715}),
    "AAA_SRV_RADIUS_POLICY_DEVICE_KEY_REMOVE":      _t(**{"1715": AAA_SRV_RADIUS_POLICY_DEVICE_KEY_REMOVE_1715}),
    "AAA_SRV_RADIUS_POLICY_DEVICE_MESSAGE_AUTHENTICATOR_IGNORE": _t(**{"1715": AAA_SRV_RADIUS_POLICY_DEVICE_MESSAGE_AUTHENTICATOR_IGNORE_1715}),
    "AAA_SRV_RADIUS_POLICY_DEVICE_MESSAGE_AUTHENTICATOR_IGNORE_REMOVE": _t(**{"1715": AAA_SRV_RADIUS_POLICY_DEVICE_MESSAGE_AUTHENTICATOR_IGNORE_REMOVE_1715}),

    # §12. native/radius
    "RADIUS_FILTER":                                _t(**{"1715": RADIUS_FILTER_1715}),
    "RADIUS_FILTER_REMOVE":                         _t(**{"1715": RADIUS_FILTER_REMOVE_1715}),
    "RADIUS_SERVER_CREATE":                         _t(**{"1715": RADIUS_SERVER_CREATE_1715}),
    "RADIUS_SERVER_CREATE_REMOVE":                  _t(**{"1715": RADIUS_SERVER_CREATE_REMOVE_1715}),
        "RADIUS_SERVER_ADDRESS_IPV4":                   _t(**{"1715": RADIUS_SERVER_ADDRESS_IPV4_1715}),
    "RADIUS_SERVER_ADDRESS_IPV4_REMOVE":            _t(**{"1715": RADIUS_SERVER_ADDRESS_IPV4_REMOVE_1715}),
    "RADIUS_SERVER_ADDRESS_IPV6":                   _t(**{"1715": RADIUS_SERVER_ADDRESS_IPV6_1715}),
    "RADIUS_SERVER_ADDRESS_IPV6_REMOVE":            _t(**{"1715": RADIUS_SERVER_ADDRESS_IPV6_REMOVE_1715}),
    "RADIUS_SERVER_ADDRESS_FQDN":                   _t(**{"1715": RADIUS_SERVER_ADDRESS_FQDN_1715}),
    "RADIUS_SERVER_ADDRESS_FQDN_REMOVE":            _t(**{"1715": RADIUS_SERVER_ADDRESS_FQDN_REMOVE_1715}),
    "RADIUS_SERVER_ADDRESS_PORTS":                  _t(**{"1715": RADIUS_SERVER_ADDRESS_PORTS_1715}),
    "RADIUS_SERVER_ADDRESS_PORTS_REMOVE":           _t(**{"1715": RADIUS_SERVER_ADDRESS_PORTS_REMOVE_1715}),
    "RADIUS_SERVER_TIMEOUT":                        _t(**{"1715": RADIUS_SERVER_TIMEOUT_1715}),
    "RADIUS_SERVER_TIMEOUT_REMOVE":                 _t(**{"1715": RADIUS_SERVER_TIMEOUT_REMOVE_1715}),
    "RADIUS_SERVER_TLS_PORT":                       _t(**{"1715": RADIUS_SERVER_TLS_PORT_1715}),
    "RADIUS_SERVER_TLS_PORT_REMOVE":                _t(**{"1715": RADIUS_SERVER_TLS_PORT_REMOVE_1715}),
    "RADIUS_SERVER_TLS_TRUSTPOINT_CLIENT":          _t(**{"1715": RADIUS_SERVER_TLS_TRUSTPOINT_CLIENT_1715}),
    "RADIUS_SERVER_TLS_TRUSTPOINT_CLIENT_REMOVE":   _t(**{"1715": RADIUS_SERVER_TLS_TRUSTPOINT_CLIENT_REMOVE_1715}),
    "RADIUS_SERVER_TLS_TRUSTPOINT_SERVER":          _t(**{"1715": RADIUS_SERVER_TLS_TRUSTPOINT_SERVER_1715}),
    "RADIUS_SERVER_TLS_TRUSTPOINT_SERVER_REMOVE":   _t(**{"1715": RADIUS_SERVER_TLS_TRUSTPOINT_SERVER_REMOVE_1715}),
    "RADIUS_SERVER_TLS_MATCH_SERVER_IDENTITY_HOSTNAME": _t(**{"1715": RADIUS_SERVER_TLS_MATCH_SERVER_IDENTITY_HOSTNAME_1715}),
    "RADIUS_SERVER_TLS_MATCH_SERVER_IDENTITY_HOSTNAME_REMOVE": _t(**{"1715": RADIUS_SERVER_TLS_MATCH_SERVER_IDENTITY_HOSTNAME_REMOVE_1715}),
    "RADIUS_SERVER_AUTOMATE_TESTER":                _t(**{"1715": RADIUS_SERVER_AUTOMATE_TESTER_1715}),
    "RADIUS_SERVER_AUTOMATE_TESTER_REMOVE":         _t(**{"1715": RADIUS_SERVER_AUTOMATE_TESTER_REMOVE_1715}),
    "RADIUS_SERVER_AUTOMATE_TESTER_PROBE_ON_CONFIG": _t(**{"1715": RADIUS_SERVER_AUTOMATE_TESTER_PROBE_ON_CONFIG_1715}),
    "RADIUS_SERVER_AUTOMATE_TESTER_PROBE_ON_CONFIG_REMOVE": _t(**{"1715": RADIUS_SERVER_AUTOMATE_TESTER_PROBE_ON_CONFIG_REMOVE_1715}),
    "RADIUS_SERVER_AUTOMATE_TESTER_IDLE_TIME":      _t(**{"1715": RADIUS_SERVER_AUTOMATE_TESTER_IDLE_TIME_1715}),
    "RADIUS_SERVER_AUTOMATE_TESTER_IDLE_TIME_REMOVE": _t(**{"1715": RADIUS_SERVER_AUTOMATE_TESTER_IDLE_TIME_REMOVE_1715}),
    "RADIUS_SERVER_AUTOMATE_TESTER_IGNORE_AUTH_PORT": _t(**{"1715": RADIUS_SERVER_AUTOMATE_TESTER_IGNORE_AUTH_PORT_1715}),
    "RADIUS_SERVER_AUTOMATE_TESTER_IGNORE_AUTH_PORT_REMOVE": _t(**{"1715": RADIUS_SERVER_AUTOMATE_TESTER_IGNORE_AUTH_PORT_REMOVE_1715}),
    "RADIUS_SERVER_AUTOMATE_TESTER_IGNORE_ACCT_PORT": _t(**{"1715": RADIUS_SERVER_AUTOMATE_TESTER_IGNORE_ACCT_PORT_1715}),
    "RADIUS_SERVER_AUTOMATE_TESTER_IGNORE_ACCT_PORT_REMOVE": _t(**{"1715": RADIUS_SERVER_AUTOMATE_TESTER_IGNORE_ACCT_PORT_REMOVE_1715}),
    "RADIUS_SERVER_AUTOMATE_TESTER_VRF":            _t(**{"1715": RADIUS_SERVER_AUTOMATE_TESTER_VRF_1715}),
    "RADIUS_SERVER_AUTOMATE_TESTER_VRF_REMOVE":     _t(**{"1715": RADIUS_SERVER_AUTOMATE_TESTER_VRF_REMOVE_1715}),
    "RADIUS_SERVER_BACKOFF_EXPONENTIAL":            _t(**{"1715": RADIUS_SERVER_BACKOFF_EXPONENTIAL_1715}),
    "RADIUS_SERVER_BACKOFF_EXPONENTIAL_REMOVE":     _t(**{"1715": RADIUS_SERVER_BACKOFF_EXPONENTIAL_REMOVE_1715}),
    "RADIUS_SERVER_PAC_KEY":                        _t(**{"1715": RADIUS_SERVER_PAC_KEY_1715}),
    "RADIUS_SERVER_PAC_KEY_REMOVE":                 _t(**{"1715": RADIUS_SERVER_PAC_KEY_REMOVE_1715}),
    "RADIUS_SERVER_KEY":                            _t(**{"1715": RADIUS_SERVER_KEY_1715}),
    "RADIUS_SERVER_KEY_REMOVE":                     _t(**{"1715": RADIUS_SERVER_KEY_REMOVE_1715}),
    "RADIUS_SERVER_RETRANSMIT":                     _t(**{"1715": RADIUS_SERVER_RETRANSMIT_1715}),
    "RADIUS_SERVER_RETRANSMIT_REMOVE":              _t(**{"1715": RADIUS_SERVER_RETRANSMIT_REMOVE_1715}),
    "RADIUS_SERVER_DSCP":                           _t(**{"1715": RADIUS_SERVER_DSCP_1715}),
    "RADIUS_SERVER_DSCP_REMOVE":                    _t(**{"1715": RADIUS_SERVER_DSCP_REMOVE_1715}),

    # §13. native/ldap
    "LDAP_SERVER_CREATE":                           _t(**{"1715": LDAP_SERVER_CREATE_1715}),
    "LDAP_SERVER_CREATE_REMOVE":                    _t(**{"1715": LDAP_SERVER_CREATE_REMOVE_1715}),
    "LDAP_SERVER_IPV4":                             _t(**{"1715": LDAP_SERVER_IPV4_1715}),
    "LDAP_SERVER_IPV4_REMOVE":                      _t(**{"1715": LDAP_SERVER_IPV4_REMOVE_1715}),
    "LDAP_SERVER_IPV6":                             _t(**{"1715": LDAP_SERVER_IPV6_1715}),
    "LDAP_SERVER_IPV6_REMOVE":                      _t(**{"1715": LDAP_SERVER_IPV6_REMOVE_1715}),
    "LDAP_SERVER_FQDN":                             _t(**{"1715": LDAP_SERVER_FQDN_1715}),
    "LDAP_SERVER_FQDN_REMOVE":                      _t(**{"1715": LDAP_SERVER_FQDN_REMOVE_1715}),
    "LDAP_SERVER_AUTHENTICATION_BIND_FIRST":        _t(**{"1715": LDAP_SERVER_AUTHENTICATION_BIND_FIRST_1715}),
    "LDAP_SERVER_AUTHENTICATION_BIND_FIRST_REMOVE": _t(**{"1715": LDAP_SERVER_AUTHENTICATION_BIND_FIRST_REMOVE_1715}),
    "LDAP_SERVER_AUTHENTICATION_BIND_FIRST_NO_AUTHZ": _t(**{"1715": LDAP_SERVER_AUTHENTICATION_BIND_FIRST_NO_AUTHZ_1715}),
    "LDAP_SERVER_AUTHENTICATION_BIND_FIRST_NO_AUTHZ_REMOVE": _t(**{"1715": LDAP_SERVER_AUTHENTICATION_BIND_FIRST_NO_AUTHZ_REMOVE_1715}),
    "LDAP_SERVER_AUTHENTICATION_COMPARE":           _t(**{"1715": LDAP_SERVER_AUTHENTICATION_COMPARE_1715}),
    "LDAP_SERVER_AUTHENTICATION_COMPARE_REMOVE":    _t(**{"1715": LDAP_SERVER_AUTHENTICATION_COMPARE_REMOVE_1715}),
    "LDAP_SERVER_AUTOMATE_TESTER":                  _t(**{"1715": LDAP_SERVER_AUTOMATE_TESTER_1715}),
    "LDAP_SERVER_AUTOMATE_TESTER_REMOVE":           _t(**{"1715": LDAP_SERVER_AUTOMATE_TESTER_REMOVE_1715}),
    "LDAP_SERVER_BASE_DN":                          _t(**{"1715": LDAP_SERVER_BASE_DN_1715}),
    "LDAP_SERVER_BASE_DN_REMOVE":                   _t(**{"1715": LDAP_SERVER_BASE_DN_REMOVE_1715}),
    "LDAP_SERVER_DEADTIME":                         _t(**{"1715": LDAP_SERVER_DEADTIME_1715}),
    "LDAP_SERVER_DEADTIME_REMOVE":                  _t(**{"1715": LDAP_SERVER_DEADTIME_REMOVE_1715}),
    "LDAP_SERVER_TIMEOUT_RETRANSMIT":               _t(**{"1715": LDAP_SERVER_TIMEOUT_RETRANSMIT_1715}),
    "LDAP_SERVER_TIMEOUT_RETRANSMIT_REMOVE":        _t(**{"1715": LDAP_SERVER_TIMEOUT_RETRANSMIT_REMOVE_1715}),
    "LDAP_SERVER_BIND_AUTHENTICATE":                _t(**{"1715": LDAP_SERVER_BIND_AUTHENTICATE_1715}),
    "LDAP_SERVER_BIND_AUTHENTICATE_REMOVE":         _t(**{"1715": LDAP_SERVER_BIND_AUTHENTICATE_REMOVE_1715}),
    "LDAP_SERVER_BIND_ROOT_DN":                     _t(**{"1715": LDAP_SERVER_BIND_ROOT_DN_1715}),
    "LDAP_SERVER_BIND_ROOT_DN_REMOVE":              _t(**{"1715": LDAP_SERVER_BIND_ROOT_DN_REMOVE_1715}),
    "LDAP_SERVER_BIND_USERNAME":                    _t(**{"1715": LDAP_SERVER_BIND_USERNAME_1715}),
    "LDAP_SERVER_BIND_USERNAME_REMOVE":             _t(**{"1715": LDAP_SERVER_BIND_USERNAME_REMOVE_1715}),
    "LDAP_SERVER_BIND_PASSWORD":                    _t(**{"1715": LDAP_SERVER_BIND_PASSWORD_1715}),
    "LDAP_SERVER_BIND_PASSWORD_REMOVE":             _t(**{"1715": LDAP_SERVER_BIND_PASSWORD_REMOVE_1715}),
    "LDAP_SERVER_MODE_SECURE":                      _t(**{"1715": LDAP_SERVER_MODE_SECURE_1715}),
    "LDAP_SERVER_MODE_SECURE_REMOVE":               _t(**{"1715": LDAP_SERVER_MODE_SECURE_REMOVE_1715}),
    "LDAP_SERVER_MODE_SECURE_NO_NEGOTIATION":       _t(**{"1715": LDAP_SERVER_MODE_SECURE_NO_NEGOTIATION_1715}),
    "LDAP_SERVER_MODE_SECURE_NO_NEGOTIATION_REMOVE": _t(**{"1715": LDAP_SERVER_MODE_SECURE_NO_NEGOTIATION_REMOVE_1715}),
    "LDAP_SERVER_SEARCH_TYPE_NESTED":               _t(**{"1715": LDAP_SERVER_SEARCH_TYPE_NESTED_1715}),
    "LDAP_SERVER_SEARCH_TYPE_NESTED_REMOVE":        _t(**{"1715": LDAP_SERVER_SEARCH_TYPE_NESTED_REMOVE_1715}),
    "LDAP_SERVER_SEARCH_FILTER_USER_OBJECT_TYPE":   _t(**{"1715": LDAP_SERVER_SEARCH_FILTER_USER_OBJECT_TYPE_1715}),
    "LDAP_SERVER_SEARCH_FILTER_USER_OBJECT_TYPE_REMOVE": _t(**{"1715": LDAP_SERVER_SEARCH_FILTER_USER_OBJECT_TYPE_REMOVE_1715}),
    "LDAP_SERVER_SECURE_CIPHER":                    _t(**{"1715": LDAP_SERVER_SECURE_CIPHER_1715}),
    "LDAP_SERVER_SECURE_CIPHER_REMOVE":             _t(**{"1715": LDAP_SERVER_SECURE_CIPHER_REMOVE_1715}),
    "LDAP_SERVER_SECURE_TRUSTPOINT":                _t(**{"1715": LDAP_SERVER_SECURE_TRUSTPOINT_1715}),
    "LDAP_SERVER_SECURE_TRUSTPOINT_REMOVE":         _t(**{"1715": LDAP_SERVER_SECURE_TRUSTPOINT_REMOVE_1715}),
    "LDAP_SERVER_TRANSPORT_PORT":                   _t(**{"1715": LDAP_SERVER_TRANSPORT_PORT_1715}),
    "LDAP_SERVER_TRANSPORT_PORT_REMOVE":            _t(**{"1715": LDAP_SERVER_TRANSPORT_PORT_REMOVE_1715}),

    # §14. native/radius-server
    "RS_ATTRIBUTE_4":                               _t(**{"1715": RS_ATTRIBUTE_4_1715}),
    "RS_ATTRIBUTE_4_REMOVE":                        _t(**{"1715": RS_ATTRIBUTE_4_REMOVE_1715}),
    "RS_ATTRIBUTE_SEND":                            _t(**{"1715": RS_ATTRIBUTE_SEND_1715}),
    "RS_ATTRIBUTE_SEND_REMOVE":                     _t(**{"1715": RS_ATTRIBUTE_SEND_REMOVE_1715}),
    "RS_ATTRIBUTE_25_ACCESS_REQUEST_INCLUDE":       _t(**{"1715": RS_ATTRIBUTE_25_ACCESS_REQUEST_INCLUDE_1715}),
    "RS_ATTRIBUTE_25_ACCESS_REQUEST_INCLUDE_REMOVE": _t(**{"1715": RS_ATTRIBUTE_25_ACCESS_REQUEST_INCLUDE_REMOVE_1715}),
    "RS_ATTRIBUTE_31_MAC":                          _t(**{"1715": RS_ATTRIBUTE_31_MAC_1715}),
    "RS_ATTRIBUTE_31_MAC_REMOVE":                   _t(**{"1715": RS_ATTRIBUTE_31_MAC_REMOVE_1715}),
    "RS_ATTRIBUTE_31_SEND":                         _t(**{"1715": RS_ATTRIBUTE_31_SEND_1715}),
    "RS_ATTRIBUTE_31_SEND_REMOVE":                  _t(**{"1715": RS_ATTRIBUTE_31_SEND_REMOVE_1715}),
    "RS_ATTRIBUTE_11_DEFAULT_DIRECTION":            _t(**{"1715": RS_ATTRIBUTE_11_DEFAULT_DIRECTION_1715}),
    "RS_ATTRIBUTE_11_DEFAULT_DIRECTION_REMOVE":     _t(**{"1715": RS_ATTRIBUTE_11_DEFAULT_DIRECTION_REMOVE_1715}),
    "RS_ATTRIBUTE_11_OPTIONAL":                     _t(**{"1715": RS_ATTRIBUTE_11_OPTIONAL_1715}),
    "RS_ATTRIBUTE_11_OPTIONAL_REMOVE":              _t(**{"1715": RS_ATTRIBUTE_11_OPTIONAL_REMOVE_1715}),
    "RS_WIRELESS_ACCOUNTING_NAS_PORT_ID_EXCLUDE":   _t(**{"1715": RS_WIRELESS_ACCOUNTING_NAS_PORT_ID_EXCLUDE_1715}),
    "RS_WIRELESS_ACCOUNTING_NAS_PORT_ID_EXCLUDE_REMOVE": _t(**{"1715": RS_WIRELESS_ACCOUNTING_NAS_PORT_ID_EXCLUDE_REMOVE_1715}),
    "RS_WIRELESS_ACCOUNTING_USERNAME_CASE":         _t(**{"1715": RS_WIRELESS_ACCOUNTING_USERNAME_CASE_1715}),
    "RS_WIRELESS_ACCOUNTING_USERNAME_CASE_REMOVE":  _t(**{"1715": RS_WIRELESS_ACCOUNTING_USERNAME_CASE_REMOVE_1715}),
    "RS_WIRELESS_ACCOUNTING_USERNAME_DELIMITER":    _t(**{"1715": RS_WIRELESS_ACCOUNTING_USERNAME_DELIMITER_1715}),
    "RS_WIRELESS_ACCOUNTING_USERNAME_DELIMITER_REMOVE": _t(**{"1715": RS_WIRELESS_ACCOUNTING_USERNAME_DELIMITER_REMOVE_1715}),
    "RS_WIRELESS_ACCOUNTING_CALL_STATION_ID":       _t(**{"1715": RS_WIRELESS_ACCOUNTING_CALL_STATION_ID_1715}),
    "RS_WIRELESS_ACCOUNTING_CALL_STATION_ID_REMOVE": _t(**{"1715": RS_WIRELESS_ACCOUNTING_CALL_STATION_ID_REMOVE_1715}),
    "RS_WIRELESS_ACCOUNTING_CALL_STATION_ID_CASE":  _t(**{"1715": RS_WIRELESS_ACCOUNTING_CALL_STATION_ID_CASE_1715}),
    "RS_WIRELESS_ACCOUNTING_CALL_STATION_ID_CASE_REMOVE": _t(**{"1715": RS_WIRELESS_ACCOUNTING_CALL_STATION_ID_CASE_REMOVE_1715}),
    "RS_WIRELESS_ACCOUNTING_MAC_DELIMITER":         _t(**{"1715": RS_WIRELESS_ACCOUNTING_MAC_DELIMITER_1715}),
    "RS_WIRELESS_ACCOUNTING_MAC_DELIMITER_REMOVE":  _t(**{"1715": RS_WIRELESS_ACCOUNTING_MAC_DELIMITER_REMOVE_1715}),
    "RS_WIRELESS_AUTHENTICATION_CALL_STATION_ID":   _t(**{"1715": RS_WIRELESS_AUTHENTICATION_CALL_STATION_ID_1715}),
    "RS_WIRELESS_AUTHENTICATION_CALL_STATION_ID_REMOVE": _t(**{"1715": RS_WIRELESS_AUTHENTICATION_CALL_STATION_ID_REMOVE_1715}),
    "RS_WIRELESS_AUTHENTICATION_CALL_STATION_ID_CASE": _t(**{"1715": RS_WIRELESS_AUTHENTICATION_CALL_STATION_ID_CASE_1715}),
    "RS_WIRELESS_AUTHENTICATION_CALL_STATION_ID_CASE_REMOVE": _t(**{"1715": RS_WIRELESS_AUTHENTICATION_CALL_STATION_ID_CASE_REMOVE_1715}),
    "RS_WIRELESS_AUTHENTICATION_MAC_DELIMITER":     _t(**{"1715": RS_WIRELESS_AUTHENTICATION_MAC_DELIMITER_1715}),
    "RS_WIRELESS_AUTHENTICATION_MAC_DELIMITER_REMOVE": _t(**{"1715": RS_WIRELESS_AUTHENTICATION_MAC_DELIMITER_REMOVE_1715}),
    "RS_WIRELESS_ATTR44":                           _t(**{"1715": RS_WIRELESS_ATTR44_1715}),
    "RS_WIRELESS_ATTR44_REMOVE":                    _t(**{"1715": RS_WIRELESS_ATTR44_REMOVE_1715}),
    "RS_WIRELESS_ATTR44_INCLUDE_IN_ACCESS_REQ":     _t(**{"1715": RS_WIRELESS_ATTR44_INCLUDE_IN_ACCESS_REQ_1715}),
    "RS_WIRELESS_ATTR44_INCLUDE_IN_ACCESS_REQ_REMOVE": _t(**{"1715": RS_WIRELESS_ATTR44_INCLUDE_IN_ACCESS_REQ_REMOVE_1715}),
    "RS_WIRELESS_ATTR44_EXTEND_WITH_MAC":           _t(**{"1715": RS_WIRELESS_ATTR44_EXTEND_WITH_MAC_1715}),
    "RS_WIRELESS_ATTR44_EXTEND_WITH_MAC_REMOVE":    _t(**{"1715": RS_WIRELESS_ATTR44_EXTEND_WITH_MAC_REMOVE_1715}),
    "RS_WIRELESS_LOCATION_DELIVERY_OUT_OF_BAND":    _t(**{"1715": RS_WIRELESS_LOCATION_DELIVERY_OUT_OF_BAND_1715}),
    "RS_WIRELESS_LOCATION_DELIVERY_OUT_OF_BAND_REMOVE": _t(**{"1715": RS_WIRELESS_LOCATION_DELIVERY_OUT_OF_BAND_REMOVE_1715}),
    "RS_WIRELESS_LOCATION_DELIVERY_INCLUDE_LOCATION_CAPABLE": _t(**{"1715": RS_WIRELESS_LOCATION_DELIVERY_INCLUDE_LOCATION_CAPABLE_1715}),
    "RS_WIRELESS_LOCATION_DELIVERY_INCLUDE_LOCATION_CAPABLE_REMOVE": _t(**{"1715": RS_WIRELESS_LOCATION_DELIVERY_INCLUDE_LOCATION_CAPABLE_REMOVE_1715}),
    "RS_WIRELESS_LOCATION_CIVIC_LOCATION_ID":       _t(**{"1715": RS_WIRELESS_LOCATION_CIVIC_LOCATION_ID_1715}),
    "RS_WIRELESS_LOCATION_CIVIC_LOCATION_ID_REMOVE": _t(**{"1715": RS_WIRELESS_LOCATION_CIVIC_LOCATION_ID_REMOVE_1715}),
    "RS_WIRELESS_LOCATION_GEO_LOCATION_ID":         _t(**{"1715": RS_WIRELESS_LOCATION_GEO_LOCATION_ID_1715}),
    "RS_WIRELESS_LOCATION_GEO_LOCATION_ID_REMOVE":  _t(**{"1715": RS_WIRELESS_LOCATION_GEO_LOCATION_ID_REMOVE_1715}),
    "RS_WIRELESS_LOCATION_OPERATOR_ID":             _t(**{"1715": RS_WIRELESS_LOCATION_OPERATOR_ID_1715}),
    "RS_WIRELESS_LOCATION_OPERATOR_ID_REMOVE":      _t(**{"1715": RS_WIRELESS_LOCATION_OPERATOR_ID_REMOVE_1715}),
    "RS_CACHE_AUTHENTICATION_PROFILE":              _t(**{"1715": RS_CACHE_AUTHENTICATION_PROFILE_1715}),
    "RS_CACHE_AUTHENTICATION_PROFILE_REMOVE":       _t(**{"1715": RS_CACHE_AUTHENTICATION_PROFILE_REMOVE_1715}),
    "RS_CACHE_AUTHORIZATION_PROFILE":               _t(**{"1715": RS_CACHE_AUTHORIZATION_PROFILE_1715}),
    "RS_CACHE_AUTHORIZATION_PROFILE_REMOVE":        _t(**{"1715": RS_CACHE_AUTHORIZATION_PROFILE_REMOVE_1715}),
    "RS_CACHE_EXPIRY":                              _t(**{"1715": RS_CACHE_EXPIRY_1715}),
    "RS_CACHE_EXPIRY_REMOVE":                       _t(**{"1715": RS_CACHE_EXPIRY_REMOVE_1715}),
    "RS_CACHE_EXPIRY_OPTIONS":                      _t(**{"1715": RS_CACHE_EXPIRY_OPTIONS_1715}),
    "RS_CACHE_EXPIRY_OPTIONS_REMOVE":               _t(**{"1715": RS_CACHE_EXPIRY_OPTIONS_REMOVE_1715}),
    "RS_DEAD_CRITERIA":                             _t(**{"1715": RS_DEAD_CRITERIA_1715}),
    "RS_DEAD_CRITERIA_REMOVE":                      _t(**{"1715": RS_DEAD_CRITERIA_REMOVE_1715}),
    "RS_DEADTIME":                                  _t(**{"1715": RS_DEADTIME_1715}),
    "RS_DEADTIME_REMOVE":                           _t(**{"1715": RS_DEADTIME_REMOVE_1715}),
    "RS_DIRECTED_REQUEST":                          _t(**{"1715": RS_DIRECTED_REQUEST_1715}),
    "RS_DIRECTED_REQUEST_REMOVE":                   _t(**{"1715": RS_DIRECTED_REQUEST_REMOVE_1715}),
    "RS_HOST_CREATE":                               _t(**{"1715": RS_HOST_CREATE_1715}),
    "RS_HOST_CREATE_REMOVE":                        _t(**{"1715": RS_HOST_CREATE_REMOVE_1715}),
    "RS_HOST_PORTS":                                _t(**{"1715": RS_HOST_PORTS_1715}),
    "RS_HOST_PORTS_REMOVE":                         _t(**{"1715": RS_HOST_PORTS_REMOVE_1715}),
    "RS_HOST_RETRANSMIT":                           _t(**{"1715": RS_HOST_RETRANSMIT_1715}),
    "RS_HOST_RETRANSMIT_REMOVE":                    _t(**{"1715": RS_HOST_RETRANSMIT_REMOVE_1715}),
    "RS_HOST_TIMEOUT":                              _t(**{"1715": RS_HOST_TIMEOUT_1715}),
    "RS_HOST_TIMEOUT_REMOVE":                       _t(**{"1715": RS_HOST_TIMEOUT_REMOVE_1715}),
    "RS_HOST_KEY":                                  _t(**{"1715": RS_HOST_KEY_1715}),
    "RS_HOST_KEY_REMOVE":                           _t(**{"1715": RS_HOST_KEY_REMOVE_1715}),
    "RS_HOST_TEST_USERNAME":                        _t(**{"1715": RS_HOST_TEST_USERNAME_1715}),
    "RS_HOST_TEST_USERNAME_REMOVE":                 _t(**{"1715": RS_HOST_TEST_USERNAME_REMOVE_1715}),
    "RS_HOST_TEST_USERNAME_KEY":                    _t(**{"1715": RS_HOST_TEST_USERNAME_KEY_1715}),
    "RS_HOST_TEST_USERNAME_KEY_REMOVE":             _t(**{"1715": RS_HOST_TEST_USERNAME_KEY_REMOVE_1715}),
    "RS_KEY":                                       _t(**{"1715": RS_KEY_1715}),
    "RS_KEY_REMOVE":                                _t(**{"1715": RS_KEY_REMOVE_1715}),
    "RS_LOAD_BALANCE_LEAST_OUTSTANDING":            _t(**{"1715": RS_LOAD_BALANCE_LEAST_OUTSTANDING_1715}),
    "RS_LOAD_BALANCE_LEAST_OUTSTANDING_REMOVE":     _t(**{"1715": RS_LOAD_BALANCE_LEAST_OUTSTANDING_REMOVE_1715}),
    "RS_LOAD_BALANCE_BATCH_SIZE":                   _t(**{"1715": RS_LOAD_BALANCE_BATCH_SIZE_1715}),
    "RS_LOAD_BALANCE_BATCH_SIZE_REMOVE":            _t(**{"1715": RS_LOAD_BALANCE_BATCH_SIZE_REMOVE_1715}),
    "RS_LOAD_BALANCE_IGNORE_PREFERRED_SERVER":      _t(**{"1715": RS_LOAD_BALANCE_IGNORE_PREFERRED_SERVER_1715}),
    "RS_LOAD_BALANCE_IGNORE_PREFERRED_SERVER_REMOVE": _t(**{"1715": RS_LOAD_BALANCE_IGNORE_PREFERRED_SERVER_REMOVE_1715}),
    "RS_RETRANSMIT":                                _t(**{"1715": RS_RETRANSMIT_1715}),
    "RS_RETRANSMIT_REMOVE":                         _t(**{"1715": RS_RETRANSMIT_REMOVE_1715}),
    "RS_SOURCE_PORTS_EXTENDED":                     _t(**{"1715": RS_SOURCE_PORTS_EXTENDED_1715}),
    "RS_SOURCE_PORTS_EXTENDED_REMOVE":              _t(**{"1715": RS_SOURCE_PORTS_EXTENDED_REMOVE_1715}),
    "RS_TIMEOUT":                                   _t(**{"1715": RS_TIMEOUT_1715}),
    "RS_TIMEOUT_REMOVE":                            _t(**{"1715": RS_TIMEOUT_REMOVE_1715}),
    "RS_VSA_DISALLOW_UNKNOWN":                      _t(**{"1715": RS_VSA_DISALLOW_UNKNOWN_1715}),
    "RS_VSA_DISALLOW_UNKNOWN_REMOVE":               _t(**{"1715": RS_VSA_DISALLOW_UNKNOWN_REMOVE_1715}),
    "RS_VSA_SEND":                                  _t(**{"1715": RS_VSA_SEND_1715}),
    "RS_VSA_SEND_REMOVE":                           _t(**{"1715": RS_VSA_SEND_REMOVE_1715}),
    "RS_VSA_SEND_ACCOUNTING_ONLY":                  _t(**{"1715": RS_VSA_SEND_ACCOUNTING_ONLY_1715}),
    "RS_VSA_SEND_ACCOUNTING_ONLY_REMOVE":           _t(**{"1715": RS_VSA_SEND_ACCOUNTING_ONLY_REMOVE_1715}),
    "RS_VSA_SEND_AUTHENTICATION_ONLY":              _t(**{"1715": RS_VSA_SEND_AUTHENTICATION_ONLY_1715}),
    "RS_VSA_SEND_AUTHENTICATION_ONLY_REMOVE":       _t(**{"1715": RS_VSA_SEND_AUTHENTICATION_ONLY_REMOVE_1715}),
    "RS_VSA_SEND_ACCOUNTING_THREEGPP2":             _t(**{"1715": RS_VSA_SEND_ACCOUNTING_THREEGPP2_1715}),
    "RS_VSA_SEND_ACCOUNTING_THREEGPP2_REMOVE":      _t(**{"1715": RS_VSA_SEND_ACCOUNTING_THREEGPP2_REMOVE_1715}),
    "RS_VSA_SEND_AUTHENTICATION_THREEGPP2":         _t(**{"1715": RS_VSA_SEND_AUTHENTICATION_THREEGPP2_1715}),
    "RS_VSA_SEND_AUTHENTICATION_THREEGPP2_REMOVE":  _t(**{"1715": RS_VSA_SEND_AUTHENTICATION_THREEGPP2_REMOVE_1715}),
    "RS_VSA_SEND_CISCO_NAS_PORT":                   _t(**{"1715": RS_VSA_SEND_CISCO_NAS_PORT_1715}),
    "RS_VSA_SEND_CISCO_NAS_PORT_REMOVE":            _t(**{"1715": RS_VSA_SEND_CISCO_NAS_PORT_REMOVE_1715}),
    "RS_VSA_SEND_CISCO_NAS_PORT_THREEGPP2":         _t(**{"1715": RS_VSA_SEND_CISCO_NAS_PORT_THREEGPP2_1715}),
    "RS_VSA_SEND_CISCO_NAS_PORT_THREEGPP2_REMOVE":  _t(**{"1715": RS_VSA_SEND_CISCO_NAS_PORT_THREEGPP2_REMOVE_1715}),
    "RS_DSCP":                                      _t(**{"1715": RS_DSCP_1715}),
    "RS_DSCP_REMOVE":                               _t(**{"1715": RS_DSCP_REMOVE_1715}),

    # §15. source-interface under ip / ipv6
    "IP_RADIUS_SOURCE_INTERFACE":                   _t(**{"1715": IP_RADIUS_SOURCE_INTERFACE_1715}),
    "IP_RADIUS_SOURCE_INTERFACE_REMOVE":            _t(**{"1715": IP_RADIUS_SOURCE_INTERFACE_REMOVE_1715}),
    "IP_RADIUS_SOURCE_INTERFACE_VRF":               _t(**{"1715": IP_RADIUS_SOURCE_INTERFACE_VRF_1715}),
    "IP_RADIUS_SOURCE_INTERFACE_VRF_REMOVE":        _t(**{"1715": IP_RADIUS_SOURCE_INTERFACE_VRF_REMOVE_1715}),
    "IPV6_RADIUS_SOURCE_INTERFACE":                 _t(**{"1715": IPV6_RADIUS_SOURCE_INTERFACE_1715}),
    "IPV6_RADIUS_SOURCE_INTERFACE_REMOVE":          _t(**{"1715": IPV6_RADIUS_SOURCE_INTERFACE_REMOVE_1715}),
    "IPV6_RADIUS_SOURCE_INTERFACE_VRF":             _t(**{"1715": IPV6_RADIUS_SOURCE_INTERFACE_VRF_1715}),
    "IPV6_RADIUS_SOURCE_INTERFACE_VRF_REMOVE":      _t(**{"1715": IPV6_RADIUS_SOURCE_INTERFACE_VRF_REMOVE_1715}),
    "IP_TACACS_SOURCE_INTERFACE":                   _t(**{"1715": IP_TACACS_SOURCE_INTERFACE_1715}),
    "IP_TACACS_SOURCE_INTERFACE_REMOVE":            _t(**{"1715": IP_TACACS_SOURCE_INTERFACE_REMOVE_1715}),
    "IP_TACACS_SOURCE_INTERFACE_VRF":               _t(**{"1715": IP_TACACS_SOURCE_INTERFACE_VRF_1715}),
    "IP_TACACS_SOURCE_INTERFACE_VRF_REMOVE":        _t(**{"1715": IP_TACACS_SOURCE_INTERFACE_VRF_REMOVE_1715}),
        "IPV6_TACACS_SOURCE_INTERFACE":                 _t(**{"1715": IPV6_TACACS_SOURCE_INTERFACE_1715}),
    "IPV6_TACACS_SOURCE_INTERFACE_REMOVE":          _t(**{"1715": IPV6_TACACS_SOURCE_INTERFACE_REMOVE_1715}),
    "IPV6_TACACS_SOURCE_INTERFACE_VRF":             _t(**{"1715": IPV6_TACACS_SOURCE_INTERFACE_VRF_1715}),
    "IPV6_TACACS_SOURCE_INTERFACE_VRF_REMOVE":      _t(**{"1715": IPV6_TACACS_SOURCE_INTERFACE_VRF_REMOVE_1715}),

    # §16. native/tacacs
    "TACACS_SERVER_CREATE":                         _t(**{"1715": TACACS_SERVER_CREATE_1715}),
    "TACACS_SERVER_CREATE_REMOVE":                  _t(**{"1715": TACACS_SERVER_CREATE_REMOVE_1715}),
    "TACACS_SERVER_ADDRESS_IPV4":                   _t(**{"1715": TACACS_SERVER_ADDRESS_IPV4_1715}),
    "TACACS_SERVER_ADDRESS_IPV4_REMOVE":            _t(**{"1715": TACACS_SERVER_ADDRESS_IPV4_REMOVE_1715}),
    "TACACS_SERVER_ADDRESS_IPV6":                   _t(**{"1715": TACACS_SERVER_ADDRESS_IPV6_1715}),
    "TACACS_SERVER_ADDRESS_IPV6_REMOVE":            _t(**{"1715": TACACS_SERVER_ADDRESS_IPV6_REMOVE_1715}),
    "TACACS_SERVER_ADDRESS_FQDN":                   _t(**{"1715": TACACS_SERVER_ADDRESS_FQDN_1715}),
    "TACACS_SERVER_ADDRESS_FQDN_REMOVE":            _t(**{"1715": TACACS_SERVER_ADDRESS_FQDN_REMOVE_1715}),
    "TACACS_SERVER_PORT":                           _t(**{"1715": TACACS_SERVER_PORT_1715}),
    "TACACS_SERVER_PORT_REMOVE":                    _t(**{"1715": TACACS_SERVER_PORT_REMOVE_1715}),
    "TACACS_SERVER_TIMEOUT":                        _t(**{"1715": TACACS_SERVER_TIMEOUT_1715}),
    "TACACS_SERVER_TIMEOUT_REMOVE":                 _t(**{"1715": TACACS_SERVER_TIMEOUT_REMOVE_1715}),
    "TACACS_SERVER_KEY":                            _t(**{"1715": TACACS_SERVER_KEY_1715}),
    "TACACS_SERVER_KEY_REMOVE":                     _t(**{"1715": TACACS_SERVER_KEY_REMOVE_1715}),

    # §17. native/tacacs-server
    "TS_TIMEOUT":                                   _t(**{"1715": TS_TIMEOUT_1715}),
    "TS_TIMEOUT_REMOVE":                            _t(**{"1715": TS_TIMEOUT_REMOVE_1715}),
    "TS_DIRECTED_REQUEST":                          _t(**{"1715": TS_DIRECTED_REQUEST_1715}),
    "TS_DIRECTED_REQUEST_REMOVE":                   _t(**{"1715": TS_DIRECTED_REQUEST_REMOVE_1715}),
    "TS_DIRECTED_REQUEST_RESTRICTED":               _t(**{"1715": TS_DIRECTED_REQUEST_RESTRICTED_1715}),
    "TS_DIRECTED_REQUEST_RESTRICTED_REMOVE":        _t(**{"1715": TS_DIRECTED_REQUEST_RESTRICTED_REMOVE_1715}),
    "TS_DIRECTED_REQUEST_NO_TRUNCATE":              _t(**{"1715": TS_DIRECTED_REQUEST_NO_TRUNCATE_1715}),
    "TS_DIRECTED_REQUEST_NO_TRUNCATE_REMOVE":       _t(**{"1715": TS_DIRECTED_REQUEST_NO_TRUNCATE_REMOVE_1715}),
    "TS_KEY":                                       _t(**{"1715": TS_KEY_1715}),
    "TS_KEY_REMOVE":                                _t(**{"1715": TS_KEY_REMOVE_1715}),
    "TS_ATTRIBUTE_ALLOW_UNKNOWN":                   _t(**{"1715": TS_ATTRIBUTE_ALLOW_UNKNOWN_1715}),
    "TS_ATTRIBUTE_ALLOW_UNKNOWN_REMOVE":            _t(**{"1715": TS_ATTRIBUTE_ALLOW_UNKNOWN_REMOVE_1715}),

    # §18. username[name]
    "USER_COMMON_CRITERIA_POLICY":                  _t(**{"1715": USER_COMMON_CRITERIA_POLICY_1715}),
    "USER_COMMON_CRITERIA_POLICY_REMOVE":           _t(**{"1715": USER_COMMON_CRITERIA_POLICY_REMOVE_1715}),
    "USER_COMMON_CRITERIA_PASSWORD":                _t(**{"1715": USER_COMMON_CRITERIA_PASSWORD_1715}),
    "USER_COMMON_CRITERIA_PASSWORD_REMOVE":         _t(**{"1715": USER_COMMON_CRITERIA_PASSWORD_REMOVE_1715}),
    "USER_AAA_ATTRIBUTE_LIST":                      _t(**{"1715": USER_AAA_ATTRIBUTE_LIST_1715}),
    "USER_AAA_ATTRIBUTE_LIST_REMOVE":               _t(**{"1715": USER_AAA_ATTRIBUTE_LIST_REMOVE_1715}),

    # §19. native/security
    "SEC_AUTHENTICATION_FAILURE_RATE":              _t(**{"1715": SEC_AUTHENTICATION_FAILURE_RATE_1715}),
    "SEC_AUTHENTICATION_FAILURE_RATE_REMOVE":       _t(**{"1715": SEC_AUTHENTICATION_FAILURE_RATE_REMOVE_1715}),
    "SEC_PASSWORDS_MIN_LENGTH":                     _t(**{"1715": SEC_PASSWORDS_MIN_LENGTH_1715}),
    "SEC_PASSWORDS_MIN_LENGTH_REMOVE":              _t(**{"1715": SEC_PASSWORDS_MIN_LENGTH_REMOVE_1715}),
}


    
    
 from string import Template
from xml.sax.saxutils import escape

from string import Template

NC  = "urn:ietf:params:xml:ns:netconf:base:1.0"
N   = "http://cisco.com/ns/yang/Cisco-IOS-XE-native"
AAA = "http://cisco.com/ns/yang/Cisco-IOS-XE-aaa"

RAW = {"methods", "opt_extra", "opt_gc"}

def build_edit_config(label, values, train):
    v = dict(values)
    for k in ("groups", "exec_groups"):
        if k in v and isinstance(v[k], (list, tuple)):
            v[k] = "".join(f"<group>{g}</group>" for g in v[k])
    frag = Template(TEMPLATES[label][train]).substitute(v)

    if label.startswith("SEC_"):
        inner = frag
    elif label.startswith("LDAP_"):
        inner = f'<ldap xmlns="{AAA}">{frag}</ldap>'
    elif label.startswith("AAA_"):
        inner = f'<aaa xmlns="{AAA}">{frag}</aaa>'
    elif label.startswith("TACACS_"):
        inner = f'<tacacs xmlns="{AAA}">{frag}</tacacs>'
    elif label.startswith("TS_"):
        inner = f'<tacacs-server xmlns="{AAA}">{frag}</tacacs-server>'
    elif label.startswith("RADIUS_"):
        inner = f'<radius xmlns="{AAA}">{frag}</radius>'
    elif label.startswith("IPV6_"):
        inner = f'<ipv6 xmlns="{AAA}">{frag}</ipv6>'
    elif label.startswith("IP_"):
        inner = f'<ip xmlns="{AAA}">{frag}</ip>'
    elif label.startswith("USER_"):
        inner = f'<username xmlns="{AAA}"><name>{v["uname"]}</name>{frag}</username>'
    elif label.startswith("RS_"):
        inner = f'<radius-server xmlns="{AAA}">{frag}</radius-server>'
    else:
        raise KeyError(f"No anchor rule for label {label!r}")

    return (
        f'<config xmlns="{NC}" xmlns:nc="{NC}">'
        f'<native xmlns="{N}">{inner}</native>'
        f'</config>'
    )