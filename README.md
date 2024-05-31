# Project Name

World Wide Quiz Application

## Project Overview

Welcome to our trivia extravaganza! 🌍 Our project is like having your very own world tour guide, but with a twist – it's a quiz game! We'll whisk you away on a journey of geographical discovery, asking you quirky questions about countries from all corners of the globe. Ever wondered which currency belongs to which country or what's the capital of a place you've never heard of? We've got you covered!

But wait, there's more! 🎉 This isn't your run-of-the-mill quiz. We've spiced things up by giving you three tantalizing options for each question, only one of which is the correct answer. Think you can separate fact from fiction? Put your skills to the test!

Our mission? To educate, entertain, and elevate your trivia prowess to legendary status! 🏆 Whether you're a seasoned explorer or a geography newbie, there's something for everyone here. And hey, who doesn't love a bit of friendly competition? Compete against your friends and see who can claim the title of ultimate quiz champion!

Main Features:

- Geographical Trivia: Dive into a world of wacky questions about countries and their quirks.
- Multiple Choice Madness: We'll give you three options, but only one will lead you to victory!
- Web API Whimsy: We use web APIs to conjure up a never-ending stream of trivia, ensuring every game is a new adventure.
- Highscore Hijinks: Keep track of your triumphs and see if you've got what it takes to reach the top.
- Stats & Shenanigans: Dive into the data and uncover the secrets of your quiz prowess. Who knows, you might be the next trivia superstar!

So buckle up, fellow adventurer! It's time to embark on a journey of knowledge, laughter, and maybe a few eyebrow-raising moments. Let's make learning about the world as fun as a rollercoaster ride! 🎢

## Installation

[Provide detailed steps on how to install your project. Include any prerequisites, dependencies, or setup instructions.]

## Usage

**Instructions for Using the Application via Docker Commands:**

1. Download Docker Image:
docker pull lara283/flask-app

2. Start the Container:
docker run -d -p 80:80 lara283/flask-app

3. Access the Application:
Open http://localhost in your web browser to access the application

**Instructions for Using the Application via Docker Desktop:**
1. Launch Docker Desktop on your local computer
2. Search for the Docker image lara283/flask-app on Docker Hub
3. Click on the desired image and select "Pull"
4. Click on the downloaded image and select "Run"
5. Click on Optional settings and set Host port to 80
6. Click on Run
7. Open http://localhost in your web browser to access the application
8. Enter your Username and chase the highscore!

### country_code_data_utils.ipynb

The **`country_code_data_utils.ipynb`** notebook is a crucial component responsible for fetching, processing, and storing country code data retrieved from the XY API. This API supplies a list of countries, each identified by a unique code (e.g., 'CH' for Switzerland), which we store in our database for future reference.

#### Instructions:


3. **Fetching and Processing Data**: Once the 'drop table' code is commented again, run all cells to fetch and process the new data. Ensure all cells execute successfully.

#### Notes:
- The data processed within this notebook is utilized in other sections of the application, making its accurate processing crucial.
- Regularly check for updates from the XY API to ensure the database remains current.
