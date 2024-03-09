// user profile button

function logout() {
    localStorage.clear()
    console.log("logging out")
    window.location.reload()
}

function Logout(props) {
    // API: delete user account
    return (
        <button className="user-profile" onClick={() => {
            localStorage.clear()
            props.setLogin()
        }}>
            Logout
        </button>
    )
}

export default Logout