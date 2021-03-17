# point-calc

## Use
Used for a points system between multiple participant based on interviews, deliveries, and quiz scores.

## Setup
1. (a) If you have Windows, install the Linux subsystem. Follow the steps [here](https://docs.microsoft.com/en-us/windows/wsl/install-win10). Then in Ubuntu, clone the repository. You'll need git and python3, there's probably a command that installs all the necessary packages. If you have Mac or Linux, you can skip this step. Open your terminal and change into the directory where you want to store the app using `cd`.

2. Create a virtual environment by typing in `python3 -m venv venv'. This creates a special python environment to work in that will store all the dependencies for the app.

3. Activate the virtual environment by typing in `. venv/bin/activate`. Your shell line will now have a (venv) in front of it.

4. Install the program dependencies by typing in `pip install -r requirements.txt`

5. Update the CSV files under /dict with whatever names you need. Add the current roster of interviewees to brotherList.csv, and the current roster of pledges to totalList.csv

## Run

Simply typing `python pointcalc.py` will run the applet. To change the lists of people to total for, simply change the list of names and replace the rest of the CSV columns with 0. All of the scores are stored in the /dicts folder.

## Bugs

-Will not work on a Windows PC with the Linux Subsystem, or in Docker/any other VM. This is because tkinter can't figure out where to point the GUI to display. If there's a way around this, please let me know. I can't figure out how to fix it.
-Dates will only go up to 2020. This is appJar's fault because their DatePicker is still in beta. I may just change it to text fields but I was feeling lazy. 


