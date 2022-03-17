var API_ENDPOINT = '';
var dimlist = ["Außenanlagen", "Baumaßnahme", "Bepflanzungen", "Brandschutz", "Dach", "Diverse", "Eingangsbereich", "Farbe", "Fassade", "Gebäude", "Gebäudenutzung", "Haustechnik", "Maßnahme", "Nutzungsänderung", "Werbeanlage", "path", "hidas", "doctype", "ext", "vorhaben", "district", "Sachbegriff", "Denkmalart", "Denkmalname"];
var dimobj = {};

for (var i in dimlist) {
  dimobj[dimlist[i]] = [];
}

var allobj = JSON.parse(JSON.stringify(dimobj));
allobj.resolved = [];
var KIBarDokSearch = React.createClass({
  // sets initial state
  getInitialState: function () {
    return {
      "search": '',
      "page": 1,
      "pageSize": 30,
      pdfurl: 'https://semtalk.sharepoint.com/sites/KSAG/Freigegebene%20Dokumente/General/pdf/',
      selected: JSON.parse(JSON.stringify(dimobj)),
      // all: allobj,
      resolved: [],
      resolvedCount: 0,
      dimensions: dimlist
    };
  },
  // sets state, triggers render method
  handleChange: function (event) {
    // grab value form input box
    var search = event.target.value;
    window.localStorage.setItem('kibardocpage', 0);
    window.localStorage.setItem('kibardocsearch', search);
    this.setState({
      "search": search,
      "page": 0
    });
    this.fetchResolved(search);
    this.fetchFacets(search);
    console.log("scope updated!");
  },
  pagesCount: function () {
    return Math.floor(this.state.resolvedCount / this.state.pageSize) + 1;
  },
  previousPageDisabled: function () {
    this.setState({
      "page": 0
    });
  },
  nextPageDisabled: function () {
    return this.state.page === this.pagesCount() - 1;
  },
  selectedFilters: function () {
    var res = [];

    var f = function (value) {
      return {
        value: value,
        type: dim,
        icon: 'map-marker'
      };
    };

    for (var i in dimlist) {
      var dim = dimlist[i];
      res = res.concat(this.state.selected[dim].map(f));
    }

    return res;
  },
  previousPage: function () {
    var page = this.state.page;
    page--;
    this.setState({
      "page": page
    });
    window.localStorage.setItem('kibardocpage', page);
    this.fetchResolved(this.state.search, page, this.state.pageSize);
  },
  nextPage: function () {
    var page = this.state.page;
    page++;
    window.localStorage.setItem('kibardocpage', page);
    this.fetchResolved(this.state.search, page, this.state.pageSize);
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
    var facetList = this.state.selected[type];
    if (!facetList) return;
    var facetIndex = facetList.indexOf(value); // add facet

    if (facetIndex === -1) {
      this.addFacet(value, type);
    } else {
      // remove facet
      this.removeFacet(value, type);
    }
  },
  addFacet: function (value, type) {
    var selected = this.state.selected;
    var page = 0;
    selected[type].push(value);
    this.setState({
      "selected": selected,
      "page": page
    });
    window.localStorage.setItem('kibardocpage', page);
    window.localStorage.setItem('kibardocselection', JSON.stringify(selected));
    this.fetchResolved(this.state.search, page, this.state.pageSize);
    this.fetchFacets(this.state.search);
  },
  removeFacet: function (value, type) {
    var selected = this.state.selected;
    var page = 0;
    var facetIndex = selected[type].indexOf(value);
    selected[type].splice(facetIndex, 1);
    this.setState({
      "selected": selected,
      "page": page
    });
    window.localStorage.setItem('kibardocpage', page);
    window.localStorage.setItem('kibardocselection', JSON.stringify(selected));
    this.fetchResolved(this.state.search, page, this.state.pageSize);
    this.fetchFacets(this.state.search);
  },
  isFacetSelected: function (value, type) {
    var facetList = this.state.selected[type];
    if (!facetList) return false;
    return facetList.indexOf(value) !== -1;
  },
  backwards: function () {},
  clearAll: function () {
    var selected = JSON.parse(JSON.stringify(dimobj));
    var page = 0;
    this.setState({
      "selected": selected,
      "page": page
    });
    window.localStorage.setItem('kibardocpage', page);
    window.localStorage.setItem('kibardocselection', JSON.stringify(selected));
    this.fetchResolved(this.state.search, page, this.state.pageSize);
    this.fetchFacets(this.state.search);
  },
  getQueryOptions: function (search, page, pageSize) {
    var options = {
      params: {
        "page": page,
        "page_size": pageSize,
        "search": search
      }
    };

    for (var i in dimlist) {
      var d = dimlist[i];

      if (this.state.selected[d]) {
        options.params[d] = this.state.selected[d].join(',');
        if (!options.params[d]) delete options.params[d];
      }
    }

    if (this.state.page <= 0) delete options.params.page;
    if (!search) delete options.params.search;
    return options;
  },
  fetchResolved: function (search, page, pageSize) {
    var self = this;
    window.localStorage.setItem('kibardocsearch', search);
    var options = this.getQueryOptions(search, page, pageSize);
    return axios.get(API_ENDPOINT + '/search/resolved2', options).then(function (response) {
      self.setState({
        "resolved": response.data.metadata,
        "resolvedCount": response.data.count
      });
    });
  },
  excelResolved: function () {
    var options = this.getQueryOptions(this.state.search, this.state.page, this.state.pageSize);
    var params = options.params;
    var s = "?";

    for (var p in params) {
      var d = options.params[p];
      s += p + "=" + d + "&";
    }

    window.open(API_ENDPOINT + '/excel/resolved2' + s); //   return axios.get(API_ENDPOINT + '/excel/resolved2', options).then(function (response) {
    //         window.open(response.data);
    //     });
  },
  excelqsResolved: function () {
    window.open(API_ENDPOINT + '/excel/qs');
  },
  hyperlinkSettings: function () {
    var s = "?";

    if (this.state.page > 0) {
      s = s + "page=" + this.state.page + "&";
    }

    if (this.state.pageSize != 30) {
      s = s + "pageSize=" + this.state.pageSize + "&";
    }

    if (this.state.search && this.state.search.length > 0) {
      s = s + "search=" + this.state.search + "&";
    }

    for (var setting in this.state.selected) {
      if (this.state.selected[setting].length > 0) {
        var val = this.state.selected[setting][0];
        s = s + setting + "=" + val + "&";
      }
    }

    if (s.indexOf("&") > 0) s = s.substring(0, s.length - 1);
    window.open(API_ENDPOINT + 'index.html' + s);
  },
  getOrderedFacets: function (selectedValues, facets) {
    if (facets === undefined) {
      console.debug("no facets..");
      facets = [];
    }

    return selectedValues.map(function (value) {
      // get selected facets (and add count if exists)
      var facet = facets.find(function (facet) {
        return facet.value === value;
      });
      return {
        value: value,
        count: facet && facet.count || 'x'
      };
    }).concat( // then add unselect facets (excluding the ones that are selected)
    facets.filter(function (facet) {
      return selectedValues.indexOf(facet.value) === -1;
    }));
  },
  fetchFacets: function (search) {
    var self = this;
    var options = this.getQueryOptions(search, 1, 30);
    delete options.params.page;
    delete options.params.page_size;
    return axios.get(API_ENDPOINT + '/search/resolved2_facets', options).then(function (response) {
      for (var i in dimlist) {
        var d = dimlist[i];
        self.state.all[d] = self.getOrderedFacets(self.state.selected[d], response.data[d]);
      }
    });
  },
  render: function () {
    var countries = this.props.items;
    var searchString = this.state.search.trim().toLowerCase(); // filter countries list by value from input box

    if (searchString.length > 0) {
      countries = countries.filter(function (country) {
        return country.name.toLowerCase().match(searchString);
      });
    }

    var rc = this.state.resolvedCount;
    return React.createElement("div", null, React.createElement("div", {
      "class": "page-title"
    }, React.createElement("img", {
      src: "logo.png",
      "class": "logo",
      alt: "forl and spoon crossed"
    }), React.createElement("h2", null, React.createElement("a", {
      href: "services",
      target: "_blank"
    }, "KIbarDok"), ". Suche in ", this.state.resolvedCount, " Dokumenten.         ", React.createElement("a", {
      href: "/hidafacet"
    }, "Denkmalliste"))), React.createElement("div", null, "Seite ", this.state.page + 1, " von ", this.state.pagesCount, React.createElement("button", {
      onclick: "previousPage",
      "class": "page-button",
      title: "Vorherige Seite",
      disabled: this.previousPageDisabled
    }, " \u2039 "), React.createElement("button", {
      onclick: "nextPage",
      "class": "page-button",
      title: "Nächste Seite",
      disabled: this.nextPageDisabled
    }, " \u203A "), React.createElement("button", {
      onclick: "excel",
      "class": "button",
      title: "Excel"
    }, "Excel"), React.createElement("button", {
      onclick: "excelqs1",
      "class": "button",
      title: "Excel QS"
    }, "Excel QS"), React.createElement("button", {
      onclick: "hyperlink",
      "class": "button",
      title: "Hyperlink"
    }, "Hyperlink")), React.createElement("input", {
      type: "text",
      "class": "searchbox",
      value: this.state.search,
      onChange: this.handleChange,
      placeholder: "Suche!"
    }), React.createElement("div", {
      "class": "resolved-list"
    }, React.createElement("table", {
      "class": "table"
    }, React.createElement("thead", null, React.createElement("tr", null, React.createElement("td", null, "ID"), React.createElement("td", null, "Dokument"), React.createElement("td", null, "Ordner"), React.createElement("td", null, "Typ"), React.createElement("td", null, "Strasse"), React.createElement("td", null, "Vorhaben"), React.createElement("td", null, "Denkmalname"), React.createElement("td", null, "Denkmal"))), React.createElement("tbody", null, this.state.resolved.map(function (resolved) {
      return React.createElement("tr", null, React.createElement("td", null, resolved.ID), React.createElement("td", null, resolved.file), React.createElement("td", null, resolved.path), React.createElement("td", null, resolved.doctype));
    })))));
  }
}); // list of countries, defined with JavaScript object literals

var countries = [{
  "name": "Sweden"
}, {
  "name": "China"
}, {
  "name": "Peru"
}, {
  "name": "Czech Republic"
}, {
  "name": "Bolivia"
}, {
  "name": "Latvia"
}, {
  "name": "Samoa"
}, {
  "name": "Armenia"
}, {
  "name": "Greenland"
}, {
  "name": "Cuba"
}, {
  "name": "Western Sahara"
}, {
  "name": "Ethiopia"
}, {
  "name": "Malaysia"
}, {
  "name": "Argentina"
}, {
  "name": "Uganda"
}, {
  "name": "Chile"
}, {
  "name": "Aruba"
}, {
  "name": "Japan"
}, {
  "name": "Trinidad and Tobago"
}, {
  "name": "Italy"
}, {
  "name": "Cambodia"
}, {
  "name": "Iceland"
}, {
  "name": "Dominican Republic"
}, {
  "name": "Turkey"
}, {
  "name": "Spain"
}, {
  "name": "Poland"
}, {
  "name": "Haiti"
}];
ReactDOM.render(React.createElement(KIBarDokSearch, {
  items: countries
}), document.getElementById('main'));