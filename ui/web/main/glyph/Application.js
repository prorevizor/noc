//---------------------------------------------------------------------
// main.glyph application
//---------------------------------------------------------------------
// Copyright (C) 2007-2020 The NOC Project
// See LICENSE for details
//---------------------------------------------------------------------
console.debug("Defining NOC.main.glyph.Application");

Ext.define("NOC.main.glyph.Application", {
    extend: "NOC.core.ModelApplication",
    requires: [
        "NOC.main.glyph.Model",
        "NOC.main.font.LookupField"
    ],
    model: "NOC.main.glyph.Model",
    search: true,

    initComponent: function() {
        var me = this;

        me.jsonPanel = Ext.create("NOC.core.JSONPreview", {
            app: me,
            restUrl: new Ext.XTemplate('/main/font/{id}/json/'),
            previewName: new Ext.XTemplate('Font: {name}')
        });

        me.ITEM_JSON = me.registerItem(me.jsonPanel);

        Ext.apply(me, {
            columns: [
                {
                    text: __("Name"),
                    dataIndex: "name",
                    width: 200
                },
                {
                    text: __("Font"),
                    dataIndex: "font",
                    renderer: NOC.render.Lookup("font"),
                    width: 100
                },
                {
                    text: __("Glyph"),
                    dataIndex: "code",
                    width: 100,
                    renderer: function(value, meta, record) {
                        return "<span style='font-family: " + record.get("font__label") + "'>&#" + value + ";</span>";
                    }
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
                    name: "uuid",
                    xtype: "displayfield",
                    fieldLabel: __("UUID"),
                    allowBlank: true
                },
                {
                    name: "font",
                    xtype: "main.font.LookupField",
                    fieldLabel: __("Font"),
                    allowBlank: false
                },
                {
                    name: "code",
                    xtype: "numberfield",
                    fieldLabel: __("Code (HEX)"),
                    allowBlank: false,
                    minValue: 0,
                    hideTrigger: true,
                    uiStyle: "small",
                }
            ],

            formToolbar: [
                {
                    text: __("JSON"),
                    glyph: NOC.glyph.file,
                    tooltip: __("Show JSON"),
                    hasAccess: NOC.hasPermission("read"),
                    scope: me,
                    handler: me.onJSON
                }
            ]
        });
        me.callParent();
    },

    onJSON: function () {
        var me = this;
        me.showItem(me.ITEM_JSON);
        me.jsonPanel.preview(me.currentRecord);
    }
});