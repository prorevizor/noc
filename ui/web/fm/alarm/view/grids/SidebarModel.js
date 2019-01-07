//---------------------------------------------------------------------
// fm.alarm application
//---------------------------------------------------------------------
// Copyright (C) 2007-2018 The NOC Project
// See LICENSE for details
//---------------------------------------------------------------------
console.debug("Defining NOC.fm.alarm.view.grids.SidebarModel");

Ext.define("NOC.fm.alarm.view.grids.SidebarModel", {
    extend: "Ext.app.ViewModel",
    alias: "viewmodel.fm.alarm.sidebar",

    data: {
        volume: false,
        autoReload: false,
        loadingStore:true
    },
    formulas: {
        volumeIcon: function(get) {
            // NOC.glyph.volume_up or NOC.glyph.volume_off
            return get("volume") ? "xf028" : "xf026";
        },
        autoReloadIcon: function(get) {
            //  NOC.glyph.refresh or NOC.glyph.ban
            return get("autoReload") ? "xf021" : "xf05e";
        },
        status: {
            bind: "{activeFilter.status}",
            get: function(value) {
                return {
                    status: value
                }
            },
            set: function(value) {
                this.set("activeFilter.status", value.status);
            }
        },
        collapse: {
            bind: "{activeFilter.collapse}",
            get: function(value) {
                return {
                    collapse: value
                }
            },
            set: function(value) {
                this.set("activeFilter.collapse", value.collapse);
            }
        },
        wait_tt: {
            bind: "{activeFilter.wait_tt}",
            get: function(value) {
                return {
                    wait_tt: value
                }
            },
            set: function(value) {
                this.set("activeFilter.wait_tt", value.wait_tt);
            }
        },
        maintenance: {
            bind: "{activeFilter.maintenance}",
            get: function(value) {
                return {
                    maintenance: value
                }
            },
            set: function(value) {
                this.set("activeFilter.maintenance", value.maintenance);
            }
        }
    }
});