# CloudfrontToElasticSearch
This is a AWS Lambda Function to get logs from Cloudfront stored in S3 and send it to an Elasticsearch domain so that we can search for anything whenever we want to and maybe use Elasticsearch Machine Learning to create a better product for your customers or even to understand and automate your own infrastructure in a better way.

-If you want this code to work, you probably already created your Elasticsearch domain using Elasticsearch Service. (If not, I'll put some guide here in the future)

-You'll need a Bucket to put your logs from Cloudfront to S3.

-You'll need permission to edit a Cloudfront Distribution, Create a Lambda Function and maybe others that I'm forgetting.

#1. Enable Logs on your Cloudfront Distribution
Go to your Distribution click on Edit and configure the S3 bucket for logs. 

#2. Create a Lambda function
Go to Lambda console, click on Create Function -> Author from scratch. 
Choose python 2.7 as scripting language.
In the Triggers section of the Lambda you've created, choose S3 Bucket and configure:
Suffix: gz
Prefix: cloudfront/
Event type: ObjectCreated

This means that when someone (like cloudfront) put a new file to S3 bucket inside of the /cloudfront folder, if the content has the extension ".gz" (like cloudfront logs) it will trigger this function.

#3. Change the Elasticsearch domain 
Go to the code you've cloned and change the 155 line, which has to be your Elasticsearch domain. (For this demo, mine was configured public, I'll not get in permissions to access Elasticsearch domain).

Finish. Don't forget enabling your trigger.

You can see if it's everything working well in your Monitoring tab of the Lambda function.

To see the results and do your queries, I encourage you to use Kibana. If you're using Elasticsearch Service, there's a link to direct send you to the Kibana Page of your Domain. If you need some help with queries, don't be afraid of asking me!

