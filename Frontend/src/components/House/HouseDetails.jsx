import "./HouseContainer.css"
import {useState} from 'react';
import logo from "./user_icon.png"

function HouseDetails(props) {
    const [addChore, showAddChore] = useState(false)
    const [choreName, setChoreName] = useState("")
    const [choreDesc, setChoreDesc] = useState("")
    const [freq, setFreq] = useState(3)

    const handleSubmit = (e) => {
        // API post with form data 

        console.log("added chore")
        showAddChore(false)
    }

    // console.log(props.houseData)
    const addChoreForm = (
        <div className="add-chore">
			<div className="form">
				<h1>Add new chore</h1>
				<form onSubmit={handleSubmit}>
					<div className="input-container">
						<label>Chore name</label>
						<input 
							type="text" 
							name="name" 
							required
							onChange={({ target }) => setChoreName(target.value)}
						/>
					</div>
					<div className="input-container">
						<label>Chore description</label>
						<input 
							type="text" 
							name="desc" 
							optional
							onChange={({ target }) => setChoreDesc(target.value)}	
						/>
					</div>
                    <div className="input-container">
						<label>Chore frequency (days)</label>
						<input 
							type="number" 
							name="freq" 
                            placeholder="3 days"
							optional
							onChange={({ target }) => setFreq(target.value)}	
						/>
					</div>
					<div className="button-container">
						<input type="submit" value="Submit"/>
					</div>
				</form>
			</div>
        </div>
    );

    return (
        <div className="house-details">
            <h1>{props.houseName}</h1>

            {props.houseData &&
            (<div className="house-occupants">
                {props.houseData.map((user) => 
                    // <HouseOccupant key={user["UserID"]} username={user["name"]} />
                    <div key={user["UserID"]} className="occupant">
                        <img src={logo}/>
                        <div>{user["name"]}</div>
                    </div>)}
            </div>)}
            
            <div className="add-chore">
                <button onClick={() => showAddChore(true)}>Add chore</button>
            </div>

            {addChore && 
            (<div className="add-chore-form">
                {addChoreForm}
            </div>)}
            
        </div>
    )
}

export default HouseDetails