import "./HouseContainer.css"

function AddChore() {
    // API call - button onclick function
    return (
        <>
            <div className="add-chore">
                <button onClick={() => console.log("Added chore")}>Add chore</button>
            </div>
        </>
    )
}

export default AddChore