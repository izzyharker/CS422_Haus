/*
Author: Izzy Harker
Date updated: 3/9/24
Description: Contains and exports the HouseDetails function, which displays the users and allows one to add a new chore or delete their account.
*/

import "./HouseContainer.css"
import {useState} from 'react';
import logo from "./user_icon.png"

function HouseDetails(props) {
    // create state elements
    const [addChore, showAddChore] = useState(false)
    const [choreName, setChoreName] = useState("")
    const [choreDesc, setChoreDesc] = useState("")
    const [choreLen, setChoreLen] = useState(15)
    const [freq, setFreq] = useState(3)
	const [delPass, setDelPass] = useState(false)
    const [errorMessages, setErrorMessages] = useState({})
    const [password, setPassword] = useState()

    // error message for incorrect password
    const errors = {
		pass: "x Invalid password"
	};

    // handles the submission for the add chore form
    const submitAddChore = (e) => {
        // API post with form data 
        e.preventDefault()
        
		var chore_data = new FormData()
		chore_data.append('Chore Name', choreName)
		chore_data.append('Description', choreDesc)
        chore_data.append('Frequency', freq)
        chore_data.append('Expected Duration', choreLen)

		fetch("http://localhost:5000/chore/create", {
			method: 'POST',
			mode: 'cors',
			body: chore_data
		})
        console.log("added chore")

        // stop displaying form
        showAddChore(false)

        setTimeout(() => window.location.reload(), 1000)
    }

    // display the correct error message, returns a div containing the error
    const renderErrorMessage = (name) =>
        // check that the given name is the current message and return the div
		name === errorMessages.name && (
		<div className="error">{errorMessages.message}</div>
    );

    // handles the submission for the delete account form
    const deleteAccount = (e) => {
        // stop displaying form
		// setDelPass(false)

        e.preventDefault()

        var delete_data = new FormData()
        delete_data.append('user', localStorage.getItem("user"))
        delete_data.append('pass', password)
        console.log(localStorage.getItem("user"), password)
        fetch("http://localhost:5000/user/delete", {
			method: 'POST',
			mode: 'cors',
			body: delete_data
        }).then(
            response => response.json()
        ).then(
            data => {
                console.log(data)
                if (data.success == true) {
                    // stop displaying form
                    setDelPass(false)

                    // remove from browser storage
                    localStorage.removeItem("user");
                    // logout
                    props.setLogin(false)
                }
                else {
                    // set the error message on incorrect password and do nothing
                    // setDelPass(true)
                    setErrorMessages({ name: "pass", message: errors.pass });
                }
            }
        )
	}

    // form to add a chore to the haus
    // contains name, description, and frequency fields
    // submit button and close form button are also set. 
    const addChoreForm = (
        <div className="popup-form">
            <div className="add-chore user-form">
                <div className="form">
                    <h1>Add new chore</h1>
                    <form onSubmit={submitAddChore}>
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

                        <div className="input-container">
                            <label>Chore length (minutes)</label>
                            <input 
                                type="number" 
                                name="len" 
                                placeholder="15 minutes"
                                optional
                                onChange={({ target }) => setChoreLen(target.value)}	
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

    // form to delete account
    // contains password field and submit button
    // also has button to exit, as well as a warning about the action. 
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

    // function returns users and buttons for adding a chore and deleting an account
    // the add chore and delete account forms are shown conditionally
    return (
        <div className="house-details">
            {delPass && 
                <div className="del-pass">
                    {delAcctForm}
                </div>}

            {addChore && 
            (<div className="add-chore-form">
                {addChoreForm}
            </div>)}

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

            <div className="add-chore">
					<button onClick={() => setDelPass(true)}>Delete Account</button>
			</div>
        </div>
    )
}

export default HouseDetails