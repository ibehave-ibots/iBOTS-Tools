# Zoom attendance register

[![Run tests](https://github.com/ibehave-ibots/course-attendance-service/actions/workflows/run-tests.yml/badge.svg)](https://github.com/ibehave-ibots/course-attendance-service/actions/workflows/run-tests.yml)

## Generate access token
1. Ensure that you have set the required environment variables (`ACCOUNT_ID`,`CLIENT_ID`,`CLIENT_SECRET`) in your .env file
2. Call the `create_access_token` function from `zoom_integration` module to obtain access token
3. Use the returned access token for further API calls to authenticate with ZOOM API

### Example

```python
response = create_access_token()
access_token = response['access_token']
```
## List groups
1. Obtain an access token through the authentication process.
2. Run the get_group_details function separately to identify the group ID and retrieve details of the Zoom groups.
3. Add the retrieved group ID to the .env file as GROUP_ID for further use in your application.

**NOTE** Before running the function, ensure that you have set the required access token in the access_token variable. This function is intended to be run separately to identify the group ID and obtain the group details. Once you have the group ID, add it to the .env file as GROUP_ID for use in other parts of your application.

### Example
```python
response = get_groups(access_token)
```

## List group members

1. Obtain an access token through the authentication process.
2. Set the environment variable GROUP_ID to the desired Zoom group ID.
3. Run the get_group_members function to retrieve the members of the Zoom group associated with the specified group ID.

**NOTE** Before running the function, ensure that you have set the required access token in the access_token variable. This function is intended to be run separately to identify the group ID and obtain the group details. Once you have the user ID, add it to the .env file as USER_ID for use in other parts of your application.

### Example
```python
access_token = "your-access-token"
response = get_group_members(access_token)
```

## List member meetings

1. Obtain an access token through the authentication process.
2. Set the environment variable USER_ID to the desired Zoom member's user ID.
3. Run the get_meetings_of_member function to retrieve themeetings of the Zoom member associated with the specified user ID.

### Example
```python
access_token = "your-access-token"
response = get_meetings_of_member(access_token, from_date='2023-01-01', to_date='2023-12-31')
```

## Get participant details of a meeting
1. Obtain an access token through the authentication process.
2. Identify the meeting ID for which you want to retrieve the participant report.
3. Run the get_participant_report function, passing the access token and meeting ID as arguments, to retrieve the participant report for the specified Zoom meeting.

### Example
```python
access_token = "your-access-token"
meeting_id = "your-meeting-id". It can be integer value or a uuid string.
response = get_participant_report(access_token, meeting_id)
```

## Get attendance 
1. Generate a Zoom meeting report using the zoom_integration.get_participant_report() module.
2. Pass the meeting report to the get_attendance function.
3. The function will extract the names and durations of participants who were marked as 'in_meeting'.
4. The attendance details will be returned as a dictionary, which you can further process or use as needed.

### Example

```python
meeting_report = {
    'participants': [
        {
            'name': 'John Doe',
            'status': 'in_meeting',
            'duration': 1800
        },
        {
            'name': 'Jane Smith',
            'status': 'in_meeting',
            'duration': 2400
        },
        {
            'name': 'Alice Johnson',
            'status': 'not_in_meeting',
            'duration': 0
        }
    ]
}
attendance = get_attendance(meeting_report)
```