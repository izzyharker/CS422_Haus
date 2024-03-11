/*
Author: Izzy Harker
Date updated: 3/9/24
Description: Contains and exports the HelpButton function, which creates a button to link to the github page for this project. 
*/

function HelpButton() {
    // return a link to the github page
    return (
        <a className="help" target="_blank" href="https://github.com/izzyharker/CS422_Haus">
            Help
        </a>
    )
}

export default HelpButton