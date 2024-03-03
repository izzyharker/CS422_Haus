import "./NavBar.css"
import HelpButton from "./Help"
import UserProfileButton from "./UserProfile"
import WebsiteTabs from "./WebsiteTabs"

function NavBar() {
    return (
        <>
            <div className="dummynav"></div>
            <div className="navigation">
                <h1>HAUS</h1>
                <WebsiteTabs tabs={["House", "Chores"]} />
            </div>
            
            <div className="icon-buttons">
                    <HelpButton />
                    <UserProfileButton />
            </div>
        </>
    );
}


export default NavBar;