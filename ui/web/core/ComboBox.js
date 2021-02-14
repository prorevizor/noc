//---------------------------------------------------------------------
// fm.alarm application
//---------------------------------------------------------------------
// Copyright (C) 2007-2021 The NOC Project
// See LICENSE for details
//---------------------------------------------------------------------
console.debug("Defining NOC.core.ComboBox");

Ext.define("NOC.core.ComboBox", {
    extend: "Ext.form.field.ComboBox",
    alias: "widget.core.combo",
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
    listConfig: {
        minWidth: 240
    },
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
    // custom properties
    isLookupField: true,
    restUrl: null,
    askPermission: true,

    initComponent: function() {
        var tokens,
            me = this;

        // Calculate restUrl
        if(!me.restUrl
            && Ext.String.startsWith(me.$className, 'NOC.')
            && Ext.String.endsWith(me.$className, 'LookupField')) {
            me.restUrl = me.$className
            .replace('NOC', '')
            .replace(/\./g, '/')
            .replace('/LookupField', '/lookup/');
        }

        if(this.restUrl) {
            this.store.proxy.url = this.restUrl;
            tokens = this.restUrl.split("/");
            this.app = tokens[1] + "." + tokens[2];
        }
        // Fix combobox with paging
        this.pickerId = this.getId() + '_picker';
        // end
        // add triggers
        if(NOC.hasOwnProperty("permissions")) {
            me.showTriggers(null);
        } else {
            if(me.askPermission) {
                Ext.Ajax.request({
                    url: me.restUrl.replace("/lookup/", "/launch_info/"),
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
        }
        this.callParent();
    },

    showTriggers: function(value) {
        this.getTrigger("create").hide();
        this.getTrigger("clear").show();
        if(value == null || value === "") {
            if(NOC.hasOwnProperty("permissions")
                && NOC.permissions[this.app]
                && Ext.Array.contains(NOC.permissions[this.app], "create")) {
                this.getTrigger("create").show();
            }
            this.getTrigger("clear").hide();
            this.getTrigger("update").hide();
            return;
        }
        if(NOC.hasOwnProperty("permissions")
            && NOC.permissions[this.app]
            && Ext.Array.contains(NOC.permissions[this.app], "launch")) {
            this.getTrigger("update").show();
        }
    },

    getLookupData: function() {
        return this.getDisplayValue();
    },

    onSpecialKey: function(field, e) {
        var me = this;
        switch(e.keyCode) {
            case e.ESC:
                me.clearValue();
                me.fireEvent("clear");
                break;
        }
    },

    onBeforeQuery: function() {
        var me = this,
            v = this.getRawValue();
        if (typeof v === "undefined" || v === null || v === "") {
            me.clearValue();
            me.fireEvent("clear");
        }
    },

    setValue: function(value, doSelect) {
        var me = this,
            vm,
            params = {};
        if(typeof value === "string" || typeof value === "number") {
            if(value === "" || value === 0) {
                me.clearValue();
                return;
            }
            params[me.valueField] = value;
            Ext.Ajax.request({
                url: me.restUrl,
                method: "GET",
                scope: me,
                params: params,
                success: function (response) {
                    var data = Ext.decode(response.responseText);
                    if (data.length === 1) {
                        vm = me.store.getModel().create(data[0]);
                        me.setValue(vm);
                        if(doSelect) {
                            me.fireEvent("select", me, vm, {});
                        }
                    }
                }
            });
        } else {
            me.callParent([value]);
        }
    },
    // Called by ModelApplication
    cleanValue: function(record, restURL) {
        var me = this,
            rv = record.get(me.name),
            mv = {};
        if(!rv || rv === "" || rv === 0) {
            return ""
        }
        mv[me.valueField] = rv;
        mv[me.displayField] = record.get(me.name + "__label");
        if(mv[me.displayField] === undefined) {
            // Incomplete input data. Just use value as label
            mv[me.displayField] = rv
        }
        return me.store.getModel().create(mv)
    }
});
