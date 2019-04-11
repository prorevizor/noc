//---------------------------------------------------------------------
// sa.managedobject ConfDBPanel
//---------------------------------------------------------------------
// Copyright (C) 2007-2019 The NOC Project
// See LICENSE for details
//---------------------------------------------------------------------
console.debug("Defining NOC.sa.managedobject.ConfDBPanel");

Ext.define("NOC.sa.managedobject.ConfDBPanel", {
    extend: "NOC.core.ApplicationPanel",
    app: null,
    autoScroll: true,
    layout: "border",
    //
    initComponent: function() {
        var me = this;

        me.currentObject = null;
        me.defaultRoot = {
            text: __("."),
            expanded: true,
            children: []
        };
        me.store = Ext.create("Ext.data.TreeStore", {
            root: me.defaultRoot,
            listeners: {
                scope: me,
                endupdate: this.leafCount
            }
        });
        me.searchField = Ext.create({
            xtype: "textfield",
            emptyText: __("Search ..."),
            flex: 2,
            enableKeyEvents: true,
            anchor: "100%",
            triggers: {
                clear: {
                    cls: "x-form-clear-trigger",
                    hidden: true,
                    weight: -1,
                    handler: function(field) {
                        field.setValue(null);
                        field.fireEvent("select", field);
                    }
                }
            },
            listeners: {
                change: function(field, value) {
                    if(value == null || value === "") {
                        field.getTrigger("clear").hide();
                        this.clearFilter();
                        return;
                    }
                    field.getTrigger("clear").show();
                },
                scope: me,
                specialkey: me.onSpecialKey
            }
        });
        me.matchField = Ext.create({
            xtype: "displayfield"
        });
        // Buttons
        me.refreshButton = Ext.create("Ext.button.Button", {
            text: __("Refresh"),
            glyph: NOC.glyph.refresh,
            scope: me,
            handler: me.onRefresh
        });
        me.queryButton = Ext.create("Ext.button.Button", {
            text: __("Query"),
            glyph: NOC.glyph.search_plus,
            enableToggle: true,
            scope: me,
            handler: me.onShowQueryPanel
        });
        me.runButton = Ext.create("Ext.button.Button", {
            text: __("Run"),
            glyph: NOC.glyph.play,
            disabled: true,
            scope: me,
            handler: me.runQuery
        });
        me.helpButton = Ext.create("Ext.button.Button", {
            tooltip: __("Help"),
            glyph: NOC.glyph.question,
            scope: me,
            handler: me.onHelp
        });
        // Panels
        me.confDBPanel = Ext.create({
            xtype: "treepanel",
            region: "center",
            store: me.store,
            rootVisible: false,
            useArrows: true,
            tbar: [
                me.getCloseButton(),
                me.refreshButton,
                "-",
                me.queryButton,
                "->",
                me.searchField,
                me.matchField
            ]
        });
        me.queryPanel = Ext.create({
            xtype: "panel",
            region: "center",
            height: "30%",
            layout: "fit",
            items: [{
                xtype: "cmtext",
                itemId: "query",
                mode: "python",
                listeners: {
                    scope: me,
                    change: function(field, value) {
                        this.runButton.setDisabled(!value);
                    },
                    run: me.runQuery
                }
            }],
            tbar: [
                me.runButton,
                {
                    xtype: "checkbox",
                    itemId: "cleanup",
                    checked   : true,
                    boxLabel  : __("Cleanup")
                },
                "->",
                me.helpButton
            ]
        });
        me.resultPanel = me.createResultPanel();
        me.rightPanel = Ext.create({
            xtype: "panel",
            layout: "border",
            region: "east",
            width: "30%",
            split: true,
            hidden: true,
            items: [
                me.queryPanel,
                me.resultPanel
            ]

        });
        Ext.apply(me, {
            items: [
                me.confDBPanel,
                me.rightPanel
            ]
        });
        me.callParent();
    },
    //
    setConfDB: function(data) {
        var me = this,
            result = {
                text: ".",
                expanded: true,
                children: []
            },
            applyNode = function(node, conf) {
                Ext.each(conf, function(item) {
                    var r = {
                        text: item.node
                    };
                    if(item.children) {
                        r.children = [];
                        applyNode(r, item.children);
                        r.expanded = r.children.length < 100
                    } else {
                        r.leaf = true
                    }
                    node.children.push(r)
                })
            };
        applyNode(result, data);
        me.store.setRootNode(result)
    },
    //
    preview: function(record, backItem) {
        var me = this;
        me.callParent(arguments);
        me.setTitle(record.get("name") + " ConfDB");
        me.confDBPanel.mask();
        me.url = "/sa/managedobject/" + record.get("id") + "/confdb/";
        Ext.Ajax.request({
            url: me.url,
            method: "GET",
            scope: me,
            success: function(response) {
                var data = Ext.decode(response.responseText);
                me.setConfDB(data);
                me.confDBPanel.unmask()
            },
            failure: function() {
                NOC.error(__("Failed to load data"));
                me.confDBPanel.unmask()
            }
        });
    },
    //
    onRefresh: function() {
        var me = this;
        me.preview(me.currentRecord);
    },
    //
    onSpecialKey: function(field, key) {
        var me = this;
        if(field.xtype !== "textfield")
            return;
        switch(key.getKey()) {
            case Ext.EventObject.ENTER:
                key.stopEvent();
                me.setFilter(field.getValue());
                break;
            case Ext.EventObject.ESC:
                key.stopEvent();
                field.setValue(null);
                break;
        }
    },
    //
    setFilter: function(value) {
        var me = this, matches = 0, searchPattern;
        try {
            searchPattern = new RegExp(value, 'i');
            Ext.suspendLayouts();
            me.store.filter({
                filterFn: function(node) {
                    var children = node.childNodes,
                        len = children && children.length,
                        visible = node.isLeaf() ? searchPattern.test(node.get('text')) : false,
                        i;

                    for(i = 0; i < len && !(visible = children[i].get('visible')); i++) ;

                    if(visible && node.isLeaf()) {
                        matches++;
                    }
                    return visible;
                }
            });
            me.setMatched(matches);
            Ext.resumeLayouts(true);
        } catch(e) {
            NOC.error(__("Invalid regular expression"));
        }
    },
    //
    clearFilter: function() {
        var me = this;
        me.store.clearFilter();
        me.leafCount();
    },
    //
    onShowQueryPanel: function() {
        var me = this;
        if(me.rightPanel.isHidden()) {
            me.rightPanel.show();
        } else {
            me.rightPanel.hide();
        }
    },
    //
    onHelp: function() {
        console.log("show help, not implemented");
    },
    //
    leafCount: function() {
        var me = this, leafCount = 0;
        if(me.store) {
            me.store.getRoot().visitPostOrder("", function(node) {
                if(node.isLeaf()) {
                    leafCount++;
                }
            });
            me.setMatched(leafCount);
        }
    },
    //
    runQuery: function() {
        var me = this;
        me.mask(__("Querying ..."));
        Ext.Ajax.request({
            url: me.url,
            method: "POST",
            scope: me,
            jsonData: {
                query: Ext.String.trim(
                    me.queryPanel.down("[itemId=query]").getValue()
                ),
                // dump: true,
                cleanup: me.queryPanel.down("[itemId=cleanup]").getValue()
            },
            success: function(response) {
                var data = Ext.decode(response.responseText);
                me.unmask();
                if(data.status) {
                    me.resultPanel.destroy();
                    me.rightPanel.add(me.resultPanel = this.createResultPanel(data.result));
                } else {
                    NOC.error(data.error);
                }
            },
            failure: function() {
                me.unmask();
                NOC.error(__("Query failure"))
            }
        });
    },
    //
    setMatched: function(count) {
        var me = this;
        me.matchField.setValue(__("Matched") + ":&nbsp;" + count);
    },
    //
    createResultPanel: function(data) {
        var keys = {},
            cols = [],
            conf = {
                xtype: "panel",
                region: "south",
                height: "70%",
                split: true

            };
        if(data) {
            Ext.each(data, function(e) {
                Ext.each(Object.keys(e), function(k) {
                    keys[k] = true;
                })
            });
            Ext.each(Object.keys(keys), function(e) {
                cols.push({text: e, dataIndex: e})
            });
            Ext.merge(conf, {
                xtype: "grid",
                scrollable: true,
                columns: cols,
                store: {
                    fields: keys,
                    data: data
                },
                tbar: [
                    {
                        xtype: "displayfield",
                        value: __("Result")
                    },
                    "->",
                    {
                        xtype: "displayfield",
                        value: __("Total") + ":&nbsp;" + data.length
                    }]
            });
        }
        return Ext.create(conf);
    }
});
