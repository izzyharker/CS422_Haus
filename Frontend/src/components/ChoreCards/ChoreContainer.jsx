import "./ChoreCards.css"
import ChoreList from "./ChoreList"

function ChoreContainer() {
    const chores = ["Sweep", "Unload dishwasher", "Vacuum"]

    return (
        <div className="chore-container">
            <ChoreList myChores={true} chores={chores}/>
            <ChoreList myChores={false} chores={["test1", "test2"]}/>
        </div>
    )
}

export default ChoreContainer