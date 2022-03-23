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