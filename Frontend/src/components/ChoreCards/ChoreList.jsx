/*
Author: Izzy Harker
Date updated: 3/9/24
Description: Contains and exports the ChoreList function, which dynamically displays the chores assigned to the user. 
*/

import "./Chores.css"
import { useState, useEffect } from "react";

function ChoreList(props) {
    // state - contains the chore information
    const [chores, setChores] = useState();

    // button onclick function - effectively removes that particular chore card
    const completeChore = (id) => {
        // API call - update chore in backend
		var chore_info = new FormData()
        chore_info.append('chore_id', id)
        fetch("http://localhost:5000/chore/complete", {
			method: 'POST',
			mode: 'cors',
			body: chore_info
        })
        setChores(chores.filter((ch) => ch["Chore ID"] != id))

        setTimeout(() => window.location.reload(), 1000)
    }

    // fetch the user's chores from the backend
    useEffect(() => {
        // fetch and parse the chore data
		var chore_info = new FormData()
        chore_info.append('user', localStorage.getItem("user"))
        fetch("http://localhost:5000/chore/serve", {
			method: 'POST',
			mode: 'cors',
			body: chore_info
        })
        .then((res) => res.json())
        .then((chores) => {
            // console.log(data);
            // set data to the state variable
            setChores(chores);
        });
    }, []);

    // returns the header along with the chore "cards"
    // one card for each chore in the fetched list
    // each chore "card" contains a name, description, and "Complete" button
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
                    <div className="chore-deadline">Due {chore["Deadline Date"]}</div>
                    <button onClick={() => completeChore(chore["Chore ID"])}>Complete</button>
                </div>)}
        </div>)}
    </div>
    )
}

export default ChoreList