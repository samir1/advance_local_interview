# Advance Local Interview

## How to Run
`chalice deploy` or `chalice local`

how to run your code, how the code works and how you approached the exercise.

## Goals
1. **API status.** Define "status" as you will. This can be as simple as "OK", or could return more info such as: the time, information about the server and processes, performance profiling, etc.

   `https://[rest_api_id].execute-api.us-east-1.amazonaws.com/api/status`  
   This is a simple route that returns Returns the "status" as "OK" and the current time.

2. **Transform publicly available data into something fun.** A good list of free JSON APIs is available
here: https://github.com/toddmotto/public-apis but you can use any API you like as long as it is freely available to us when it comes time to check your work.

   `https://[rest_api_id].execute-api.us-east-1.amazonaws.com/api/news_for_state`  
   Using The Guardian API, this endpoint returns the top articles for a random state.

   `https://[rest_api_id].execute-api.us-east-1.amazonaws.com/api/news_for_state/{state}`  
   Using The Guardian API, this endpoint returns the top articles for a given state. `{state}` can also be "random" for a random state.

3. **Upload a PNG image to S3** and return the address of an HTML resource hosted on S3 that has at least that image on it.

   Upload file.png:  
   `curl --header "Content-Type:image/png" --data-binary @file.png -X POST https://[rest_api_id].execute-api.us-east-1.amazonaws.com/api/upload_png`

   This endpoint accepts a PNG file and uploads it to an S3 bucket. Next, the script reads a template html file and replaces a placeholder with the URL for the image. Lastly, it returns a link to the HTML file with the image on it.