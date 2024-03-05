import "./HouseContainer.css"
import HouseOccupant from "./HouseOccupant"
import AddChore from "./AddChore"
import AddUser from "./AddUser"

function HouseDetails(props) {
    // console.log(props.houseData)

    return (
        <div className="house-details">
            <h1>{props.houseName}</h1>

            {props.houseData &&
            (<div className="house-occupants">
                {props.houseData.map((user) => 
                    <HouseOccupant key={user["UserID"]} username={user["name"]} />)}

            </div>)}
            <AddChore />
            <AddUser />
        </div>
    )
}

export default HouseDetails