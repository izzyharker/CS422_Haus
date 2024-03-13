/*
Author: Izzy Harker
Date updated: 3/9/24
Description: Contains and exports the App function, which acts as the top-level controller for the entire website. 
*/

import './App.css'
import "./components/NavBar/NavBar"
import NavBar from './components/NavBar/NavBar'
import ChoreContainer from "./components/ChoreCards/ChoreContainer"
import HouseContainer from "./components/House/HouseContainer"
import { useEffect, useState } from 'react'

function App() {
	// create state information
	const [username, setUsername] = useState("");
	const [password, setPassword] = useState("");
	const [user, setUser] = useState()
	const [isLoggedIn, setLogin] = useState(false)
	const [errorMessages, setErrorMessages] = useState({})
	const [create, setCreate] = useState(false)
	  
	// error messages for login clarity
	const errors = {
		uname: "x Invalid username",
		pass: "x Invalid password",
		c_uname: "x Existing username"
	};

	// API call: this needs to login the correct user
    const submitLogin = (event) => {
        event.preventDefault()

		var login_data = new FormData()
        login_data.append('user', username)
        login_data.append('pass', password)
        fetch("http://localhost:5000/user/login", {
			method: 'POST',
			mode: 'cors',
			body: login_data
        }).then(
            response => response.json()
        ).then(
            data => {
                if (data.user_exists) {
					if (data.pass_valid) {
						// Successful login
						setLogin(true)
						localStorage.setItem("user", username)
					}
					else {
						// Invalid password
						setErrorMessages({ name: "pass", message: errors.pass });
					}
                }
                else {
					// Username not found
					setErrorMessages({ name: "uname", message: errors.uname });
                }
            }
        )
    }

	// display the correct error messages
	const renderErrorMessage = (name) =>
		name === errorMessages.name && (
		<div className="error">{errorMessages.message}</div>
    );

	// create a new user account for the haus (also logs in upon submission)
	const createAccount = (event) => {
        event.preventDefault()
		var login_data = new FormData()
		login_data.append('user', username)
		login_data.append('pass', password)
		fetch("http://localhost:5000/user/create", {
			method: 'POST',
			mode: 'cors',
			body: login_data
        }).then(
			response => response.json()
		).then(
			data => {
				if (data.success) {
					// login with new acct
					setLogin(true)
					localStorage.setItem("user", username)
				}
				else {
					setErrorMessages({name : "c_uname", message: errors.c_uname})
				}
			}
		)
		// API post to create new account
	}

	// contains the login form information, username and password, as well as an option to create an account
    const loginForm = (
        <div className="login">
			<div className="form">
				<h1>Enter HAUS</h1>
				<form onSubmit={submitLogin}>
					<div className="input-container">
						<label>Username </label>
						<input 
							type="text" 
							name="uname" 
							required
							onChange={({ target }) => setUsername(target.value)}
						/>
						{renderErrorMessage("uname")}
					</div>
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
						<input type="submit" value="Login"/>
					</div>
				</form>
				<button className="new-acct" onClick={() => setCreate(true)}>Create account</button>
			</div>
        </div>
    );

	// prompts for username/password to create an account. Also has an option to cancel and go back to login screen.
	const createAcctForm = (
        <div className="login">
			<div className="form">
				<h1>Join HAUS</h1>
				<form onSubmit={createAccount}>
					<div className="input-container">
						<label>Username </label>
						<input 
							type="text" 
							name="uname" 
							required
							onChange={({ target }) => setUsername(target.value)}
						/>
						{renderErrorMessage("c_uname")}
					</div>
					<div className="input-container">
						<label>Password </label>
						<input 
							type="password" 
							name="pass" 
							required
							onChange={({ target }) => setPassword(target.value)}	
						/>
					</div>
					<div className="button-container">
						<input type="submit" value="Create Account"/>
					</div>
				</form>
				<button className="new-acct" onClick={() => setCreate(false)}>Cancel</button>
			</div>
        </div>
    );

	// checks whether there is a logged-in user on reload or page opening
	useEffect(() => {
		setCreate(false);
		const loggedInUser = localStorage.getItem("user");
		if (loggedInUser) {
			setUser(loggedInUser);
			setLogin(true)
		}
		else setLogin(false);
	}, []);

	// returns page information
	return (
		<>
		<div className="haus">
			<NavBar renderButtons={isLoggedIn} user={username} setLogin={setLogin} />

		{(isLoggedIn) ? <>
				<div className="haus-content">
					<ChoreContainer user={user}/>
					<HouseContainer user={user} setLogin={setLogin}/>
				</div> 
			</>: (create) ? createAcctForm : loginForm}
		</div>

		<div className="credits">Created for CS 422, Winter 2024 by Izzy Harker, Andrew Rehmann, Alex Peterson Santos, Connie Williamson, Carter Young</div>
		</>
	)
}

export default App