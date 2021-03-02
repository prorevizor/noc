//---------------------------------------------------------------------
// inv.firmware application
//---------------------------------------------------------------------
// Copyright (C) 2007-2016 The NOC Project
// See LICENSE for details
//---------------------------------------------------------------------
console.debug("Defining NOC.inv.firmware.Application");

Ext.define("NOC.inv.firmware.Application", {
    extend: "NOC.core.ModelApplication",
    requires: [
        "NOC.core.JSONPreview",
        "NOC.inv.firmware.Model",
        "NOC.inv.vendor.LookupField",
        "NOC.sa.profile.LookupField"
    ],
    model: "NOC.inv.firmware.Model",
    search: true,

    initComponent: function() {
        var me = this;

        me.cardButton = Ext.create("Ext.button.Button", {
            text: __("Card"),
            glyph: NOC.glyph.eye,
            scope: me,
            handler: me.onCard
        });

        me.jsonPanel = Ext.create("NOC.core.JSONPreview", {
            app: me,
            restUrl: new Ext.XTemplate('/inv/firmware/{id}/json/'),
            previewName: new Ext.XTemplate('Firmware: {version}')
        });

        Ext.apply(me, {
            columns: [
                {
                    text: __("Profile"),
                    dataIndex: "profile",
                    width: 100,
                    renderer: NOC.render.Lookup("profile")
                },
                {
                    text: __("Vendor"),
                    dataIndex: "vendor",
                    width: 100,
                    renderer: NOC.render.Lookup("vendor")
                },
                {
                    text: __("Version"),
                    dataIndex: "version",
                    flex: 1
                },
                {
                    text: __("Builtin"),
                    dataIndex: "is_builtin",
                    width: 30,
                    renderer: NOC.render.Bool,
                    sortable: false
                }
            ],

            fields: [
                {
                    name: "profile",
                    xtype: "sa.profile.LookupField",
                    fieldLabel: __("Profile"),
                    allowBlank: false,
                    labelAlign: "left"
                },
                {
                    name: "vendor",
                    xtype: "inv.vendor.LookupField",
                    fieldLabel: __("Vendor"),
                    allowBlank: false,
                    labelAlign: "left"
                },
                {
                    name: "version",
                    xtype: "textfield",
                    fieldLabel: __("Version"),
                    allowBlank: false
                },
                {
                    name: "uuid",
                    xtype: "displayfield",
                    fieldLabel: __("UUID")
                },
                {
                    name: "description",
                    xtype: "textarea",
                    fieldLabel: __("Description"),
                    allowBlank: true
                },
                {
                    name: "download_url",
                    xtype: "textfield",
                    fieldLabel: __("URL"),
                    allowBlank: true
                }
            ],

            formToolbar: [
                me.cardButton,
                {
                    text: __("JSON"),
                    glyph: NOC.glyph.file,
                    tooltip: __("Show JSON"),
                    hasAccess: NOC.hasPermission("read"),
                    scope: me,
                    handler: me.onJSON
                }
            ],

            filters: [
                {
                    title: __("By Profile"),
                    name: "profile",
                    ftype: "lookup",
                    lookup: "sa.profile"
                },
                {
                    title: __("By Vendor"),
                    name: "vendor",
                    ftype: "lookup",
                    lookup: "inv.vendor"
                }
            ]
        });
        me.callParent();
    },

    //
    onCard: function() {
        var me = this;
        if(me.currentRecord) {
            window.open(
                "/api/card/view/firmware/" + me.currentRecord.get("id") + "/"
            );
        }
    },

    onJSON: function() {
        var me = this;
        me.showItem(me.ITEM_JSON);
        me.jsonPanel.preview(me.currentRecord);
    }
});
