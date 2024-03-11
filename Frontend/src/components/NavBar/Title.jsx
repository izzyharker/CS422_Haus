/*
Author: Izzy Harker
Date updated: 3/9/24
Description: Contains and exports the Title function, which displays the given title of the app, taken as an argument. 
*/

function Title(props) {
    // return div with title
    return (
        <div className="app-title">{props.title}</div>
    )
}

export default Title