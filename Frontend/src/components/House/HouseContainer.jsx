import "./HouseContainer.css"
import { useState, useEffect } from 'react';
import HouseDetails from "./HouseDetails"
import AddChore from "./AddChore"

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
            <HouseDetails houseName="House #1" houseData={data}/>
        </div>
    )
}

export default HouseContainer