/*
Author: Izzy Harker
Date updated: 3/9/24
Description: Contains and exports the HouseContainer function, which creates the main div for the house information visualization. 
*/

import "./HouseContainer.css"
import { useState, useEffect } from 'react';
import HouseDetails from "./HouseDetails"

function HouseContainer(props) {
    // create state for the data
    const [data, setData] = useState([]);

    // fetch list of house users from backend
    useEffect(() => {
        fetch('/users.json')
        .then((res) => res.json())
        .then((data) => {
            setData(data);
        });
    }, []);

    // return a div containg the haus details
    // pass the user data and the title. 
    return (
        <div className="house">
            <HouseDetails houseName="Haus Information" houseData={data}/>
        </div>
    )
}

export default HouseContainer