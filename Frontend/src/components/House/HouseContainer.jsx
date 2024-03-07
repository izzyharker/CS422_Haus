import "./HouseContainer.css"
import { useState, useEffect } from 'react';
import HouseDetails from "./HouseDetails"

function HouseContainer(props) {
    const [data, setData] = useState([]);

    useEffect(() => {
        fetch('/users.json')
        .then((res) => res.json())
        .then((data) => {
            setData(data);
        });
    }, []);

    return (
        <div className="house">
            <HouseDetails houseName="Haus Members" houseData={data}/>
        </div>
    )
}

export default HouseContainer