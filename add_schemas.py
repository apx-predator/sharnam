from __future__ import annotations

from enum import Enum
from typing import Literal, Optional, Annotated, Union
from pydantic import BaseModel, Field, field_validator
from aaa_xml_1715 import TEMPLATES, build_edit_config


class Train(str, Enum):
    xe_1612 = "1612"
    xe_173  = "173"
    xe_179  = "179"
    xe_1712 = "1712"
    xe_1715 = "1715"


# ───────────────────────────── §1 ─────────────────────────────
class AaaNewModel(BaseModel):
    feature: Literal["aaa_new_model"]
    train: Train = Train.xe_1715
    remove: bool = False

class AaaSessionMibDisconnect(BaseModel):
    feature: Literal["aaa_session_mib_disconnect"]
    train: Train = Train.xe_1715
    remove: bool = False

class AaaSessionMibPopulateSetup(BaseModel):
    feature: Literal["aaa_session_mib_populate_setup"]
    train: Train = Train.xe_1715
    remove: bool = False

class AaaSessionMibPopulateStart(BaseModel):
    feature: Literal["aaa_session_mib_populate_start"]
    train: Train = Train.xe_1715
    remove: bool = False

class AaaSessionId(BaseModel):
    feature: Literal["aaa_session_id"]
    train: Train = Train.xe_1715
    remove: bool = False
    mode: Optional[Literal["common", "unique"]] = None

class AaaLoginDisplay(BaseModel):
    feature: Literal["aaa_login_display"]
    train: Train = Train.xe_1715
    remove: bool = False
    disp: Optional[str] = None

class AaaLoginSuccessTrackConfTime(BaseModel):
    feature: Literal["aaa_login_success_track_conf_time"]
    train: Train = Train.xe_1715
    remove: bool = False
    hours: Optional[int] = Field(None, ge=0, le=168)

class AaaMaxSessions(BaseModel):
    feature: Literal["aaa_max_sessions"]
    train: Train = Train.xe_1715
    remove: bool = False
    max: Optional[int] = Field(None, ge=1)

class AaaMemoryThresholdAccountingDisable(BaseModel):
    feature: Literal["aaa_memory_threshold_accounting_disable"]
    train: Train = Train.xe_1715
    remove: bool = False
    pct: Optional[int] = Field(None, ge=1, le=100)

class AaaMemoryThresholdAuthenticationReject(BaseModel):
    feature: Literal["aaa_memory_threshold_authentication_reject"]
    train: Train = Train.xe_1715
    remove: bool = False
    pct: Optional[int] = Field(None, ge=1, le=100)

class AaaPasswordRestriction(BaseModel):
    feature: Literal["aaa_password_restriction"]
    train: Train = Train.xe_1715
    remove: bool = False

class AaaPolicyInterfaceConfig(BaseModel):
    feature: Literal["aaa_policy_interface_config"]
    train: Train = Train.xe_1715
    remove: bool = False

class AaaRouteDownloadUpdatePeriod(BaseModel):
    feature: Literal["aaa_route_download_update_period"]
    train: Train = Train.xe_1715
    remove: bool = False
    minutes: Optional[int] = Field(None, ge=1)

class AaaRouteDownloadAuthorization(BaseModel):
    feature: Literal["aaa_route_download_authorization"]
    train: Train = Train.xe_1715
    remove: bool = False
    mlist: Optional[str] = None

class AaaTracebackRecording(BaseModel):
    feature: Literal["aaa_traceback_recording"]
    train: Train = Train.xe_1715
    remove: bool = False

class AaaRemoteUsername(BaseModel):
    feature: Literal["aaa_remote_username"]
    train: Train = Train.xe_1715
    remove: bool = False
    remote_user: Optional[str] = None


# ───────────────────────────── §2 ─────────────────────────────
class AaaCacheProfileCreate(BaseModel):
    feature: Literal["aaa_cache_profile_create"]
    train: Train = Train.xe_1715
    remove: bool = False
    profile: str

class AaaCacheProfileAll(BaseModel):
    feature: Literal["aaa_cache_profile_all"]
    train: Train = Train.xe_1715
    remove: bool = False
    profile: str

class AaaCacheProfileAllNoAuth(BaseModel):
    feature: Literal["aaa_cache_profile_all_no_auth"]
    train: Train = Train.xe_1715
    remove: bool = False
    profile: str

class AaaCacheProfileRegexpAny(BaseModel):
    feature: Literal["aaa_cache_profile_regexp_any"]
    train: Train = Train.xe_1715
    remove: bool = False
    profile: str
    regex: str

class AaaCacheProfileRegexpOnly(BaseModel):
    feature: Literal["aaa_cache_profile_regexp_only"]
    train: Train = Train.xe_1715
    remove: bool = False
    profile: str
    regex: str

class AaaCacheProfileRegexpNoAuth(BaseModel):
    feature: Literal["aaa_cache_profile_regexp_no_auth"]
    train: Train = Train.xe_1715
    remove: bool = False
    profile: str
    regex: str

class AaaCacheProfileProfile(BaseModel):
    feature: Literal["aaa_cache_profile_profile"]
    train: Train = Train.xe_1715
    remove: bool = False
    profile: str
    match: str

class AaaCacheProfileProfileNoAuth(BaseModel):
    feature: Literal["aaa_cache_profile_profile_no_auth"]
    train: Train = Train.xe_1715
    remove: bool = False
    profile: str
    match: str

class AaaCacheProfileDefaultAll(BaseModel):
    feature: Literal["aaa_cache_profile_default_all"]
    train: Train = Train.xe_1715
    remove: bool = False
    profile: str

class AaaCacheProfileDefaultRegexpAny(BaseModel):
    feature: Literal["aaa_cache_profile_default_regexp_any"]
    train: Train = Train.xe_1715
    remove: bool = False
    profile: str
    regex: str

class AaaCacheProfileDefaultRegexpOnly(BaseModel):
    feature: Literal["aaa_cache_profile_default_regexp_only"]
    train: Train = Train.xe_1715
    remove: bool = False
    profile: str
    regex: str

class AaaCacheProfileDefaultProfile(BaseModel):
    feature: Literal["aaa_cache_profile_default_profile"]
    train: Train = Train.xe_1715
    remove: bool = False
    profile: str
    match: str


# ───────────────────────────── §3 ─────────────────────────────
class AaaGrpTacacsCreate(BaseModel):
    feature: Literal["aaa_grp_tacacs_create"]
    train: Train = Train.xe_1715
    remove: bool = False
    grp: str

class AaaGrpTacacsLegacyCreate(BaseModel):
    feature: Literal["aaa_grp_tacacs_legacy_create"]
    train: Train = Train.xe_1715
    remove: bool = False
    grp: str

class AaaGrpTacacsServerName(BaseModel):
    feature: Literal["aaa_grp_tacacs_server_name"]
    train: Train = Train.xe_1715
    remove: bool = False
    grp: str
    srv: str

class AaaGrpTacacsServerIp(BaseModel):
    feature: Literal["aaa_grp_tacacs_server_ip"]
    train: Train = Train.xe_1715
    remove: bool = False
    grp: str
    host: str

class AaaGrpTacacsServerPrivate(BaseModel):
    feature: Literal["aaa_grp_tacacs_server_private"]
    train: Train = Train.xe_1715
    remove: bool = False
    grp: str
    host: str
    opt_extra: str = ""

class AaaGrpTacacsServerPrivatePort(BaseModel):
    feature: Literal["aaa_grp_tacacs_server_private_port"]
    train: Train = Train.xe_1715
    remove: bool = False
    grp: str
    host: str
    port: int = Field(..., ge=1, le=65535)

class AaaGrpTacacsServerPrivateTimeout(BaseModel):
    feature: Literal["aaa_grp_tacacs_server_private_timeout"]
    train: Train = Train.xe_1715
    remove: bool = False
    grp: str
    host: str
    secs: int = Field(..., ge=1)

class AaaGrpTacacsServerPrivateKey(BaseModel):
    feature: Literal["aaa_grp_tacacs_server_private_key"]
    train: Train = Train.xe_1715
    remove: bool = False
    grp: str
    host: str
    enc: int
    key: str

class AaaGrpTacacsIpTacacsSourceInterface(BaseModel):
    feature: Literal["aaa_grp_tacacs_ip_tacacs_source_interface"]
    train: Train = Train.xe_1715
    remove: bool = False
    grp: str
    if_type: str
    if_num: str

class AaaGrpTacacsIpVrf(BaseModel):
    feature: Literal["aaa_grp_tacacs_ip_vrf"]
    train: Train = Train.xe_1715
    remove: bool = False
    grp: str
    vrf: str

class AaaGrpTacacsIpv6TacacsSourceInterface(BaseModel):
    feature: Literal["aaa_grp_tacacs_ipv6_tacacs_source_interface"]
    train: Train = Train.xe_1715
    remove: bool = False
    grp: str
    if_type: str
    if_num: str

class AaaGrpTacacsIpv6Vrf(BaseModel):
    feature: Literal["aaa_grp_tacacs_ipv6_vrf"]
    train: Train = Train.xe_1715
    remove: bool = False
    grp: str
    vrf: str

