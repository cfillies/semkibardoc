import React from 'react'
import {MenuItem} from './MenuItem'
import {MenuInnerWithSub} from './MenuInnerWithSub'
import {MegaMenu} from './MegaMenu'
import {useIntl} from 'react-intl'

export function MenuInner() {
  const intl = useIntl()
  return (
    <>
      
      <ol className="breadcrumb breadcrumb-dot text-muted fs-6 fw-bold">
        <li className="breadcrumb-item pe-3">
          <a href="#" className="pe-3">
            Kartenansicht
          </a>
        </li>
        <li className="breadcrumb-item pe-3">
          <a href="#" className="pe-3">
            Tabellensicht
          </a>
        </li>
        <li className="breadcrumb-item pe-3">
          <a href="#" className="pe-3">
          Denkmalliste
          </a>
        </li>
        <li className="breadcrumb-item pe-3">
          <a href="#" className="pe-3">
          Sachbegriffe
          </a>
        </li>
        <li className="breadcrumb-item pe-3">
          <a href="#" className="pe-3">
          Hilfe
          </a>
        </li>
      </ol>
    </>
  )
}
