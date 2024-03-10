import './App.css'
import "./components/NavBar/NavBar"
import NavBar from './components/NavBar/NavBar'
import ChoreContainer from "./components/ChoreCards/ChoreContainer"
import HouseContainer from "./components/House/HouseContainer"
import { useEffect, useState } from 'react'

function App() {
	const [username, setUsername] = useState("");
	const [password, setPassword] = useState("");
	const [user, setUser] = useState()
	const [isLoggedIn, setLogin] = useState(false)
	const [errorMessages, setErrorMessages] = useState({})
	const [create, setCreate] = useState(false)

	// const database = [
	// 	{
	// 		username: "user1",
	// 		password: "pass1"
	// 	},
	// 	{
	// 		username: "user2",
	// 		password: "pass2"
	// 	}
	// ];
	  
	const errors = {
		uname: "x Invalid username",
		pass: "x Invalid password"
	};

	// API call: this needs to login the correct user
    const handleSubmit = (event) => {
        event.preventDefault()

		// this will be the fetch method
		// const userData = database.find((user) => user.username === username);

		// if (userData) {
		// 	if (userData.password !== password) {
		// 		// Invalid password
		// 		setErrorMessages({ name: "pass", message: errors.pass });
		// 	} 
		// 	else {
		// 		setLogin(true);
		// 	}
		// 	} 
		// else {
		// 	// Username not found
		// 	setErrorMessages({ name: "uname", message: errors.uname });
		// }

		setLogin(true)
		localStorage.setItem("user", "default")
    }

	const renderErrorMessage = (name) =>
		name === errorMessages.name && (
		<div className="error">{errorMessages.message}</div>
    );

	const createAccount = (event) => {
		// API post to create new account
		setLogin(true)

		// login with new acct
		localStorage.setItem("user", username)
	}

    const loginForm = (
        <div className="login">
			<div className="form">
				<h1>Enter HAUS</h1>
				<form onSubmit={handleSubmit}>
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
						{/* {renderErrorMessage("uname")} */}
					</div>
					<div className="input-container">
						<label>Password </label>
						<input 
							type="password" 
							name="pass" 
							required
							onChange={({ target }) => setPassword(target.value)}	
						/>
						{/* {renderErrorMessage("pass")} */}
					</div>
					<div className="button-container">
						<input type="submit" value="Create Account"/>
					</div>
				</form>
				<button className="new-acct" onClick={() => setCreate(false)}>Cancel</button>
			</div>
        </div>
    );

	useEffect(() => {
		const loggedInUser = localStorage.getItem("user");
		if (loggedInUser) {
			setUser(loggedInUser);
			setLogin(true)
		}
		else setLogin(false);
	}, []);

	return (
		<>
		<div className="haus">
			<NavBar renderButtons={isLoggedIn} setLogin={setLogin} />

		{(isLoggedIn) ? <>
				<div className="haus-content">
					<ChoreContainer user={user}/>
					<HouseContainer user={user}/>
				</div> 
			</>: (create) ? createAcctForm : loginForm}
		</div>
		</>
	)
}

export default App