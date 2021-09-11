# Discord.py
A discord bot with a leveling system (like mee6)

## Pre-requisites

- Knowing how to get create an app/bot via discord's developer portal.

Website: ```https://discord.com/developers/docs/intro```

- A MongoDB account (that's what's used as a database)

If you don't have an account then you can simply head over to [this website.](https://account.mongodb.com/)

Follow the following steps once you sign up for an account/sign in with your Gmail account (preferred):

1. Name your organisation (can be anything), name your project, and select python as your preferred language.
2. Select shared cluser on the following page.
3. Next will be the server location, which can be anything. It's better if you leave it be. Change your cluster name to something more suitable and finish setting it up.

Once you're on the main MongoDB page. You'll have to wait for it to create a cluster. If it doesn't do that by itself then click on **create a cluster** and wait for it to be ready. After the cluster is ready, click **connect** and do the following:

1. Enable **select access from anywhere**.
2. On the next page, create a database user. You can use **any** username and password.
3. Once you're done with those, click **connect your application** and copy the link that it gives you (the **Add your connection string into your application code** one)
4. Paste it to a notepad and proceed with setting up.

On your MongoDB's main page, head over to **Collections** and select **Add My Own Data**. Name your database and the collection name.


## Installation (dependencies)

Run the following commands on your terminal to install the dependencies;-

```pip install disord```

```pip install pymongo```

```pip install dnspython```

Next, clone the repository using ```git clone https://www.github.com/Sitiaro/Discord.py```

### Note

Once you're done with all those steps, head over to levels.py in your IDE and read the comments bc you'll have to make a few changes there to make it work.

## Execution

Once you're changed those things, add the bot to your server (refer to the developer portal documentation if you don't know how to) and run the bot using-

```python discord.py```


Enjoy <3


**Ps. You can start a discussion if you face any difficulties and I'll try getting back ASAP, thanks.**
