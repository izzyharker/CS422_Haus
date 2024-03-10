import "./HouseContainer.css"
import {useState} from 'react';
import logo from "./user_icon.png"

function HouseDetails(props) {
    const [addChore, showAddChore] = useState(false)
    const [choreName, setChoreName] = useState("")
    const [choreDesc, setChoreDesc] = useState("")
    const [freq, setFreq] = useState(3)
	const [delPass, setDelPass] = useState(false)
    const [errorMessages, setErrorMessages] = useState({})


    const handleSubmit = (e) => {
        // API post with form data 

        console.log("added chore")
        showAddChore(false)
    }

    const renderErrorMessage = (name) =>
		name === errorMessages.name && (
		<div className="error">{errorMessages.message}</div>
    );

    const deleteAccount = (pass) => {
		setDelPass(false)

		if (true) {
			// remove from backend (API)

			// remove from browser storage
			localStorage.removeItem("user")
			setLogin(false)
		}
		else {
			setErrorMessages({ name: "pass", message: errors.pass });
		}
	}

    // console.log(props.houseData)
    const addChoreForm = (
        <div className="popup-form">
            <div className="add-chore user-form">
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
                <div className="exit-form">
                    <button onClick={() => showAddChore(false)}>X</button>
                </div>
            </div>
        </div>
    );

    const delAcctForm = (
        <div className="popup-form">
            <div className="add-chore user-form">
                <div className="form">
                    <h1>Enter password to delete account</h1>
                    <div className="del-warning">Warning: this action is irreversible!</div>
                    <form onSubmit={deleteAccount}>
                        <div className="input-container">
                            <label>Password </label>
                            <input 
                                type="password" 
                                name="pass" 
                                required
                                onChange={({ target }) => setPassword(target.value)}	
                            />
                            {renderErrorMessage("pass")}
                        </div>
                        <div className="button-container">
                            <input type="submit" value="Delete Account"/>
                        </div>
                    </form>
                </div>
                <div className="exit-form">
                    <button onClick={() => setDelPass(false)}>X</button>
                </div>
            </div>
        </div>
    );

    return (
        <div className="house-details">
            {delPass && 
                <div className="del-pass">
                    {delAcctForm}
                </div>}
                
            <h1>{props.houseName}</h1>

            <div className="add-chore">
                <button onClick={() => showAddChore(true)}>Add chore</button>
            </div>

            {addChore && 
            (<div className="add-chore-form">
                {addChoreForm}
            </div>)}

            {props.houseData &&
            (<div className="house-occupants">
                {props.houseData.map((user) => 
                    // <HouseOccupant key={user["UserID"]} username={user["name"]} />
                    <div key={user["UserID"]} className="occupant">
                        <img src={logo}/>
                        <div>{user["name"]}</div>
                    </div>)}
            </div>)}

            <div className="delete-acct">
					<button onClick={() => setDelPass(true)}>Delete Account</button>
			</div>
        </div>
    )
}

export default HouseDetails