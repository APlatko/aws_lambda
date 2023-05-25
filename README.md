# aws_lambda

Lambda functions. Connections with api gateway and s3.

### 1. api_gateway_lambda

    - 'index.html' has AJAX script where user enter the website url. By clicking submit button, page make POST request 
      to AWS API gateway url.
    - API gateway has a model in 'method request' that checks if user entered any url into the form. 
      If check has succeeds it invokes lambda function.
    - Function parses the passed website with beautifulsoup, format the necessary data and return it in body response.
    - User see on the screen required data.

    *The 'python.zip' layer was created for lambda function. It consists of libraries: requests, beautifulsoup, html5lib.

### 2. restart_lambda_challenge

    This was a challenge lab from AWS re/Start program course.

    - Function is invoked when an object is loaded to s3 bucket.
    - If object is one of the text documents ('txt', 'doc', 'docx'), function count the number of words in the object.
    - Then function sends the number of words to email with the help of AWS SNS.
