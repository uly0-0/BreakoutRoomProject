# BreakoutRoomProject

How to Run Program for Testing
1. Run systemserver.py 
    ex. python systemser.py
2. run studentgui.py
3. press connect to server on gui
    - you should see a message on system server window indicating connection was successful
4.run instructor gui
INSTRUCTOR_GUI COMMANDS
/room "room_name" -- switches instructor to specified room
/create_room "room_name" -- creates room with the specified name
/list_room -- will list all available rooms

#need to add
/move_student "student address", "room name"

TO DO LIST
* add 3 rooms + main room should have movies already playing
* pause play and stop movie by instructor
* display movies on screen in gui
* get short videos to display in each room
* document how to run instructor.py
* report on entire program
* have usernames instead of addresses for students
* get movie player working


Current Issues
- connection issues : gui crashes and disconnects right after sending message or requesting breakout room. Messages sent get received by server but connection gets killed. Might be a Time to live issue thats killing connection. 

