import "./NavBar.css"
import HelpButton from "./Help"
import Settings from "./UserProfile"
import Title from "./Title"

function NavBar() {
    return (
        <div className="navigation">
            <Title title={"HAUS"}/>
            
            <div className="icon-buttons">
                    <HelpButton />
                    <Settings />
            </div>
        </div>
    );
}


export default NavBar;