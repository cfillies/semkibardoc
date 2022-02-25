/* eslint-disable jsx-a11y/anchor-is-valid */
import React from 'react'
import {ListItem} from './ListItem'

type Props = {
  className: string,
  docs: {
    id: number,
    file: string,
    path: string,
    doctype: string,
    adresse: string,
    hidas: string,
    denkmalart: string,
    doc_image: string,
    vorhaben: string
  }[],
}

const ListsWidget7: React.FC<Props> = ({className, docs}) => {
  return (
        <ul>
          {docs.map((doc, index) => (
            <ListItem 
              key={index} 
              doc_props = {doc}
            />
          ))}
        </ul>
  )
}

export {ListsWidget7}
