(function () {
    "use strict";

    var API_ENDPOINT = '';

    var app = new Vue(
        {
        el: '#main',
        template: '#app',
        data: function () {
            return {
                page: 0,
                pageSize: 50,
                search: '',
                pdfurl: 'https://semtalk.sharepoint.com/sites/KSAG/Freigegebene%20Dokumente/General/pdf/',
                selected: {
                    Außenanlagen: [],
                    Baumaßnahme: [],
                    Bepflanzungen: [],
                    Brandschutz: [],
                    Dach: [],
                    Diverse: [],
                    Eingangsbereich: [],
                    Farbe: [],
                    Fassade: [],
                    Gebäude: [],
                    Gebäudenutzung: [],
                    Haustechnik: [],
                    Maßnahme: [],
                    Nutzungsänderung: [],
                    Werbeanlage: [],
                    path: [],
                    hidas: [],
                    doctype: [],
                    ext: [],
                    vorhaben: [],
                    Sachbegriff: [],
                    Denkmalart: [],
                    Denkmalname: [],
                },
                all: {
                    Außenanlagen: [],
                    Baumaßnahme: [],
                    Bepflanzungen: [],
                    Brandschutz: [],
                    Dach: [],
                    Diverse: [],
                    Eingangsbereich: [],
                    Farbe: [],
                    Fassade: [],
                    Gebäude: [],
                    Gebäudenutzung: [],
                    Haustechnik: [],
                    Maßnahme: [],
                    Nutzungsänderung: [],
                    Werbeanlage: [],
                    path: [],
                    hidas: [],
                    doctype: [],
                    ext: [],
                    vorhaben: [],
                    Sachbegriff: [],
                    Denkmalart: [],
                    Denkmalname: [],
                },
                resolvedCount: '',
            };
        },
        computed: {
            pagesCount: function () {
                return Math.floor(this.resolvedCount / this.pageSize) + 1;
            },
            previousPageDisabled: function () {
                return this.page === 0;
            },
            nextPageDisabled: function () {
                return this.page === this.pagesCount - 1;
            },
            selectedFilters: function () {
                return []
                    .concat(
                        this.selected.Außenanlagen.map(function (value) {
                            return {
                                value: value,
                                type: 'Außenanlagen',
                                icon: 'cutlery'
                            };
                        })
                    ).concat(
                        this.selected.Baumaßnahme.map(function (value) {
                            return {
                                value: value,
                                type: 'Baumaßnahme',
                                icon: 'building'
                            };
                        })
                    ).concat(
                        this.selected.Bepflanzungen.map(function (value) {
                            return {
                                value: value,
                                type: 'Bepflanzungen',
                                icon: 'map-marker'
                            };
                        })
                    ).concat(
                        this.selected.Dach.map(function (value) {
                            return {
                                value: value,
                                type: 'Dach',
                                icon: 'map-marker'
                            };
                        })
                    ).concat(
                        this.selected.Diverse.map(function (value) {
                            return {
                                value: value,
                                type: 'Diverse',
                                icon: 'map-marker'
                            };
                        })
                    ).concat(
                        this.selected.Eingangsbereich.map(function (value) {
                            return {
                                value: value,
                                type: 'Eingangsbereich',
                                icon: 'map-marker'
                            };
                        })
                    ).concat(
                        this.selected.Farbe.map(function (value) {
                            return {
                                value: value,
                                type: 'Farbe',
                                icon: 'map-marker'
                            };
                        })
                    ).concat(
                        this.selected.Fassade.map(function (value) {
                            return {
                                value: value,
                                type: 'Fassade',
                                icon: 'map-marker'
                            };
                        })
                    ).concat(
                        this.selected.Gebäude.map(function (value) {
                            return {
                                value: value,
                                type: 'Gebäude',
                                icon: 'map-marker'
                            };
                        })
                    ).concat(
                        this.selected.Gebäudenutzung.map(function (value) {
                            return {
                                value: value,
                                type: 'Gebäudenutzung',
                                icon: 'map-marker'
                            };
                        })
                    ).concat(
                        this.selected.Haustechnik.map(function (value) {
                            return {
                                value: value,
                                type: 'Haustechnik',
                                icon: 'map-marker'
                            };
                        })
                    ).concat(
                        this.selected.Maßnahme.map(function (value) {
                            return {
                                value: value,
                                type: 'Maßnahme',
                                icon: 'map-marker'
                            };
                        })
                    ).concat(
                        this.selected.Nutzungsänderung.map(function (value) {
                            return {
                                value: value,
                                type: 'Nutzungsänderung',
                                icon: 'map-marker'
                            };
                        })
                    ).concat(
                        this.selected.Werbeanlage.map(function (value) {
                            return {
                                value: value,
                                type: 'Werbeanlage',
                                icon: 'map-marker'
                            };
                        })
                    ).concat(
                        this.selected.path.map(function (value) {
                            return {
                                value: value,
                                type: 'path',
                                icon: 'map-marker'
                            };
                        })
                    ).concat(
                        this.selected.hidas.map(function (value) {
                            return {
                                value: value,
                                type: 'hidas',
                                icon: 'map-marker'
                            };
                        })
                    ).concat(
                        this.selected.doctype.map(function (value) {
                            return {
                                value: value,
                                type: 'doctype',
                                icon: 'map-marker'
                            };
                        })
                    ).concat(
                        this.selected.ext.map(function (value) {
                            return {
                                value: value,
                                type: 'ext',
                                icon: 'map-marker'
                            };
                        })
                    ).concat(
                        this.selected.vorhaben.map(function (value) {
                            return {
                                value: value,
                                type: 'vorhaben',
                                icon: 'map-marker'
                            };
                        })
                    ).concat(
                        this.selected.Sachbegriff.map(function (value) {
                            return {
                                value: value,
                                type: 'Sachbegriff',
                                icon: 'map-marker'
                            };
                        })
                    ).concat(
                        this.selected.Denkmalart.map(function (value) {
                            return {
                                value: value,
                                type: 'Denkmalart',
                                icon: 'map-marker'
                            };
                        })
                    ).concat(
                        this.selected.Denkmalname.map(function (value) {
                            return {
                                value: value,
                                type: 'Denkmalname',
                                icon: 'map-marker'
                            };
                        })
                    );
            },
        },
        watch: {
            search: function () {
                this.page = 0;
                this.fetchResolved();
                this.fetchFacets();
            },
        },
        methods: {
            previousPage: function () {
                this.page--;
                this.fetchResolved();
            },
            nextPage: function () {
                this.page++;
                this.fetchResolved();
            },
            removeChip: function (chip) {
                this.removeFacet(chip.value, chip.type);
            },
            facetClicked: function (value, type) {
                var facetList = this.selected[type];
                if (!facetList) return;

                var facetIndex = facetList.indexOf(value);
                // add facet
                if (facetIndex === -1) {
                    this.addFacet(value, type);
                } else { // remove facet
                    this.removeFacet(value, type);
                }
            },
            addFacet: function (value, type) {
                this.selected[type].push(value);
                this.page = 0;
                this.fetchResolved();
                this.fetchFacets();
            },
            removeFacet: function (value, type) {
                var facetIndex = this.selected[type].indexOf(value);
                this.selected[type].splice(facetIndex, 1);
                this.page = 0;
                this.fetchResolved();
                this.fetchFacets();
            },
            isFacetSelected: function (value, type) {
                var facetList = this.selected[type];
                if (!facetList) return false;
                return facetList.indexOf(value) !== -1;
            },
            clearAll: function () {
                this.selected.Außenanlagen = [];
                this.selected.Baumaßnahme = [];
                this.selected.Bepflanzungen = [];
                this.selected.Brandschutz = [];
                this.selected.Dach = [];
                this.selected.Diverse = [];
                this.selected.Eingangsbereich = [];
                this.selected.Farbe = [];
                this.selected.Fassade = [];
                this.selected.Gebäude = [];
                this.selected.Gebäudenutzung = [];
                this.selected.Haustechnik = [];
                this.selected.Maßnahme = [];
                this.selected.Nutzungsänderung = [];
                this.selected.Werbeanlage = [];
                this.selected.path = [];
                this.selected.hidas = [];
                this.selected.doctype = [];
                this.selected.ext = [];
                this.selected.vorhaben = [];
                this.selected.Sachbegriff = [];
                this.selected.Denkmalart = [];
                this.selected.Denkmalname = [];
                this.page = 0;
                this.fetchResolved();
                this.fetchFacets();
            },
            getQueryOptions: function () {
                var options = {
                    params: {
                        page: this.page,
                        page_size: this.pageSize,
                        search: this.search,
                        Außenanlagen: this.selected.Außenanlagen.join(','),
                        Baumaßnahme: this.selected.Baumaßnahme.join(','),
                        Bepflanzungen: this.selected.Bepflanzungen.join(','),
                        Dach: this.selected.Dach.join(','),
                        Diverse: this.selected.Diverse.join(','),
                        Eingangsbereich: this.selected.Eingangsbereich.join(','),
                        Farbe: this.selected.Farbe.join(','),
                        Fassade: this.selected.Fassade.join(','),
                        Gebäude: this.selected.Gebäude.join(','),
                        Gebäudenutzung: this.selected.Gebäudenutzung.join(','),
                        Haustechnik: this.selected.Haustechnik.join(','),
                        Maßnahme: this.selected.Maßnahme.join(','),
                        Nutzungsänderung: this.selected.Nutzungsänderung.join(','),
                        Werbeanlage: this.selected.Werbeanlage.join(','),
                        path: this.selected.path.join(','),
                        hidas: this.selected.hidas.join(','),
                        doctype: this.selected.doctype.join(','),
                        ext: this.selected.ext.join(','),
                        vorhaben: this.selected.vorhaben.join(','),
                        Sachbegriff: this.selected.Sachbegriff.join(','),
                        Denkmalart: this.selected.Denkmalart.join(','),
                        Denkmalname: this.selected.Denkmalname.join(','),
                    }
                };
                if (this.page <= 0) delete options.params.page;
                if (!this.search) delete options.params.search;
                if (!options.params.Außenanlagen) delete options.params.Außenanlagen;
                if (!options.params.Baumaßnahme) delete options.params.Baumaßnahme;
                if (!options.params.Bepflanzungen) delete options.params.Bepflanzungen;
                if (!options.params.Dach) delete options.params.Dach;
                if (!options.params.Diverse) delete options.params.Diverse;
                if (!options.params.Eingangsbereich) delete options.params.Eingangsbereich;
                if (!options.params.Farbe) delete options.params.Farbe;
                if (!options.params.Fassade) delete options.params.Fassade;
                if (!options.params.Gebäude) delete options.params.Gebäude;
                if (!options.params.Gebäudenutzung) delete options.params.Gebäudenutzung;
                if (!options.params.Haustechnik) delete options.params.Haustechnik;
                if (!options.params.Maßnahme) delete options.params.Maßnahme;
                if (!options.params.Nutzungsänderung) delete options.params.Nutzungsänderung;
                if (!options.params.Werbeanlage) delete options.params.Werbeanlage;
                if (!options.params.path) delete options.params.path;
                if (!options.params.hidas) delete options.params.hidas;
                if (!options.params.doctype) delete options.params.doctype;
                if (!options.params.ext) delete options.params.ext;
                if (!options.params.vorhaben) delete options.params.vorhaben;
                if (!options.params.Sachbegriff) delete options.params.Sachbegriff;
                if (!options.params.Denkmalart) delete options.params.Denkmalart;
                if (!options.params.Denkmalname) delete options.params.Denkmalname;
                return options;
            },
            fetchResolved: function () {
                var self = this;
                var options = this.getQueryOptions();
                return axios.get(API_ENDPOINT + '/search/resolved2', options).then(function (response) {
                    self.all.resolved = response.data.metadata;
                    self.resolvedCount = response.data.count;
                });
            },
            fetchDocumentURL: function () {
                var self = this;
                return axios.get(API_ENDPOINT + '/search/doclib').then(function (response) {
                    self.pdfurl = response.data.doclib;
                });
            },

            fetchFacets: function () {
                var self = this;
                var options = this.getQueryOptions();
                delete options.params.page;
                delete options.params.page_size;
                return axios.get(API_ENDPOINT + '/search/resolved2_facets', options).then(function (response) {
                    self.all.Außenanlagen = _getOrderedFacets(
                        self.selected.Außenanlagen,
                        response.data.Außenanlagen
                    );
                    self.all.Baumaßnahme = _getOrderedFacets(
                        self.selected.Baumaßnahme,
                        response.data.Baumaßnahme
                    );
                    self.all.Bepflanzungen = _getOrderedFacets(
                        self.selected.Bepflanzungen,
                        response.data.Bepflanzungen
                    );
                    self.all.Brandschutz = _getOrderedFacets(
                        self.selected.Brandschutz,
                        response.data.Brandschutz
                    );
                    self.all.Dach = _getOrderedFacets(
                        self.selected.Dach,
                        response.data.Dach
                    );
                    self.all.Diverse = _getOrderedFacets(
                        self.selected.Diverse,
                        response.data.Diverse
                    );
                    self.all.Eingangsbereich = _getOrderedFacets(
                        self.selected.Eingangsbereich,
                        response.data.Eingangsbereich
                    );
                    self.all.Farbe = _getOrderedFacets(
                        self.selected.Farbe,
                        response.data.Farbe
                    );
                    self.all.Fassade = _getOrderedFacets(
                        self.selected.Fassade,
                        response.data.Fassade
                    );
                    self.all.Gebäude = _getOrderedFacets(
                        self.selected.Gebäude,
                        response.data.Gebäude
                    );
                    self.all.Gebäudenutzung = _getOrderedFacets(
                        self.selected.Gebäudenutzung,
                        response.data.Gebäudenutzung
                    );
                    self.all.Haustechnik = _getOrderedFacets(
                        self.selected.Haustechnik,
                        response.data.Haustechnik
                    );
                    self.all.Maßnahme = _getOrderedFacets(
                        self.selected.Maßnahme,
                        response.data.Maßnahme
                    );
                    self.all.Nutzungsänderung = _getOrderedFacets(
                        self.selected.Nutzungsänderung,
                        response.data.Nutzungsänderung
                    );
                    self.all.Werbeanlage = _getOrderedFacets(
                        self.selected.Werbeanlage,
                        response.data.Werbeanlage
                    );
                    self.all.path = _getOrderedFacets(
                        self.selected.path,
                        response.data.path
                    );
                    self.all.hidas = _getOrderedFacets(
                        self.selected.hidas,
                        response.data.hidas
                    );
                    self.all.doctype = _getOrderedFacets(
                        self.selected.doctype,
                        response.data.doctype
                    );
                    self.all.ext = _getOrderedFacets(
                        self.selected.ext,
                        response.data.ext
                    );
                    self.all.vorhaben = _getOrderedFacets(
                        self.selected.vorhaben,
                        response.data.vorhaben
                    );
                    self.all.Sachbegriff = _getOrderedFacets(
                        self.selected.Sachbegriff,
                        response.data.Sachbegriff
                    );
                    self.all.Denkmalart = _getOrderedFacets(
                        self.selected.Denkmalart,
                        response.data.Denkmalart
                    );
                    self.all.Denkmalname = _getOrderedFacets(
                        self.selected.Denkmalname,
                        response.data.Denkmalname
                    );
                });
            },
        },
        created: function () {
            console.debug(window.location.href);
        },
        mounted: function () {
            this.fetchDocumentURL();
            this.fetchResolved();
            this.fetchFacets();
        }
    });

    function _getOrderedFacets(selectedValues, facets) {
        if (facets === undefined) {
            console.debug("no facts..");
            facets = [];
        }
        return selectedValues
            .map(function (value) { // get selected facets (and add count if exists)
                var facet = facets.find(function (facet) {
                    return facet.value === value;
                });
                return {
                    value: value,
                    count: (facet && facet.count) || 'x',
                };
            })
            .concat( // then add unselect facets (excluding the ones that are selected)
                facets.filter(function (facet) {
                    return selectedValues.indexOf(facet.value) === -1;
                })
            );
    }



})();