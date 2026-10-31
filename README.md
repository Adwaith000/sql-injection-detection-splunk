# SQL Injection Detection Using Splunk SIEM

A cybersecurity lab project demonstrating the detection and monitoring of SQL Injection attacks using a vulnerable Python Flask web application, SQLite, Splunk Enterprise, and Splunk Universal Forwarder.

## Project Overview

This project demonstrates:

- Creation of a deliberately vulnerable Flask web application
- Simulation of SQL Injection login bypass
- Application log generation
- Forwarding logs to Splunk Enterprise
- Detection of suspicious SQL Injection patterns using SPL
- Dashboard-based visualization and monitoring
- Real-time alerting through email
- Supplementary Telegram notification
- Mitigation using parameterized SQL queries

> **Lab only:** The web application in this repository is intentionally vulnerable. Run it only in an isolated lab environment and never expose it to the public internet.

## Environment

| System | Purpose |
|---|---|
| Windows | Splunk Enterprise |
| Ubuntu | Vulnerable web application + Splunk Universal Forwarder |

## Technologies

- Python 3
- Flask
- SQLite
- Splunk Enterprise
- Splunk Universal Forwarder
- SPL
- Linux / Ubuntu
- Windows

## Project Architecture

```text
User / Attacker
       |
       v
Vulnerable Flask Application
       |
       v
   flask.log
       |
       v
Splunk Universal Forwarder
       |
       v
Splunk Enterprise
       |
       +----> SPL Detection
       |
       +----> Dashboard
       |
       +----> Email Alert
       |
       +----> Telegram Notification
```

## Vulnerable Application

The application intentionally builds an SQL query by directly inserting username and password input:

```python
q = f"SELECT * FROM users WHERE username='{u}' AND password='{p}'"
r = db.execute(q).fetchone()
```

This is included only for controlled security testing.

## SQL Injection Simulation

The project documentation demonstrates a login-bypass test using a crafted username containing a SQL comment sequence.

Example lab input:

```text
Username: admin' --
Password: anything
```

The documented result was a successful login bypass in the intentionally vulnerable application.

## Log Collection

The Flask application generates login-attempt logs. The Splunk Universal Forwarder monitors the log file and forwards events to Splunk Enterprise.

Example monitoring command used in the lab:

```bash
/opt/splunkforwarder/bin/splunk add monitor /home/vboxuser/sql_lab/flask.log
/opt/splunkforwarder/bin/splunk restart
```

Replace the path with your own lab path.

## SQL Injection Detection

Detection query used in the project:

```spl
index=* sourcetype=flask ("--" OR "' OR" OR "1=1")
```

Enumeration query documented in the project:

```spl
source="flask.log" ("--" OR "' OR" OR "1=1")
```

These searches identify suspicious patterns in the application logs.

## Alerting

The project configured a Splunk alert with:

- Trigger condition: number of results > 0
- Time range: last 1 minute
- Email notification
- Optional Telegram notification

**Do not commit Gmail passwords, app passwords, Telegram bot tokens, webhook URLs, or other secrets to GitHub.**

## Mitigation

The vulnerable SQL query was replaced with a parameterized query:

```python
q = "SELECT * FROM users WHERE username=? AND password=?"
r = db.execute(q, (u, p)).fetchone()
```

The project documentation reports that the SQL Injection attempt then failed after the parameterized query was implemented.

## Repository Structure

```text
sql-injection-detection-splunk/
├── README.md
├── vulnerable-app/
│   ├── app.py
│   ├── requirements.txt
│   ├── templates/
│   │   ├── login.html
│   │   └── dashboard.html
│   └── static/
│       └── style.css
├── splunk/
│   └── detection-queries.spl
├── screenshots/
├── documentation/
│   └── SIEM-PROJECT.pdf
├── .gitignore
└── LICENSE
```

## Results

The project demonstrated:

1. SQL Injection activity generated against the lab application.
2. Login attempts captured in application logs.
3. Logs forwarded to Splunk Enterprise.
4. Suspicious SQL Injection patterns identified through SPL.
5. Detection visualized in a Splunk dashboard.
6. Alerts triggered for detected activity.
7. Real-time email notification and supplementary Telegram notification.
8. The vulnerability mitigated using parameterized queries.

## Disclaimer

This repository is for educational and authorized security-testing purposes only. Do not use the vulnerable application against systems you do not own or have explicit permission to test.
