// user profile button

function logout() {
    localStorage.clear()
    console.log("logging out")
    window.location.reload()
}

function Settings() {
    // API: delete user account
    return (
        <button className="user-profile" onClick={() => logout()}>
            Logout
        </button>
    )
}

export default Settings