# BreakoutRoomProject

How to Run Program for Testing
1. Run systemserver.py 
    ex. python systemserver.py
2. run instructor_gui.py first in order to be assigned as instructor
3. press connect to server on gui
    - you should see a message on system server window indicating connection was successful
4.run student_gui.py
5.press connect on student gui

student can press play and stop video, request moving to new room, and chat with people in current room

INSTRUCTOR_GUI COMMANDS
/room "room_name" -- switches instructor to specified room
/create_room "room_name" -- creates room with the specified name
/list_room -- will list all available rooms

#need to add
/move_student "student address", "room name"
/play_video "room" --start movie in specified room
/list_connected_users -- list of current users online
/close_room "room" -- closes current room and returns everyone to main room

student command /private "message" will send a private message to instructor

TO DO LIST
* add 3 rooms + main room should have movies already playing
* pause play and stop movie by instructor
* display movies on screen in gui
* get short videos to display in each room
* document how to run instructor.py
* report on entire program
* have usernames instead of addresses for students
* get movie player working
*fix chat box no messages from other appear in box

*initial main room should be blank and then move into room1,2,3
*instructor to be able to create new 
* add private message with instructor



Current Issues
- users cant connect to server
connection failed "MovieTheaterClient' object has no attribute 'username' 

