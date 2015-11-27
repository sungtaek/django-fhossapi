from django.db import models

# Create your models here

class Imsu(models.Model):
    id          = models.IntegerField(db_column='id', primary_key=True, editable=False)
    name        = models.CharField(db_column='name', max_length=255, unique=True)
    scscf_name  = models.CharField(db_column='scscf_name', max_length=255, null=True, blank=True)
    diameter_name = models.CharField(db_column='diameter_name', max_length=255, null=True, default='', blank=True)
    capa_set    = models.IntegerField(db_column='id_capabilities_set', null=True, default=-1)
    pref_scscf  = models.IntegerField(db_column='id_preferred_scscf_set', null=True, default=-1)
    
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
    ealry_ims_ip= models.CharField(db_column='ip', max_length=64, default='')
    dsl_line_id = models.CharField(db_column='line_identifier', max_length=64, default='')
    zh_uicc_type= models.IntegerField(db_column='zh_uicc_type', null=True, default=0)
    zh_key_life_time= models.IntegerField(db_column='zh_key_life_time', null=True, default=3600)
    zh_def_auth = models.IntegerField(db_column='zh_default_auth_scheme', choices=AUTH_CHOICE, default=SIP_DIGEST)
    impus       = models.ManyToManyField('Impu', through='ImpiImpu', editable=False)

    class Meta:
        db_table = 'impi'
        managed = False
        

class ImpiImpu(models.Model):
    id          = models.IntegerField(db_column='id', primary_key=True, editable=False)
    impi        = models.ForeignKey('Impi', db_column='id_impi', related_name='impis', editable=False)
    impu        = models.ForeignKey('Impu', db_column='id_impu', related_name='impus', editable=False)
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
    service_profile=models.IntegerField(db_column='id_sp', default=-1)
    implicit_set = models.IntegerField(db_column='id_implicit_set', default=-1)
    charging_info_set=models.IntegerField(db_column='id_charging_info', null=True, default=-1)
    wildcard_psi= models.CharField(db_column='wildcard_psi', max_length=255, default='')
    display_name= models.CharField(db_column='display_name', max_length=255, default='')
    psi_activation= models.BooleanField(db_column='psi_activation', default=False)
    can_register= models.BooleanField(db_column='can_register', default=True)
    impis       = models.ManyToManyField('Impi', through='ImpiImpu', editable=False)
    visited_networks = models.ManyToManyField('VisitedNetwork', through='ImpuVisitedNetwork', editable=False)
    
    class Meta:
        db_table = 'impu'
        managed = False
        
class ImpuVisitedNetwork(models.Model):
    id          = models.IntegerField(db_column='id', primary_key=True, editable=False)
    impu        = models.ForeignKey('Impu', db_column='id_impu', related_name='impus', editable=False)
    visited_network= models.ForeignKey('VisitedNetwork', db_column='id_visited_network', related_name='visited_networks', editable=False)
    
    class Meta:
        db_table = 'impu_visited_network'
        managed = False
        
class VisitedNetwork(models.Model):
    id          = models.IntegerField(db_column='id', primary_key=True, editable=False)
    identity    = models.CharField(db_column='identity', max_length=255, unique=True)
    impus       = models.ManyToManyField('Impu', through='ImpuVisitedNetwork', editable=False)
    
    class Meta:
        db_table = 'visited_network'
        managed = False

