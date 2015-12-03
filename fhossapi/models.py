from django.db import models

# Create your models here

class Imsu(models.Model):
    id          = models.IntegerField(db_column='id', primary_key=True, editable=False)
    name        = models.CharField(db_column='name', max_length=255, unique=True)
    scscf_name  = models.CharField(db_column='scscf_name', max_length=255, null=True, blank=True)
    diameter_name = models.CharField(db_column='diameter_name', max_length=255, null=True, default='', blank=True)
    capa_set    = models.ForeignKey('CapabilitiesSet', db_column='id_capabilities_set', to_field='id_set', null=True, editable=False)
    pref_scscf  = models.ForeignKey('PreferredScscfSet', db_column='id_preferred_scscf_set', to_field='id_set', null=True, editable=False)
    
    def dict(self):
        val = {}
        val['name'] = self.name
        val['scscf_name'] = self.scscf_name
        val['diameter_name'] = self.diameter_name
        if self.capa_set:
            val['capa_set'] = self.capa_set.name
        if self.pref_scscf:
            val['pref_scscf'] = self.pref_scscf.name
        val['impi'] = []
        for impi in self.impis.all():
            val['impi'].append(impi.dict())
        return val
    
    class Meta:
        db_table = 'imsu'
        managed = False
        
class Impi(models.Model):
    DIGEST_AKAV1_MD5    = 1
    DIGEST_AKAV2_MD5    = 2
    DIGEST_MD5          = 4
    DIGEST              = 8
    HTTP_DIGEST_MD5     = 16
    EARLY_IMS_SECURITY  = 32
    NASS_BUNDLED        = 64
    SIP_DIGEST          = 128
    AUTH_CHOICE = (
        (DIGEST_AKAV1_MD5, 'Digest-AKAv1-MD5'),
        (DIGEST_AKAV2_MD5, 'Digest-AKAv2-MD5'),
        (DIGEST_MD5, 'Digest-MD5'),
        (DIGEST, 'Digest'),
        (HTTP_DIGEST_MD5, 'HTTP-Digest-MD5'),
        (EARLY_IMS_SECURITY, 'Ealry-IMS-Security'),
        (NASS_BUNDLED, 'NASS-Bundled'),
        (SIP_DIGEST, 'SIP-Digest'),
    )

    id          = models.IntegerField(db_column='id', primary_key=True, editable=False)
    imsu        = models.ForeignKey('Imsu', db_column='id_imsu', related_name='impis', editable=False)
    identity    = models.CharField(db_column='identity', max_length=255, unique=True)
    secret_key  = models.BinaryField(db_column='k')
    avail_auth  = models.IntegerField(db_column='auth_scheme', default=129)
    def_auth    = models.IntegerField(db_column='default_auth_scheme', choices=AUTH_CHOICE, default=SIP_DIGEST)
    amf         = models.BinaryField(db_column='amf', default='0000')
    op          = models.BinaryField(db_column='op', default='00000000000000000000000000000000')
    sqn         = models.CharField(db_column='sqn', max_length=64, default='000000000000')
    early_ims_ip= models.CharField(db_column='ip', max_length=64, default='')
    dsl_line_id = models.CharField(db_column='line_identifier', max_length=64, default='')
    zh_uicc_type= models.IntegerField(db_column='zh_uicc_type', null=True, default=0)
    zh_key_life_time= models.IntegerField(db_column='zh_key_life_time', null=True, default=3600)
    zh_def_auth = models.IntegerField(db_column='zh_default_auth_scheme', choices=AUTH_CHOICE, default=SIP_DIGEST)
    
    def dict(self):
        val = {}
        val['identity'] = self.identity
        val['secret_key'] = self.secret_key
        val['avail_auth'] = []
        for auth in self.AUTH_CHOICE:
            if auth[0] & self.avail_auth:
                val['avail_auth'].append(auth[1])
        val['def_auth'] = self.get_def_auth_display()
        val['amf'] = self.amf
        val['op'] = self.op
        val['sqn'] = self.sqn
        val['early_ims_ip'] = self.early_ims_ip
        val['dsl_line_id'] = self.dsl_line_id
        val['zh_uicc_type'] = self.zh_uicc_type
        val['zh_key_life_time'] = self.zh_key_life_time
        val['zh_def_auth'] = self.get_zh_def_auth_display()
        val['impu'] = []
        for impu in self.impus.all():
            val['impu'].append(impu.dict())
        return val
    
    class Meta:
        db_table = 'impi'
        managed = False
        

