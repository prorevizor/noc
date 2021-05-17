//---------------------------------------------------------------------
// inv.sensorprofile application
//---------------------------------------------------------------------
// Copyright (C) 2007-2020 The NOC Project
// See LICENSE for details
//---------------------------------------------------------------------
console.debug("Defining NOC.inv.sensorprofile.Application");

Ext.define("NOC.inv.sensorprofile.Application", {
  extend: "NOC.core.ModelApplication",
  requires: [
    "NOC.core.LabelField",
    "NOC.core.ListFormField",
    "NOC.main.handler.LookupField",
    "NOC.inv.sensorprofile.Model",
    "NOC.wf.workflow.LookupField",
    "NOC.main.style.LookupField"
  ],
  model: "NOC.inv.sensorprofile.Model",
  search: true,
  rowClassField: "row_class",

  initComponent: function() {
    var me = this;
    Ext.apply(me, {
      columns: [
        {
          text: __("Name"),
          dataIndex: "name",
          flex: 1
        },
        {
          text: __("Labels"),
          dataIndex: "labels",
          renderer: NOC.render.LabelField,
          width: 100
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
          allowBlank: true,
          uiStyle: "extra"
        },
        {
          name: "workflow",
          xtype: "wf.workflow.LookupField",
          fieldLabel: __("WorkFlow"),
          allowBlank: false
        },
        {
          name: "style",
          xtype: "main.style.LookupField",
          fieldLabel: __("Style"),
          allowBlank: true
        },
        {
          name: "enable_collect",
          xtype: "checkbox",
          boxLabel: __("Enable Collect"),
          allowBlank: true
        },
        {
          name: "bi_id",
          xtype: "displayfield",
          fieldLabel: __("BI ID"),
          allowBlank: true,
          uiStyle: "medium"
        },
        {
          name: "labels",
          xtype: "labelfield",
          fieldLabel: __("Labels"),
          allowBlank: true,
          query: {
            "enable_sensorprofile": true
          }
          },
          {
            name: "match_rules",
            xtype: "listform",
            fieldLabel: __("Match Rules"),
            items: [
                {
                  name: "dynamic_order",
                  xtype: "numberfield",
                  fieldLabel: __("Dynamic Order"),
                  allowBlank: true,
                  defaultValue: 0,
                  uiStyle: "small"
                },
                {
                  name: "labels",
                  xtype: "labelfield",
                  fieldLabel: __("Match Labels"),
                  allowBlank: false,
                  uiStyle: "extra"
                },
                {
                  name: "handler",
                  xtype: "main.handler.LookupField",
                  fieldLabel: __("Match Handler"),
                  allowBlank: true,
                  uiStyle: "medium",
                  query: {
                    "allow_match_rule": true
                }
                }
              ]
          }
      ]
    });
    me.callParent();
  }
});
