export interface FilterInterface {
    "Antrag": boolean,
    "Eigangsbestätigung": boolean,
    "Genehmigung": boolean,
    "Versagung": boolean,
    "Stellungnahme": boolean,
    "Anhorungrag": boolean,
    "page": number,
    "page_size": number
  }
  
export interface DocumentsInterface {
    id: number,
    file: string,
    path: string,
    doctype: string,
    adresse: string,
    hidas: string,
    denkmalart: string,
    doc_image: string,
  }

 export interface SearchInterface {
    "field": string,
    "search": string
  }

  export interface AsideMenuInterface {
    "Außenanlagen": InnerAsideMenuInterface[],
    "Baumaßnahme": InnerAsideMenuInterface[],
    "Bepflanzungen": InnerAsideMenuInterface[],
    "Brandschutz": InnerAsideMenuInterface[],
    "Dach": InnerAsideMenuInterface[],
    "Denkmalart": InnerAsideMenuInterface[],
    "Denkmalname": InnerAsideMenuInterface[],
    "Diverse": InnerAsideMenuInterface[],
    "Eingangsbereich": InnerAsideMenuInterface[],
    "Farbe": InnerAsideMenuInterface[],
    "Fassade": InnerAsideMenuInterface[],
    "Fenster": InnerAsideMenuInterface[],
    "Funk": InnerAsideMenuInterface[],
    "Gebäude": InnerAsideMenuInterface[],
    "Gebäudenutzung": InnerAsideMenuInterface[],
    "Haustechnik": InnerAsideMenuInterface[],
    "Kunst": InnerAsideMenuInterface[],
    "Maßnahme": InnerAsideMenuInterface[],
    "Nutzungsänderung": InnerAsideMenuInterface[],
    "Sachbegriff": InnerAsideMenuInterface[],
    "Solaranlage": InnerAsideMenuInterface[],
    "Treppenhaus": InnerAsideMenuInterface[],
    "Tür": InnerAsideMenuInterface[],
    "Werbeanlage": InnerAsideMenuInterface[],
    "district": InnerAsideMenuInterface[],
    "doctype": InnerAsideMenuInterface[],
    "ext": InnerAsideMenuInterface[],
    "hidas": InnerAsideMenuInterface[],
    "path": InnerAsideMenuInterface[],
    "vorhaben": InnerAsideMenuInterface[]
  }

  export interface InnerAsideMenuInterface {
    value: string,
    count: number
  }

  export interface AsideMenuItemFetchInterface {
    fieldName: string, 
    valueField: string
  }

  export interface AsideFiltersInterface {
    "Außenanlagen": String[],
    "Baumaßnahme": String[],
    "Bepflanzungen": String[],
    "Brandschutz": String[],
    "Dach": String[],
    "Denkmalart": String[],
    "Denkmalname": String[],
    "Diverse": String[],
    "Eingangsbereich": String[],
    "Farbe": String[],
    "Fassade": String[],
    "Fenster": String[],
    "Funk": String[],
    "Gebäude": String[],
    "Gebäudenutzung": String[],
    "Haustechnik": String[],
    "Kunst": String[],
    "Maßnahme": String[],
    "Nutzungsänderung": String[],
    "Sachbegriff": String[],
    "Solaranlage": String[],
    "Treppenhaus": String[],
    "Tür": String[],
    "Werbeanlage": String[],
    "district": String[],
    "doctype": String[],
    "ext": String[],
    "hidas": String[],
    "path": String[],
    "vorhaben": String[],
  }

  export interface AsideMatchFiltersInterface {
    "Außenanlagen": MatchInterface,
    "Baumaßnahme": MatchInterface,
    "Bepflanzungen": MatchInterface,
    "Brandschutz": MatchInterface,
    "Dach": MatchInterface,
    "Denkmalart": MatchInterface,
    "Denkmalname": MatchInterface,
    "Diverse": MatchInterface,
    "Eingangsbereich": MatchInterface,
    "Farbe": MatchInterface,
    "Fassade": MatchInterface,
    "Fenster": MatchInterface,
    "Funk": MatchInterface,
    "Gebäude": MatchInterface,
    "Gebäudenutzung": MatchInterface,
    "Haustechnik": MatchInterface,
    "Kunst": MatchInterface,
    "Maßnahme": MatchInterface,
    "Nutzungsänderung": MatchInterface,
    "Sachbegriff": MatchInterface,
    "Solaranlage": MatchInterface,
    "Treppenhaus": MatchInterface,
    "Tür": MatchInterface,
    "Werbeanlage": MatchInterface,
    "district": MatchInterface,
    "doctype": MatchInterface,
    "ext": MatchInterface,
    "hidas": MatchInterface,
    "path": MatchInterface,
    "vorhaben": MatchInterface,
  }

  export interface MatchInterface {
    "$in": String[]
  }

  export interface AsideFiltersCounterInterface {
    "Außenanlagen": number,
    "Baumaßnahme": number,
    "Bepflanzungen": number,
    "Brandschutz": number,
    "Dach": number,
    "Denkmalart": number,
    "Denkmalname": number,
    "Diverse": number,
    "Eingangsbereich": number,
    "Farbe": number,
    "Fassade": number,
    "Fenster": number,
    "Funk": number,
    "Gebäude": number,
    "Gebäudenutzung": number,
    "Haustechnik": number,
    "Kunst": number,
    "Maßnahme": number,
    "Nutzungsänderung": number,
    "Sachbegriff": number,
    "Solaranlage": number,
    "Treppenhaus": number,
    "Tür": number,
    "Werbeanlage": number,
    "district": number,
    "doctype": number,
    "ext": number,
    "hidas": number,
    "path": number,
    "vorhaben": number,
  }