class ImpiImpu(models.Model):
    id          = models.IntegerField(db_column='id', primary_key=True, editable=False)
    impi        = models.ForeignKey('Impi', db_column='id_impi', editable=False)
    impu        = models.ForeignKey('Impu', db_column='id_impu', editable=False)
    user_status = models.IntegerField(db_column='user_state', default=0)
    
    class Meta:
        db_table = 'impi_impu'
        managed = False
        
class Impu(models.Model):
    PUBLIC_USER_IDENTITY    = 0
    DISTINCT_PSI            = 1
    WILDCARDED_PSI          = 2
    IMPU_TYPE_CHOICE = (
        (PUBLIC_USER_IDENTITY, 'Public User Identity'),
        (DISTINCT_PSI, 'Distinct PSI'),
        (WILDCARDED_PSI, 'Wildcarted PSI'),
    )
    
    NOT_REGISTERED          = 0
    REGISTERED              = 1
    UNREGISTERED            = 2
    AUTH_PENDING            = 3
    USER_STATUS_CHOICE = (
        (NOT_REGISTERED, 'Not Registered'),
        (REGISTERED, 'Registered'),
        (UNREGISTERED, 'Unregistered'),
        (AUTH_PENDING, 'Auth Pending'),
    )

    id          = models.IntegerField(db_column='id', primary_key=True, editable=False)
    identity    = models.CharField(db_column='identity', max_length=255, unique=True)
    impu_type   = models.IntegerField(db_column='type', choices=IMPU_TYPE_CHOICE, default=PUBLIC_USER_IDENTITY)
    barring     = models.BooleanField(db_column='barring', default=False)
    user_status = models.IntegerField(db_column='user_state', choices=USER_STATUS_CHOICE, default=NOT_REGISTERED)
    service_profile=models.ForeignKey('ServiceProfile', db_column='id_sp', related_name='impus', null=True, editable=False)
    implicit_set = models.IntegerField(db_column='id_implicit_set', default=-1)
    charging_info_set=models.IntegerField(db_column='id_charging_info', null=True, default=-1)
    wildcard_psi= models.CharField(db_column='wildcard_psi', max_length=255, default='')
    display_name= models.CharField(db_column='display_name', max_length=255, default='')
    psi_activation= models.BooleanField(db_column='psi_activation', default=False)
    can_register= models.BooleanField(db_column='can_register', default=True)
    impis       = models.ManyToManyField('Impi', through='ImpiImpu', related_name='impus', editable=False)
    
    def dict(self):
        val = {}
        val['identity'] = self.identity
        val['impu_type'] = self.get_impu_type_display()
        val['barring'] = self.barring
        val['user_status'] = self.get_user_status_display()
        if self.service_profile:
            val['service_profile'] = self.service_profile.name
        val['implicit_set'] = self.implicit_set
        val['charging_info_set'] = self.charging_info_set
        val['wildcard_psi'] = self.wildcard_psi
        val['display_name'] = self.display_name
        val['psi_activation'] = self.psi_activation
        val['can_register'] = self.can_register
        return val

    class Meta:
        db_table = 'impu'
        managed = False
        
    
class ServiceProfile(models.Model):
    id          = models.IntegerField(db_column='id', primary_key=True, editable=False)
    name        = models.CharField(db_column='name', max_length=255, unique=True)
    cn_service_auth= models.IntegerField(db_column='cn_service_auth', null=True, default=0)
    
    def dict(self):
        val = {}
        val['name'] = self.name
        val['ifc'] = []
        for ifc in self.ifcs.all():
            val['ifc'].append(ifc.dict())
        return val

    class Meta:
        db_table = 'sp'
        managed = False

class ServiceProfileIfc(models.Model):
    id          = models.IntegerField(db_column='id', primary_key=True, editable=False)
    id_sp       = models.ForeignKey('ServiceProfile', db_column='id_sp', editable=False)
    id_ifc      = models.ForeignKey('Ifc', db_column='id_ifc', editable=False)
    priority    = models.IntegerField(db_column='priority', default=0)
    
    class Meta:
        db_table = 'sp_ifc'
        managed = False
    
class Ifc(models.Model):
    ANY         = -1
    REGISTERED  = 0
    UNREGISTERED= 1
    PROFILE_CHOICE = (
        (ANY, 'Any'),
        (REGISTERED, 'Registered'),
        (UNREGISTERED, 'Unregistered'),
    )

    id          = models.IntegerField(db_column='id', primary_key=True, editable=False)
    name        = models.CharField(db_column='name', max_length=255, unique=True)
    application_server=models.ForeignKey('ApplicationServer', db_column='id_application_server', editable=False)
    trigger_point=models.ForeignKey('TriggerPoint', db_column='id_tp', editable=False)
    profile_part_indicator=models.IntegerField(db_column='profile_part_ind', choices=PROFILE_CHOICE, default=ANY)
    service_profiles = models.ManyToManyField('ServiceProfile', through='ServiceProfileIfc', related_name='ifcs', editable=False)
    
    def dict(self):
        val = {}
        val['name'] = self.name
        val['application_server'] = self.application_server.dict()
        val['trigger_point'] = self.trigger_point.dict()
        val['profile_part_indicator'] = self.get_profile_part_indicator_display()
        return val

    class Meta:
        db_table = 'ifc'
        managed = False
        
