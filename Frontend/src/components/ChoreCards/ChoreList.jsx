import "./ChoreCards.css"
import ChoreCard from "./ChoreCard"

function ChoreList(props) {
    let which_chores = "My"
    if (!props.myChores) {
        which_chores = "House"
    }
    return ( 
    <div className="chore-list">
        <div className={(props.myChores ? "chore-title my-chores" : "chore-title house-chores")}>
            <h1>{which_chores} chores</h1>
        </div>
        <div className={(props.myChores ? "chore-cards my-chores" : "chore-cards house-chores")}>
            {props.chores.map((chore) => 
                <ChoreCard key={chore} whichChore={chore} />)}
        </div>
    </div>
    )
}

export default ChoreList