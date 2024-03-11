/*
Author: Izzy Harker
Date updated: 3/9/24
Description: Contains and exports the NavBar function, which creates the main div for the navigation bar at the top of the screen, including the title and help/logout buttons.  
*/

import "./NavBar.css"
import HelpButton from "./Help"
import Logout from "./Logout"
import Title from "./Title"

function NavBar(props) {
    // return navbar div
    return (
        <div className="navigation">
            <Title title={"HAUS"}/>
            
            <div className="icon-buttons">
                    <HelpButton />
                    {props.renderButtons &&
                    (<Logout setLogin={props.setLogin}/>)}
            </div>
        </div>
    );
}


export default NavBar;