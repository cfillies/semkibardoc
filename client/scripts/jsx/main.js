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
// allobj.resolved = [];

function array2string(a) {
    if (a) {
    return a.toString().replace(/,/g, ", ");
    } else {
      return "";
    }
  }
  function toggle_hidden(div) {
    var x = document.getElementById(div);
    if (x) {
      if (x.style.display === "none") {
        x.style.display = "block";
      } else {
        x.style.display = "none";
      }
    }
  }
  function hl(s) {
    if (s) {
      return "/showdocument?docid=" + s;
    } else return "";
  }
  function qs(s) {
    if (s) {
      return "/document/" + s + "/edit";
    } else return "";
  }
  function pdfhl(pdfurl,file, path) {
    if (file) {
      var p = path.replace ("C:\\Data\\test\\KIbarDok\\Treptow\\", "" );
      p = p.replace("E:\\2_Köpenick", "");
      p = p.replace("E:\\3_Pankow\\", "");
      p = p.replace (/\\/g, "/");

      return pdfurl + p + "/" + file;
    } else return "";
  }
  function hidaref(s) {
    if (s) {
      return "/showhida/" + s;
    } else return "";
  }

function renderFolder(s) {
    if (s) {
      var li = s.lastIndexOf("\\");
      if (li>0) 
        s=s.substring(li+1);
      return s;
    } else return "";
  }
