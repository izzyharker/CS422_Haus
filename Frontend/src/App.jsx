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

	// API call: this needs to login the correct user
    const handleSubmit = (event) => {
        event.preventDefault()

		const user = { user: username, pass: password};
		console.log("user: ")
		console.log(user)

		var userdata = new FormData()
		userdata.append('user', user['user'])
		userdata.append('pass', user['pass'])
		fetch("http://localhost:5000/login/login_user", {
			method: 'POST',
			mode: 'cors',
			body: userdata
		}).then(
			response => response.json()
		).then(
			data => console.log(data)
		)
		// Use the response json to decide what to do here
		setUser(user)

		localStorage.setItem('user', username)

		setLogin(true)
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
						<input type="submit" value="Login"/>
					</div>
				</form>
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
		<div className="haus">
			< NavBar />

			{(isLoggedIn) ? <div className="haus-content">
					<ChoreContainer user={user}/>
					<HouseContainer user={user}/>
				</div> : loginForm}
		</div>
	)
}

export default App