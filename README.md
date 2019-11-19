# IMDb 
This project extends IMDb's Top 250 movie list into the top 10,000 movies

## Process Description
This fermentation simulates a fed-batch process in which an acidic glucose feed, base and antifoam are added to the reactor. The feed is triggered once the microbes show signs of
starvation through the rise of the pH and DO. During the batch phase the pH is allowed to reach a value of 7.27,
indicating all the glucose is depleted. At this point, acidic feed will be added until the pH is dropped
to the set point (7.20). Since it takes time for the feed to homogenize with the tank broth, the pH will fall
below the set point which is why the base control is needed. When the feed is first triggered, the motor ramps to 1500 rpm
as the microbes are more metabolically active and will require more oxygen for the aerobic fermentation process.
Antifoam is added on a set schedule and turns on for every 3 hours for 10 minutes after an EFT of 10 hours is
reached.
    
### Process Specifications

    Process Set Points
        Temperature - 32.0 °C
        pH - 7.20
        Airflow - 60 mL/s
        Agitation - 1000 rpm -> 1500 rpm ramp after the feed is triggered
        DO - Not controlled

    Additions
        Feed - triggered by pH
        Base - triggered by pH
        Antifoam - set time schedule

### [Demo Video](https://youtu.be/R_-4DszZCs4)
0:00 - 2:10 full fermentation run without any deviations  
2:10 - 5:24 run with deviations the notification system displayed

## Getting Started

Clone the repo: ```git clone https://github.com/Michaelli26/bioreactor-simulator```

### Prerequisites

```
pip install requirements.txt
```
### How to Run
Run ```simulatorpyqt.py``` to start the application

### How it Works
The bottom buttons alternate between changing the current top and bottom plots on display.
The top buttons introduce any of the possible 
deviations one at a time.

### Alert System
To use the email alert system, change the email addresses and update the password to an accessible account. To use the 
text alert system, an active Twilio account is needed. Both the email_alert and text_alert function calls 
(line 266 and 267) in deviation_notifier.py are commented out for these reasons.