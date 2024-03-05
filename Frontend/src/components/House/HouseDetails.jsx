import "./HouseContainer.css"
import HouseOccupant from "./HouseOccupant"

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
        </div>
    )
}

export default HouseDetails