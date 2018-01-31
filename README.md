# OpenGMS
[![Build Status](https://travis-ci.org/shikkanobish/OpenGMS.svg?branch=master)](https://travis-ci.org/shikkanobish/OpenGMS)


An Open Source Garments Management System

## Features

- Production-ready configuration for Static Files, Database Settings, Gunicorn, etc.
- Enhancements to Django's static file serving functionality via WhiteNoise.
- Both Python 2.7 & 3.6 runtime environment support.
- Use of Machine Learning to predict order finish time & sort unconfirmed orders.

## How to Use

To use this project, follow these steps:
1. Clone this repo using git. Ex: `$ git clone git@github.com:shikkanobish/OpenGMS.git`
2. Create your working environment.
3. Install requirements.txt
4. Create a .env file that have entries which are in sample.env file

## Deployment

- The system is now deployed at Heroku in [this link](https://opengms.herokuapp.com/).
- Media file Hosting in Amazon AWS.
- Connected to Travis CI for build testing.
- Automated deloyment to Heroku after build passing.
- Dockerfile to develop using the power of Docker tools.

## Some Screenshots

![Alt text](media/Screenshots/TechnicalOfficerCreateAccount.png?raw=true "Technical Officer Create Account View")
Fig: Technical Officer Create Account View


![Alt text](media/Screenshots/TechnicalOfficerAccounts.png?raw=true "Technical Officer Accounts List View")
Fig: Technical Officer Accounts List View

![Alt text](media/Screenshots/ServiceManagerProfile.png?raw=true "Service Manager Profile View")
Fig: Service Manager Profile View


![Alt text](media/Screenshots/ServiceManagerNewOrder.png?raw=true "Service Manager New Order View")
Fig: Service Manager New Order View


![Alt text](media/Screenshots/ServiceManagerOrderApproval.png?raw=true "Service Manager Order Approval View")
Fig: Service Manager Order Approval View


![Alt text](media/Screenshots/ServiceManagerTechnicalSelection.png?raw=true "Service Manager Technical Manager Selection View")
Fig: Service Manager Technical Manager Selection View


![Alt text](media/Screenshots/ServiceManagerOrderHistory.png?raw=true "Service Manager Order History View")
Fig: Service Manager Order History View


![Alt text](media/Screenshots/ServiceManagerGraphs.png?raw=true "Service Manager Order Graphs View")
Fig: Service Manager Order Graphs View


![Alt text](media/Screenshots/ServiceManagerPriority.png?raw=true "Service Manager Order Priority View")
Fig: Service Manager Order Priority View


![Alt text](media/Screenshots/ServiceManagerNotification.png?raw=true "Service Manager Notification View")
Fig: Service Manager Notification View


![Alt text](media/Screenshots/ClientOrderProgress.png?raw=true "Client Order Progress View")
Fig: Client Order Progress View


![Alt text](media/Screenshots/ProductionManagerEstimate.png?raw=true "Production Manager Estimate Finish Time View")
Fig: Production Manager Estimate Finish Time View

