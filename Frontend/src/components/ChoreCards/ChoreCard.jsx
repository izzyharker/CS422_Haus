// for individual chore cards

function ChoreCard(props) {
    let chore = props.whichChore
    return (
        <>
            <div className="chore-card">
                {chore}
            </div>
        </>
    )
}

export default ChoreCard