function getOrderedFacets  (selectedValues, facets) {
    if (facets === undefined) {
        console.debug("no facets..");
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
  
var KIBarDokSearch = React.createClass({

  // sets initial state
  getInitialState: function(){
    return { "search": '', "page": 0, "pageSize": 30,
    pdfurl: 'https://semtalk.sharepoint.com/sites/KSAG/Freigegebene%20Dokumente/General/pdf/',
    selected: JSON.parse(JSON.stringify(dimobj)),
    all: allobj,
    resolved: [],
    resolvedCount: 0
    };
  },

  // sets state, triggers render method
  handleChange: function (event) {
    // grab value form input box
    var search = event.target.value
    window.localStorage.setItem('kibardocpage', 0);
    window.localStorage.setItem('kibardocsearch', search);

    this.setState({"search": search, "page": 0});

    this.fetchResolved(search);
    this.fetchFacets(search);
    console.log("scope updated!");
  },

  pagesCount: function (){
      return Math.floor(this.state.resolvedCount / this.state.pageSize) + 1;
  },
  previousPageDisabled: function (){
    this.setState({"page": 0});
  },
  nextPageDisabled: function (){
      return this.state.page === this.pagesCount() - 1;
  },
  selectedFilters: function (){
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

  previousPage: function (){
      var page = this.state.page;
      page=page--;
      this.setState({ "page": page });
      window.localStorage.setItem('kibardocpage', page);
      this.fetchResolved(this.state.search, page, this.state.pageSize);
  },
  nextPage: function (){
      var page = this.state.page;
      page = page++;
      window.localStorage.setItem('kibardocpage', page);
      this.fetchResolved(this.state.search, page,this.state.pageSize);
  },
  excel: function (){
      this.excelResolved();
  },
  excelqs1: function (){
      this.excelqsResolved();
  },
  hyperlink: function (){
      this.hyperlinkSettings();
  },
  removeChip: function (chip){
      this.removeFacet(chip.value, chip.type);
  },
  facetClicked: function (value, type){
      var facetList = this.state.selected[type];
      if (!facetList) return;

      var facetIndex = facetList.indexOf(value);
      // add facet
      if (facetIndex === -1) {
          this.addFacet(value, type);
      } else { // remove facet
          this.removeFacet(value, type);
      }
  },
  addFacet: function (value, type){
      var selected = this.state.selected;
      var page = 0;
      selected[type].push(value);
      this.setState({ "selected": selected, "page": page });
      window.localStorage.setItem('kibardocpage', page);
      window.localStorage.setItem('kibardocselection', JSON.stringify(selected));
      this.fetchResolved(this.state.search, page,this.state.pageSize);
      this.fetchFacets(this.state.search);
  },
  removeFacet: function (value, type){
      var selected = this.state.selected;
      var page = 0;
      var facetIndex = selected[type].indexOf(value);
      selected[type].splice(facetIndex, 1);
      this.setState({ "selected": selected, "page": page });
      window.localStorage.setItem('kibardocpage', page);
      window.localStorage.setItem('kibardocselection', JSON.stringify(selected));
      this.fetchResolved(this.state.search, page,this.state.pageSize);
      this.fetchFacets(this.state.search);
  },
  isFacetSelected: function (value, type){
      var facetList = this.state.selected[type];
      if (!facetList) return false;
      return facetList.indexOf(value) !== -1;
  },
  backwards: function (){

  },
  clearAll: function (){
    var selected = JSON.parse(JSON.stringify(dimobj));
    var page = 0;
    this.setState({ "selected": selected, "page": page });
      window.localStorage.setItem('kibardocpage', page);
      window.localStorage.setItem('kibardocselection', JSON.stringify(selected));
      this.fetchResolved(this.state.search, page,this.state.pageSize);
      this.fetchFacets(this.state.search);
  },

  getQueryOptions: function (search, page, pageSize) {
    var options = {
        params: {
            "page": page,
            "page_size": pageSize,
            "search": search,
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

  fetchResolved: function (search, page, pageSize){
    var self = this;
    window.localStorage.setItem('kibardocsearch', search);
    var options = this.getQueryOptions(search, page, pageSize);
    return axios.get(API_ENDPOINT + '/search/resolved2', options).then(function (response) {
        console.log("fetchResolved: ", response.data);
        self.setState({"resolved": response.data.metadata, "resolvedCount": response.data.count});
    });
  },
  excelResolved: function (){
    var options = this.getQueryOptions(this.state.search, this.state.page, this.state.pageSize);
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
excelqsResolved: function (){
    window.open(API_ENDPOINT + '/excel/qs');
},
hyperlinkSettings: function (){
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

fetchFacets: function (search) {
  var self = this;
  var options = this.getQueryOptions(search, 1, 30);
  delete options.params.page;
  delete options.params.page_size;
  return axios.get(API_ENDPOINT + '/search/resolved2_facets', options).then(function (response) {
    if (response.data) {
        var data = response.data;
        console.log("fetchFacets: ", data);
        var selected = self.state.selected;
        var all = self.state.all; 
        for (var i in dimlist) {
            var d = dimlist[i];
            all[d] = getOrderedFacets(
                selected[d],
                data[d]
            );
        }
        self.setState({ "all": all });
        };
  });
},


renderrow: function (row){
    console.log("Row: ", row);
    return (<tr>
                <td className="resolved-cell">{ row.docid}</td>
                <td className="resolved-cell">{ row.file}</td>
                <td className="resolved-cell">{ renderFolder(row.path)}</td>
                <td className="resolved-cell">{ row.doctype}</td>
                <td className="resolved-cell">{ array2string(row.adresse)}</td> 
                <td className="resolved-cell">{ array2string(row.vorhaben)}</td>
                <td className="resolved-cell">{ array2string(row.Denkmalname)}</td>
            </tr>);
},
renderFilters: function () {
    var fi = this.state.selectedFilters.map((chip) => {
        <span onclick={this.removeChip(chip)} class="facet-chip">
            <i className="'fa fa-'+chip.icon" aria-hidden="true"></i>
            {chip.value } <span class="close">✖</span>
            </span>});
    return (fi);
},

renderFacetValues: function (dim) {
    var facets = this.state.all[dim];
    var fl = facets.map((facet)=> {
        let selected = this.isFacetSelected(facet.value,dim);
        if (selected) {
            return <div className="facet-item.selected text-clickable"
            onClick={ this.facetClicked(facet.value, dim) }>{ facet.value + ' (' + facet.count + ')' }</div>
        } else {
            return <div className="facet-item text-clickable"
            onClick={ this.facetClicked(facet.value, dim) }>{ facet.value + ' (' + facet.count + ')' }</div>
        }
    });
    // console.debug(fl);
    return [];
    // <div
    // v-for="facet in all.doctype"
                                // class="facet-item text-clickable"
                                // :class="{selected: isFacetSelected(facet.value, 'doctype')}"
                                // @click="facetClicked(facet.value, 'doctype')">
                                // {{ facet.value + ' (' + facet.count + ')' }}

},
render: function() {

    // var countries = this.props.items;
    // var searchString = this.state.search.trim().toLowerCase();

    // // filter countries list by value from input box
    // if(searchString.length > 0){
    //   countries = countries.filter(function(country){
    //     return country.name.toLowerCase().match( searchString );
    //   });
    // }
    var tb = this.state.resolved.map(this.renderrow);
    // console.log(tb);

     return <div>
               <div className="page-title">
                  <img src="logo.png" className="logo" alt="forl and spoon crossed"/>
                  <h2><a href="services" target="_blank">KIbarDok</a>. Suche in {this.state.resolvedCount} Dokumenten.         <a href="/hidafacet">Denkmalliste</a></h2>
                </div>
                <div className="selected-facets">
                { this.selectedFilters.length>0 &&
                    <div>
                        <span>Filtern nach: </span>
                        { this.renderFilters()}
                        <span className="clear-all" onclick={this.clearAll}>Alle Löschen</span>
                      </div>
                }
                </div> 
                <h2>Suche</h2>
                <span>
                    <input type="text" className="searchbox" value={this.state.search} onChange={this.handleChange} placeholder="Suche!" />
                    Seite { this.state.page + 1 } von { this.state.pagesCount }
                    <button onClick={ this.previousPage} className="page-button" title="Vorherige Seite" disabled={this.previousPageDisabled()}> ‹ </button>
                    <button onClick={this.nextPage} className="page-button" title="Nächste Seite" disabled={ this.nextPageDisabled()}> › </button>
                    <button onClick={this.excel} className="button" title="Excel">Excel</button>
                    <button onClick={this.excelqs1} className="button" title="Excel QS">Excel QS</button>
                    <button onClick={this.hyperlink} className="button" title="Hyperlink">Hyperlink</button>
                </span>
                <div className="content">
                    <div className="resolved-facets">
                        <div class="list-facet">
                            <div onClick= { toggle_hidden('fac_doctype') }><i className="fa fa-map-marker" aria-hidden="true"></i><b> Typ</b></div>
                            <div id="fac_doctype">
                                { this.renderFacetValues('doctype') }
                            </div>
                        </div>
                    </div>
                    <div className="resolved-list">
                        <table className="table">
                            <thead>                    
                                <tr><td>ID</td><td>Dokument</td><td>Ordner</td><td>Typ</td><td>Strasse</td><td>Vorhaben</td><td>Denkmalname</td><td>Denkmal</td></tr>
                            </thead>
                            <tbody>
                                { tb }
                            </tbody>
                        </table>
                    </div>
                </div>
         </div>;
  }

});


ReactDOM.render(
  <KIBarDokSearch/>,
  document.getElementById('main')
);