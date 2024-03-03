// for the chore/house tabs

function WebsiteTab(props) {
    return (
        <button key={props.tab} className="tab-button" onClick={() => console.log("Pressed tab button")}>
            {props.tab}
        </button>
    )
}

function WebsiteTabs(props) {
    return (
        <div className="user-tabs">
            {props.tabs.map((tab) => (
                <WebsiteTab key={tab} tab={tab} />))}
        </div>
    )
}

export default WebsiteTabs