//---------------------------------------------------------------------
// inv.interface L2 Panel
//---------------------------------------------------------------------
// Copyright (C) 2007-2012 The NOC Project
// See LICENSE for details
//---------------------------------------------------------------------
console.debug("Defining NOC.inv.interface.L2Panel");

Ext.define("NOC.inv.interface.L2Panel", {
    extend: "Ext.panel.Panel",
    requires: [
        "Ext.ux.grid.column.GlyphAction"
    ],
    title: __("Switchports"),
    closable: false,
    layout: "fit",

    initComponent: function() {
        var me = this;

        Ext.apply(me, {
            items: [
                {
                    xtype: "gridpanel",
                    border: false,
                    autoScroll: true,
                    stateful: true,
                    stateId: "inv.interface-L2-grid",
                    store: me.store,
                    columns: [
                        {
                            xtype: "glyphactioncolumn",
                            width: 25,
                            items: [
                                {
                                    tooltip: __("Show MACs"),
                                    glyph: NOC.glyph.play,
                                    scope: me,
                                    handler: me.showMAC,
                                    disabled: !me.app.hasPermission("get_mac")
                                }
                            ]
                        },
                        {
                            text: __("Name"),
                            dataIndex: "name"
                        },
                        {
                            text: __("Untag."),
                            dataIndex: "untagged_vlan",
                            width: 50
                        },
                        {
                            text: __("Tagged"),
                            dataIndex: "tagged_vlans",
                            hidden: true
                        },
                        {
                            text: __("Tagged (Ranges)"),
                            dataIndex: "tagged_range"
                        },
                        {
                            text: __("Description"),
                            dataIndex: "description",
                            flex: 1
                        }
                    ]
                }
            ]
        });
        me.callParent();
    },
    //
    showMAC: function(grid, rowIndex, colIndex, item, event, record) {
        var me = this,
            offset = 0,
            rxChunk = /^(\d+)\|/,
            xhr = new XMLHttpRequest();

        me.currentMAC = record;

        me.mask();
        // Start streaming request
        xhr.open(
            'POST',
            '/api/mrt/',
            true
        );
        xhr.setRequestHeader('Content-Type', 'text/json');
        xhr.onprogress = function() {
            // Parse incoming chunks
            var ft = xhr.responseText.substr(offset),
                match, l, lh, chunk, record;

            while(ft) {
                match = ft.match(rxChunk);
                if(!match) {
                    break;
                }
                lh = match[0].length;
                l = parseInt(match[1]);
                chunk = JSON.parse(ft.substr(lh, l));
                offset += lh + l;
                ft = ft.substr(lh + l);
            }
            if(!chunk.running) {
                me.unmask();
                me.showMACForm(chunk.result);
            }
        };
        xhr.send(JSON.stringify([
            {
                id: me.app.currentObject,
                script: "get_mac_address_table",
                args: {
                    interface: record.get("name")
                }
            }
        ]));
        xhr.onerror = function() {
            me.unmask();
            NOC.error(__("Failed to get MACs"));
        };
    },
    //
    showMACForm: function(result) {
        var me = this;
        Ext.create("NOC.inv.interface.MACForm", {
            data: result,
            title: Ext.String.format("MACs on {0}",
                me.currentMAC.get("name"))
        });
    }
});
