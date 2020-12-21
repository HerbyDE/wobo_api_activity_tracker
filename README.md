# wobo_api_activity_tracker
This app is an extension that allows a user to fetch OKR metrics and insights from Workboard's RESTful API. All that's required is a valid user account and an associated API key.

The ideas was to fetch all available metrics and make them available for custom evaluations and analyses, which turned out to be useful for a number of clients.
As of now the project allows to extract data either in the native JSON format or as an Excel Workbook. This may be used within PowerBI for easy custom insights.
A simple tweak would also allow to stream the data directly into PowerBI if the Django application is deployed on a server. In this case, MAKE SURE TO GENERATE A NEW SECRET KEY and optimally use environment variables.
