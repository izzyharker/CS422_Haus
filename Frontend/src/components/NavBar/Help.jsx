// help button

function HelpButton() {
    return (
        <button className="user-profile" onClick={() => {fetch('/api/data')
            .then(response => response.text())
            .then(response => console.log(response))
            //.then(data => console.log(data));
            }}>
            Help
        </button>
    )
}

export default HelpButton