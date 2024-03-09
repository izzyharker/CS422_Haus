import "./ChoreCards.css"
import ChoreCard from "./ChoreCard"
import { useState, useEffect } from "react";

function ChoreList(props) {
    const [chores, setChores] = useState();

    useEffect(() => {
        fetch('/chores.json')
        .then((res) => res.json())
        .then((chores) => {
            // console.log(data);
            setChores(chores);
        });
    }, []);

    return ( 
    <div className="chore-list">
        <div className={("chore-title my-chores")}>
            <h1>My chores</h1>
        </div>
        {chores &&
        (<div className={"chore-cards my-chores"}>
            {chores.map((chore) => 
                <ChoreCard key={chore["Chore ID"]} chore={chore} />)}
            {/* <AddChore /> */}
        </div>)}
    </div>
    )
}

export default ChoreList