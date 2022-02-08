export interface FilterInterface {
    "Antrag": boolean,
    "Eigangsbestätigung": boolean,
    "Genehmigung": boolean,
    "Versagung": boolean,
    "Stellungnahme": boolean,
    "Anhorungrag": boolean,
    "from": number,
    "size": number
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
    "vorhaben": InnerAsideMenuInterface[],
    "objektnummer": InnerAsideMenuInterface[],
    "sachbegriff": InnerAsideMenuInterface[],
    "denkmalart": InnerAsideMenuInterface[],
    "count": {total: number},
  }

  export interface InnerAsideMenuInterface {
    _id: string,
    count: number
  }

  export interface AsideMenuItemFetchInterface {
    fieldName: string, 
    valueField: string
  }