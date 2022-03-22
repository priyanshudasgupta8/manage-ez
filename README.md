# ManageEZ

 ------

 ### Video Demo: [This link](https://youtu.be/E73S_C6QnYc)

 ------

 ### Description:

  My web-app or website is called **ManageEZ**. The web-app is hosted on [this URL](https://ide-70814a949ddd41e4be5aa79158acea2c-8080.cs50.ws/) It is developed for automating and simplifying the __management system__ of many communities (rental apartments and etc.). It is built using Flask and minimal jQuery. The languages I used for building this website are JavaScript, Python, HTML and CSS. I built this project off of my problem set for C$50 Finance, which is why the styling of ManageEZ is almost identical to that of my C$50 Finance problem set. I worked on this project solely, and did not receive or take any help from any peers or parents. However, I will admit referring to stackoverflow and GitHub for help solving several bugs and learning new methods for solving some problems I faced along the way. I can confidently say I didn't encounter any dilemmas along the way for building this project, in fact it turned out exactly how I hoped it would. The following paragraphs are going to serve as an explanation of my code in each and every file:

 ------

 ### Explanation of code in different files:

 #### 1. manage.db

 The file "manage.db" contains an SQL database by the name of "manage". This database consists of 3 different tables corresponding to 3 different aspects of the web-app. The tables are:

 1. users -- info regarding all users
 2. staffschedule -- schedules of all staff
 3. calls -- all information regarding all requests

 These tables contain information regarding the users, staff schedules, and requests from residents.

 This table showcases all of the columns in the **users** table:

 |       User-ID        |    Username     |        Password        |     Type     |   Community    |     Expertise     |
 | :------------------: | :-------------: | :--------------------: | :----------: | :------------: | :---------------: |
 | stores the user's id | stores username | stores user's password | account type | community name | area of expertise |

 This table showcases all of the columns in the **staffschedule** table:

 |       Staff-ID        |     User-ID     |                        Start-Day                         |                        End-Day                         |      Start-Time      |      End-Time      |
 | :-------------------: | :-------------: | :------------------------------------------------------: | :----------------------------------------------------: | :------------------: | :----------------: |
 | staff ID (only staff) | staff's user ID | day of the week when the staff member starts their shift | day of the week when the staff member ends their shift | start time for shift | end time for shift |

 This table showcases all of the columns in the **calls** table:

 | Request-ID |    Resident-ID     |    Staff-ID     |        Status         |          Description          |             Requirement              |                  Request-Time                  |                  Accept-Time                  |                    Complete-Time                    |                   Staff-Description                    |                 Rating                  |                          Complaints                          |
 | :--------: | :----------------: | :-------------: | :-------------------: | :---------------------------: | :----------------------------------: | :--------------------------------------------: | :-------------------------------------------: | :-------------------------------------------------: | :----------------------------------------------------: | :-------------------------------------: | :----------------------------------------------------------: |
 | Request ID | Resident's user ID | Staff's user ID | Status of the request | Description given by resident | Type of staff needed for the request | Time request should be solved by (future only) | Time request was accepted by any staff member | Time request was completed (blank if not completed) | Description of what the staff did to complete the task | Rating from resident for the completion | Any complaints from the resident (must be valid in order to be considered by staff in the future) |

 #### 2. helpers.py

 The "helpers.py" file is there to provide assistance to "application.py" with 2 different helper functions. The two functions are:

 1. apology:

    This function helps to return any error code to the user in a clear way. The messages look like this:

     ![This is the error message.](/images/err.png "This is a error image.")



 2. login_required

    This function serves as a decorator for the flask code. This simplifies the code in "application.py" to check if the user is logged in or not at the time of creating routes for different pages of the app.



 #### 3. application.py

 The "application.py" file is the main file of the entire project and it handles all requests and routes them accordingly. Atop the file, the code imports all of the required libraries, files, and functions. It also configures the flask application by configuring the responses and requests, it also sets up the "manage.db" SQL database. The remainder of the file mainly talks about and sets up the functionalities of the different routes. This file contains code for 9 different successful routes the names of which are:

 - "/" -- The index route or the main page
 - "/tasks" -- This route is accessible only to staff members. The route is used for displaying the tasks the staff member is responsible for
 - "/my_req" -- This route is accessible only to residents. The route is used for displaying the requests the resident raised.
 - "/schedule" -- This route is accessible to staff members only. It shows the schedule or the uniform work hours for the staff member.
 - "/login" -- This route allows users of the application to log into their accounts
 - "/logout" -- This route returns a redirect to the login route after logging the previous user out
 - "/register" -- This route allows users to create their own accounts (to be used if user doesn't already have an account)
 - "/call" -- This route allows the resident to raise a request using a form. It is exclusive to residents only.
 - "/listr" -- This route shows the staff members of a particular community all of the pending requests the residents of the community have raised. The staff members can accept certain requests which interest them. Only one staff member will be allowed to accept a request. This is exclusive to staff members only.

 And finally, at the bottom of the file, are several pieces of code which help with handling various kinds of errors. They are mainly error handlers. For instance, this is the code which is present in the bottom of the file and it handles all exceptions and errors that might unexpectedly pop up:

 ```python
 def errorhandler(e):
     """Handle error"""
     if not isinstance(e, HTTPException):
         e = InternalServerError()
     return apology(e.name, e.code)


 # Listen for errors
 for code in default_exceptions:
     app.errorhandler(code)(errorhandler)
 ```

 #### 4. static/images/

 This folder as the name itself suggests, contains all of the images the project uses. Images such as the error cat and another photo by the name of "cancel.png". The "cancel.png" is a cross icon such as this one but only a bit smaller in size than this one:

 <img src="/images/cancel.png" alt="This is the close icon." title="This is a close icon." style="zoom:15%" />

 Although at the moment it only contains two images, in the days to come, alongside many future features and additions will also come more images into this folder. But for now, it is pretty dry inside of this folder.



 #### 5. static/

 This folder consists of all of the static or unchanging files. These files are not dynamic and contain code which are called pretty rarely unlike the "application.py " or any of the HTML files. The folder contains files named "style.css", "styles.css", "script.js", and "favicon.ico". all details of these files are mentioned and described below from the points 6 - 8. The "favicon.ico" calls for barely any explanation. It is just a square image that I graphically designed on Adobe Illustrator. It is the tiny image that is displayed on the left of the title of the tab this application is open in.



 <img src="/images/fav.png" alt="This is the close icon." title="This is a close icon." style="zoom:1.5;" />



 #### 6. style.css

 This Cascading Style Sheets file styles 2 different functionalities of the project. For the majority of the file, the file programs how the modals or popups appear when certain buttons are pressed in the file. This file is one of the main reasons why the site is so fluid and smooth. It is the main reason why it feels good to use the website. The last part of the file programs the appearance the 5-star (in this case, 5-circle) rating system. The rating also involves a bit of JavaScript however that will be explained later on in this file. That was all there was to the first of the two stylesheets of this projects, modals and ratings.



 #### 7. styles.css

 This CSS file provides styling to almost the entire project. Although many elements in the project contain in-line styling, this file is pretty similar to "style.css" and is very much required. Because most of the styling of the site is provided by Bootstrap, this file mainly designs the navigation bar and the ManageEZ logo. It also styles all of the buttons in site with an interesting hover animation. However this file overwrites some Bootstrap stylings such as the text overflows and screen widths. That is mainly everything about the "styles.css" file.



 #### 8. script.js

 This is the only JavaScript file in the entire project and it provides dynamicity to the registration form the users of this website need to fill out when using it for the first time. It is very small in size, in fact it only contains two small functions. Although this project uses a lot of JavaScript, most of it is present in script tags inside of some HTML files. In this JavaScript file, 2 functions are present and they are called showStaffOption() and hideStaffOption(). The showStaffOption() function allows the user to see and fill up an extra field of information if they say that they are a staff member. That extra field is a required section and it asks the user to enter their field of expertise such as being an electrician or a carpenter. And on the other hand, the hideStaffOption() function is used to hide that extra field. This function is called when an user says that they are a resident instead of a staff member.



 #### 9. templates/

 This another major folder for the project. Although it is called templates, in its essence it is just a folder storing all of the HTML files for the project. It contains 12 different HTML files each serving up a different page of the project. All of the information which is displayed on these files are supplied from the "application.py" file. All of this information is then embedded into the files using the help of a programming language called jinja. It serves the purpose of templating the html for the information from the python file. The following parts of this description go through each of the files in detail:



 #### 10. layout.html

 This HTML file is a template for all of the other HTML files which are present in this project. This is to help reduce redundancy and repetition of code, it also makes coding such projects an easier task. It is majorly responsible for implementing all of the dependencies such as Bootstrap and jQuery into the project. This file also programs the navigation bar depending on the type of user who is using the the site.  And at the very bottom of the file, it also implements a tiny footer saying, "To be used by communities". These details are then implemented into all of the the other HTML files.



 #### 11. apology.html

 This is the shortest and simplest HTML file inside of this folder. It was brought into my project from my own C$50 Finance problem set. All it does is display an image of a cat alongside a brief and concise description of the error that has occurred. This screen is closely related to the apology function in "helpers.py", since the function send the error message and "apology.html" just renders it properly.



 <img src="/images/err2.png" alt="This is the error screen." title="This is an error screen." style="zoom:100%;" />



 #### 12. login.html

 This HTML file is almost identical to the one that I used for my CS50 Finance Project. It is a simple file which helps the user log into their account. If the login was successful, they are redirected to the index page, but if the login was unsuccessful, they are thrown into an apology screen telling the user what the problem was. The screen only contains 2 fields of input, one for the full name of the user and the other one for their password.  Also note that this page will not provide a successful login for a first-time user who did not register for an account yet.



 #### 13. register.html

 Register.html is a very essential page which helps the app create a new account for a first-time user. This is the only file which deals with the previously described "script.js" file. It presents a form with 5 required and 1 optional field. The optional field is displayed only when the user describes themselves as a staff member. The first field asks for the community the user is living/working in. The second field requires the user to enter their full name; this is going to  serve as a username for logging in. The next 2 fields are for setting a password, the second field asking for the password is present in order to double check the password before setting it. This double-checking is helpful since it helps the user be sure of what the password is and it also minimizes the risk of setting a faulty password. After those text-based fields, 2 radio buttons are placed. The first one should be selected if the user identifies themselves as a resident and the second one is for all users who are staff members. If the second choice is selected, a dropdown appears under the buttons which asks for the user to choose what their specialty is.  The specialties include being a carpenter to a receptionist. Once the user registers, their account is instantly created.



 <img src="/images/register.png" alt="This is the calls screen." title="This is what the screen looks like." style="zoom:100%;" />



 #### 14. call.html

 This HTML file is an important one, if not the most important one.  The entire purpose of this application is dependent on this one file. This file is accessible only for residents. It presents the users with a form with 3 main fields. The fields are the date and time, requirement type, and a small description of a problem. To prevent unnecessary harassment of the staff members of the community, date and time that the resident can enter has to be in the future. This form serves as information for creating a working order for the staff members. Once this form is submitted this information will be sent to the database and it will also displayed in the pending work orders list for every staff member. This is what the screen looks like:

 <img src="/images/form.png" alt="This is the calls screen." title="This is what the screen looks like." style="zoom:100%;" />



 #### 15. index.html

 This is the screen or page which is displayed for the request requesting for the index route. It is a simple page which only greets the user to the site since it where they will usually land after logging in. It also displays a table whose sole purpose is to let the user know who the staff members are for their community. It only has three different columns letting the user know about the member's name, their area of expertise and the community they are a part of. This is a sample table which was used while building this project.



 <img src="/images/table.png" alt="This is the table in the index screen." title="This is what the table looks like." style="zoom:100%;" />



 #### 16. listr.html

 The "listr.html" file is also a very simple file. It serves the sole purpose of displaying all of the pending and in progress tasks. The pending concerns from the residents of the community are shown here. The staff member can accept the task for their own to-do list. As long as that staff member doesn't complete the task, it will still be shown in the list as an "in progress" task. These types of tasks cannot be accepted by other staff members. Once the task is completed, the item disappears from this table unless it is re-opened by the resident. The table consists of 7 different columns with only 6 of them displaying data and the last one being used to accept a certain request. This screen looks like the following:



 <img src="/images/listr.png" alt="This is the pending list screen." title="This is what the screen looks like." style="zoom:100%;" />



 #### 17. schedule.html

 The "schedule.html" file is a concise file as well. It only displays the regular work hours for the staff members of the community. After creating a new account, this schedule is usually assigned to the member within 3 days. The administrator of the app usually assigns this schedule. Currently, this job is done by me, but as a future feature this process will be further automated and streamlined. The table displayed in this screen only contains 2 columns one describing the time slot and another describing the days of the week they should be working. To prove that these schedules are not always going to be so regular, a disclaimer is also provided near the bottom of the table. It reads, "Please note that this schedule is subject to change from week to week and therefore, this isn't a permanent schedule." This is how the screen looks.



 <img src="/images/schedule.png" alt="This is the pending list screen." title="This is what the screen looks like." style="zoom:100%;" />



 #### 18. my_req.html

 This file is a important one since it displays the different requests a certain resident has made. This page is only visible and accessible to residents. Once the resident enters this screen, they will notice three different tables, the first representing all of that resident's ongoing requests, the second one shows all of the completed requests, and the table shows all of the closed requests. For a request to turn into a closed request from a completed one, the user must give a rating to the completion. If the rating is a 3  or lower on a scale of 5, the request is reopened and is shown as incomplete. But on the other hand, if the resident is at least satisfied with the service they got, the request will be marked as a closed one. The resident can also view what was done to complete their request and all of the other descriptions of the case in a summary section once the request is marked as closed.

 <img src="/images/my_req.png" alt="This is the my requests screen." title="This is what the screen looks like." style="zoom:100%;" />



 #### 19. tasks.html

 The "tasks.html" is very similar to the "my_req.html" file, except for the fact this page is only accessible by staff members. This file also contains three tables. The first table displays all of the requests that were accepted by the staff member and are now ongoing, the second table shows all of the completed requests, and the last table shows all of the closed requests which were attended to by the user of the page. On the first table, there is an option for completing a particular request that the member has accepted. The successfully mark it as completed, the user must also describe the steps they took in order to accomplish the request. Once it is marked as completed, the staff member needs to wait for the requesting resident to close or reopen the request.

 <img src="/images/tasks.png" alt="This is the tasks screen." title="This is what the screen looks like." style="zoom:100%;" />

 ------

 ### Sources:

 - #### Creating a Modal: [YouTube Tutorial](https://www.youtube.com/watch?v=bGNeZ6P3nqU&t=16s)
 - #### Creating a star rating system: [Stack overflow](https://stackoverflow.com/questions/8118266/integrating-css-star-rating-into-an-html-form)
 - #### Getting a formatted timestamp in JS: [Stack overflow](https://stackoverflow.com/questions/221294/how-do-you-get-a-timestamp-in-javascript)