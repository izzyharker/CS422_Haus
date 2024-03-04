import "./NavBar.css"
import HelpButton from "./Help"
import UserProfileButton from "./UserProfile"
import Title from "./Title"

function NavBar() {
    return (
        <div className="navigation">
            <Title title={"HAUS"}/>
            
            <div className="icon-buttons">
                    <HelpButton />
                    <UserProfileButton />
            </div>
        </div>
    );
}


export default NavBar;