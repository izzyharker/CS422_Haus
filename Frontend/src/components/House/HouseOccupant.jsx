import "./HouseContainer.css"
import logo from "./user_icon.png"

function HouseOccupant(props) {
    let user = props.username;

    return (
        <div className="occupant">
            <img src={logo}/>
            <div>{user}</div>
        </div>
    )
}

export default HouseOccupant