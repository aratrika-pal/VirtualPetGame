# VirtualPetGame

Developers: Aratrika Pal, Eva Arya
Overview
Kawaii Virtual Pet is an interactive Python simulation that lets users care for a virtual pet while managing finances and health. The program teaches responsibility, budgeting, and logical thinking through real-time gameplay. Players feed, play with, and heal their pets, manage a starting balance of $1,000, and respond to random events such as sickness. The pet’s mood and health dynamically update based on user actions.

Features
Create a personalized pet with a name, type (Dog, Cat, Hamster), and color.
Real-time stat tracking: health, happiness, hunger, age, and balance.
Dynamic graphical user interface (GUI) with:
Gradient animated background
Live-updating pet stats
Mood-based pet images (happy, neutral, sad, sick)
Popup input windows for actions
Animated sparkle effects
Realistic game mechanics:
Feeding increases hunger, health, and happiness
Playing increases happiness and health but decreases hunger
Aging system triggered after repeated care
Random sickness events affect pet health
Financial management:
Purchase food and toys
Heal pets with a cost to balance and happiness
Work jobs to earn money, with proportional happiness decrease
Input validation to prevent invalid numbers, over-purchasing, and selecting invalid options
Timestamped health and expense reports

Installation
Install Python 3.8 or higher: https://www.python.org/downloads/
Clone or download this repository.
Ensure the following files are in the same directory:
main.py (source code)
Image assets: happy.png, neutral.png, sad.png, sick.png, and optional mood-based images (dog_happy.png, cat_sad.png, etc.)
Install required libraries (usually included with Python):
pip install tk

How to Play
Run the program:
python main.py
Enter your pet’s name, type, and color.
Use the action buttons to:
Feed your pet
Play with your pet
Heal your pet
Buy food and toys
Work to earn money
View health and expense reports
Monitor pet stats and manage your balance carefully. The pet’s health can decrease over time due to hunger or sickness. If health reaches zero, the pet dies and the game ends.

Code Structure
Modular Functions: Each action (feeding, playing, healing, buying, working) is implemented as a function for readability and ease of debugging.
Conditional Statements: if, elif, and else statements control pet mood, survival logic, aging, random sickness, and input validation.
Data Structures:
Dictionaries: store pet stats, food and toy prices, job earnings
Lists: track health and expense reports
Global variables: track player balance and pet state
Game Loop: Uses root.after(20000, game_tick) to update stats every 20 seconds.

Libraries Used
Tkinter: for GUI components, buttons, popups, and images
Datetime: for timestamped reports
Random: to simulate random sickness events

Input Validation
Ensures integer values are entered where required
Checks for maximum allowed values when feeding, playing, or buying items
Validates that user-selected options exist in dictionaries
Prevents spending beyond the current balance

Credits
Python: https://www.python.org
Tkinter Documentation: https://docs.python.org/3/library/tkinter.html
Image Assets: Custom-designed or free assets credited in the images/ folder

Notes
The program must remain open while playing to simulate real-time progression.
Users are encouraged to manage resources responsibly, reflecting real-world pet ownership.
All values (health, happiness, hunger, balance) are capped at 100 or minimum 0 to ensure game balance.

