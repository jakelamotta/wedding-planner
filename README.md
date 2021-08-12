### How to use crowd_user_management_app

#### Pre-requisites

* Docker

#### Commands to run

docker run -d -p 8000:8000 -e APP_PASS=<APPLICATION_PASSWORD> --name <INSTANCE_NAME>  docker-registry.scila.internal:5000/crowd-user-management-app


#### Environment configuration

APP_PASS*: The password of the application, this password is set for the application in Crowd. Does not have a default value and is therefore mandatory 
APP_NAME: The name of the application in Crowd to be used. If you don't set this the default value "scila-user-management-web" will be used. 
CROWD_SERVER_URL: The url to Scilas Crowd instance. Default value is "http://crowd.scila.dmz:8095/crowd"
SMTP_SERVER_URL: SMTP Server url for Scila. Default value is smtp.scila.dmz
JIRA_RESET_PASSWORD_LINK: Link to the Jira reset password page. Default value is "https://web.scila.se/jira/secure/ForgotLoginDetails.jspa"

*Mandatory 

#### Troubleshooting

If you have troubles connecting to the Crowd API. Make sure the host of the application is in the IPs allowd list in Crowd. 

https://www.digitalocean.com/community/tutorials/how-to-add-authentication-to-your-app-with-flask-login