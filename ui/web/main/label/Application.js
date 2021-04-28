//---------------------------------------------------------------------
// main.label application
//---------------------------------------------------------------------
// Copyright (C) 2007-2021 The NOC Project
// See LICENSE for details
//---------------------------------------------------------------------
console.debug("Defining NOC.main.label.Application");

Ext.define("NOC.main.label.Application", {
  extend: "NOC.core.ModelApplication",
  requires: [
    "NOC.main.label.Model",
    "NOC.main.remotesystem.LookupField",
    "Ext.ux.form.ColorField"
  ],
  model: "NOC.main.label.Model",
  search: true,
  initComponent: function() {
    var me = this;
    Ext.apply(me, {
      columns: [
        {
          text: __("Label"),
          dataIndex: "name",
          width: 100,
          renderer: function(v, _x, item) {
            return NOC.render.Label({
              name: item.data.name,
              description: item.data.description || "",
              bg_color1: item.data.bg_color1 || 0,
              fg_color1: item.data.fg_color1 || 0,
              bg_color2: item.data.bg_color2 || 0,
              fg_color2: item.data.fg_color2 || 0
            });
          }
        },
        {
          text: __("Protected"),
          dataIndex: "is_protected",
          width: 50,
          renderer: NOC.render.Bool
        },
        {
          text: __("Allow"),
          dataIndex: "enable_agent",
          flex: 1,
          renderer: function(_x, _y, item) {
            let r = [];
            if (item.data.enable_agent) {
              r.push(__("Agent"));
            }
            if (item.data.enable_service) {
              r.push(__("Service"));
            }
            if (item.data.enable_serviceprofile) {
              r.push(__("Service Profile"));
            }
            if (item.data.enable_managedobject) {
              r.push(__("Managed Object"));
            }
            if (item.data.enable_managedobjectprofile) {
              r.push(__("Managed Object Profile"));
            }
            if (item.data.enable_administrativedomain) {
              r.push(__("Administrative Domain"));
            }
            if (item.data.enable_authprofile) {
              r.push(__("Auth Profile"));
            }
            if (item.data.enable_commandsnippet) {
              r.push(__("Command Snippet"));
            }
            if (item.data.enable_allocationgroup) {
              r.push(__("Allocation Group"));
            }
            if (item.data.enable_networksegment) {
              r.push(__("Network Segment"));
            }
            if (item.data.enable_object) {
              r.push(__("Object"));
            }
            if (item.data.enable_objectmodel) {
              r.push(__("Object Model"));
            }
            if (item.data.enable_platform) {
              r.push(__("Platfrom"));
            }
            if (item.data.enable_resourcegroup) {
              r.push(__("Resource Group"));
            }
            if (item.data.enable_sensorprofile) {
              r.push(__("Sensor Profile"));
            }
            if (item.data.enable_sensor) {
              r.push(__("Sensor"));
            }
            if (item.data.enable_subscriber) {
              r.push(__("Subscriber"));
            }
            if (item.data.enable_subscriberprofile) {
              r.push(__("Subscriber Profile"));
            }
            if (item.data.enable_supplier) {
              r.push(__("Supplier"));
            }
            if (item.data.enable_supplierprofile) {
              r.push(__("Supplier Profile"));
            }
            if (item.data.enable_dnszone) {
              r.push(__("DNS Zone"));
            }
            if (item.data.enable_dnszonerecord) {
              r.push(__("DNS Zone Record"));
            }
            if (item.data.enable_division) {
              r.push(__("GIS Division"));
            }
            if (item.data.enable_kbentry) {
              r.push(__("KB Entry"));
            }
            if (item.data.enable_ipaddress) {
              r.push(__("IP Address"));
            }
            if (item.data.enable_addressprofile) {
              r.push(__("IP Address Profile"));
            }
            if (item.data.enable_ipaddressrange) {
              r.push(__("IP Address Range"));
            }
            if (item.data.enable_ipprefix) {
              r.push(__("IP Prefix"));
            }
            if (item.data.enable_prefixprofile) {
              r.push(__("Prefix Profile"));
            }
            if (item.data.enable_vrf) {
              r.push(__("VRF"));
            }
            if (item.data.enable_vrfgroup) {
              r.push(__("VRF Group"));
            }
            if (item.data.enable_asn) {
              r.push(__("AS"));
            }
            if (item.data.enable_assetpeer) {
              r.push(__("Asset Peer"));
            }
            if (item.data.enable_peer) {
              r.push(__("Peer"));
            }
            if (item.data.enable_vc) {
              r.push(__("VC"));
            }
            if (item.data.enable_vlan) {
              r.push(__("VLAN"));
            }
            if (item.data.enable_vlanprofile) {
              r.push(__("VLAN Profile"));
            }
            if (item.data.enable_vpn) {
              r.push(__("VPN"));
            }
            if (item.data.enable_vpnprofile) {
              r.push(__("VPN Profile"));
            }
            if (item.data.enable_slaprobe) {
              r.push(__("SLA Probe"));
            }
            if (item.data.enable_slaprofile) {
              r.push(__("SLA Profile"));
            }
            return r.join(", ");
          }
        },
        {
          text: __("Expose"),
          dataIndex: "expose_metric",
          flex: 1,
          renderer: function(_x, _y, item) {
            let r = [];
            if (item.data.expose_metric) {
              r.push(__("Metric"));
            }
            if (item.data.expose_datastream) {
              r.push(__("Datastream"));
            }
            return r.join(", ");
          }
        }
      ],
      fields: [
        {
          name: "name",
          xtype: "textfield",
          fieldLabel: __("Label"),
          uiStyle: "medium",
          allowBlank: false
        },
        {
          name: "description",
          xtype: "textarea",
          fieldLabel: __("Description"),
          allowBlank: true
        },
        {
          name: "is_protected",
          xtype: "checkbox",
          boxLabel: __("Protected"),
          allowBlank: true
        },
        {
          name: "is_autogenerated",
          xtype: "checkbox",
          boxLabel: __("Autogenerated"),
          disabled: true
        },
        {
          xtype: "fieldset",
          layout: "hbox",
          title: __("Colors"),
          defaults: {
            padding: 4,
            labelAlign: "right"
          },
          items: [
            {
              name: "bg_color1",
              xtype: "colorfield",
              fieldLabel: __("Background"),
              allowBlank: false,
              uiStyle: "medium"
            },
            {
              name: "fg_color1",
              xtype: "colorfield",
              fieldLabel: __("Foreground"),
              allowBlank: false,
              uiStyle: "medium"
            }
          ]
        },
        {
          xtype: "fieldset",
          layout: "hbox",
          title: __("Scoped Colors"),
          defaults: {
            padding: 4,
            labelAlign: "right"
          },
          items: [
            {
              name: "bg_color2",
              xtype: "colorfield",
              fieldLabel: __("Background"),
              allowBlank: false,
              uiStyle: "medium"
            },
            {
              name: "fg_color2",
              xtype: "colorfield",
              fieldLabel: __("Foreground"),
              allowBlank: false,
              uiStyle: "medium"
            }
          ]
        },
        {
          xtype: "fieldset",
          layout: "vbox",
          title: __("Enable"),
          defaults: {
            padding: 4,
            labelAlign: "right"
          },
          items: [
        {
          xtype: "fieldset",
          layout: "hbox",
          title: __("ManagedObject"),
          defaults: {
            padding: 4,
            labelAlign: "right"
          },
          items: [
            {
              name: "enable_managedobject",
              xtype: "checkbox",
              boxLabel: __("Managed Object")
            },
            {
              name: "enable_managedobjectprofile",
              xtype: "checkbox",
              boxLabel: __("Managed Object Profile")
            },
              {
              name: "enable_agent",
              xtype: "checkbox",
              boxLabel: __("Agent")
            },
            {
              name: "enable_service",
              xtype: "checkbox",
              boxLabel: __("Service")
            },
            {
              name: "enable_serviceprofile",
              xtype: "checkbox",
              boxLabel: __("Service Profile")
            },
            {
              name: "enable_slaprobe",
              xtype: "checkbox",
              boxLabel: __("SLA Probe")
            },
            {
              name: "enable_slaprofile",
              xtype: "checkbox",
              boxLabel: __("SLA Profile")
            }
            ]
        },
        {
          xtype: "fieldset",
          layout: "hbox",
          title: __("IP / DNS"),
          defaults: {
            padding: 4,
            labelAlign: "right"
          },
          items: [
            {
              name: "enable_ipaddress",
              xtype: "checkbox",
              boxLabel: __("IP Address")
            },
            {
              name: "enable_addressprofile",
              xtype: "checkbox",
              boxLabel: __("IP Address Profile")
            },
            {
              name: "enable_ipaddressrange",
              xtype: "checkbox",
              boxLabel: __("IP Address Range")
            },
            {
              name: "enable_ipprefix",
              xtype: "checkbox",
              boxLabel: __("IP Prefix")
            },
            {
              name: "enable_prefixprofile",
              xtype: "checkbox",
              boxLabel: __("Prefix Profile")
            },
            {
              name: "enable_vrf",
              xtype: "checkbox",
              boxLabel: __("VRF")
            },
            {
              name: "enable_vrfgroup",
              xtype: "checkbox",
              boxLabel: __("VRF Group")
            },
              {
              name: "enable_asn",
              xtype: "checkbox",
              boxLabel: __("AS")
            },
            {
              name: "enable_assetpeer",
              xtype: "checkbox",
              boxLabel: __("Asset Peer")
            },
              {
              name: "enable_peer",
              xtype: "checkbox",
              boxLabel: __("Peer")
            },
            {
              name: "enable_dnszone",
              xtype: "checkbox",
              boxLabel: __("DNS Zone")
            },
            {
              name: "enable_dnszonerecord",
              xtype: "checkbox",
              boxLabel: __("DNS Zone")
            },
            ]
        },
        {
          xtype: "fieldset",
          layout: "hbox",
          title: __("Inventory"),
          defaults: {
            padding: 4,
            labelAlign: "right"
          },
          items: [
            {
              name: "enable_allocationgroup",
              xtype: "checkbox",
              boxLabel: __("Allocation Group")
            },
            {
              name: "enable_networksegment",
              xtype: "checkbox",
              boxLabel: __("Network Segment")
            },
            {
              name: "enable_object",
              xtype: "checkbox",
              boxLabel: __("Object")
            },
            {
              name: "enable_objectmodel",
              xtype: "checkbox",
              boxLabel: __("Object Model")
            },
            {
              name: "enable_platform",
              xtype: "checkbox",
              boxLabel: __("Platform")
            },
            {
              name: "enable_resourcegroup",
              xtype: "checkbox",
              boxLabel: __("Resource Group")
            },
            {
              name: "enable_sensorprofile",
              xtype: "checkbox",
              boxLabel: __("Sensor Profile")
            },
            {
              name: "enable_sensor",
              xtype: "checkbox",
              boxLabel: __("Sensor")
            },
            {
              name: "enable_division",
              xtype: "checkbox",
              boxLabel: __("GIS Division")
            },
          ]
        },
        {
          xtype: "fieldset",
          layout: "hbox",
          title: __("VC"),
          defaults: {
            padding: 4,
            labelAlign: "right"
          },
          items: [
            {
              name: "enable_vc",
              xtype: "checkbox",
              boxLabel: __("VC")
            },
            {
              name: "enable_vlan",
              xtype: "checkbox",
              boxLabel: __("VLAN")
            },
            {
              name: "enable_vlanprofile",
              xtype: "checkbox",
              boxLabel: __("VLAN Profile")
            },
            {
              name: "enable_vpn",
              xtype: "checkbox",
              boxLabel: __("VPN")
            },
            {
              name: "enable_vpnprofile",
              xtype: "checkbox",
              boxLabel: __("VPN Profile")
            }
           ]
        },
        {
          xtype: "fieldset",
          layout: "hbox",
          title: __("Other"),
          defaults: {
            padding: 4,
            labelAlign: "right"
          },
          items: [
            {
              name: "enable_administrativedomain",
              xtype: "checkbox",
              boxLabel: __("Administrative Domain")
            },
            {
              name: "enable_authprofile",
              xtype: "checkbox",
              boxLabel: __("Auth Profile")
            },
            {
              name: "enable_commandsnippet",
              xtype: "checkbox",
              boxLabel: __("Command Snippet")
            },
            {
              name: "enable_subscriber",
              xtype: "checkbox",
              boxLabel: __("Subscriber")
            },
            {
              name: "enable_subscriberprofile",
              xtype: "checkbox",
              boxLabel: __("Subscriber Profile")
            },
            {
              name: "enable_supplier",
              xtype: "checkbox",
              boxLabel: __("Supplier")
            },
            {
              name: "enable_supplierprofile",
              xtype: "checkbox",
              boxLabel: __("Supplier Profile")
            },
            {
              name: "enable_kbentry",
              xtype: "checkbox",
              boxLabel: __("KB Entry")
            }
          ]
          }
        ]},
        {
          xtype: "fieldset",
          layout: "hbox",
          title: __("Expose"),
          defaults: {
            padding: 4,
            labelAlign: "right"
          },
          items: [
            {
              name: "expose_metric",
              xtype: "checkbox",
              boxLabel: __("Metrics")
            },
            {
              name: "expose_datastream",
              xtype: "checkbox",
              boxLabel: __("Datastream")
            }
          ]
        },
        {
          xtype: "fieldset",
          layout: "hbox",
          title: __("Integration"),
          defaults: {
            padding: 4,
            labelAlign: "right"
          },
          items: [
            {
              name: "remote_system",
              xtype: "main.remotesystem.LookupField",
              fieldLabel: __("Remote System"),
              allowBlank: true
            },
            {
              name: "remote_id",
              xtype: "textfield",
              fieldLabel: __("Remote ID"),
              allowBlank: true,
              uiStyle: "medium"
            }
          ]
        }
      ]
    });
    me.callParent();
  }
});
