import "./HouseContainer.css"

function HouseOccupant(props) {
    let user = props.username;

    return (
        <div className="occupant">
            <div>{user}</div>
        </div>
    )
}

export default HouseOccupant