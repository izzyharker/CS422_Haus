/*
Author: Izzy Harker
Date updated: 3/9/24
Description: Contains and exports the ChoreContainer function, which creates the main div for the chore visualization. 
*/

import "./Chores.css"
import ChoreList from "./ChoreList"

function ChoreContainer() {
    // top-level container for showing the chores
    // returns flex div containing the ChoreList
    return (
        <div className="chore-container">
            <ChoreList/>
        </div>
    )
}

export default ChoreContainer