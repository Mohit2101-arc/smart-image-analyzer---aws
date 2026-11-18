# Smart Image Analyzer Using AWS

A web application that analyzes an uploaded photo using Amazon Rekognition. It detects objects, reads text, analyzes faces and checks whether the image is safe.

Built for the **Cloud Computing: Tool Explorer** assignment using **Amazon Web Services (AWS)**.

## Features
- Upload a JPG or PNG photo (under 3 MB) by clicking or drag and drop
- **Objects:** labels with confidence scores (for example Strawberry 100%)
- **Text:** reads text found in the image
- **Faces:** age range, emotion, smile and glasses
- **Safety:** flags unsafe or inappropriate content
- No server to manage

## AWS Services Used
| Service | Purpose |
|---|---|
| Amazon S3 | Hosts the web page (static website hosting) |
| AWS Lambda | Python function that sends the image to Rekognition |
| Amazon Rekognition | AI service that analyzes the image |
| AWS IAM | Gives Lambda permission to use Rekognition |
| Lambda Function URL | Web address the page uses to call Lambda |

## Architecture
```
Browser (page hosted on S3)
        |
        v
Lambda Function URL
        |
        v
AWS Lambda (Python)
        |
        v
Amazon Rekognition
        |
        v
Results shown on the page
```

## Files
- `index.html`: front end (HTML, CSS and JavaScript)
- `lambda_function.py`: Lambda function code

## Setup
1. Create an AWS account (Free plan).
2. Create an S3 bucket, turn off Block Public Access, enable static website hosting with `index.html` as the index document, and add a bucket policy that allows public `s3:GetObject`.
3. Create a Lambda function (Python 3.12) and paste in `lambda_function.py`. Set the timeout to 30 seconds.
4. Attach the `AmazonRekognitionReadOnlyAccess` policy to the Lambda execution role in IAM.
5. Create a Function URL for the Lambda function with auth type `NONE` and CORS enabled.
6. In `index.html`, replace `PASTE_YOUR_FUNCTION_URL_HERE` with your Function URL.
7. Upload `index.html` to the S3 bucket and open the bucket website endpoint.

## How It Works
1. The user selects a photo on the web page.
2. The page converts the photo to base64 and sends it to the Lambda Function URL.
3. Lambda decodes the image and calls Rekognition (labels, text, faces and moderation).
4. Lambda returns the results as JSON.
5. The page displays the results in tabs.

## Real-World Applications
- Photo moderation on social media
- Vehicle counting and number plate reading in traffic monitoring
- Face verification for attendance and security
- Automatic photo tagging and search

## Limitations
- Results are probabilities and can be wrong
- Images must be under 3 MB
- This is a demo project, not a production system

## Note
The Function URL in `index.html` is a placeholder. Use your own URL when deploying.