class AaaGrpTacacsAccountingAckBroadcast(BaseModel):
    feature: Literal["aaa_grp_tacacs_accounting_ack_broadcast"]
    train: Train = Train.xe_1715
    remove: bool = False
    grp: str

class AaaGrpTacacsCacheAuthenticationProfile(BaseModel):
    feature: Literal["aaa_grp_tacacs_cache_authentication_profile"]
    train: Train = Train.xe_1715
    remove: bool = False
    grp: str
    profile: str

class AaaGrpTacacsCacheAuthorizationProfile(BaseModel):
    feature: Literal["aaa_grp_tacacs_cache_authorization_profile"]
    train: Train = Train.xe_1715
    remove: bool = False
    grp: str
    profile: str

class AaaGrpTacacsCacheExpiry(BaseModel):
    feature: Literal["aaa_grp_tacacs_cache_expiry"]
    train: Train = Train.xe_1715
    remove: bool = False
    grp: str
    expiry: int = Field(..., ge=0)

class AaaGrpTacacsDnsAliasLookup(BaseModel):
    feature: Literal["aaa_grp_tacacs_dns_alias_lookup"]
    train: Train = Train.xe_1715
    remove: bool = False
    grp: str

class AaaGrpTacacsHost(BaseModel):
    feature: Literal["aaa_grp_tacacs_host"]
    train: Train = Train.xe_1715
    remove: bool = False
    grp: str
    host: str

class AaaGrpTacacsPickMethod(BaseModel):
    feature: Literal["aaa_grp_tacacs_pick_method"]
    train: Train = Train.xe_1715
    remove: bool = False
    grp: str
    method: str

class AaaGrpTacacsTimeout(BaseModel):
    feature: Literal["aaa_grp_tacacs_timeout"]
    train: Train = Train.xe_1715
    remove: bool = False
    grp: str
    secs: int = Field(..., ge=1)


# ───────────────────────────── §4 ─────────────────────────────
class AaaGrpRadiusCreate(BaseModel):
    feature: Literal["aaa_grp_radius_create"]
    train: Train = Train.xe_1715
    remove: bool = False
    grp: str

class AaaGrpRadiusServerName(BaseModel):
    feature: Literal["aaa_grp_radius_server_name"]
    train: Train = Train.xe_1715
    remove: bool = False
    grp: str
    srv: str

class AaaGrpRadiusServerDirect(BaseModel):
    feature: Literal["aaa_grp_radius_server_direct"]
    train: Train = Train.xe_1715
    remove: bool = False
    grp: str
    host: str
    opt_extra: str = ""

class AaaGrpRadiusServerDirectPorts(BaseModel):
    feature: Literal["aaa_grp_radius_server_direct_ports"]
    train: Train = Train.xe_1715
    remove: bool = False
    grp: str
    host: str
    aport: int = Field(..., ge=1, le=65535)
    cport: int = Field(..., ge=1, le=65535)

class AaaGrpRadiusSubscriberMacFiltering(BaseModel):
    feature: Literal["aaa_grp_radius_subscriber_mac_filtering"]
    train: Train = Train.xe_1715
    remove: bool = False
    grp: str
    mode: str

class AaaGrpRadiusMacDelimiter(BaseModel):
    feature: Literal["aaa_grp_radius_mac_delimiter"]
    train: Train = Train.xe_1715
    remove: bool = False
    grp: str
    delim: str

class AaaGrpRadiusServerPrivate(BaseModel):
    feature: Literal["aaa_grp_radius_server_private"]
    train: Train = Train.xe_1715
    remove: bool = False
    grp: str
    host: str
    opt_extra: str = ""

class AaaGrpRadiusServerPrivatePorts(BaseModel):
    feature: Literal["aaa_grp_radius_server_private_ports"]
    train: Train = Train.xe_1715
    remove: bool = False
    grp: str
    host: str
    aport: int = Field(..., ge=1, le=65535)
    cport: int = Field(..., ge=1, le=65535)

class AaaGrpRadiusServerPrivateTimeout(BaseModel):
    feature: Literal["aaa_grp_radius_server_private_timeout"]
    train: Train = Train.xe_1715
    remove: bool = False
    grp: str
    host: str
    secs: int = Field(..., ge=1)

class AaaGrpRadiusServerPrivateRetransmit(BaseModel):
    feature: Literal["aaa_grp_radius_server_private_retransmit"]
    train: Train = Train.xe_1715
    remove: bool = False
    grp: str
    host: str
    retries: int = Field(..., ge=0)

class AaaGrpRadiusServerPrivatePac(BaseModel):
    feature: Literal["aaa_grp_radius_server_private_pac"]
    train: Train = Train.xe_1715
    remove: bool = False
    grp: str
    host: str

class AaaGrpRadiusServerPrivateKey(BaseModel):
    feature: Literal["aaa_grp_radius_server_private_key"]
    train: Train = Train.xe_1715
    remove: bool = False
    grp: str
    host: str
    enc: int
    key: str

class AaaGrpRadiusDeadtime(BaseModel):
    feature: Literal["aaa_grp_radius_deadtime"]
    train: Train = Train.xe_1715
    remove: bool = False
    grp: str
    minutes: int = Field(..., ge=0)

class AaaGrpRadiusIpRadiusSourceInterface(BaseModel):
    feature: Literal["aaa_grp_radius_ip_radius_source_interface"]
    train: Train = Train.xe_1715
    remove: bool = False
    grp: str
    if_type: str
    if_num: str

class AaaGrpRadiusIpVrf(BaseModel):
    feature: Literal["aaa_grp_radius_ip_vrf"]
    train: Train = Train.xe_1715
    remove: bool = False
    grp: str
    vrf: str

class AaaGrpRadiusIpv6RadiusSourceInterface(BaseModel):
    feature: Literal["aaa_grp_radius_ipv6_radius_source_interface"]
    train: Train = Train.xe_1715
    remove: bool = False
    grp: str
    if_type: str
    if_num: str

class AaaGrpRadiusIpv6Vrf(BaseModel):
    feature: Literal["aaa_grp_radius_ipv6_vrf"]
    train: Train = Train.xe_1715
    remove: bool = False
    grp: str
    vrf: str

class AaaGrpRadiusAccountingRequestReject(BaseModel):
    feature: Literal["aaa_grp_radius_accounting_request_reject"]
    train: Train = Train.xe_1715
    remove: bool = False
    grp: str
    attrs: str

class AaaGrpRadiusCacheAuthenticationProfile(BaseModel):
    feature: Literal["aaa_grp_radius_cache_authentication_profile"]
    train: Train = Train.xe_1715
    remove: bool = False
    grp: str
    profile: str

class AaaGrpRadiusCacheAuthorizationProfile(BaseModel):
    feature: Literal["aaa_grp_radius_cache_authorization_profile"]
    train: Train = Train.xe_1715
    remove: bool = False
    grp: str
    profile: str

class AaaGrpRadiusCacheExpiry(BaseModel):
    feature: Literal["aaa_grp_radius_cache_expiry"]
    train: Train = Train.xe_1715
    remove: bool = False
    grp: str
    hours: int = Field(..., ge=0)

class AaaGrpRadiusDscp(BaseModel):
    feature: Literal["aaa_grp_radius_dscp"]
    train: Train = Train.xe_1715
    remove: bool = False
    grp: str
    auth: int = Field(..., ge=0, le=63)
    acct: int = Field(..., ge=0, le=63)

class AaaGrpRadiusLoadBalanceLeastOutstanding(BaseModel):
    feature: Literal["aaa_grp_radius_load_balance_least_outstanding"]
    train: Train = Train.xe_1715
    remove: bool = False
    grp: str

class AaaGrpRadiusLoadBalanceBatchSize(BaseModel):
    feature: Literal["aaa_grp_radius_load_balance_batch_size"]
    train: Train = Train.xe_1715
    remove: bool = False
    grp: str
    size: int = Field(..., ge=1)


# ───────────────────────────── §5 ─────────────────────────────
class AaaGrpLdapCreate(BaseModel):
    feature: Literal["aaa_grp_ldap_create"]
    train: Train = Train.xe_1715
    remove: bool = False
    grp: str

class AaaGrpLdapServerName(BaseModel):
    feature: Literal["aaa_grp_ldap_server_name"]
    train: Train = Train.xe_1715
    remove: bool = False
    grp: str
    srv: str


# ───────────────────────────── §6 ─────────────────────────────
class AaaAttrListCreate(BaseModel):
    feature: Literal["aaa_attr_list_create"]
    train: Train = Train.xe_1715
    remove: bool = False
    alist: str

class AaaAttrListType(BaseModel):
    feature: Literal["aaa_attr_list_type"]
    train: Train = Train.xe_1715
    remove: bool = False
    alist: str
    aname: str
    aval: str
    opt_extra: str = ""

class AaaAttrListTypeMandatory(BaseModel):
    feature: Literal["aaa_attr_list_type_mandatory"]
    train: Train = Train.xe_1715
    remove: bool = False
    alist: str
    aname: str
    aval: str

class AaaAttrListTypeTag(BaseModel):
    feature: Literal["aaa_attr_list_type_tag"]
    train: Train = Train.xe_1715
    remove: bool = False
    alist: str
    aname: str
    aval: str
    tag: int


