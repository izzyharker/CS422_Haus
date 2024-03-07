import './App.css'
import "./components/NavBar/NavBar"
import NavBar from './components/NavBar/NavBar'
import ChoreContainer from "./components/ChoreCards/ChoreContainer"
import HouseContainer from "./components/House/HouseContainer"
import { useState } from 'react'

function App() {
	const [isSubmitted, setIsSubmitted] = useState(false);
	const [userName, setUserName] = useState({})

	// API call: this needs to login the correct user
    const handleSubmit = (event) => {
        event.preventDefault()

        setIsSubmitted(true)
		setUserName("default")
    }

    const loginForm = (
        <div className="login">
			<div className="form">
				<h1>Enter HAUS</h1>
				<form onSubmit={handleSubmit}>
					<div className="input-container">
						<label>Username </label>
						<input type="text" name="uname" required />
					</div>
					<div className="input-container">
						<label>Password </label>
						<input type="password" name="pass" required />
					</div>
					<div className="button-container">
						<input type="submit" value="Login"/>
					</div>
				</form>
			</div>
        </div>
     );

	return (
		<div className="haus">
			< NavBar />

			{isSubmitted ? <div className="haus-content">
					<ChoreContainer user={userName}/>
					<HouseContainer user={userName}/>
				</div> : loginForm}
		</div>
	)
}

export default App
