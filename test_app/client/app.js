(function () {
    "use strict";

    var API_ENDPOINT = '';
    var dimlist = ["Außenanlagen", "Baumaßnahme", "Bepflanzungen", "Brandschutz",
        "Dach", "Diverse", "Eingangsbereich", "Farbe", "Fassade", "Gebäude", "Gebäudenutzung",
        "Haustechnik", "Maßnahme", "Nutzungsänderung", "Werbeanlage", "path", "hidas", 
        "doctype", "ext", "vorhaben",
        "district", "Sachbegriff", "Denkmalart", "Denkmalname"
    ];

    var dimobj = {};
    for (var i in dimlist) {
        dimobj[dimlist[i]] = [];
    }
    var allobj = JSON.parse(JSON.stringify(dimobj));
    allobj.resolved = [];

    var app = new Vue({
        el: '#main',
        template: '#app',
        data: function () {
            return {
                page: 0,
                pageSize: 30,
                search: '',
                pdfurl: 'https://semtalk.sharepoint.com/sites/KSAG/Freigegebene%20Dokumente/General/pdf/',
                selected: JSON.parse(JSON.stringify(dimobj)),
                all: allobj,
                resolvedCount: '',
                dimensions: dimlist,
                // componentKey: 0,
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
                        this.selected.district.map(function (value) {
                            return {
                                value: value,
                                type: 'district',
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
                window.localStorage.setItem('kibardocpage', this.page);
                window.localStorage.setItem('kibardocsearch', this.search);
                this.fetchResolved();
                this.fetchFacets();
                // this.fetchResolved();
                // this.fetchFacets();
            },
        },
        methods: {
            // forceRerender1: function () {
            //     this.componentKey += 1;  
            //   },
            previousPage: function () {
                this.page--;
                window.localStorage.setItem('kibardocpage', this.page);
                this.fetchResolved();
            },
            nextPage: function () {
                this.page++;
                window.localStorage.setItem('kibardocpage', this.page);
                this.fetchResolved();
            },
            excel: function () {
                this.excelResolved();
            },
            excelqs1: function () {
                this.excelqsResolved();
            },
            hyperlink: function () {
                this.hyperlinkSettings();
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
                window.localStorage.setItem('kibardocpage', this.page);
                window.localStorage.setItem('kibardocselection', JSON.stringify(this.selected));
                this.fetchResolved();
                this.fetchFacets();
            },
            removeFacet: function (value, type) {
                var facetIndex = this.selected[type].indexOf(value);
                this.selected[type].splice(facetIndex, 1);
                this.page = 0;
                window.localStorage.setItem('kibardocpage', this.page);
                window.localStorage.setItem('kibardocselection', JSON.stringify(this.selected));
                this.fetchResolved();
                this.fetchFacets();
            },
            isFacetSelected: function (value, type) {
                var facetList = this.selected[type];
                if (!facetList) return false;
                return facetList.indexOf(value) !== -1;
            },
            backwards: function () {

            },
            clearAll: function () {
                this.selected = JSON.parse(JSON.stringify(dimobj));
                this.page = 0;
                window.localStorage.setItem('kibardocpage', this.page);
                window.localStorage.setItem('kibardocselection', JSON.stringify(this.selected));
                this.fetchResolved();
                this.fetchFacets();
            },
            getQueryOptions: function () {
                var options = {
                    params: {
                        page: this.page,
                        page_size: this.pageSize,
                        search: this.search,
                    }
                };
                for (var i in dimlist) {
                    var d = dimlist[i];
                    if (this.selected[d]) {
                        options.params[d] = this.selected[d].join(',');
                        if (!options.params[d]) delete options.params[d];
                    }
                }
                if (this.page <= 0) delete options.params.page;
                if (!this.search) delete options.params.search;
                return options;
            },
            fetchResolved: function () {
                var self = this;
                window.localStorage.setItem('kibardocsearch', this.search);
                var options = this.getQueryOptions();
                return axios.get(API_ENDPOINT + '/search/resolved2', options).then(function (response) {
                    self.all.resolved = response.data.metadata;
                    self.resolvedCount = response.data.count;
                    // self.forceRerender1();
                    app.$forceUpdate();
                });
            },
            excelResolved: function () {
                var self = this;
                var options = this.getQueryOptions();
                var params = options.params;
                var s = "?";
                for (var p in params) {
                    var d = options.params[p];
                    s += p + "=" + d + "&";
                }
                window.open(API_ENDPOINT + '/excel/resolved2' + s);
                //   return axios.get(API_ENDPOINT + '/excel/resolved2', options).then(function (response) {
                //         window.open(response.data);
                //     });
            },
            excelqsResolved: function () {
                window.open(API_ENDPOINT + '/excel/qs');
            },
            hyperlinkSettings: function () {
                var s = "?";
                if (this.page > 0) {
                    s = s + "page=" + this.page + "&";
                }
                if (this.pageSize != 30) {
                    s = s + "pageSize=" + this.pageSize + "&";
                }
                if (this.search && this.search.length > 0) {
                    s = s + "search=" + this.search + "&";
                }
                for (var setting in this.selected) {
                    if (this.selected[setting].length > 0) {
                        var val = this.selected[setting][0];
                        s = s + setting + "=" + val + "&";
                    }
                }
                if (s.indexOf("&") > 0) s = s.substring(0, s.length - 1);
                window.open(API_ENDPOINT + 'index.html' + s);
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
                    for (var i in dimlist) {
                        var d = dimlist[i];
                        self.all[d] = _getOrderedFacets(
                            self.selected[d],
                            response.data[d]
                        );
                    }
                });
            },
        },
        created: function () {
            console.debug(window.location.href);
        },
        mounted: function () {
            var sel = JSON.parse(window.localStorage.getItem('kibardocselection'));
            if (sel) {
                for (var index1 in dimlist) {
                    var d = dimlist[index1];
                    if (!sel[d]) {
                        sel[d] = [];
                    }
                }
                this.selected = sel;
            }
            var pag = window.localStorage.getItem('kibardocpage');
            if (pag) this.page = parseInt(pag);
            var sea = window.localStorage.getItem('kibardocsearch');
            if (sea) this.search = sea;
            if (location.search.indexOf("?") == 0) {
                var args = location.search.substring(1).split("&");
                for (var index2 in args) {
                    var setting = args[index2].split("=");
                    switch (setting[0]) {
                        case "search": {
                            this.search = decodeURIComponent(setting[1]);
                            break;
                        }
                        case "page": {
                            this.page = parseInt(setting[1]);
                            break;
                        }
                        case "pageSize": {
                            this.pageSize = parseInt(setting[1]);
                            break;
                        }
                        case "pdfurl": {
                            this.pdfurl = decodeURIComponent(setting[1]);
                            break;
                        }
                        default: {
                            var arg = decodeURIComponent(setting[0]);
                            var val = decodeURIComponent(setting[1]);
                            if (dimlist.indexOf(arg) > -1) {
                                this.selected[arg] = [val];
                            }
                            break;
                        }
                    }
                }
            }
            this.fetchDocumentURL();
            this.fetchFacets();
            this.fetchResolved();
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