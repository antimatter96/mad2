❌ ✅ 🔘

### Core Functionality


- [✅] Base requirements
  - [✅] User signup and login
  - [✅] User profile view with basic stats
  - [✅] Blog Post Management
  - [✅] Search and Follow / Unfollow Others
  - [✅] User’s Feed

- [✅] Backend Jobs
  - [✅]  Export Jobs
  - [✅]  Reporting Jobs
  - [✅]  Alert Jobs

- [✅] Backend Performance


### Core - User Signup and Login


- [✅] Form for username and password (both login and signup)
- [✅] Use Flask Security and Token Based Authentication
- [✅] Suitable model for user


### Core - User's Profile


- [✅] Basic profile view for a user
- [✅] Ability to view the number of blogs created
- [✅] Ability to view the number of followers and people you follow
- [✅] Ability to view the list of posts created


### Core - Blog management


- [✅] Create a new blog
  - [✅]  Storage should handle multiple languages - usually UTF-8 encoding is sufficient for this
  - [✅]  Content should handle the safe HTML tags

- [✅] Edit a blog
  - [✅]  Change title/caption or image

- [✅] Remove a blog**
  - [✅]  With a confirmation from the user

- [✅] Export option is required


### Core - Search and Follow / Unfollow Others


- [✅] Ability to search other users
- [✅] Ability to follow others
- [✅] Ability to unfollow others


### User’s Feed


- [✅] Show the blogs/posts created by other users
- [✅] Navigate to the user’s profile on clicking the username on the blog or post


### Core - Daily Reminder Jobs


- [✅] Scheduled Job - Daily reminders on Google Chat using webhook or SMS or Email
  - [✅]  In the evening, every day (you can choose time of your choice)
  - [✅]  Check if the user has not visited/posted anything
  - [✅]  If yes, then send the alert asking them to visit/post


### Core - Scheduled Job - Monthly Engagement Report


- [✅] Scheduled Job - Monthly Engagement Report
  - [✅] Come Up with a monthly progress report in HTML (email)
  - [✅] On the first day of the month
    - [✅] Start a job
    - [✅] Create a report
    - [✅] Send it as email


### Core - User Triggered Async Job - Export as CSV


- [✅] User Triggered Async Job - Export as CSV
  - [✅] Come up with an export CSV format for blogs
  - [✅] Have a dashboard where the user can export
  - [✅] Trigger a batch job, send an alert once done


### Core - Performance and Caching


- [✅] Add caching where required to increase the performance
- [✅] Add cache expiry
- [??] API Performance


### Recommended (graded)


- [🔘] Backend Jobs
  - [🔘]  Import Jobs

- [✅] Well designed PDF reports (User can choose between HTML and PDF reports)

- [🔘] Single Responsive UI for both Mobile and Desktop
  - [🔘]  Unified UI that works across devices
  - [🔘]  Add to desktop feature
