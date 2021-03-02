//---------------------------------------------------------------------
// sa.groupaccess application
//---------------------------------------------------------------------
// Copyright (C) 2007-2012 The NOC Project
// See LICENSE for details
//---------------------------------------------------------------------
console.debug("Defining NOC.sa.groupaccess.Application");

Ext.define("NOC.sa.groupaccess.Application", {
    extend: "NOC.core.ModelApplication",
    requires: [
        "NOC.sa.groupaccess.Model",
        "NOC.aaa.group.LookupField",
        "NOC.sa.managedobjectselector.LookupField",
        "NOC.sa.administrativedomain.LookupField"
    ],
    model: "NOC.sa.groupaccess.Model",
    columns: [
        {
            text: __("Group"),
            dataIndex: "group",
            renderer: NOC.render.Lookup("group")
        },
        {
            text: __("Selector"),
            dataIndex: "selector",
            renderer: NOC.render.Lookup("selector")
        },
        {
            text: __("Adm. Domain"),
            dataIndex: "administrative_domain",
            renderer: NOC.render.Lookup("administrative_domain")
        }
    ],
    fields: [
        {
            name: "group",
            xtype: "aaa.group.LookupField",
            fieldLabel: __("Group"),
            labelAlign: "left",
            allowBlank: false
        },
        {
            name: "selector",
            xtype: "sa.managedobjectselector.LookupField",
            fieldLabel: __("Object Selector"),
            labelAlign: "left",
            allowBlank: true
        },
        {
            name: "administrative_domain",
            xtype: "sa.administrativedomain.LookupField",
            fieldLabel: __("Adm. Domain"),
            labelAlign: "left",
            allowBlank: true
        }
    ],
    filters: [
        {
            title: __("By Group"),
            name: "group",
            ftype: "lookup",
            lookup: "aaa.group"
        },
        {
            title: __("By Selector"),
            name: "selector",
            ftype: "lookup",
            lookup: "sa.managedobjectselector"
        },
        {
            title: __("By Administrative Domain"),
            name: "administrative_domain",
            ftype: "lookup",
            lookup: "sa.administrativedomain"
        }
    ]
});
