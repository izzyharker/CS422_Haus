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

	// API call: this needs to login the correct user
    const handleSubmit = (event) => {
        event.preventDefault()

		e.preventDefault();

		const user = { user: username, pass: password};
		setUser(user)

		localStorage.setItem('user', username)

		console.log(user)
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
		console.log(loggedInUser)
		if (loggedInUser) {
			setUser(loggedInUser);
		}
	}, []);

	return (
		<div className="haus">
			< NavBar />

			{(user) ? <div className="haus-content">
					<ChoreContainer user={user}/>
					<HouseContainer user={user}/>
				</div> : loginForm}
		</div>
	)
}

export default App
