/* eslint-disable jsx-a11y/anchor-is-valid */
import React, { useState } from 'react'
import {KTSVG, toAbsoluteUrl} from '../../../helpers'

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
          <h5 className="card-title align-items-start flex-column">
            <a href="#" className="pe-3">
              {doc_props.file}
            </a>
          </h5>
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
                                {doc_props.path}
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
