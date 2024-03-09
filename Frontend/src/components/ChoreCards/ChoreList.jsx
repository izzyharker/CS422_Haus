import "./ChoreCards.css"
import { useState, useEffect } from "react";

function ChoreList(props) {
    const [chores, setChores] = useState();

    const completeChore = (id) => {
        // API call - update chore in backend

        setChores(chores.filter((ch) => ch["Chore ID"] != id))
    }

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
                <div key={chore["Chore ID"]} className="chore-card">
                    <h1>{chore["Chore Name"]}</h1>
                    <div className="chore-description">{chore["Description"]}</div>
                    <button onClick={() => completeChore(chore["Chore ID"])}>Complete</button>
                </div>)}
        </div>)}
    </div>
    )
}

export default ChoreList