//---------------------------------------------------------------------
// ip.addressprofile application
//---------------------------------------------------------------------
// Copyright (C) 2007-2018 The NOC Project
// See LICENSE for details
//---------------------------------------------------------------------
console.debug("Defining NOC.ip.addressprofile.Application");

Ext.define("NOC.ip.addressprofile.Application", {
    extend: "NOC.core.ModelApplication",
    requires: [
        "NOC.core.LabelField",
        "NOC.ip.addressprofile.Model",
        "NOC.wf.workflow.LookupField",
        "NOC.main.style.LookupField",
        "NOC.main.remotesystem.LookupField",
        "NOC.main.template.LookupField"
    ],
    model: "NOC.ip.addressprofile.Model",
    search: true,
    rowClassField: "row_class",

    initComponent: function() {
        var me = this;
        Ext.apply(me, {
            columns: [
                {
                    text: __("Name"),
                    dataIndex: "name",
                    width: 100
                },
                {
                    text: __("Workflow"),
                    dataIndex: "workflow",
                    width: 100,
                    renderer: NOC.render.Lookup("workflow")
                }
            ],

            fields: [
                {
                    name: "name",
                    xtype: "textfield",
                    fieldLabel: __("Name"),
                    allowBlank: false,
                    uiStyle: "medium"
                },
                {
                    name: "description",
                    xtype: "textarea",
                    fieldLabel: __("Description"),
                    allowBlank: true
                },
                {
                    name: "workflow",
                    xtype: "wf.workflow.LookupField",
                    fieldLabel: __("Workflow"),
                    allowBlank: false
                },
                {
                    name: "style",
                    xtype: "main.style.LookupField",
                    fieldLabel: __("Style"),
                    allowBlank: true
                },
                {
                    name: "name_template",
                    xtype: "main.template.LookupField",
                    fieldLabel: __("Name Template"),
                    allowBlank: true
                },
                {
                    name: "fqdn_template",
                    xtype: "main.template.LookupField",
                    fieldLabel: __("FQDN Template"),
                    allowBlank: true
                },
                {
                    name: "seen_propagation_policy",
                    xtype: "combobox",
                    fieldLabel: __("Seen propagation"),
                    allowBlank: false,
                    store: [
                        ["E", __("Enable")],
                        ["D", __("Disable")]
                    ],
                    uiStyle: "medium"
                },
                {
                    xtype: "fieldset",
                    layout: "hbox",
                    title: __("Integration"),
                    defaults: {
                        padding: 4,
                        labelAlign: "right"
                    },
                    items: [
                        {
                            name: "remote_system",
                            xtype: "main.remotesystem.LookupField",
                            fieldLabel: __("Remote System"),
                            allowBlank: true
                        },
                        {
                            name: "remote_id",
                            xtype: "textfield",
                            fieldLabel: __("Remote ID"),
                            allowBlank: true,
                            uiStyle: "medium"
                        },
                        {
                            name: "bi_id",
                            xtype: "displayfield",
                            fieldLabel: __("BI ID"),
                            allowBlank: true,
                            uiStyle: "medium"
                        }
                    ]
                },
                {
                    name: "labels",
                    xtype: "labelfield",
                    fieldLabel: __("Labels"),
                    allowBlank: true,
                    query: {
                        "enable_addressprofile": true
                    },
                }
            ]
        });
        me.callParent();
    }
});
