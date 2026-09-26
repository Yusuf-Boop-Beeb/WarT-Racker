This is a little side project I'm working on and I'm working to expand it to something bigger than it is

At the moment what this does when you launch it via exe or run the script is this:
Warthunder stores some information about your current game status via localhost on port 8111
so, This script utilizes that in order to display that information on discord via an app which is connected via rpc (Remote procedure call)
It also has the feature of displaying vehicles currently used in game via a large database of the names of the vehicle which utilizes hashing
in order to translate the code-name of the vehicles (which is displayed on a localhost endpoint) to it's intended name.
I also added the function of kill and death counting which parses an endpoint of messages or events of the current state of the game and
detects when your username has been in one it then figures out wheather you were the one getting a kill or the victim to someone else.
It also detects which game-mode you're in though this has some issues with some air matches 40% of the time it displays it incorrectly as test flight but
I'm working on a solution soon for that.
  
