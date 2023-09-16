## FitHub
A Django-based web application has been created to offer individuals a comprehensive solution for managing various aspects of their health and fitness endeavors. This app proves invaluable for individuals seeking to monitor their dietary selections, physical activities, and overall well-being goals. The project originated as my final assignment for the CS50's Web Programming with Python and JavaScript course. However, after submitting it, I made the decision to further enhance its complexity and uniqueness. 

<img src="https://github.com/pedrofvgomes/fithub/blob/main/screenshot.jpg?raw=true">

# How To Run

In the root directory, run <code>python ./manage.py makemigrations fithub</code>, then <code>python ./manage.py migrate</code>, to make all the database migrations needed for the applications. Finally, run <code>python ./manage.py runserver</code> and open the given IP Address that's given to you by the console output in your preferred browser.

# Fitness Tracker Web Application with Django

In the world of modern technology, staying fit and healthy has become a top priority for many individuals. To assist in my fitness journey, I created an innovative web application using the Django framework. This comprehensive solution allows users to monitor weight, nutrition, and calorie intake. Let's delve into the intricacies of this web application, explaining its various components and functionalities.

# Understanding the Django Framework

Before diving into the specifics of the fitness tracker application, it's essential to have a basic understanding of the Django framework. Django is a powerful Python web framework known for its simplicity and robustness. I leveraged it to handle various tasks, from user authentication to data management.

# User Authentication and Registration

The foundation of any web application is user authentication and registration. In the fitness tracker, users can sign up for an account, providing a unique username and a secure password. Django's authentication system handles user data securely, ensuring that passwords are hashed before storage to protect user information. Users can also log in and out of their accounts with ease, thanks to Django's built-in authentication views and functions.

# User Profile Management

A central feature of the fitness tracker is user profile management. Users can input essential information, such as their age, height, starting weight, and gender. This information serves as the basis for calculating various fitness metrics, including Basal Metabolic Rate (BMR) and daily calorie requirements. Users can update their profiles, and these changes are stored securely in the database, allowing for accurate tracking of progress over time.

# Weight Tracking

Tracking weight is a fundamental aspect of any fitness journey. The fitness tracker allows users to log their weight regularly. Each weight entry is timestamped, providing a historical record of weight changes. Users can also view a graphical representation of their weight over time, helping them visualize their progress. Weight data is stored in the database, making it accessible for future analysis and reporting.

# Nutrition and Calorie Tracking

Managing nutrition and calorie intake is a crucial component of any fitness regimen. In the fitness tracker application, this task is streamlined through seamless integration with an external API that provides a comprehensive database of food items and their nutritional values. Users can effortlessly search for and select the foods they consume, ensuring accurate tracking of their dietary choices.

# Data Visualization

Visualization is a powerful tool for tracking progress and setting goals. In the fitness tracker, users can view graphical representations of their weight and calorie intake over time. Line charts display weight changes, while bar charts illustrate daily calorie consumption. These visualizations provide valuable insights and motivation for users on their fitness journey.

# Data Security

Data security is paramount in any web application, especially one that involves user information and health data. I incorporated security measures, such as password hashing and data validation, to protect user data from unauthorized access or breaches. The fitness tracker also ensures that users can only access and modify their own data, maintaining privacy and confidentiality.

# Conclusion

The fitness tracker web application built using Django offers users a comprehensive solution for monitoring their fitness progress. From weight tracking to nutrition management, this application provides valuable tools for individuals striving to lead a healthier lifestyle. With user authentication, data visualization, and robust data security, it combines functionality and security to create a reliable fitness companion.

In a world where health and fitness are of paramount importance, the fitness tracker built with Django empowers individuals to take control of their well-being. Whether you're embarking on a fitness journey or simply maintaining a healthy lifestyle, this application serves as a valuable resource for tracking and achieving your fitness goals. It exemplifies the potential of Django in creating versatile and secure web applications that cater to the diverse needs of users in today's digital age.

# Distinctiveness and Complexity

I created this web application all by myself, and it stands out through its unparalleled distinctiveness and remarkable complexity. Unlike other projects in this course, I meticulously crafted an innovative platform that transcends conventional boundaries. It's essential to note that my project does not resemble the old CS50W Pizza project, ensuring its uniqueness.

Furthermore, I avoided the clichéd path of developing yet another social network or e-commerce site, which would have been indistinguishable from previous projects. Instead, my project ventures into uncharted territory, offering an entirely new and exciting user experience.

# Created Files

I've created script.js, which contains the JavaScript code for the pages, styles.css, which contains the styling, authentication.html, which is the template file for the authentication page (I've decided to write this page in a different file, to better separate the authentication process from the app's main process), and index.html, which contains every part of the app's main process, just like the Mail project in this course. I made this decision because the screen can be automatically refreshed, without redirection or page refresh, and to better display my JavaScript abilities. The script element inside index.html contains the code for the chart, I found it better to do it this way so that I could include the src file for Chart.js.