# ───────────────────────────── §7 ─────────────────────────────
class AaaAuthnBanner(BaseModel):
    feature: Literal["aaa_authn_banner"]
    train: Train = Train.xe_1715
    remove: bool = False
    banner: Optional[str] = None

class AaaAuthnFailMessage(BaseModel):
    feature: Literal["aaa_authn_fail_message"]
    train: Train = Train.xe_1715
    remove: bool = False
    message: Optional[str] = None

class AaaAuthnAttemptsLogin(BaseModel):
    feature: Literal["aaa_authn_attempts_login"]
    train: Train = Train.xe_1715
    remove: bool = False
    attempts: Optional[int] = Field(None, ge=1)

class AaaAuthnSuppressNullUsername(BaseModel):
    feature: Literal["aaa_authn_suppress_null_username"]
    train: Train = Train.xe_1715
    remove: bool = False

class AaaAuthnDot1xDefault(BaseModel):
    feature: Literal["aaa_authn_dot1x_default"]
    train: Train = Train.xe_1715
    remove: bool = False
    methods: Optional[str] = None

class AaaAuthnDot1xList(BaseModel):
    feature: Literal["aaa_authn_dot1x_list"]
    train: Train = Train.xe_1715
    remove: bool = False
    list: str
    methods: str

class AaaAuthnEnableDefault(BaseModel):
    feature: Literal["aaa_authn_enable_default"]
    train: Train = Train.xe_1715
    remove: bool = False
    methods: Optional[str] = None

class AaaAuthnEouDefaultRadius(BaseModel):
    feature: Literal["aaa_authn_eou_default_radius"]
    train: Train = Train.xe_1715
    remove: bool = False

class AaaAuthnLogin(BaseModel):
    feature: Literal["aaa_authn_login"]
    train: Train = Train.xe_1715
    remove: bool = False
    list: str
    methods: str

class AaaAuthnOnepDefaultLocal(BaseModel):
    feature: Literal["aaa_authn_onep_default_local"]
    train: Train = Train.xe_1715
    remove: bool = False

class AaaAuthnPpp(BaseModel):
    feature: Literal["aaa_authn_ppp"]
    train: Train = Train.xe_1715
    remove: bool = False
    list: str
    methods: str

class AaaAuthnPasswordPrompt(BaseModel):
    feature: Literal["aaa_authn_password_prompt"]
    train: Train = Train.xe_1715
    remove: bool = False
    text: Optional[str] = None

class AaaAuthnUsernamePrompt(BaseModel):
    feature: Literal["aaa_authn_username_prompt"]
    train: Train = Train.xe_1715
    remove: bool = False
    text: Optional[str] = None

class AaaAuthnWebauthDefault(BaseModel):
    feature: Literal["aaa_authn_webauth_default"]
    train: Train = Train.xe_1715
    remove: bool = False
    methods: Optional[str] = None

class AaaLocalAuthnAuthorization(BaseModel):
    feature: Literal["aaa_local_authn_authorization"]
    train: Train = Train.xe_1715
    remove: bool = False
    authn: Optional[str] = None
    authz: Optional[str] = None

class AaaLocalAuthnAttemptsMaxFail(BaseModel):
    feature: Literal["aaa_local_authn_attempts_max_fail"]
    train: Train = Train.xe_1715
    remove: bool = False
    max: Optional[int] = Field(None, ge=1)


# ───────────────────────────── §8 ─────────────────────────────
class AaaAuthzAuthTypeDefaultGroupRadius(BaseModel):
    feature: Literal["aaa_authz_auth_type_default_group_radius"]
    train: Train = Train.xe_1715
    remove: bool = False

class AaaAuthzCommands(BaseModel):
    feature: Literal["aaa_authz_commands"]
    train: Train = Train.xe_1715
    remove: bool = False
    level: int = Field(..., ge=0, le=15)
    list: str
    methods: str

class AaaAuthzConfigCommands(BaseModel):
    feature: Literal["aaa_authz_config_commands"]
    train: Train = Train.xe_1715
    remove: bool = False

class AaaAuthzConfigurationList(BaseModel):
    feature: Literal["aaa_authz_configuration_list"]
    train: Train = Train.xe_1715
    remove: bool = False
    list: str
    methods: str

class AaaAuthzConfigurationDefaultGroup(BaseModel):
    feature: Literal["aaa_authz_configuration_default_group"]
    train: Train = Train.xe_1715
    remove: bool = False
    grp: str

class AaaAuthzConfigurationDefaultCache(BaseModel):
    feature: Literal["aaa_authz_configuration_default_cache"]
    train: Train = Train.xe_1715
    remove: bool = False
    cache: str

class AaaAuthzConsole(BaseModel):
    feature: Literal["aaa_authz_console"]
    train: Train = Train.xe_1715
    remove: bool = False

class AaaAuthzCredentialDownloadDefault(BaseModel):
    feature: Literal["aaa_authz_credential_download_default"]
    train: Train = Train.xe_1715
    remove: bool = False
    methods: Optional[str] = None

class AaaAuthzCredentialDownloadList(BaseModel):
    feature: Literal["aaa_authz_credential_download_list"]
    train: Train = Train.xe_1715
    remove: bool = False
    list: str
    methods: str

class AaaAuthzRadiusProxyDefault(BaseModel):
    feature: Literal["aaa_authz_radius_proxy_default"]
    train: Train = Train.xe_1715
    remove: bool = False
    methods: Optional[str] = None

class AaaAuthzRadiusProxyList(BaseModel):
    feature: Literal["aaa_authz_radius_proxy_list"]
    train: Train = Train.xe_1715
    remove: bool = False
    list: str
    methods: str

class AaaAuthzExec(BaseModel):
    feature: Literal["aaa_authz_exec"]
    train: Train = Train.xe_1715
    remove: bool = False
    list: str
    methods: str

class AaaAuthzEventmanagerGroup(BaseModel):
    feature: Literal["aaa_authz_eventmanager_group"]
    train: Train = Train.xe_1715
    remove: bool = False
    list: str
    grp: str

class AaaAuthzEventmanagerLocal(BaseModel):
    feature: Literal["aaa_authz_eventmanager_local"]
    train: Train = Train.xe_1715
    remove: bool = False
    list: str

class AaaAuthzEventmanagerNone(BaseModel):
    feature: Literal["aaa_authz_eventmanager_none"]
    train: Train = Train.xe_1715
    remove: bool = False
    list: str

class AaaAuthzNetwork(BaseModel):
    feature: Literal["aaa_authz_network"]
    train: Train = Train.xe_1715
    remove: bool = False
    list: str
    methods: str

class AaaAuthzAuthProxyDefaultLocal(BaseModel):
    feature: Literal["aaa_authz_auth_proxy_default_local"]
    train: Train = Train.xe_1715
    remove: bool = False

class AaaAuthzAuthProxyDefaultGroup(BaseModel):
    feature: Literal["aaa_authz_auth_proxy_default_group"]
    train: Train = Train.xe_1715
    remove: bool = False

class AaaAuthzOnepDefaultGroup(BaseModel):
    feature: Literal["aaa_authz_onep_default_group"]
    train: Train = Train.xe_1715
    remove: bool = False
    grp: Optional[str] = None


# ───────────────────────────── §9 ─────────────────────────────
class AaaAcctIdentityList(BaseModel):
    feature: Literal["aaa_acct_identity_list"]
    train: Train = Train.xe_1715
    remove: bool = False
    list: str
    opt_gc: str = ""
    groups: list[str] = Field(default_factory=list)
    opt_extra: str = ""

class AaaAcctOnepDefaultNone(BaseModel):
    feature: Literal["aaa_acct_onep_default_none"]
    train: Train = Train.xe_1715
    remove: bool = False

class AaaAcctOnepDefault(BaseModel):
    feature: Literal["aaa_acct_onep_default"]
    train: Train = Train.xe_1715
    remove: bool = False
    mode: Literal["start-stop", "stop-only", "wait-start", "none"]
    opt_extra: str = ""
    groups: list[str] = Field(default_factory=list)

class AaaAcctExecNone(BaseModel):
    feature: Literal["aaa_acct_exec_none"]
    train: Train = Train.xe_1715
    remove: bool = False
    list: str

class AaaAcctExec(BaseModel):
    feature: Literal["aaa_acct_exec"]
    train: Train = Train.xe_1715
    remove: bool = False
    list: str
    mode: Literal["start-stop", "stop-only", "wait-start", "none"]
    opt_extra: str = ""
    groups: list[str] = Field(default_factory=list)

class AaaAcctExecSubmodeNone(BaseModel):
    feature: Literal["aaa_acct_exec_submode_none"]
    train: Train = Train.xe_1715
    remove: bool = False
    list: str

class AaaAcctExecSubmode(BaseModel):
    feature: Literal["aaa_acct_exec_submode"]
    train: Train = Train.xe_1715
    remove: bool = False
    list: str
    mode: Literal["start-stop", "stop-only", "wait-start", "none"]
    exec_groups: list[str] = Field(default_factory=list)
    opt_extra: str = ""

class AaaAcctNetworkNone(BaseModel):
    feature: Literal["aaa_acct_network_none"]
    train: Train = Train.xe_1715
    remove: bool = False
    list: str

