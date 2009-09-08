# -*- coding: utf-8 -*-
##----------------------------------------------------------------------
## Django's standard models module
## For VC application
##----------------------------------------------------------------------
## Copyright (C) 2007-2009 The NOC Project
## See LICENSE for details
##----------------------------------------------------------------------
"""
"""
from django.db import models
from django.db.models import Q
from noc.main.menu import Menu
from noc.main.search import SearchResult
from noc.main.models import NotificationGroup
from noc.sa.models import ManagedObjectSelector
from noc.lib.validators import is_int
import re
##
## VC Type
##
class VCType(models.Model):
    class Meta:
        verbose_name="VC Type"
        verbose_name_plural="VC Types"
    name=models.CharField("Name",max_length=32,unique=True)
    min_labels=models.IntegerField("Min. Labels",default=1)
    label1_min=models.IntegerField("Label1 min")
    label1_max=models.IntegerField("Label1 max")
    label2_min=models.IntegerField("Label2 min",null=True,blank=True)
    label2_max=models.IntegerField("Label2 max",null=True,blank=True)
    def __unicode__(self):
        return self.name
##
## Virtual circuit domain, allows to separate unique VC spaces
##
class VCDomain(models.Model):
    class Meta:
        verbose_name="VC Domain"
        verbose_name_plural="VC Domains"
    name=models.CharField("Name",max_length=64,unique=True)
    description=models.TextField("Description",blank=True,null=True)
    type=models.ForeignKey(VCType,verbose_name="Type")
    enable_provisioning=models.BooleanField("Enable Provisioning",default=False)
    def __unicode__(self):
        return u"%s: %s"%(unicode(self.type),self.name)
##
## VCDomain Provisioning Parameters
##
class VCDomainProvisioningConfig(models.Model):
    class Meta:
        verbose_name="VC Domain Provisioning Config"
        verbose_name_plural="VC Domain Provisioning Config"
        unique_together=[("vc_domain","selector")]
    vc_domain=models.ForeignKey(VCDomain,verbose_name="VC Domain")
    selector=models.ForeignKey(ManagedObjectSelector,verbose_name="Managed Object Selector")
    is_enabled=models.BooleanField("Is Enabled",default=True)
    tagged_ports=models.CharField("Tagged Ports",max_length=256,null=True,blank=True)
    notification_group=models.ForeignKey(NotificationGroup,verbose_name="Notification Group",null=True,blank=True)    
    def __unicode__(self):
        return u"%s: %s"%(unicode(self.vc_domain),unicode(self.selector))
    ##
    ## Returns a list of tagged ports
    ##
    def _tagged_ports_list(self):
        if self.tagged_ports:
            return [x.strip() for x in self.tagged_ports.split(",")]
        else:
            return []
    tagged_ports_list=property(_tagged_ports_list)
##
## Virtual circuit
##
rx_vc_underline=re.compile("\s+")
rx_vc_empty=re.compile(r"[^a-zA-Z0-9\-_]+")
class VC(models.Model):
    class Meta:
        verbose_name="VC"
        verbose_name_plural="VCs"
        unique_together=[("vc_domain","l1","l2"),("vc_domain","name")]
        ordering=["vc_domain","l1","l2"]
    vc_domain=models.ForeignKey(VCDomain,verbose_name="VC Domain")
    name=models.CharField("Name",max_length=64)
    l1=models.IntegerField("Label 1")
    l2=models.IntegerField("Label 2",default=0)
    description=models.CharField("Description",max_length=256,null=True,blank=True)

    def __unicode__(self):
        s=u"%s %s %d"%(self.vc_domain,self.name,self.l1)
        if self.l2:
            s+=u"/%d"%self.l2
        return s
    ##
    ## Enforce additional checks
    ##
    def save(self):
        if self.l1<self.vc_domain.type.label1_min or self.l1>self.vc_domain.type.label1_max:
            raise Exception("Invalid value for L1")
        if self.vc_domain.type.min_labels>1 and not self.l2:
            raise Exception("L2 required")
        if self.vc_domain.type.min_labels>1 and not (self.l2>=self.vc_domain.type.label2_min and self.l2<=self.vc_domain.type.label2_max):
            raise Exception("Invalid value for L2")
        # Format name
        if self.name:
            name=rx_vc_underline.sub("_",self.name)
            name=rx_vc_empty.sub("",name)
            self.name=name
        else:
            self.name="VC_%04d"%self.l1
        super(VC,self).save()
    ##
    ## Search engine
    ##
    @classmethod
    def search(cls,user,search,limit):
        if user.has_perm("vc.change_vc"):
            if is_int(search):
                tag=int(search)
                for r in VC.objects.filter(Q(l1=tag)|Q(l2=tag))[:limit]:
                    if r.l2:
                        label="%d,%d"%(r.l1,r.l2)
                    else:
                        label="%d"%r.l1
                    yield SearchResult(url="/admin/vc/vc/%d/"%r.id,
                        title="VC: %s, Domain: %s, Label=%s"%(r.type,r.vc_domain.name,label),
                        text=r.description,
                        relevancy=1.0)
##
## Application Menu
##
class AppMenu(Menu):
    app="vc"
    title="Virtual Circuit Management"
    items=[
        ("Virtual Circuits", "/admin/vc/vc/", "vc.change_vc"),
        ("Setup",[
            ("VC Domains", "/admin/vc/vcdomain/", "vc.change_vcdomain"),
            ("VC Types",   "/admin/vc/vctype/", "vc.change_vctype"),
        ])
    ]
