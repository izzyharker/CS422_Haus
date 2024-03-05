import "./HouseContainer.css"

function AddChore() {
    return (
        <>
            <div className="add-chore">
                <button onClick={() => console.log("Added chore")}>Add chore</button>
            </div>
        </>
    )
}

export default AddChore