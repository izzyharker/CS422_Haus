import "./ChoreCards.css"
import ChoreList from "./ChoreList"
import { useState, useEffect } from 'react';

function ChoreContainer() {
    const [data, setData] = useState([]);

    useEffect(() => {
        fetch('/chores.json')
        .then((res) => res.json())
        .then((data) => {
            // console.log(data);
            setData(data);
        });
    }, []);

    return (
        <div className="chore-container">
            <ChoreList myChores={true} chores={data}/>
            {/* <ChoreL ist myChores={false} chores={null}/> */}
        </div>
    )
}

export default ChoreContainer