class ApplicationServer(models.Model):
    SESSION_CONTINUE    = 0
    SESSION_TERMINATED  = 1
    DEFAULT_HANDLING_CHOICE = (
        (SESSION_CONTINUE, 'Session Continue'),
        (SESSION_TERMINATED, 'Session Terminated'),
    )

    id          = models.IntegerField(db_column='id', primary_key=True, editable=False)
    name        = models.CharField(db_column='name', max_length=255, unique=True)
    server_name = models.CharField(db_column='server_name', max_length=255, unique=True)
    default_handling= models.IntegerField(db_column='default_handling', choices=DEFAULT_HANDLING_CHOICE, default=SESSION_CONTINUE)
    service_info= models.CharField(db_column='service_info', max_length=255, default='')
    diameter_fqdn= models.CharField(db_column='diameter_address', max_length=255, unique=True)
    rep_data_limit= models.IntegerField(db_column='rep_data_size_limit', default=1024)
    udr_allow   = models.BooleanField(db_column='udr', default=True)
    pur_allow   = models.BooleanField(db_column='pur', default=True)
    snr_allow   = models.BooleanField(db_column='snr', default=True)
    include_regi_response=models.BooleanField(db_column='include_register_response', default=False)
    include_regi_request=models.BooleanField(db_column='include_register_request', default=False)
    
    def dict(self):
        val = {}
        val['name'] = self.name
        val['server_name'] = self.server_name
        val['default_handling'] = self.get_default_handling_display()
        val['service_info'] = self.service_info
        val['diameter_fqdn'] = self.diameter_fqdn
        val['rep_data_limit'] = self.rep_data_limit
        val['udr_allow'] = self.udr_allow
        val['pur_allow'] = self.pur_allow
        val['snr_allow'] = self.snr_allow
        val['include_regi_response'] = self.include_regi_response
        val['include_regi_request'] = self.include_regi_request
        return val
    
    class Meta:
        db_table = 'application_server'
        managed = False
        
class TriggerPoint(models.Model):
    CONDITION_TYPE_DNF  = 0
    CONDITION_TYPE_CNF  = 1
    CONDITION_TYPE_CHOICE = (
        (CONDITION_TYPE_DNF, 'Disjunctive Normal Format'),
        (CONDITION_TYPE_CNF, 'Conjunctive Normal Format'),
    )

    id          = models.IntegerField(db_column='id', primary_key=True, editable=False)
    name        = models.CharField(db_column='name', max_length=255, unique=True)
    condition_type = models.IntegerField(db_column='condition_type_cnf', choices=CONDITION_TYPE_CHOICE, default=CONDITION_TYPE_DNF)
    
    def dict(self):
        val = {}
        val['name'] = self.name
        val['condition_type'] = self.get_condition_type_display()
        val['spt'] = []
        for spt in self.spts.all():
            val['spt'].append(spt.dict())
        return val
    
    class Meta:
        db_table = 'tp'
        managed = False
        
