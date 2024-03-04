// for individual chore cards

function ChoreCard(props) {
    let chore = props.chore
    return (
        <>
            <div className="chore-card">
                <h1>{chore["Chore Name"]}</h1>
                <div className="chore-description">{chore["Description"]}</div>
                <button onClick={() => console.log("Completed chore")}>Complete</button>
            </div>
        </>
    )
}

export default ChoreCard