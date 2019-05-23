//---------------------------------------------------------------------
// main.user application
//---------------------------------------------------------------------
// Copyright (C) 2007-2019 The NOC Project
// See LICENSE for details
//---------------------------------------------------------------------
console.debug("Defining NOC.main.user.Application");

Ext.define("NOC.main.user.Application", {
    extend: "NOC.core.ModelApplication",
    requires: [
        "NOC.core.PasswordField",
        "NOC.main.user.Model",
        "NOC.main.group.Permission"
    ],
    model: "NOC.main.user.Model",
    search: true,
    recordReload: true,
    initComponent: function() {
        var me = this;
        me.setPasswordBtn = Ext.create(
            {
                xtype: "button",
                itemId: "password-update",
                text: __("Set password"),
                margin: "0 0 0 5",
                scope: me,
                handler: me.updatePassword
            }
        );
        Ext.apply(me, {
            columns: [
                {
                    text: __("Username"),
                    dataIndex: "username",
                    width: 110
                },
                {
                    text: __("e-mail Address"),
                    dataIndex: "email",
                    width: 150
                },
                {
                    text: __("First Name"),
                    dataIndex: "first_name",
                    width: 100
                },
                {
                    text: __("Last Name"),
                    dataIndex: "last_name",
                    width: 100
                },
                {
                    text: __("Active"),
                    dataIndex: "is_active",
                    renderer: NOC.render.Bool
                },
                {
                    text: __("Superuser"),
                    dataIndex: "is_superuser",
                    renderer: NOC.render.Bool
                }
            ],
            fields: [
                {
                    name: "username",
                    xtype: "textfield",
                    fieldLabel: __("Username"),
                    autoFocus: true,
                    allowBlank: false,
                    uiStyle: "large"
                },
                {
                    name: "email",
                    xtype: "textfield",
                    fieldLabel: __("e-mail Address"),
                    allowBlank: true,
                    uiStyle: "large"
                },
                {
                    name: "first_name",
                    xtype: "textfield",
                    fieldLabel: __("First Name"),
                    allowBlank: true,
                    uiStyle: "large"
                },
                {
                    name: "last_name",
                    xtype: "textfield",
                    fieldLabel: __("Last Name"),
                    allowBlank: true,
                    uiStyle: "large"
                },
                {
                    name: "is_active",
                    xtype: "checkboxfield",
                    fieldLabel: __("Active"),
                    allowBlank: false
                },
                {
                    name: "is_superuser",
                    xtype: "checkboxfield",
                    fieldLabel: __("Superuser status"),
                    allowBlank: true
                },
                {
                    xtype: "fieldcontainer",
                    itemId: "password",
                    fieldLabel: __("Password"),
                    layout: "hbox",
                    items: [
                        {
                            layout: "vbox",
                            border: false,
                            items: [
                                {
                                    xtype: "password",
                                    name: "password",
                                    uiStyle: "medium"
                                },
                                {
                                    xtype: "password",
                                    name: "password1",
                                    uiStyle: "medium"
                                }
                            ]
                        },
                        me.setPasswordBtn
                    ]
                },
                {
                    xtype: "fieldcontainer",
                    fieldLabel: __("Groups"),
                    items: [
                        {
                            xtype: "multiselector",
                            name: "groups",
                            title: __("Selected Groups"),
                            fieldName: "label",
                            viewConfig: {
                                deferEmptyText: false,
                                emptyText: __("No group selected")
                            },

                            search: {
                                field: "label",
                                store: {
                                    proxy: {
                                        url: "/main/group/lookup/",
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
                                }
                            }
                        }
                    ]
                },
                {
                    xtype: "fieldcontainer",
                    fieldLabel: __("User Permissions"),
                    allowBlank: true,
                    items: [
                        {
                            name: "user_permissions",
                            xtype: "noc.group.permission"
                        }
                    ]
                },
                {
                    name: "last_login",
                    xtype: "displayfield",
                    fieldLabel: __("Last Login"),
                    allowBlank: true,
                    renderer: NOC.render.DateTime
                },
                {
                    name: "date_joined",
                    xtype: "displayfield",
                    fieldLabel: __("Date of joined"),
                    allowBlank: true,
                    renderer: NOC.render.DateTime
                }
            ]
        })
        ;
        me.callParent();
    },
    filters: [
        {
            title: __("Active"),
            name: "is_active",
            ftype: "boolean"
        },
        {
            title: __("Superuser"),
            name: "is_superuser",
            ftype: "boolean"
        }
    ],
    updatePassword: function() {
        var me = this,
            passwordFieldset = me.down("[itemId=password]"),
            passwd = me.form.findField("password").getValue(),
            passwd1 = me.form.findField("password1").getValue();
        if(passwd === passwd1) {
            passwordFieldset.unsetActiveError();
            Ext.Ajax.request({
                url: "/main/user/" + me.currentRecord.id + "/password/",
                method: "POST",
                jsonData: {password: passwd},
                scope: me,
                success: function(response) {
                    var data = Ext.decode(response.responseText);
                    if(data.status) {
                        NOC.info(data.result);
                    }
                },
                failure: function() {
                    NOC.error(__("Failed to set password"));
                }
            });
        } else {
            passwordFieldset.setActiveError(__("Password mismatch"));
        }
    },
    editRecord: function(record) {
        this.setPasswordBtn.show();
        this.down("[name=groups]").getStore().loadData(record.get("groups"));
        this.callParent([record]);
    },
    newRecord: function(defaults) {
        this.setPasswordBtn.hide();
        this.callParent([defaults]);
    },
    saveRecord: function(data) {
        var groups = [],
            groupStore = this.down("[name=groups]").getStore();
        groupStore.each(function(record) {
            groups.push("" + record.id);
        });
        Ext.merge(data, {groups: groups});
        this.callParent([data]);
    },
    onNewRecord: function() {
        var me = this;
        me.down("[name=groups]").getStore().removeAll();
        Ext.Ajax.request({
            url: "/main/group/new_permissions/",
            method: "GET",
            scope: me,
            success: function(response) {
                var me = this,
                    data = Ext.decode(response.responseText).data;
                me.newRecord({user_permissions: data.permissions});
            },
            failure: function() {
                NOC.error(__("Failed to get data"));
            }
        });
    },
    onReset: function() {
        var me = this, msg = __("Reset");
        me.mask(msg);
        Ext.TaskManager.start({
            run: function() {
                me.down("[name=groups]").getStore().removeAll();
                me.form.findField("user_permissions").resetAllPermission();
                me.unmask(msg);
            },
            interval: 0,
            repeat: 1,
            scope: me
        });
        me.callParent();
    }
});