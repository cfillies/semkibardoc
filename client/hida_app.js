(function() {
"use strict";

var API_ENDPOINT = '';
    
var hida_app = new Vue({
    el: '#main',
    template: '#hida_app',
    data: function() {
        return {
            page: 0,
            pageSize: 50,
            search: '',
            selected: {
                "Bezirk": [],
                "Ortsteil": [],
                "Sachbegriff": [],
                "Num-Dat": [],
                "Künstler-Rolle": [],
                "Künstler-Name": [],
                "Künstler-Funktion": [],
                "Sozietät-Art-Rolle": [],
                "Sozietät-Name": [],
                "Sozietät-ber-Funktion": [],
                "Ausw-Stelle": []          
                },
            all: {
                "Bezirk": [],
                "Ortsteil": [],
                "Sachbegriff": [],
                "Num-Dat": [],
                "Künstler-Rolle": [],
                "Künstler-Name": [],
                "Künstler-Funktion": [],
                "Sozietät-Art-Rolle": [],
                "Sozietät-Name": [],
                "Sozietät-ber-Funktion": [],
                "Ausw-Stelle": []          
            },
            resolvedCount: '',
        };
    },
    computed: {
        pagesCount: function() {
            return Math.floor(this.resolvedCount / this.pageSize) + 1;
        },
        previousPageDisabled: function() {
            return this.page === 0;
        },
        nextPageDisabled: function() {
            return this.page === this.pagesCount - 1;
        },        
        selectedFilters: function() {
            return [].concat(
                    this.selected.Bezirk.map(function(value){return {value: value, type: 'Bezirk', icon: 'cutlery'};})
                ).concat(
                    this.selected.Ortsteil.map(function(value){return {value: value, type: 'Ortsteil', icon: 'building'};})
                ).concat(
                    this.selected.Sachbegriff.map(function(value){return {value: value, type: 'Sachbegriff', icon: 'map-marker'};})
                ).concat(
                    this.selected["Num-Dat"].map(function(value){return {value: value, type: "Num-Dat", icon: 'map-marker'};})
                ).concat(
                    this.selected["Künstler-Rolle"].map(function(value){return {value: value, type: "Künstler-Rolle", icon: 'map-marker'};})
                ).concat(
                   this.selected["Künstler-Name"].map(function(value){return {value: value, type: "Künstler-Name", icon: 'map-marker'};})
                ).concat(
                   this.selected["Sozietät-Art-Rolle"].map(function(value){return {value: value, type: "Sozietät-Art-Rolle", icon: 'map-marker'};})
                ).concat(
                   this.selected["Sozietät-Name"].map(function(value){return {value: value, type: "Sozietät-Name", icon: 'map-marker'};})
                ).concat(
                   this.selected["Sozietät-ber-Funktion"].map(function(value){return {value: value, type: "Sozietät-ber-Funktion", icon: 'map-marker'};})
                ).concat(
                    this.selected["Ausw-Stelle"].map(function(value){return {value: value, type: "Ausw-Stelle", icon: 'map-marker'};})
                    );
        },
    },
    watch: {
        search: function() {
            this.page = 0;
            this.fetchHida();
            this.fetchFacets();
        },
    },
    methods: {
        previousPage: function() {
            this.page--;
            this.fetchHida();
        },
        nextPage: function() {
            this.page++;
            this.fetchHida();
        },
        removeChip: function(chip) {
            this.removeFacet(chip.value, chip.type);
        },
        facetClicked: function(value, type) {
            var facetList = this.selected[type];
            if (!facetList) return;

            var facetIndex = facetList.indexOf(value);
            // add facet
            if (facetIndex === -1 ) {
                this.addFacet(value, type);
            }
            else { // remove facet
                this.removeFacet(value, type);
            }
        },
        addFacet: function(value, type) {
            this.selected[type].push(value);
            this.page = 0;
            this.fetchHida();
            this.fetchFacets();
        },
        removeFacet: function(value, type) {
            var facetIndex = this.selected[type].indexOf(value);
            this.selected[type].splice(facetIndex, 1);
            this.page = 0;
            this.fetchHida();
            this.fetchFacets();
        },
        isFacetSelected: function(value, type) {
            var facetList = this.selected[type];
            if (!facetList) return false;
            return facetList.indexOf(value) !== -1;
        },
        clearAll: function() {
            this.selected.Bezirk = [];
            this.selected.Ortsteil = [];
            this.selected.Sachbegriff = [];
            this.selected["Num-Dat"] = [];
            this.selected["Künstler-Rolle"] = [];
            this.selected["Künstler-Name"] = [];
            this.selected["Künstler-Funktion"] = [];
            this.selected["Sozietät-Art-Rolle"] = [];
            this.selected["Sozietät-Name"] = [];
            this.selected["Sozietät-ber-Funktion"] = [];
            this.selected["Ausw-Stelle"] = [];
            this.page = 0;
            this.fetchHida();
            this.fetchFacets();
        },
        getQueryOptions: function() {
            var options = {
                params: {
                    page: this.page,
                    page_size: this.pageSize,
                    search: this.search,
                    Bezirk: this.selected.Bezirk.join(','),
                    Ortsteil: this.selected.Ortsteil.join(','),
                    Sachbegriff: this.selected.Sachbegriff.join(','),
                    "Num-Dat": this.selected["Num-Dat"].join(','),
                    "Künstler-Rolle": this.selected["Künstler-Rolle"].join(','),
                    "Künstler-Name": this.selected["Künstler-Name"].join(','),
                    "Künstler-Funktion": this.selected["Künstler-Funktion"].join(','),
                    "Sozietät-Art-Rolle": this.selected["Sozietät-Art-Rolle"].join(','),
                    "Sozietät-Name": this.selected["Sozietät-Name"].join(','),
                    "Sozietät-ber-Funktion": this.selected["Sozietät-ber-Funktion"].join(','),
                    "Ausw-Stelle": this.selected["Ausw-Stelle"].join(','),
                }
            };
            if (this.page <= 0) delete options.params.page;
            if (!this.search) delete options.params.search;
            if (!options.params.Bezirk) delete options.params.Bezirk;
            if (!options.params.Ortsteil) delete options.params.Ortsteil;
            if (!options.params.Sachbegriff) delete options.params.Sachbegriff;
            if (!options.params["Num-Dat"]) delete options.params["Num-Dat"];
            if (!options.params["Künstler-Rolle"]) delete options.params["Künstler-Rolle"];
            if (!options.params["Künstler-Name"]) delete options.params["Künstler-Name"];
            if (!options.params["Künstler-Funktion"]) delete options.params["Künstler-Funktion"];
            if (!options.params["Sozietät-Art-Rolle"]) delete options.params["Sozietät-Art-Rolle"];
            if (!options.params["Sozietät-Name"]) delete options.params["Sozietät-Name"];
            if (!options.params["Sozietät-ber-Funktion"]) delete options.params["Sozietät-ber-Funktion"];
            if (!options.params["Ausw-Stelle"]) delete options.params["Ausw-Stelle"];
            return options;
        },
        fetchHida: function() {
            var self = this;
            var options = this.getQueryOptions();
            return axios.get(API_ENDPOINT + '/search/hida2', options).then(function(response) {
                self.all.resolved = response.data.hida;
                self.resolvedCount = response.data.count;
            });
        },
        fetchFacets: function() {
            var self = this;
            var options = this.getQueryOptions();
            delete options.params.page;
            delete options.params.page_size;
            return axios.get(API_ENDPOINT + '/search/hida2_facets', options).then(function(response) {
                self.all.Bezirk = _getOrderedFacets(
                    self.selected.Bezirk,
                    response.data.Bezirk
                );
                self.all.Ortsteil = _getOrderedFacets(
                    self.selected.Ortsteil,
                    response.data.Ortsteil
                );
                self.all.Sachbegriff = _getOrderedFacets(
                    self.selected.Sachbegriff,
                    response.data.Sachbegriff
                );
                self.all["Num-Dat"] = _getOrderedFacets(
                    self.selected["Num-Dat"],
                    response.data["Num-Dat"]
                );
                self.all["Künstler-Rolle"] = _getOrderedFacets(
                    self.selected["Künstler-Rolle"],
                    response.data["Künstler-Rolle"]
                );
                self.all["Künstler-Name"] = _getOrderedFacets(
                    self.selected["Künstler-Name"],
                    response.data["Künstler-Name"]
                );
                self.all["Künstler-Funktion"] = _getOrderedFacets(
                    self.selected["Künstler-Funktion"],
                    response.data["Künstler-Funktion"]
                );
                self.all["Sozietät-Art-Rolle"] = _getOrderedFacets(
                    self.selected["Sozietät-Art-Rolle"],
                    response.data["Sozietät-Art-Rolle"]
                );
                self.all["Sozietät-Name"] = _getOrderedFacets(
                    self.selected["Sozietät-Name"],
                    response.data["Sozietät-Name"]
                );
                self.all["Sozietät-ber-Funktion"] = _getOrderedFacets(
                    self.selected["Sozietät-ber-Funktion"],
                    response.data["Sozietät-ber-Funktion"]
                );
                self.all["Ausw-Stelle"] = _getOrderedFacets(
                    self.selected["Ausw-Stelle"],
                    response.data["Ausw-Stelle"]
                );
             });
        },
    },
    mounted: function() {
        this.fetchHida();
        this.fetchFacets();
    }
});

function _getOrderedFacets(selectedValues, facets) {
    return selectedValues
        .map(function(value) { // get selected facets (and add count if exists)
            var facet = facets.find(function(facet) {
                return facet.value === value;
            });
            return {
                value: value,
                count: (facet && facet.count) || 'x',
            };
        })
        .concat( // then add unselect facets (excluding the ones that are selected)
             facets.filter(function(facet){ 
                return selectedValues.indexOf(facet.value) === -1;
            })
        );
}


    
})(); 