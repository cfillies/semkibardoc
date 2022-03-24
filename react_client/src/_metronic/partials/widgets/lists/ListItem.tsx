/* eslint-disable jsx-a11y/anchor-is-valid */
import React, { useState } from 'react'
import {KTSVG, toAbsoluteUrl} from '../../../helpers'

const SHAREPOINT: string = (process.env.REACT_APP_SHAREPOINT_URL as string)

type Props = {
  doc_props: {
    id: number
    file: string,
    path: string,
    doctype: string,
    adresse: string,
    hidas: string,
    denkmalart: string,
    doc_image: string,
    vorhaben: string
  }
}

const ListItem: React.FC<Props> = ({doc_props}) => {
  
  const muted = 'btn btn-sm btn-light btn-color-muted px-4 py-2'
  const lightDanger = 'btn btn-sm btn-light btn-light-danger px-4 py-2'

  const [buttonMerken, setButtonMerken] = useState(false)
  const [buttonColor, setButtonColor] = useState(muted)

  const toggleButtonHandler = () => {
    if (buttonMerken){
      setButtonMerken(false)
      setButtonColor(muted)
    }
    else {
      setButtonMerken(true)
      setButtonColor(lightDanger)
    }
  }

  return (
    
    <div className="row-xl-12 card" style={{marginTop:"10px", marginBottom:"30px"}}>
      <div className="row-xl-2 border-gray-300 border-bottom">
        <div className="card-body pt-3">
          <div className="d-flex flex-row h-50px">
            <div className="d-flex flex-column flex-row-auto w-50px">
                <div className="d-flex flex-column-auto h-50px">
                  {
                    (doc_props.file.endsWith(".pdf") && 
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 384 512">
                      
                      <path d="M365.3 93.38l-74.63-74.64C278.6 6.742 262.3 0 245.4 0H64C28.65 0 0 28.65 0 64l.0065 384c0 35.34 28.65 64 64 64H320c35.2 0 64-28.8 64-64V138.6C384 121.7 377.3 105.4 365.3 93.38zM336 448c0 8.836-7.164 16-16 16H64.02c-8.838 0-16-7.164-16-16L48 64.13c0-8.836 7.164-16 16-16h160L224 128c0 17.67 14.33 32 32 32h79.1V448zM202 286.1c.877-2.688 1.74-5.398 2.582-8.145c1.434-5.762 7.488-31.54 7.488-52.47C212.1 207 197.1 192 178.6 192C160.1 192 145.1 207 145.1 225.5c0 .2969 .1641 28.81 13.85 62.3c-7.035 19.36-15.57 38.8-25.41 57.93c-21.49 10.11-39.24 22.23-52.8 36.07c-6.234 6.438-9.367 14.74-9.367 24.72c0 18.45 15.01 33.46 33.46 33.46c10.8 0 20.98-5.227 27.22-13.98c7.322-10.28 18.38-26.9 30.47-48.95c15.8-6.352 33.88-11.72 53.88-16c13.55 9.578 28.9 17.29 45.71 22.95c4.527 1.551 9.402 2.348 14.43 2.348c20.26 0 36.13-16.19 36.13-36.86c0-20.33-16.54-36.87-36.87-36.87h-3.705c-2.727 .125-20.51 1.141-45.37 5.367C216.9 308.9 208.6 298.3 202 286.1zM110.2 410.4c-3.273 4.688-12.03 2.777-12.03-5.312c0-1.754 .6289-3.43 1.729-4.555c9.02-9.219 19.94-17.05 31.85-23.72C122.3 393.1 114.3 404.7 110.2 410.4zM178.6 218.8c3.693 0 6.703 3.008 6.703 6.703c0 15.21-4.109 34.84-5.746 42.1C172.1 245 171.9 227.2 171.9 225.5C171.9 221.8 174.9 218.8 178.6 218.8zM162.3 348.3c6.611-13.48 13.22-28.46 19.38-44.7c6.389 10.92 14.56 21.86 24.96 31.97C192.6 338.8 177.4 342.9 162.3 348.3zM272.4 339.5h3.352c5.539 0 10.05 4.5 10.05 10.79c0 5.129-4.176 9.32-9.32 9.32c-2.029 0-4.059-.3164-5.852-.9414c-12.33-4.137-23.11-9.32-32.54-15.19C258.3 340.3 272.1 339.5 272.4 339.5z"/>
                    </svg>)
                    ||
                    ((doc_props.file.endsWith(".doc") || doc_props.file.endsWith(".docx") || doc_props.file.endsWith(".DOC")) && 
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 384 512">
                      <path d="M365.3 93.38l-74.63-74.64C278.6 6.742 262.3 0 245.4 0H64C28.65 0 0 28.65 0 64l.0065 384c0 35.34 28.65 64 64 64H320c35.2 0 64-28.8 64-64V138.6C384 121.7 377.3 105.4 365.3 93.38zM336 448c0 8.836-7.164 16-16 16H64.02c-8.838 0-16-7.164-16-16L48 64.13c0-8.836 7.164-16 16-16h160L224 128c0 17.67 14.33 32 32 32h79.1V448zM214.6 248C211.3 238.4 202.2 232 192 232s-19.25 6.406-22.62 16L144.7 318.1l-25.89-77.66C114.6 227.8 101 221.2 88.41 225.2C75.83 229.4 69.05 243 73.23 255.6l48 144C124.5 409.3 133.5 415.9 143.8 416c10.17 0 19.45-6.406 22.83-16L192 328.1L217.4 400C220.8 409.6 229.8 416 240 416c10.27-.0938 19.53-6.688 22.77-16.41l48-144c4.188-12.59-2.594-26.16-15.17-30.38c-12.61-4.125-26.2 2.594-30.36 15.19l-25.89 77.66L214.6 248z"/>
                    </svg>
                    )
                    ||
                    (doc_props.file.endsWith(".msg")  && 
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">
                      <path d="M448 64H64C28.65 64 0 92.65 0 128v256c0 35.35 28.65 64 64 64h384c35.35 0 64-28.65 64-64V128C512 92.65 483.3 64 448 64zM64 112h384c8.822 0 16 7.178 16 16v22.16l-166.8 138.1c-23.19 19.28-59.34 19.27-82.47 .0156L48 150.2V128C48 119.2 55.18 112 64 112zM448 400H64c-8.822 0-16-7.178-16-16V212.7l136.1 113.4C204.3 342.8 229.8 352 256 352s51.75-9.188 71.97-25.98L464 212.7V384C464 392.8 456.8 400 448 400z"/>
                    </svg>
                    )
                    ||
                    ((doc_props.file.endsWith(".jpg") || doc_props.file.endsWith(".png")) && 
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 384 512">
                      <path d="M365.3 93.38l-74.63-74.64C278.6 6.742 262.3 0 245.4 0H64C28.65 0 0 28.65 0 64l.0065 384c0 35.34 28.65 64 64 64H320c35.2 0 64-28.8 64-64V138.6C384 121.7 377.3 105.4 365.3 93.38zM336 448c0 8.836-7.164 16-16 16H64.02c-8.838 0-16-7.164-16-16L48 64.13c0-8.836 7.164-16 16-16h160L224 128c0 17.67 14.33 32 32 32h79.1V448zM215.3 292c-4.68 0-9.051 2.34-11.65 6.234L164 357.8l-11.68-17.53C149.7 336.3 145.3 334 140.7 334c-4.682 0-9.053 2.34-11.65 6.234l-46.67 70c-2.865 4.297-3.131 9.82-.6953 14.37C84.09 429.2 88.84 432 93.1 432h196c5.163 0 9.907-2.844 12.34-7.395c2.436-4.551 2.17-10.07-.6953-14.37l-74.67-112C224.4 294.3 220 292 215.3 292zM128 288c17.67 0 32-14.33 32-32S145.7 224 128 224S96 238.3 96 256S110.3 288 128 288z"/>
                    </svg>
                    )
                    ||
                    ((doc_props.file.endsWith(".zip") || doc_props.file.endsWith(".rar")) && 
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 384 512">
                      <path d="M365.3 93.38l-74.63-74.64C278.6 6.742 262.3 0 245.4 0L64-.0001c-35.35 0-64 28.65-64 64l.0065 384c0 35.34 28.65 64 64 64H320c35.2 0 64-28.8 64-64V138.6C384 121.7 377.3 105.4 365.3 93.38zM336 448c0 8.836-7.164 16-16 16H64.02c-8.838 0-16-7.164-16-16L48 64.13c0-8.836 7.164-16 16-16h48V64h64V48.13h48.01L224 128c0 17.67 14.33 32 32 32h79.1V448zM176 96h-64v32h64V96zM176 160h-64v32h64V160zM176 224h-64l-30.56 116.5C73.51 379.5 103.7 416 144.3 416c40.26 0 70.45-36.3 62.68-75.15L176 224zM160 368H128c-8.836 0-16-7.164-16-16s7.164-16 16-16h32c8.836 0 16 7.164 16 16S168.8 368 160 368z"/>
                    </svg>
                    )
                  }
                </div>
                
              </div>
              <div className="d-flex flex-column-auto h-50px">
                  <h5 className="card-title align-items-start flex-column" style={{paddingTop:"20px", marginLeft:"20px"}}>
                    <a href={
                      `${SHAREPOINT}Treptow/${doc_props.path.split("\\")[doc_props.path.split("\\").length - 1]}/${doc_props.file}`
                      //          SHAREPOINT?.concat("Treptow/")
                      //         .concat(doc_props.path.split("\\")[doc_props.path.split("\\").length - 1])
                      //         .concat("/")
                      //         .concat(doc_props.file)
                            } 
                              target="_blank" className="pe-3">
                      {doc_props.file}
                      
                    </a>
                  </h5>
                </div>
            </div>
          
          {/* <h5 className="card-title align-items-start flex-column">
            <a href="#" className="pe-3">
              {doc_props.file}
            </a>
          </h5> */}
        </div>
      </div>
      
      <div className="row g-5 g-xl-8">
        <div className="col-xl-5">
          <div className="card card-xl-stretch mb-xl-8">
            <div className="card-body pt-3">
              <div className="d-flex align-items-sm-center mb-7">
                <div className="col-xl-4">
                  <div className="symbol symbol-60px symbol-2by3 me-4">
                      <div
                        className='symbol-label'
                        style={{backgroundImage: `url(${toAbsoluteUrl('/media/stock/600x400/img-20.jpg')})`}}
                      >
                      </div>
                    </div>       
                </div>
                <div className="col-xl-8">
                  <div className="d-flex flex-row-fluid flex-wrap align-items-center">
                    <div className="flex-grow-1 me-2">
                      <div className="row g-5 g-xl-8">
                        <div className="col-xl-6">
                          <span className='text-muted fw-bold d-block pt-1'>Ordner</span>
                        </div>
                        <div className="col-xl-6">
                         <span className='text-muted fw-bold d-block pt-1'> 
                            <a href='#' className='text-gray-800 fw-bolder text-hover-primary'>
                                {doc_props.path.split("\\")[doc_props.path.split("\\").length - 1]}
                            </a>
                          </span>
                        </div>
                      </div>
                      <div className="row g-5 g-xl-8">
                        <div className="col-xl-6">
                          <span className='text-muted fw-bold d-block pt-1'>DocumentTyp</span>
                        </div>
                        <div className="col-xl-6">
                          <span className='text-muted fw-bold d-block pt-1'>{doc_props.doctype}</span>
                        </div>
                      </div>
                      <div className="row g-5 g-xl-8">
                        <div className="col-xl-6">
                          <span className='text-muted fw-bold d-block pt-1'>Addresse</span>
                        </div>
                        <div className="col-xl-6">
                          <span className='text-muted fw-bold d-block pt-1'>{doc_props.adresse}</span>
                        </div>
                      </div>
                      <div className="row g-5 g-xl-8">
                        <div className="col-xl-6">
                          <span className='text-muted fw-bold d-block pt-1'>Objectnr</span>
                        </div>
                        <div className="col-xl-6">
                          <span className='text-muted fw-bold d-block pt-1'>{doc_props.hidas}</span>
                        </div>
                      </div>
                      <div className="row g-5 g-xl-8">
                        <div className="col-xl-6">
                          <span className='text-muted fw-bold d-block pt-1'>Denkmalart</span>
                        </div>
                        <div className="col-xl-6">
                          <span className='text-muted fw-bold d-block pt-1'>{doc_props.denkmalart}</span>
                        </div>
                      </div>
                      <div className="row g-5 g-xl-8">
                        <div className="col-xl-6">
                          <span className='text-muted fw-bold d-block pt-1'>Vorhaben</span>
                        </div>
                        <div className="col-xl-6">
                          <span className='text-muted fw-bold d-block pt-1'>{doc_props.vorhaben}</span>
                        </div>
                      </div>
                    </div>
                  </div>
                  
                </div>
              </div>
            </div>
          </div>
        </div>

        <div className="col-xl-7">
          <div className="card card-xl-stretch mb-xl-8">
            <div className="card-body pt-3">
              <div className="row-xl-2">
                <div className="d-flex flex-row-fluid flex-wrap align-items-center">
                  <a href="#" className="btn btn-bg-light btn-active-icon-dark btn-active-light-primary">
                    Zusammenfassung: 
                    <span className="svg-icon svg-icon-1" style={{marginLeft:"10px"}}> 
                      <svg aria-hidden="true" focusable="false" data-prefix="fas" data-icon="volume-up" className="svg-inline--fa fa-volume-up fa-w-18" role="img" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 576 512">
                        <path fill="currentColor" d="M215.03 71.05L126.06 160H24c-13.26 0-24 10.74-24 24v144c0 13.25 10.74 24 24 24h102.06l88.97 88.95c15.03 15.03 40.97 4.47 40.97-16.97V88.02c0-21.46-25.96-31.98-40.97-16.97zm233.32-51.08c-11.17-7.33-26.18-4.24-33.51 6.95-7.34 11.17-4.22 26.18 6.95 33.51 66.27 43.49 105.82 116.6 105.82 195.58 0 78.98-39.55 152.09-105.82 195.58-11.17 7.32-14.29 22.34-6.95 33.5 7.04 10.71 21.93 14.56 33.51 6.95C528.27 439.58 576 351.33 576 256S528.27 72.43 448.35 19.97zM480 256c0-63.53-32.06-121.94-85.77-156.24-11.19-7.14-26.03-3.82-33.12 7.46s-3.78 26.21 7.41 33.36C408.27 165.97 432 209.11 432 256s-23.73 90.03-63.48 115.42c-11.19 7.14-14.5 22.07-7.41 33.36 6.51 10.36 21.12 15.14 33.12 7.46C447.94 377.94 480 319.54 480 256zm-141.77-76.87c-11.58-6.33-26.19-2.16-32.61 9.45-6.39 11.61-2.16 26.2 9.45 32.61C327.98 228.28 336 241.63 336 256c0 14.38-8.02 27.72-20.92 34.81-11.61 6.41-15.84 21-9.45 32.61 6.43 11.66 21.05 15.8 32.61 9.45 28.23-15.55 45.77-45 45.77-76.88s-17.54-61.32-45.78-76.86z">
                        </path>
                      </svg>
                    </span>
                  </a>
                </div>
              </div>
              <div className="row-xl-8">
                <div className="d-flex flex-row-fluid flex-wrap align-items-center">
                  <p className="text-gray-800 fw-normal mb-5">
                    Teller pa wandte am dieses wu durren. Sind ihn sage zum mirs was den. Augen se ernst am steil in litze immer zu sitzt. Wovon mir gluck zwirn vor nah bibel ruhig ers wuste. Stadtchen ertastete gestrigen eia wei. Gelernt gewohnt mir hof schritt erstieg ein. Litze las mir abend dabei alles hosen. Wasser zu seiest en sa fellen solche ruhten se. Du es wachter zu spuckte glatten 
                  </p>
                </div>
              </div>
              <div className="row-xl-2">
                <div className="d-flex flex-row-fluid flex-wrap align-items-center">
                  <a
                    href='#'
                    className={buttonColor}
                    // id={'merken_'.concat(doc_props.id.toString())}
                    ref={React.createRef()}
                    onClick={() => toggleButtonHandler()}
                  >
                    <KTSVG path='/media/icons/duotune/general/gen030.svg' className='svg-icon-2' />
                    Merken
                  </a>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

  )
}

export {ListItem}
