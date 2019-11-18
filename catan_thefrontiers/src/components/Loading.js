import React from 'react'
import ReactLoading from 'react-loading'

export default function Loading({color, size}) {
    return <ReactLoading type={'bars'} color={color} height={size} width={size}/>
}