class Spt(models.Model):
    TYPE_REQUEST_URI    = 0
    TYPE_METHOD         = 1
    TYPE_SIP_HEADER     = 2
    TYPE_SESSION_CASE   = 3
    TYPE_SDP_LINE       = 4
    TYPE_CHOICE = (
        (TYPE_REQUEST_URI, 'Request-URI'),
        (TYPE_METHOD, 'SIP Method'),
        (TYPE_SIP_HEADER, 'SIP Header'),
        (TYPE_SESSION_CASE, 'Session Case'),
        (TYPE_SDP_LINE, 'Session Description'),
    )
    
    METHOD_INVITE       = 'INVITE'
    METHOD_REGISTER     = 'REGISTER'
    METHOD_CANCEL       = 'CANCEL'
    METHOD_OPTION       = 'OPTION'
    METHOD_PUBLISH      = 'PUBLISH'
    METHOD_SUBSCRIBE    = 'SUBSCRIBE'
    METHOD_MESSAGE      = 'MESSAGE'
    METHOD_INFO         = 'INFO'
    METHOD_REFER        = 'REFER'
    METHOD_CHOICE = (
        (METHOD_INVITE, 'INVITE'),
        (METHOD_REGISTER, 'REGISTER'),
        (METHOD_CANCEL, 'CANCEL'),
        (METHOD_OPTION, 'OPTION'),
        (METHOD_PUBLISH, 'PUBLISH'),
        (METHOD_SUBSCRIBE, 'SUBSCRIBE'),
        (METHOD_MESSAGE, 'MESSAGE'),
        (METHOD_INFO, 'INFO'),
        (METHOD_REFER, 'REFER'),
    )

    SESSION_CASE_ORIGIN     = 0
    SESSION_CASE_TERM_REG   = 1
    SESSION_CASE_TERM_UNREG = 2
    SESSION_CASE_ORIGIN_UNREG= 3
    SESSION_CASE_ORIGIN_CDIV= 4
    SESSION_CASE_CHOICE = (
        (SESSION_CASE_ORIGIN, 'Origin-Session'),
        (SESSION_CASE_TERM_REG, 'Term-Reg'),
        (SESSION_CASE_TERM_UNREG, 'Term-UnReg'),
        (SESSION_CASE_ORIGIN_UNREG, 'Origin-UnReg'),
        (SESSION_CASE_ORIGIN_CDIV, 'Origin-Cdiv'),
    )
    
    ACTIVE_REG      = 1
    ACTIVE_REREG    = 2
    ACTIVE_DEREG    = 4
    ACTIVE_CHOICE = (
        (ACTIVE_REG, 'Reg'),
        (ACTIVE_REREG, 'ReReg'),
        (ACTIVE_DEREG, 'DeReg'),
    )

    id          = models.IntegerField(db_column='id', primary_key=True, editable=False)
    trigger_point= models.ForeignKey('TriggerPoint', db_column='id_tp', related_name='spts', editable=False)
    condition_nagated=models.BooleanField(db_column='condition_negated', default=False)
    group       = models.IntegerField(db_column='grp', default=0)
    type        = models.IntegerField(db_column='type', choices=TYPE_CHOICE, default=TYPE_REQUEST_URI)
    requesturi  = models.CharField(db_column='requesturi', max_length=255, null=True)
    method      = models.CharField(db_column='method', max_length=255, choices=METHOD_CHOICE, default=METHOD_INVITE, null=True)
    header      = models.CharField(db_column='header', max_length=255, null=True)
    header_content= models.CharField(db_column='header_content', max_length=255, null=True)
    session_case= models.IntegerField(db_column='session_case', null=True, choices=SESSION_CASE_ORIGIN, default=SESSION_CASE_ORIGIN)
    sdp_line    = models.CharField(db_column='sdp_line', max_length=255, null=True)
    sdp_content = models.CharField(db_column='sdp_line_content', max_length=255, null=True)
    regi_type   = models.IntegerField(db_column='registration_type', null=True, default=0)
    
    def dict(self):
        val = {}
        val['condition_nagated'] = self.condition_nagated
        val['group'] = self.group
        val['type'] = self.get_type_display()
        if self.type == self.TYPE_REQUEST_URI:
            val['value'] = self.requesturi
        elif self.type == self.TYPE_METHOD:
            val['value'] = self.method
            if self.method == self.METHOD_REGISTER:
                val['active'] = []
                for active in self.ACTIVE_CHOICE:
                    if active[0] & self.regi_type:
                        val['active'].append(active[1])
        elif self.type == self.TYPE_SIP_HEADER:
            val['value'] = {'header': self.header, 'content': self.header_content}
        elif self.type == self.TYPE_SESSION_CASE:
            val['value'] = self.get_session_case_display()
        elif self.type == self.TYPE_SDP_LINE:
            val['value'] = {'line': self.sdp_line, 'content': self.sdp_content}
        return val
    
    class Meta:
        db_table = 'spt'
        managed = False

class CapabilitiesSet(models.Model):
    id          = models.IntegerField(db_column='id', primary_key=True, editable=False)
    id_set      = models.IntegerField(db_column='id_set', unique=True)
    name        = models.CharField(db_column='name', max_length=255, unique=True)
    id_capability= models.IntegerField(db_column='id_capability', unique=True)
    is_mandatory= models.BooleanField(db_column='is_mandatory', default=False)
    
    class Meta:
        db_table = 'capabilities_set'
        managed = False

class PreferredScscfSet(models.Model):
    id          = models.IntegerField(db_column='id', primary_key=True, editable=False)
    id_set      = models.IntegerField(db_column='id_set', unique=True)
    name        = models.CharField(db_column='name', max_length=255, unique=True)
    scscf_name  = models.CharField(db_column='scscf_name', max_length=255)
    priority    = models.IntegerField(db_column='priority', unique=True)
    
    class Meta:
        db_table = 'preferred_scscf_set'
        managed = False
        
        