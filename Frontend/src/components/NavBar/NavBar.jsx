import "./NavBar.css"
import HelpButton from "./Help"
import Logout from "./Logout"
import Title from "./Title"

function NavBar(props) {
    return (
        <div className="navigation">
            <Title title={"HAUS"}/>
            
            {props.renderButtons &&
            (<div className="icon-buttons">
                    <HelpButton />
                    <Logout setLogin={props.setLogin}/>
            </div>)}
        </div>
    );
}


export default NavBar;