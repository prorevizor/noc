# ---------------------------------------------------------------------
# Prefix Table models
# ---------------------------------------------------------------------
# Copyright (C) 2007-2020 The NOC Project
# See LICENSE for details
# ---------------------------------------------------------------------

# Third-party modules
from noc.core.translation import ugettext as _
from django.db import models

# NOC Modules
from noc.core.model.base import NOCModel
from noc.core.ip import IP
from noc.core.model.fields import CIDRField
from noc.core.model.decorator import on_delete_check
from noc.main.models.label import Label


@Label.match_labels(category="prefixfilter")
@on_delete_check(
    check=[
        # ("inv.InterfaceClassificationMatch", "prefix_table"),
        ("sa.ManagedObjectSelector", "filter_prefix")
    ],
    clean_lazy_labels="prefixfilter",
)
class PrefixTable(NOCModel):
    class Meta(object):
        verbose_name = _("Prefix Table")
        verbose_name_plural = _("Prefix Tables")
        db_table = "main_prefixtable"
        app_label = "main"
        ordering = ["name"]

    name = models.CharField(_("Name"), max_length=128, unique=True)
    description = models.TextField(_("Description"), null=True, blank=True)

    def __str__(self):
        return self.name

    def match(self, prefix):
        """
        Check the prefix is inside Prefix Table

        :param prefix: Prefix
        :type prefix: str
        :rtype: bool
        """
        p = IP.prefix(prefix)
        return (
            PrefixTablePrefix.objects.filter(table=self, afi=p.afi)
            .extra(where=["%s <<= prefix"], params=[prefix])
            .exists()
        )

    def __contains__(self, other):
        """
        Usage:
        "prefix" in table
        """
        return self.match(other)

    @classmethod
    def iter_lazy_labels(cls, prefix: str):
        p = IP.prefix(prefix)
        for pt in PrefixTablePrefix.objects.filter(afi=p.afi).extra(
            where=["%s <<= prefix"], params=[prefix]
        ):
            yield f"noc::prefixfilter::{pt.table.name}::<"
            if prefix == pt.prefix:
                yield f"noc::prefixfilter::{pt.table.name}::="


class PrefixTablePrefix(NOCModel):
    class Meta(object):
        verbose_name = _("Prefix")
        verbose_name_plural = _("Prefixes")
        app_label = "main"
        db_table = "main_prefixtableprefix"
        unique_together = [("table", "afi", "prefix")]
        ordering = ["table", "afi", "prefix"]

    table = models.ForeignKey(PrefixTable, verbose_name=_("Prefix Table"), on_delete=models.CASCADE)
    afi = models.CharField(
        _("Address Family"), max_length=1, choices=[("4", _("IPv4")), ("6", _("IPv6"))]
    )
    prefix = CIDRField(_("Prefix"))

    def __str__(self):
        return "%s %s" % (self.table.name, self.prefix)

    def save(self, *args, **kwargs):
        # Set AFI
        self.afi = IP.prefix(self.prefix).afi
        return super().save(*args, **kwargs)
