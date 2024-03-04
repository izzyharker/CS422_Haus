import './App.css'
import "./components/NavBar/NavBar"
import NavBar from './components/NavBar/NavBar'
import ChoreContainer from "./components/ChoreCards/ChoreContainer"
import HouseContainer from "./components/House/HouseContainer"

function App() {
	return (
		<div className="haus">
			< NavBar />

			<div className="haus-content">
				<ChoreContainer />
				<HouseContainer />
			</div>
		</div>
	)
}

export default App
