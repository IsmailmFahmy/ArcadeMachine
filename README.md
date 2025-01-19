# Preface
This is a fork of the [repository provided](https://github.com/CleoSchulten/ArcadeMachine).

This is the work of Group 2.
The 2 games worked on were:
- Snake game
- Racing game


---

# Welcome to CodeArcade

In this Hackathon, You will work in teams on a pre-built virtual arcade machine to add onto existing games or add your own game with the help from each other and our mentoring team.

We will be using the [PyGame](https://www.pygame.org) library to build an arcade machine with a few games in [Python](https://www.python.org). \
But our games are missing some features that would make the game more fun to play. We believe you can use your creativity combined with your programming skills to make the games more fun to play.

## Tools and Technologies used
<!-- _source:_ https://github.com/inttter/md-badges?tab=readme-ov-file# -->
| **Operating Systems** | **Languages** | **Package Managers** | **IDEs and Editors** | **Code Style** | **Documentation** |
|------------------------|---------------|-----------------------|----------------------|----------------|--|
| ![Linux](https://img.shields.io/badge/Linux-FCC624?logo=linux&logoColor=black) | ![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=fff) | ![PyPI](https://img.shields.io/badge/PyPI-3775A9?logo=pypi&logoColor=fff) | ![Visual Studio Code](https://custom-icon-badges.demolab.com/badge/Visual%20Studio%20Code-0078d7.svg?logo=vsc&logoColor=white) | ![BlackFormatBadge](https://img.shields.io/badge/code%20style-black-000000.svg) | ![ReadMe](https://img.shields.io/badge/ReadMe-018EF5?logo=readme&logoColor=fff) |
| ![macOS](https://img.shields.io/badge/macOS-000000?logo=apple&logoColor=F0F0F0) | ![YAML](https://img.shields.io/badge/YAML-CB171E?logo=yaml&logoColor=fff) |                       | ![PyCharm](https://img.shields.io/badge/PyCharm-000?logo=pycharm&logoColor=fff) | ![Git](https://img.shields.io/badge/Git-F05032?logo=git&logoColor=fff) | [![Sphinx](https://img.shields.io/badge/Sphinx-000?logo=sphinx&logoColor=fff)](#) |
| ![Windows](https://custom-icon-badges.demolab.com/badge/Windows-0078D6?logo=windows11&logoColor=white) | ![Markdown](https://img.shields.io/badge/Markdown-%23000000.svg?logo=markdown&logoColor=white) |                       |                      |                |  |
|                        | ![JSON](https://img.shields.io/badge/JSON-000?logo=json&logoColor=fff) |                       |                      |                |  |

## Setting up the project
### Prerequisites

| Tool/Software      | Version/Requirement         | Notes                                                                                                            |
|---------------------|-----------------------------|------------------------------------------------------------------------------------------------------------------|
| **Python**         | `>= v3.13`                 | Required for running scripts and applications. [Download Python](https://www.python.org/downloads/). Ensure you have at least version 3.13 installed. |
| **Git**            | Latest stable version      | Used for version control and collaboration. [Download Git](https://git-scm.com/downloads). Install if you don't have it already. |
| **PyCharm/VSCode** | Any modern version          | IDE for development; choose your preference. [Download PyCharm](https://www.jetbrains.com/pycharm/) (preferred) or [VSCode](https://code.visualstudio.com/). |

### **Setup the development-environment (**IMPORTANT**)**

* If you're a **Windows** user, please refer to this step-by-step guide: [Windows-User-Setup-Guide](setup/Windows_Setup.md#setup-only-needed-once)
* If you're a **MacOS or Linux** user, please refer to this step-by-step guide: [Mac-Linux-User-Setup-Guide](setup/Mac_Linux_Setup.md#setup-only-needed-once)

With these steps completed, you’re all set to start coding and enhancing the games! 🎉


### How to run the games
If you've followed the steps above, you should be able to run the games by running the main.py file in the games folder.
- If you're using an IDE like [PyCharm](https://www.jetbrains.com/pycharm/) or [vscode](https://code.visualstudio.com/), you can run the [main.py](main.py) file by clicking the green play button in the top right corner.
- If you're using a terminal, you can run the main.py file by typing `python main.py` in the terminal from the repository folder you cloned earlier.

Now you're ready to start playing!  🎉🎉🎉

## The Arcade Machine
When you run the main.py file, you should see a window like this pop up:

![Arcade Machine](/assets/example_pictures/ArcadeMachine.png)

This is the arcade machine. You can use the arrow keys to navigate the menu and press enter to start the selected game.

The arcade machine displays the games that are in the games folder and registered in it. When you start a game, the arcade machine will run the main game file from inside the game folder.

The main game file is not necessarily called main.py, but it is the file used when registering the game in the arcade machine. \
For example, the racing game is registered like this; the main game file is called game.py.

```python
# main.py
machine.register_game(ArcadeGame("Mumble Club", "games/aracinggame/game.py",
                                     "hard", "3-4 h", "assets/example_pictures/racinggame.png",
                                     "Singeplayer game. Drive faster than your friends and become the master of the road!",
                                     "Procedural code. Help the timekeeper find his stolen watch by coding!"))
```

### Want to add your own game?
1. Create a new folder in the games folder
1. write your game code
1. register your game in the main.py file with some description as shown in the example above

et voilà! your game is now in the arcade machine.

## Existing Games
We have already created a few games that you can build upon. These games can be found in the [games folder](games). While functional, they are missing some features that would make them more fun to play. Use your creativity and programming skills to enhance these games!

Each game includes a README file with explanations and ideas (as well as hints) on what you can add. Check them out:

| Game             | Description                                                                                     | Link to README                              |
|-------------------|-----------------------------------------------------------------------------------------------|--------------------------------------------|
| **Snake**        | A classic snake game where the goal is to eat and grow without crashing into yourself or walls. | [Snake README](games/snake/README.md)      |
| **Pong**         | A two-player paddle and ball game inspired by the original arcade classic.                     | [Pong README](games/pong/README.md)        |
| **Space Invaders** | A shooter game where you defend against waves of alien ships.                                  | [Space Invaders README](games/space_invaders/README.md) |
| **Pacman**       | Navigate mazes, eat pellets, and avoid ghosts in this arcade legend.                           | [Pacman README](games/pacman/README.md)    |
| **Pinball**      | A digital pinball game where you control flippers to keep the ball in play.                    | [Pinball README](games/pinball/README.md)  |
| **Racing Game**  | A fast-paced game where you control a car and race against obstacles or competitors.           | [Racing Game README](games/aracinggame/README.md) |

## Contributing
Done with all the games? Great! Now you can help us improve the arcade machine. \
we would like to receive your upgraded version of the arcade machine in a [pull request](https://docs.github.com/en/get-started/quickstart/contributing-to-projects#making-a-pull-request).

1. Make sure your work is up to date and pushed to your forked repository's main branch.
1. Create a pull request from your forked repository to this repository's main branch.
    1. Github should automatically detect that you're making a pull request from a forked repository. Go ahead and click the green button to create the pull request.
    ![](assets/example_pictures/create_pull_request.webp)

    1. Please ensure that the title of the pull request is your group name. In the description, let us know if there is anything else we should know about your pull request.
    ![](assets/example_pictures/pull_request_title.webp)

And That's it! We now have your upgraded version of the arcade machine and will use it for furhter evaluation of our study.\
Make sure to finish your pull request before the end of the hackathon since we will only review changes made until the end of the Event.