class AaaAcctNetwork(BaseModel):
    feature: Literal["aaa_acct_network"]
    train: Train = Train.xe_1715
    remove: bool = False
    list: str
    mode: Literal["start-stop", "stop-only", "wait-start", "none"]
    opt_extra: str = ""
    methods: str

class AaaAcctSendCountersIpv6(BaseModel):
    feature: Literal["aaa_acct_send_counters_ipv6"]
    train: Train = Train.xe_1715
    remove: bool = False

class AaaAcctSendStopRecordAlways(BaseModel):
    feature: Literal["aaa_acct_send_stop_record_always"]
    train: Train = Train.xe_1715
    remove: bool = False

class AaaAcctSendStopRecordAuthFailure(BaseModel):
    feature: Literal["aaa_acct_send_stop_record_auth_failure"]
    train: Train = Train.xe_1715
    remove: bool = False

class AaaAcctSendStopRecordAuthFailureVrf(BaseModel):
    feature: Literal["aaa_acct_send_stop_record_auth_failure_vrf"]
    train: Train = Train.xe_1715
    remove: bool = False
    vrf: str

class AaaAcctSendStopRecordAuthSuccessRemote(BaseModel):
    feature: Literal["aaa_acct_send_stop_record_auth_success_remote"]
    train: Train = Train.xe_1715
    remove: bool = False

class AaaAcctSendStopRecordAuthSuccessRemoteVrf(BaseModel):
    feature: Literal["aaa_acct_send_stop_record_auth_success_remote_vrf"]
    train: Train = Train.xe_1715
    remove: bool = False
    vrf: str

class AaaAcctSuppressNullUsername(BaseModel):
    feature: Literal["aaa_acct_suppress_null_username"]
    train: Train = Train.xe_1715
    remove: bool = False

class AaaAcctSystemDefaultNone(BaseModel):
    feature: Literal["aaa_acct_system_default_none"]
    train: Train = Train.xe_1715
    remove: bool = False

class AaaAcctSystemDefaultStartStop(BaseModel):
    feature: Literal["aaa_acct_system_default_start_stop"]
    train: Train = Train.xe_1715
    remove: bool = False
    opt_extra: str = ""
    opt_gc: str = ""
    groups: list[str] = Field(default_factory=list)

class AaaAcctSystemDefaultVrf(BaseModel):
    feature: Literal["aaa_acct_system_default_vrf"]
    train: Train = Train.xe_1715
    remove: bool = False
    vrf: str

class AaaAcctSystemGuaranteeFirst(BaseModel):
    feature: Literal["aaa_acct_system_guarantee_first"]
    train: Train = Train.xe_1715
    remove: bool = False
    flag: str

class AaaAcctUpdatePeriodic(BaseModel):
    feature: Literal["aaa_acct_update_periodic"]
    train: Train = Train.xe_1715
    remove: bool = False
    minutes: int = Field(..., ge=1)

class AaaAcctUpdateNewinfo(BaseModel):
    feature: Literal["aaa_acct_update_newinfo"]
    train: Train = Train.xe_1715
    remove: bool = False

class AaaAcctUpdateNewinfoPeriodic(BaseModel):
    feature: Literal["aaa_acct_update_newinfo_periodic"]
    train: Train = Train.xe_1715
    remove: bool = False
    minutes: int = Field(..., ge=1)

class AaaAcctAuthProxyDefaultStartStopGroup(BaseModel):
    feature: Literal["aaa_acct_auth_proxy_default_start_stop_group"]
    train: Train = Train.xe_1715
    remove: bool = False
    grp: str

class AaaAcctJitterMaximum(BaseModel):
    feature: Literal["aaa_acct_jitter_maximum"]
    train: Train = Train.xe_1715
    remove: bool = False
    secs: int = Field(..., ge=1)


# ───────────────────────────── §10 ─────────────────────────────
class AaaCcPolicyCreate(BaseModel):
    feature: Literal["aaa_cc_policy_create"]
    train: Train = Train.xe_1715
    remove: bool = False
    policy: str

class AaaCcCharChanges(BaseModel):
    feature: Literal["aaa_cc_char_changes"]
    train: Train = Train.xe_1715
    remove: bool = False
    policy: str
    n: int = Field(..., ge=0)

class AaaCcLifetime(BaseModel):
    feature: Literal["aaa_cc_lifetime"]
    train: Train = Train.xe_1715
    remove: bool = False
    policy: str
    years: int = Field(..., ge=0)
    months: int = Field(..., ge=0)
    days: int = Field(..., ge=0)
    hours: int = Field(..., ge=0)
    minutes: int = Field(..., ge=0)
    seconds: int = Field(..., ge=0)

class AaaCcLowerCase(BaseModel):
    feature: Literal["aaa_cc_lower_case"]
    train: Train = Train.xe_1715
    remove: bool = False
    policy: str
    n: int = Field(..., ge=0)

class AaaCcMaxLength(BaseModel):
    feature: Literal["aaa_cc_max_length"]
    train: Train = Train.xe_1715
    remove: bool = False
    policy: str
    n: int = Field(..., ge=1)

class AaaCcMinLength(BaseModel):
    feature: Literal["aaa_cc_min_length"]
    train: Train = Train.xe_1715
    remove: bool = False
    policy: str
    n: int = Field(..., ge=1)

class AaaCcNumericCount(BaseModel):
    feature: Literal["aaa_cc_numeric_count"]
    train: Train = Train.xe_1715
    remove: bool = False
    policy: str
    n: int = Field(..., ge=0)

class AaaCcSpecialCase(BaseModel):
    feature: Literal["aaa_cc_special_case"]
    train: Train = Train.xe_1715
    remove: bool = False
    policy: str
    n: int = Field(..., ge=0)

class AaaCcUpperCase(BaseModel):
    feature: Literal["aaa_cc_upper_case"]
    train: Train = Train.xe_1715
    remove: bool = False
    policy: str
    n: int = Field(..., ge=0)

class AaaCcCharacterRepetition(BaseModel):
    feature: Literal["aaa_cc_character_repetition"]
    train: Train = Train.xe_1715
    remove: bool = False
    policy: str
    n: int = Field(..., ge=0)

class AaaCcRestrictConsecutiveLetters(BaseModel):
    feature: Literal["aaa_cc_restrict_consecutive_letters"]
    train: Train = Train.xe_1715
    remove: bool = False
    policy: str


# ───────────────────────────── §11 ─────────────────────────────
class AaaSrvRadiusDynamicAuthor(BaseModel):
    feature: Literal["aaa_srv_radius_dynamic_author"]
    train: Train = Train.xe_1715
    remove: bool = False

class AaaSrvRadiusDynamicAuthorPort(BaseModel):
    feature: Literal["aaa_srv_radius_dynamic_author_port"]
    train: Train = Train.xe_1715
    remove: bool = False
    port: int = Field(..., ge=1, le=65535)

class AaaSrvRadiusDynamicAuthorClient(BaseModel):
    feature: Literal["aaa_srv_radius_dynamic_author_client"]
    train: Train = Train.xe_1715
    remove: bool = False
    cip: str
    opt_extra: str = ""

class AaaSrvRadiusDynamicAuthorClientDtls(BaseModel):
    feature: Literal["aaa_srv_radius_dynamic_author_client_dtls"]
    train: Train = Train.xe_1715
    remove: bool = False
    cip: str

class AaaSrvRadiusDynamicAuthorClientServerKey(BaseModel):
    feature: Literal["aaa_srv_radius_dynamic_author_client_server_key"]
    train: Train = Train.xe_1715
    remove: bool = False
    cip: str
    ktype: str
    key: str

class AaaSrvRadiusDynamicAuthorClientVrf(BaseModel):
    feature: Literal["aaa_srv_radius_dynamic_author_client_vrf"]
    train: Train = Train.xe_1715
    remove: bool = False
    cip: str
    vrf: str
    opt_extra: str = ""

class AaaSrvRadiusDynamicAuthorClientVrfServerKey(BaseModel):
    feature: Literal["aaa_srv_radius_dynamic_author_client_vrf_server_key"]
    train: Train = Train.xe_1715
    remove: bool = False
    cip: str
    vrf: str
    ktype: str
    key: str

class AaaSrvRadiusDynamicAuthorTls(BaseModel):
    feature: Literal["aaa_srv_radius_dynamic_author_tls"]
    train: Train = Train.xe_1715
    remove: bool = False

class AaaSrvRadiusDynamicAuthorTlsPort(BaseModel):
    feature: Literal["aaa_srv_radius_dynamic_author_tls_port"]
    train: Train = Train.xe_1715
    remove: bool = False
    port: int = Field(..., ge=1, le=65535)

class AaaSrvRadiusDynamicAuthorServerKey(BaseModel):
    feature: Literal["aaa_srv_radius_dynamic_author_server_key"]
    train: Train = Train.xe_1715
    remove: bool = False
    ktype: str
    key: str

class AaaSrvRadiusDynamicAuthorDomainStripping(BaseModel):
    feature: Literal["aaa_srv_radius_dynamic_author_domain_stripping"]
    train: Train = Train.xe_1715
    remove: bool = False

