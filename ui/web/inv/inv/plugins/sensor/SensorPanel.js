//---------------------------------------------------------------------
// inv.inv SensorPanel
//---------------------------------------------------------------------
// Copyright (C) 2007-2014 The NOC Project
// See LICENSE for details
//---------------------------------------------------------------------
console.debug("Defining NOC.inv.inv.plugins.sensor.SensorPanel");

Ext.define("NOC.inv.inv.plugins.sensor.SensorPanel", {
    extend: "Ext.panel.Panel",
    title: __("Sensors"),
    closable: false,
    layout: "fit",
    requires: [
        "NOC.inv.sensorprofile.LookupField",
        "NOC.pm.measurementunits.LookupField",
        "Ext.ux.form.GridField"
    ],

    initComponent: function() {
        var me = this;

        me.gridField = Ext.create({
            xtype: "gridfield",
            save: false,
            saveHandler: me.saveHandler,
            columns: [
                {
                    dataIndex: "profile",
                    text: __("Profile"),
                    renderer: NOC.render.Lookup("profile"),
                    editor: {
                        xtype: "inv.sensorprofile.LookupField"
                    }
                },
                {
                    dataIndex: "units",
                    text: __("Units"),
                    renderer: NOC.render.Lookup("units"),
                    editor: {
                        xtype: "pm.measurementunits.LookupField"
                    }
                },
                {
                    dataIndex: "object__label",
                    text: __("Object"),
                },
                {
                    dataIndex: "state",
                    text: __("State"),
                    renderer: NOC.render.Lookup("state")
                },
                {
                    dataIndex: "modbus_register",
                    text: __("modbus_register"),
                },
                {
                    dataIndex: "protocol",
                    text: __("Protocol"),
                },
                {
                    dataIndex: "snmp_oid",
                    text: __("snmp_oid"),
                }
            ]
        });
        Ext.apply(me, {
            items: [
                me.gridField
            ]
        });
        me.callParent();
    },
    //
    preview: function(data) {
        var me = this;
        me.currentId = data.id;
        me.gridField.store.loadData(data)
    },
    //
    saveHandler: function() {
        var me = this;
        console.log(me);
    }
});
