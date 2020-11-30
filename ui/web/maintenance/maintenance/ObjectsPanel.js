//---------------------------------------------------------------------
// sa.managedobjectselector ObjectsPanel
//---------------------------------------------------------------------
// Copyright (C) 2007-2020 The NOC Project
// See LICENSE for details
//---------------------------------------------------------------------
console.debug("Defining NOC.maintenance.maintenance.ObjectsPanel");

Ext.define("NOC.maintenance.maintenance.ObjectsPanel", {
    extend: "Ext.grid.Panel",
    requires: ["NOC.maintenance.maintenance.ObjectsModel"],
    mixins: [
        "NOC.core.Export"
    ],
    app: null,
    autoScroll: true,
    stateful: true,
    autoDestroy: true,
    stateId: "sa.managedobjectselector-objects",
    loadMask: true,
    defaultListenerScope: true,

    store: {
        model: "NOC.maintenance.maintenance.ObjectsModel",
        autoLoad: false,
        pageSize: 70,
        leadingBufferZone: 70,
        numFromEdge: Math.ceil(70 / 2),
        trailingBufferZone: 70,
        purgePageCount: 10,
        remoteSort: true,
        sorters: [
            {
                property: 'address',
                direction: 'DESC'
            }
        ],
        proxy: {
            type: "rest",
            pageParam: "__page",
            startParam: "__start",
            limitParam: "__limit",
            sortParam: "__sort",
            reader: {
                type: "json",
                rootProperty: "data",
                totalProperty: "total",
                successProperty: "success"
            },
            writer: {
                type: "json"
            }
        }
    },
    columns: [
        {
            text: __("Name"),
            dataIndex: "name",
            width: 200
        },
        {
            text: __("Managed"),
            dataIndex: "is_managed",
            renderer: NOC.render.Bool,
            width: 50
        },
        {
            text: __("Profile"),
            dataIndex: "profile",
            width: 100
        },
        {
            text: __("Address"),
            dataIndex: "address",
            width: 100
        },
        {
            text: __("Description"),
            dataIndex: "description",
            flex: 1
        },
        {
            text: __("Tags"),
            dataIndex: "tags",
            renderer: NOC.render.Tags,
            width: 150
        }
    ],
    dockedItems: [
        {
            xtype: "toolbar",
            dock: "top",
            items: [
                {
                    text: __("Close"),
                    glyph: NOC.glyph.arrow_left,
                    handler: "onClose"
                },
                {
                    tooltip: __("Export"),
                    text: __("Export"),
                    glyph: NOC.glyph.arrow_down,
                    handler: "onExport"

                },
                "->",
                {
                    xtype: "displayfield",
                    fieldLabel: __("Total"),
                    name: "total",
                    value: __("loading...")
                }
            ]
        }
    ],

    preview: function(record, backItem) {
        var me = this,
            bi = backItem === undefined ? me.backItem : backItem,
            store = me.getStore();

        store.getProxy().setUrl("/maintenance/maintenance/" + record.get("id") + "/objects/");
        store.load({
            scope: me,
            callback: function() {
                me.down("[name=total]").setValue(store.getTotalCount());
            }
        });
        me.currentRecord = record;
        me.backItem = bi;
    },

    onClose: function() {
        var me = this;
        me.app.showItem(me.backItem);
    },

    onExport: function() {
        var me = this;
        me.save(me, 'affected.csv');
    }
});