class AaaSrvRadiusDynamicAuthorDomainStrippingR2l(BaseModel):
    feature: Literal["aaa_srv_radius_dynamic_author_domain_stripping_r2l"]
    train: Train = Train.xe_1715
    remove: bool = False

class AaaSrvRadiusDynamicAuthorDomainDelimiter(BaseModel):
    feature: Literal["aaa_srv_radius_dynamic_author_domain_delimiter"]
    train: Train = Train.xe_1715
    remove: bool = False
    delim: str

class AaaSrvRadiusDynamicAuthorAuthType(BaseModel):
    feature: Literal["aaa_srv_radius_dynamic_author_auth_type"]
    train: Train = Train.xe_1715
    remove: bool = False
    atype: str

class AaaSrvRadiusDynamicAuthorIgnoreRetransmission(BaseModel):
    feature: Literal["aaa_srv_radius_dynamic_author_ignore_retransmission"]
    train: Train = Train.xe_1715
    remove: bool = False

class AaaSrvRadiusDynamicAuthorIgnoreServerKey(BaseModel):
    feature: Literal["aaa_srv_radius_dynamic_author_ignore_server_key"]
    train: Train = Train.xe_1715
    remove: bool = False

class AaaSrvRadiusDynamicAuthorIgnoreSessionKey(BaseModel):
    feature: Literal["aaa_srv_radius_dynamic_author_ignore_session_key"]
    train: Train = Train.xe_1715
    remove: bool = False

class AaaSrvRadiusPolicyDevice(BaseModel):
    feature: Literal["aaa_srv_radius_policy_device"]
    train: Train = Train.xe_1715
    remove: bool = False

class AaaSrvRadiusPolicyDeviceAccountingPort(BaseModel):
    feature: Literal["aaa_srv_radius_policy_device_accounting_port"]
    train: Train = Train.xe_1715
    remove: bool = False
    port: int = Field(..., ge=1, le=65535)

class AaaSrvRadiusPolicyDeviceAuthenticationPort(BaseModel):
    feature: Literal["aaa_srv_radius_policy_device_authentication_port"]
    train: Train = Train.xe_1715
    remove: bool = False
    port: int = Field(..., ge=1, le=65535)

class AaaSrvRadiusPolicyDeviceClient(BaseModel):
    feature: Literal["aaa_srv_radius_policy_device_client"]
    train: Train = Train.xe_1715
    remove: bool = False
    cip: str
    opt_extra: str = ""

class AaaSrvRadiusPolicyDeviceClientPort(BaseModel):
    feature: Literal["aaa_srv_radius_policy_device_client_port"]
    train: Train = Train.xe_1715
    remove: bool = False
    cip: str
    port: int = Field(..., ge=1, le=65535)

class AaaSrvRadiusPolicyDeviceClientKey(BaseModel):
    feature: Literal["aaa_srv_radius_policy_device_client_key"]
    train: Train = Train.xe_1715
    remove: bool = False
    cip: str
    ktype: str
    key: str

class AaaSrvRadiusPolicyDeviceClientVrf(BaseModel):
    feature: Literal["aaa_srv_radius_policy_device_client_vrf"]
    train: Train = Train.xe_1715
    remove: bool = False
    cip: str
    vrf: str
    opt_extra: str = ""

class AaaSrvRadiusPolicyDeviceKey(BaseModel):
    feature: Literal["aaa_srv_radius_policy_device_key"]
    train: Train = Train.xe_1715
    remove: bool = False
    ktype: str
    key: str

class AaaSrvRadiusPolicyDeviceMessageAuthenticatorIgnore(BaseModel):
    feature: Literal["aaa_srv_radius_policy_device_message_authenticator_ignore"]
    train: Train = Train.xe_1715
    remove: bool = False


# ───────────────────────────── §12 ─────────────────────────────
class RadiusFilter(BaseModel):
    feature: Literal["radius_filter"]
    train: Train = Train.xe_1715
    remove: bool = False
    fid: str
    match: str

class RadiusServerCreate(BaseModel):
    feature: Literal["radius_server_create"]
    train: Train = Train.xe_1715
    remove: bool = False
    rs: str

class RadiusServerAddressIpv4(BaseModel):
    feature: Literal["radius_server_address_ipv4"]
    train: Train = Train.xe_1715
    remove: bool = False
    rs: str
    addr: str
    opt_extra: str = ""

class RadiusServerAddressIpv6(BaseModel):
    feature: Literal["radius_server_address_ipv6"]
    train: Train = Train.xe_1715
    remove: bool = False
    rs: str
    addr: str
    opt_extra: str = ""

class RadiusServerAddressFqdn(BaseModel):
    feature: Literal["radius_server_address_fqdn"]
    train: Train = Train.xe_1715
    remove: bool = False
    rs: str
    addr: str
    opt_extra: str = ""

class RadiusServerAddressPorts(BaseModel):
    feature: Literal["radius_server_address_ports"]
    train: Train = Train.xe_1715
    remove: bool = False
    rs: str
    aport: int = Field(..., ge=1, le=65535)
    cport: int = Field(..., ge=1, le=65535)

class RadiusServerTimeout(BaseModel):
    feature: Literal["radius_server_timeout"]
    train: Train = Train.xe_1715
    remove: bool = False
    rs: str
    secs: int = Field(..., ge=1)

class RadiusServerTlsPort(BaseModel):
    feature: Literal["radius_server_tls_port"]
    train: Train = Train.xe_1715
    remove: bool = False
    rs: str
    port: int = Field(..., ge=1, le=65535)

class RadiusServerTlsTrustpointClient(BaseModel):
    feature: Literal["radius_server_tls_trustpoint_client"]
    train: Train = Train.xe_1715
    remove: bool = False
    rs: str
    tp: str

class RadiusServerTlsTrustpointServer(BaseModel):
    feature: Literal["radius_server_tls_trustpoint_server"]
    train: Train = Train.xe_1715
    remove: bool = False
    rs: str
    tp: str

class RadiusServerTlsMatchServerIdentityHostname(BaseModel):
    feature: Literal["radius_server_tls_match_server_identity_hostname"]
    train: Train = Train.xe_1715
    remove: bool = False
    rs: str
    host: str

class RadiusServerAutomateTester(BaseModel):
    feature: Literal["radius_server_automate_tester"]
    train: Train = Train.xe_1715
    remove: bool = False
    rs: str
    tuser: str
    opt_extra: str = ""

class RadiusServerAutomateTesterProbeOnConfig(BaseModel):
    feature: Literal["radius_server_automate_tester_probe_on_config"]
    train: Train = Train.xe_1715
    remove: bool = False
    rs: str
    tuser: str

class RadiusServerAutomateTesterIdleTime(BaseModel):
    feature: Literal["radius_server_automate_tester_idle_time"]
    train: Train = Train.xe_1715
    remove: bool = False
    rs: str
    tuser: str
    minutes: int = Field(..., ge=1)

class RadiusServerAutomateTesterIgnoreAuthPort(BaseModel):
    feature: Literal["radius_server_automate_tester_ignore_auth_port"]
    train: Train = Train.xe_1715
    remove: bool = False
    rs: str
    tuser: str

class RadiusServerAutomateTesterIgnoreAcctPort(BaseModel):
    feature: Literal["radius_server_automate_tester_ignore_acct_port"]
    train: Train = Train.xe_1715
    remove: bool = False
    rs: str
    tuser: str

class RadiusServerAutomateTesterVrf(BaseModel):
    feature: Literal["radius_server_automate_tester_vrf"]
    train: Train = Train.xe_1715
    remove: bool = False
    rs: str
    tuser: str
    vrf: str

class RadiusServerBackoffExponential(BaseModel):
    feature: Literal["radius_server_backoff_exponential"]
    train: Train = Train.xe_1715
    remove: bool = False
    rs: str
    delay: int = Field(..., ge=1)
    retry: int = Field(..., ge=1)

class RadiusServerPacKey(BaseModel):
    feature: Literal["radius_server_pac_key"]
    train: Train = Train.xe_1715
    remove: bool = False
    rs: str
    enc: int
    key: str

class RadiusServerKey(BaseModel):
    feature: Literal["radius_server_key"]
    train: Train = Train.xe_1715
    remove: bool = False
    rs: str
    enc: int
    key: str

class RadiusServerRetransmit(BaseModel):
    feature: Literal["radius_server_retransmit"]
    train: Train = Train.xe_1715
    remove: bool = False
    rs: str
    retries: int = Field(..., ge=0)

class RadiusServerDscp(BaseModel):
    feature: Literal["radius_server_dscp"]
    train: Train = Train.xe_1715
    remove: bool = False
    rs: str
    auth: int = Field(..., ge=0, le=63)
    acct: int = Field(..., ge=0, le=63)


# ───────────────────────────── §13 ─────────────────────────────
class LdapServerCreate(BaseModel):
    feature: Literal["ldap_server_create"]
    train: Train = Train.xe_1715
    remove: bool = False
    ls: str

class LdapServerIpv4(BaseModel):
    feature: Literal["ldap_server_ipv4"]
    train: Train = Train.xe_1715
    remove: bool = False
    ls: str
    addr: str

class LdapServerIpv6(BaseModel):
    feature: Literal["ldap_server_ipv6"]
    train: Train = Train.xe_1715
    remove: bool = False
    ls: str
    addr: str

