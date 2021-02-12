//---------------------------------------------------------------------
// fm.alarm application
//---------------------------------------------------------------------
// Copyright (C) 2007-2018 The NOC Project
// See LICENSE for details
//---------------------------------------------------------------------
console.debug("Defining NOC.fm.alarm.view.grids.Lookup");

Ext.define("NOC.fm.alarm.view.grids.Lookup", {
    extend: "Ext.form.field.ComboBox",
    alias: "widget.fm.alarm.lookup",
    displayField: "label",
    valueField: "id",
    queryMode: "remote",
    queryParam: "__query",
    queryCaching: false,
    queryDelay: 200,
    forceSelection: false,
    minChars: 2,
    typeAhead: true,
    triggerAction: "all",
    stateful: false,
    autoSelect: false,
    pageSize: true,
    labelAlign: "top",
    width: "100%",
    store: {
        fields: ["id", "label"],
        pageSize: 25,
        // remoteSort: true,
        // sorters: [
        //     {
        //         property: "label"
        //     }
        // ],
        // sorters: "label",
        proxy: {
            type: "rest",
            pageParam: "__page",
            startParam: "__start",
            limitParam: "__limit",
            sortParam: "__sort",
            extraParams: {
                "__format": "ext"
            },
            reader: {
                type: "json",
                rootProperty: "data",
                totalProperty: "total",
                successProperty: "success"
            }
        }
    },
    triggers: {
        clear: {
            cls: "x-form-clear-trigger",
            hidden: true,
            weight: -1,
            handler: function(field) {
                field.setValue(null);
                field.fireEvent("select", field);
            }
        },
        create: {
            cls: "x-form-plus-trigger",
            hidden: true,
            handler: function() {
                NOC.launch(this.app, "new", {});
            }
        },
        update: {
            cls: "x-form-edit-trigger",
            hidden: true,
            handler: function(field) {
                NOC.launch(this.app, "history", {args: [field.getValue()]});
            }
        }
    },
    listeners: {
        change: function(field, value) {
            this.showTriggers(value);
        }
    },
    initComponent: function() {
        var tokens,
            me = this;
        if(this.url) {
            this.store.proxy.url = this.url;
            tokens = this.url.split("/");
            this.app = tokens[1] + "." + tokens[2];
        }
        // Fix combobox with paging
        this.pickerId = this.getId() + '_picker';
        // end
        // add triggers
        if(NOC.hasOwnProperty("permissions")) {
            me.showTriggers(null);
        } else {
            Ext.Ajax.request({
                url: me.url.replace("/lookup/", "/launch_info/"),
                method: "GET",
                scope: me,
                success: function(response) {
                    var li = Ext.decode(response.responseText);
                    NOC.permissions[li.params.app_id] = li.params.permissions;
                    this.showTriggers(null);
                },
                failure: function() {
                    NOC.error(__("Failed get launch info"));
                }
            });
        }
        this.callParent();
    },
    showTriggers: function(value) {
        if(value == null || value === "") {
            if(Ext.Array.contains(NOC.permissions[this.app], "create")) {
                this.getTrigger("create").show();
            }
            this.getTrigger("clear").hide();
            this.getTrigger("update").hide();
            return;
        }
        if(Ext.Array.contains(NOC.permissions[this.app], "launch")) {
            this.getTrigger("update").show();
        }
        this.getTrigger("create").hide();
        this.getTrigger("clear").show();
    }
});
