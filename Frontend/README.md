# Instructions for setting up and running frontend 

1. Install nvm, use instructions from https://github.com/nvm-sh/nvm?tab=readme-ov-file#installing-and-updating
2. Install node and npm (installing node should automatically install npm I think)
3. cd to the Frontend directory
4. To start the local server with React, run:
```
npm install
npm run dev
```
You should get this series of lines:
  VITE v5.1.x  ready in xxx ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
  ➜  press h + enter to show help

Click on the link to open the website in your browser. (the port may be different, but Vite is usually 5173)


# Andrew
API calls will all be marked with a comment that says "API" in the files - generally anywhere there's a fetch call now and many of the buttons. All given paths are relative to `Frontend/src/components`. 

## List of Flask API functions:
+ `Frontend/src/App.jsx.jsx`: form onSubmit function should validate the login and set isSubmitted and the username
+ `NavBar/UserProfile.jsx`: This is the settings button - I will add the option to delete a user account, that button will have an API function attached to it. (This module may move!)
+ `ChoreCards/ChoreCard.jsx`: Each card has "complete" button. The onclick function should notify the backend that the chore has been completed. 
+ `House/AddChore.jsx`: This one isn't done yet, but it will bring up a short form with a chore name and description, and then submit button to that needs to notify the backend that of the new chore.