class LdapServerFqdn(BaseModel):
    feature: Literal["ldap_server_fqdn"]
    train: Train = Train.xe_1715
    remove: bool = False
    ls: str
    addr: str

class LdapServerAuthenticationBindFirst(BaseModel):
    feature: Literal["ldap_server_authentication_bind_first"]
    train: Train = Train.xe_1715
    remove: bool = False
    ls: str

class LdapServerAuthenticationBindFirstNoAuthz(BaseModel):
    feature: Literal["ldap_server_authentication_bind_first_no_authz"]
    train: Train = Train.xe_1715
    remove: bool = False
    ls: str

class LdapServerAuthenticationCompare(BaseModel):
    feature: Literal["ldap_server_authentication_compare"]
    train: Train = Train.xe_1715
    remove: bool = False
    ls: str

class LdapServerAutomateTester(BaseModel):
    feature: Literal["ldap_server_automate_tester"]
    train: Train = Train.xe_1715
    remove: bool = False
    ls: str
    tuser: str

class LdapServerBaseDn(BaseModel):
    feature: Literal["ldap_server_base_dn"]
    train: Train = Train.xe_1715
    remove: bool = False
    ls: str
    dn: str

class LdapServerDeadtime(BaseModel):
    feature: Literal["ldap_server_deadtime"]
    train: Train = Train.xe_1715
    remove: bool = False
    ls: str
    minutes: int = Field(..., ge=0)

class LdapServerTimeoutRetransmit(BaseModel):
    feature: Literal["ldap_server_timeout_retransmit"]
    train: Train = Train.xe_1715
    remove: bool = False
    ls: str
    secs: int = Field(..., ge=1)

class LdapServerBindAuthenticate(BaseModel):
    feature: Literal["ldap_server_bind_authenticate"]
    train: Train = Train.xe_1715
    remove: bool = False
    ls: str

class LdapServerBindRootDn(BaseModel):
    feature: Literal["ldap_server_bind_root_dn"]
    train: Train = Train.xe_1715
    remove: bool = False
    ls: str

class LdapServerBindUsername(BaseModel):
    feature: Literal["ldap_server_bind_username"]
    train: Train = Train.xe_1715
    remove: bool = False
    ls: str
    buser: str

class LdapServerBindPassword(BaseModel):
    feature: Literal["ldap_server_bind_password"]
    train: Train = Train.xe_1715
    remove: bool = False
    ls: str
    ptype: str
    pass_: str = Field(..., alias="pass")

class LdapServerModeSecure(BaseModel):
    feature: Literal["ldap_server_mode_secure"]
    train: Train = Train.xe_1715
    remove: bool = False
    ls: str

class LdapServerModeSecureNoNegotiation(BaseModel):
    feature: Literal["ldap_server_mode_secure_no_negotiation"]
    train: Train = Train.xe_1715
    remove: bool = False
    ls: str

class LdapServerSearchTypeNested(BaseModel):
    feature: Literal["ldap_server_search_type_nested"]
    train: Train = Train.xe_1715
    remove: bool = False
    ls: str

class LdapServerSearchFilterUserObjectType(BaseModel):
    feature: Literal["ldap_server_search_filter_user_object_type"]
    train: Train = Train.xe_1715
    remove: bool = False
    ls: str
    oc: str

class LdapServerSecureCipher(BaseModel):
    feature: Literal["ldap_server_secure_cipher"]
    train: Train = Train.xe_1715
    remove: bool = False
    ls: str
    cipher: str

class LdapServerSecureTrustpoint(BaseModel):
    feature: Literal["ldap_server_secure_trustpoint"]
    train: Train = Train.xe_1715
    remove: bool = False
    ls: str
    tp: str

class LdapServerTransportPort(BaseModel):
    feature: Literal["ldap_server_transport_port"]
    train: Train = Train.xe_1715
    remove: bool = False
    ls: str
    port: int = Field(..., ge=1, le=65535)


# ───────────────────────────── §14 ─────────────────────────────
class RsHostRetransmit(BaseModel):
    feature: Literal["rs_host_retransmit"]
    train: Train = Train.xe_1715
    remove: bool = False
    host: str
    retries: int = Field(..., ge=0)

class RsHostTimeout(BaseModel):
    feature: Literal["rs_host_timeout"]
    train: Train = Train.xe_1715
    remove: bool = False
    host: str
    secs: int = Field(..., ge=1)

class RsHostKey(BaseModel):
    feature: Literal["rs_host_key"]
    train: Train = Train.xe_1715
    remove: bool = False
    host: str
    ktype: str
    key: str

class RsHostTestUsername(BaseModel):
    feature: Literal["rs_host_test_username"]
    train: Train = Train.xe_1715
    remove: bool = False
    host: str
    tuser: str

class RsHostTestUsernameKey(BaseModel):
    feature: Literal["rs_host_test_username_key"]
    train: Train = Train.xe_1715
    remove: bool = False
    host: str
    tuser: str
    enc: int
    key: str

class RsKey(BaseModel):
    feature: Literal["rs_key"]
    train: Train = Train.xe_1715
    remove: bool = False
    enc: int
    key: str

class RsLoadBalanceLeastOutstanding(BaseModel):
    feature: Literal["rs_load_balance_least_outstanding"]
    train: Train = Train.xe_1715
    remove: bool = False

class RsLoadBalanceBatchSize(BaseModel):
    feature: Literal["rs_load_balance_batch_size"]
    train: Train = Train.xe_1715
    remove: bool = False
    size: int = Field(..., ge=1)

class RsLoadBalanceIgnorePreferredServer(BaseModel):
    feature: Literal["rs_load_balance_ignore_preferred_server"]
    train: Train = Train.xe_1715
    remove: bool = False

class RsRetransmit(BaseModel):
    feature: Literal["rs_retransmit"]
    train: Train = Train.xe_1715
    remove: bool = False
    retries: int = Field(..., ge=0)

class RsSourcePortsExtended(BaseModel):
    feature: Literal["rs_source_ports_extended"]
    train: Train = Train.xe_1715
    remove: bool = False

class RsTimeout(BaseModel):
    feature: Literal["rs_timeout"]
    train: Train = Train.xe_1715
    remove: bool = False
    secs: int = Field(..., ge=1)

class RsVsaDisallowUnknown(BaseModel):
    feature: Literal["rs_vsa_disallow_unknown"]
    train: Train = Train.xe_1715
    remove: bool = False

class RsVsaSend(BaseModel):
    feature: Literal["rs_vsa_send"]
    train: Train = Train.xe_1715
    remove: bool = False

class RsVsaSendAccountingOnly(BaseModel):
    feature: Literal["rs_vsa_send_accounting_only"]
    train: Train = Train.xe_1715
    remove: bool = False
    flag: str

class RsVsaSendAuthenticationOnly(BaseModel):
    feature: Literal["rs_vsa_send_authentication_only"]
    train: Train = Train.xe_1715
    remove: bool = False
    flag: str

class RsVsaSendAccountingThreegpp2(BaseModel):
    feature: Literal["rs_vsa_send_accounting_threegpp2"]
    train: Train = Train.xe_1715
    remove: bool = False

class RsVsaSendAuthenticationThreegpp2(BaseModel):
    feature: Literal["rs_vsa_send_authentication_threegpp2"]
    train: Train = Train.xe_1715
    remove: bool = False

class RsVsaSendCiscoNasPort(BaseModel):
    feature: Literal["rs_vsa_send_cisco_nas_port"]
    train: Train = Train.xe_1715
    remove: bool = False

class RsVsaSendCiscoNasPortThreegpp2(BaseModel):
    feature: Literal["rs_vsa_send_cisco_nas_port_threegpp2"]
    train: Train = Train.xe_1715
    remove: bool = False

class RsDscp(BaseModel):
    feature: Literal["rs_dscp"]
    train: Train = Train.xe_1715
    remove: bool = False
    auth: int = Field(..., ge=0, le=63)
    acct: int = Field(..., ge=0, le=63)


# ───────────────────────────── §15 ─────────────────────────────
class IpRadiusSourceInterface(BaseModel):
    feature: Literal["ip_radius_source_interface"]
    train: Train = Train.xe_1715
    remove: bool = False
    if_type: str
    if_num: str
    opt_extra: str = ""

class IpRadiusSourceInterfaceVrf(BaseModel):
    feature: Literal["ip_radius_source_interface_vrf"]
    train: Train = Train.xe_1715
    remove: bool = False
    if_type: str
    if_num: str
    vrf: str

class Ipv6RadiusSourceInterface(BaseModel):
    feature: Literal["ipv6_radius_source_interface"]
    train: Train = Train.xe_1715
    remove: bool = False
    if_type: str
    if_num: str
    opt_extra: str = ""

class Ipv6RadiusSourceInterfaceVrf(BaseModel):
    feature: Literal["ipv6_radius_source_interface_vrf"]
    train: Train = Train.xe_1715
    remove: bool = False
    if_type: str
    if_num: str
    vrf: str

class IpTacacsSourceInterface(BaseModel):
    feature: Literal["ip_tacacs_source_interface"]
    train: Train = Train.xe_1715
    remove: bool = False
    if_type: str
    if_num: str
    opt_extra: str = ""

