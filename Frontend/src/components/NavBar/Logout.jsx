/*
Author: Izzy Harker
Date updated: 3/9/24
Description: Contains and exports the Logout function, which creates a button to logout the user. 
*/


function Logout(props) {
    // API: reset user account
    return (
        <button className="user-profile" onClick={() => {
            // clear browser cache
            localStorage.clear()

            // set logged in to false
            props.setLogin(false)
        }}>
            Logout
        </button>
    )
}

export default Logout