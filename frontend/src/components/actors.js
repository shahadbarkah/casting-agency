import { useAuth0 } from '@auth0/auth0-react';
import { useApi } from './use-api';
import React, { useEffect, useState } from "react";

function Actors() {
     const { getAccessTokenSilently } = useAuth0();
    useEffect(() => {
       const token = getAccessTokenSilently();
        console.log("token",token);
         
        fetch('http://127.0.0.1:5000/actors', {
            method:'GET' ,
            headers : {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'Authorization': `Bearer ${token}`}})
            .then(response => response.json())
            .then(data => console.log(data));
    },[getAccessTokenSilently]);
    return(
        <>
        <h1> Actors page</h1>
        <h2> data</h2>
        </>
    );
}
 
export default Actors;