class IpMrTacacsSourceInterfaceVrf(BaseModel):
    feature: Literal["ip_tacacs_source_interface_vrf"]
    train: Train = Train.xe_1715
    remove: bool = False
    if_type: str
    if_num: str
    vrf: str

class Ipv6TacacsSourceInterface(BaseModel):
    feature: Literal["ipv6_tacacs_source_interface"]
    train: Train = Train.xe_1715
    remove: bool = False
    if_type: str
    if_num: str
    opt_extra: str = ""

class Ipv6TacacsSourceInterfaceVrf(BaseModel):
    feature: Literal["ipv6_tacacs_source_interface_vrf"]
    train: Train = Train.xe_1715
    remove: bool = False
    if_type: str
    if_num: str
    vrf: str


# ───────────────────────────── §16 ─────────────────────────────
class TacacsServerCreate(BaseModel):
    feature: Literal["tacacs_server_create"]
    train: Train = Train.xe_1715
    remove: bool = False
    ts: str

class TacacsServerAddressIpv4(BaseModel):
    feature: Literal["tacacs_server_address_ipv4"]
    train: Train = Train.xe_1715
    remove: bool = False
    ts: str
    addr: str

class TacacsServerAddressIpv6(BaseModel):
    feature: Literal["tacacs_server_address_ipv6"]
    train: Train = Train.xe_1715
    remove: bool = False
    ts: str
    addr: str

class TacacsServerAddressFqdn(BaseModel):
    feature: Literal["tacacs_server_address_fqdn"]
    train: Train = Train.xe_1715
    remove: bool = False
    ts: str
    addr: str

class TacacsServerPort(BaseModel):
    feature: Literal["tacacs_server_port"]
    train: Train = Train.xe_1715
    remove: bool = False
    ts: str
    port: int = Field(..., ge=1, le=65535)

class TacacsServerTimeout(BaseModel):
    feature: Literal["tacacs_server_timeout"]
    train: Train = Train.xe_1715
    remove: bool = False
    ts: str
    secs: int = Field(..., ge=1)

class TacacsServerKey(BaseModel):
    feature: Literal["tacacs_server_key"]
    train: Train = Train.xe_1715
    remove: bool = False
    ts: str
    enc: int
    key: str


# ───────────────────────────── §17 ─────────────────────────────
class TsTimeout(BaseModel):
    feature: Literal["ts_timeout"]
    train: Train = Train.xe_1715
    remove: bool = False
    secs: int = Field(..., ge=1)

class TsDirectedRequest(BaseModel):
    feature: Literal["ts_directed_request"]
    train: Train = Train.xe_1715
    remove: bool = False

class TsDirectedRequestRestricted(BaseModel):
    feature: Literal["ts_directed_request_restricted"]
    train: Train = Train.xe_1715
    remove: bool = False

class TsDirectedRequestNoTruncate(BaseModel):
    feature: Literal["ts_directed_request_no_truncate"]
    train: Train = Train.xe_1715
    remove: bool = False

class TsKey(BaseModel):
    feature: Literal["ts_key"]
    train: Train = Train.xe_1715
    remove: bool = False
    enc: int
    key: str

class TsAttributeAllowUnknown(BaseModel):
    feature: Literal["ts_attribute_allow_unknown"]
    train: Train = Train.xe_1715
    remove: bool = False


# ───────────────────────────── §18 ─────────────────────────────
class UserCommonCriteriaPolicy(BaseModel):
    feature: Literal["user_common_criteria_policy"]
    train: Train = Train.xe_1715
    remove: bool = False
    uname: str
    policy: Optional[str] = None

class UserCommonCriteriaPassword(BaseModel):
    feature: Literal["user_common_criteria_password"]
    train: Train = Train.xe_1715
    remove: bool = False
    uname: str
    policy: str
    enc: Optional[int] = None
    pw: Optional[str] = None

class UserAaaAttributeList(BaseModel):
    feature: Literal["user_aaa_attribute_list"]
    train: Train = Train.xe_1715
    remove: bool = False
    uname: str
    alist: Optional[str] = None


# ───────────────────────────── §19 ─────────────────────────────
class SecAuthenticationFailureRate(BaseModel):
    feature: Literal["sec_authentication_failure_rate"]
    train: Train = Train.xe_1715
    remove: bool = False
    threshold: int = Field(..., ge=1)

class SecPasswordsMinLength(BaseModel):
    feature: Literal["sec_passwords_min_length"]
    train: Train = Train.xe_1715
    remove: bool = False
    n: int = Field(..., ge=1, le=127)


