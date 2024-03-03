import './App.css'
import "./components/NavBar/NavBar"
import NavBar from './components/NavBar/NavBar'
import ChoreContainer from "./components/ChoreCards/ChoreContainer"

function App() {
	return (
		<div className="haus-content">
			< NavBar />
			<ChoreContainer />
		</div>
	)
}

export default App