# ══════════════════════════════════════════════════════════════
# DISCRIMINATED UNION — only classes actually defined above
# ══════════════════════════════════════════════════════════════
# ══════════════════════════════════════════════════════════════
# DISCRIMINATED UNION — only classes actually defined above
# ══════════════════════════════════════════════════════════════
AaaFeature = Annotated[
    Union[
        # §1
        AaaNewModel, AaaSessionMibDisconnect, AaaSessionMibPopulateSetup,
        AaaSessionMibPopulateStart, AaaSessionId, AaaLoginDisplay,
        AaaLoginSuccessTrackConfTime, AaaMaxSessions,
        AaaMemoryThresholdAccountingDisable,
        AaaMemoryThresholdAuthenticationReject, AaaPasswordRestriction,
        AaaPolicyInterfaceConfig, AaaRouteDownloadUpdatePeriod,
        AaaRouteDownloadAuthorization, AaaTracebackRecording,
        AaaRemoteUsername,
        # §2
        AaaCacheProfileCreate, AaaCacheProfileAll, AaaCacheProfileAllNoAuth,
        AaaCacheProfileRegexpAny, AaaCacheProfileRegexpOnly,
        AaaCacheProfileRegexpNoAuth, AaaCacheProfileProfile,
        AaaCacheProfileProfileNoAuth, AaaCacheProfileDefaultAll,
        AaaCacheProfileDefaultRegexpAny, AaaCacheProfileDefaultRegexpOnly,
        AaaCacheProfileDefaultProfile,
        # §3
        AaaGrpTacacsCreate, AaaGrpTacacsLegacyCreate,
        AaaGrpTacacsServerName, AaaGrpTacacsServerIp,
        AaaGrpTacacsServerPrivate, AaaGrpTacacsServerPrivatePort,
        AaaGrpTacacsServerPrivateTimeout, AaaGrpTacacsServerPrivateKey,
        AaaGrpTacacsIpTacacsSourceInterface, AaaGrpTacacsIpVrf,
        AaaGrpTacacsIpv6TacacsSourceInterface, AaaGrpTacacsIpv6Vrf,
        AaaGrpTacacsAccountingAckBroadcast,
        AaaGrpTacacsCacheAuthenticationProfile,
        AaaGrpTacacsCacheAuthorizationProfile,
        AaaGrpTacacsCacheExpiry, AaaGrpTacacsDnsAliasLookup,
        AaaGrpTacacsHost, AaaGrpTacacsPickMethod, AaaGrpTacacsTimeout,
        # §4
        AaaGrpRadiusCreate, AaaGrpRadiusServerName,
        AaaGrpRadiusServerDirect, AaaGrpRadiusServerDirectPorts,
        AaaGrpRadiusSubscriberMacFiltering, AaaGrpRadiusMacDelimiter,
        AaaGrpRadiusServerPrivate, AaaGrpRadiusServerPrivatePorts,
        AaaGrpRadiusServerPrivateTimeout, AaaGrpRadiusServerPrivateRetransmit,
        AaaGrpRadiusServerPrivatePac, AaaGrpRadiusServerPrivateKey,
        AaaGrpRadiusDeadtime, AaaGrpRadiusIpRadiusSourceInterface,
        AaaGrpRadiusIpVrf, AaaGrpRadiusIpv6RadiusSourceInterface,
        AaaGrpRadiusIpv6Vrf, AaaGrpRadiusAccountingRequestReject,
        AaaGrpRadiusCacheAuthenticationProfile,
        AaaGrpRadiusCacheAuthorizationProfile, AaaGrpRadiusCacheExpiry,
        AaaGrpRadiusDscp, AaaGrpRadiusLoadBalanceLeastOutstanding,
        AaaGrpRadiusLoadBalanceBatchSize,
        # §5
        AaaGrpLdapCreate, AaaGrpLdapServerName,
        # §6
        AaaAttrListCreate, AaaAttrListType, AaaAttrListTypeMandatory,
        AaaAttrListTypeTag,
        # §7
        AaaAuthnBanner, AaaAuthnFailMessage, AaaAuthnAttemptsLogin,
        AaaAuthnSuppressNullUsername, AaaAuthnDot1xDefault,
        AaaAuthnDot1xList, AaaAuthnEnableDefault, AaaAuthnEouDefaultRadius,
        AaaAuthnLogin, AaaAuthnOnepDefaultLocal, AaaAuthnPpp,
        AaaAuthnPasswordPrompt, AaaAuthnUsernamePrompt,
        AaaAuthnWebauthDefault, AaaLocalAuthnAuthorization,
        AaaLocalAuthnAttemptsMaxFail,
        # §8
        AaaAuthzAuthTypeDefaultGroupRadius, AaaAuthzCommands,
        AaaAuthzConfigCommands, AaaAuthzConfigurationList,
        AaaAuthzConfigurationDefaultGroup, AaaAuthzConfigurationDefaultCache,
        AaaAuthzConsole, AaaAuthzCredentialDownloadDefault,
        AaaAuthzCredentialDownloadList, AaaAuthzRadiusProxyDefault,
        AaaAuthzRadiusProxyList, AaaAuthzExec, AaaAuthzEventmanagerGroup,
        AaaAuthzEventmanagerLocal, AaaAuthzEventmanagerNone,
        AaaAuthzNetwork, AaaAuthzAuthProxyDefaultLocal,
        AaaAuthzAuthProxyDefaultGroup, AaaAuthzOnepDefaultGroup,
        # §9
        AaaAcctIdentityList, AaaAcctOnepDefaultNone, AaaAcctOnepDefault,
        AaaAcctExecNone, AaaAcctExec, AaaAcctExecSubmodeNone,
        AaaAcctExecSubmode, AaaAcctNetworkNone, AaaAcctNetwork,
        AaaAcctSendCountersIpv6, AaaAcctSendStopRecordAlways,
        AaaAcctSendStopRecordAuthFailure,
        AaaAcctSendStopRecordAuthFailureVrf,
        AaaAcctSendStopRecordAuthSuccessRemote,
        AaaAcctSendStopRecordAuthSuccessRemoteVrf,
        AaaAcctSuppressNullUsername, AaaAcctSystemDefaultNone,
        AaaAcctSystemDefaultStartStop, AaaAcctSystemDefaultVrf,
        AaaAcctSystemGuaranteeFirst, AaaAcctUpdatePeriodic,
        AaaAcctUpdateNewinfo, AaaAcctUpdateNewinfoPeriodic,
        AaaAcctAuthProxyDefaultStartStopGroup, AaaAcctJitterMaximum,
        # §10
        AaaCcPolicyCreate, AaaCcCharChanges, AaaCcLifetime,
        AaaCcLowerCase, AaaCcMaxLength, AaaCcMinLength,
        AaaCcNumericCount, AaaCcSpecialCase, AaaCcUpperCase,
        AaaCcCharacterRepetition, AaaCcRestrictConsecutiveLetters,
        # §11
        AaaSrvRadiusDynamicAuthor, AaaSrvRadiusDynamicAuthorPort,
        AaaSrvRadiusDynamicAuthorClient,
        AaaSrvRadiusDynamicAuthorClientDtls,
        AaaSrvRadiusDynamicAuthorClientServerKey,
        AaaSrvRadiusDynamicAuthorClientVrf,
        AaaSrvRadiusDynamicAuthorClientVrfServerKey,
        AaaSrvRadiusDynamicAuthorTls, AaaSrvRadiusDynamicAuthorTlsPort,
        AaaSrvRadiusDynamicAuthorServerKey,
        AaaSrvRadiusDynamicAuthorDomainStripping,
        AaaSrvRadiusDynamicAuthorDomainStrippingR2l,
        AaaSrvRadiusDynamicAuthorDomainDelimiter,
        AaaSrvRadiusDynamicAuthorAuthType,
        AaaSrvRadiusDynamicAuthorIgnoreRetransmission,
        AaaSrvRadiusDynamicAuthorIgnoreServerKey,
        AaaSrvRadiusDynamicAuthorIgnoreSessionKey,
        AaaSrvRadiusPolicyDevice,
        AaaSrvRadiusPolicyDeviceAccountingPort,
        AaaSrvRadiusPolicyDeviceAuthenticationPort,
        AaaSrvRadiusPolicyDeviceClient,
        AaaSrvRadiusPolicyDeviceClientPort,
        AaaSrvRadiusPolicyDeviceClientKey,
        AaaSrvRadiusPolicyDeviceClientVrf,
        AaaSrvRadiusPolicyDeviceKey,
        AaaSrvRadiusPolicyDeviceMessageAuthenticatorIgnore,
        # §12
        RadiusFilter, RadiusServerCreate,
        RadiusServerAddressIpv4, RadiusServerAddressIpv6,
        RadiusServerAddressFqdn, RadiusServerAddressPorts,
        RadiusServerTimeout, RadiusServerTlsPort,
        RadiusServerTlsTrustpointClient, RadiusServerTlsTrustpointServer,
        RadiusServerTlsMatchServerIdentityHostname,
        RadiusServerAutomateTester,
        RadiusServerAutomateTesterProbeOnConfig,
        RadiusServerAutomateTesterIdleTime,
        RadiusServerAutomateTesterIgnoreAuthPort,
        RadiusServerAutomateTesterIgnoreAcctPort,
        RadiusServerAutomateTesterVrf,
        RadiusServerBackoffExponential, RadiusServerPacKey,
        RadiusServerKey, RadiusServerRetransmit, RadiusServerDscp,
        # §13
        LdapServerCreate, LdapServerIpv4, LdapServerIpv6, LdapServerFqdn,
        LdapServerAuthenticationBindFirst,
        LdapServerAuthenticationBindFirstNoAuthz,
        LdapServerAuthenticationCompare, LdapServerAutomateTester,
        LdapServerBaseDn, LdapServerDeadtime, LdapServerTimeoutRetransmit,
        LdapServerBindAuthenticate, LdapServerBindRootDn,
        LdapServerBindUsername, LdapServerBindPassword,
        LdapServerModeSecure, LdapServerModeSecureNoNegotiation,
        LdapServerSearchTypeNested, LdapServerSearchFilterUserObjectType,
        LdapServerSecureCipher, LdapServerSecureTrustpoint,
        LdapServerTransportPort,
        # §14
        RsHostRetransmit, RsHostTimeout, RsHostKey,
        RsHostTestUsername, RsHostTestUsernameKey, RsKey,
        RsLoadBalanceLeastOutstanding, RsLoadBalanceBatchSize,
        RsLoadBalanceIgnorePreferredServer, RsRetransmit,
        RsSourcePortsExtended, RsTimeout, RsVsaDisallowUnknown,
        RsVsaSend, RsVsaSendAccountingOnly,
        RsVsaSendAuthenticationOnly, RsVsaSendAccountingThreegpp2,
        RsVsaSendAuthenticationThreegpp2, RsVsaSendCiscoNasPort,
        RsVsaSendCiscoNasPortThreegpp2, RsDscp,
        # §15
        IpRadiusSourceInterface, IpRadiusSourceInterfaceVrf,
        Ipv6RadiusSourceInterface, Ipv6RadiusSourceInterfaceVrf,
        IpTacacsSourceInterface, IpMrTacacsSourceInterfaceVrf,
        Ipv6TacacsSourceInterface, Ipv6TacacsSourceInterfaceVrf,
        # §16
        TacacsServerCreate, TacacsServerAddressIpv4,
        TacacsServerAddressIpv6, TacacsServerAddressFqdn,
        TacacsServerPort, TacacsServerTimeout, TacacsServerKey,
        # §17
        TsTimeout, TsDirectedRequest, TsDirectedRequestRestricted,
        TsDirectedRequestNoTruncate, TsKey, TsAttributeAllowUnknown,
        # §18
        UserCommonCriteriaPolicy, UserCommonCriteriaPassword,
        UserAaaAttributeList,
        # §19
        SecAuthenticationFailureRate, SecPasswordsMinLength,
    ],
    Field(discriminator="feature"),
]


# ══════════════════════════════════════════════════════════════
# REQUEST MODELS
# ══════════════════════════════════════════════════════════════
class DeviceRef(BaseModel):
    id: str
    management_ip: str
    platform: Optional[str] = None
    version: Optional[str] = None
    family: Optional[str] = None
    interfaces: list[dict] = Field(default_factory=list)


class Credentials(BaseModel):
    username: str
    password_cipher: str


class ConfigureFeature(BaseModel):
    train: Train = Train.xe_1715
    features: list[AaaFeature] = Field(..., min_length=1)

    @field_validator("features")
    @classmethod
    def _labels_exist(cls, v: list[AaaFeature]) -> list[AaaFeature]:
        for feat in v:
            base = feat.feature.upper()
            label = f"{base}_REMOVE" if feat.remove else base
            if label not in TEMPLATES:
                raise ValueError(f"no template for {label!r}")
        return v


class ConfigureRequest(BaseModel):
    job_id: str
    devices: list[DeviceRef] = Field(..., min_length=1)
    profile: Credentials
    change: ConfigureFeature
    async_: bool = Field(default=True, alias="async")


# ══════════════════════════════════════════════════════════════
# VALUE EXTRACTION + RENDER
# ══════════════════════════════════════════════════════════════
def _values_for(model: BaseModel) -> dict:
    raw = model.model_dump(exclude={"feature", "remove", "train"})
    if "pass_" in raw:
        raw["pass"] = raw.pop("pass_")
    return {k: v for k, v in raw.items() if v is not None}


def render(configure: ConfigureFeature, train: Train) -> str:
    train = train
    inners: list[str] = []
    for feat in configure.features:
        base = feat.feature.upper()
        label = f"{base}_REMOVE" if feat.remove else base
        inners.append(build_edit_config(label, _values_for(feat), train=train))
    return "".join(inners)