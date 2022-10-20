# Web Scraper for Competitior Price Monitoring

## Introduction
As a project relevant to both learning Python & working in digital advertising, I wanted to create a web scraper which could pull competitor product information.

There are follow-along projects for web scraping, but I wanted to make something that didn't have a predetermined solution & leveraged some of the Udemy & YouTube classes that I've been watching. Also, wanted to try some data engineering as part of this project as well. ;)

The project is seperated into four parts:

1. Creating the main script and dependencies for extracting product data
2. Adding relevant business & metadata (in this case, timestamps, product category
3. Creating a scheduler which would output to a database (thinking Google Cloud Platform would be best)
4. Creating dashboards using free software in order to visualise product trends & data over time

## Table of contents

[Technologies] (https://github.com/CSHv1/Python/edit/main/README.md) <br />
Modules Used <br />
Launch <br /> 
Illustrations <br />
Scope of Functionalities <br />
Examples of Use <br />
Project Status <br />
Sources <br />
Additional Information <br />

## Technologies
Code was written in Python (version at time of testing = Python 3.10).

## Modules Used

| Module          | Purpose        |
| --------------- |----------------|
| pandas          | DataFrame Creation |
| BeautifulSoup   | Parse HTML Content Pulled from 'requests' module |
| requests        | Pull HTML from Web Pages |
| time            | Create Timestamp for Temporal Data Creation |
| random          | Used for randomising User Agents |
| math            | Used for ceiling division in page pull logic |


## Launch

## Illustrations

## Scope of Functionalities

## Examples of Use

## Project Status

As of Oct 2022, stage 1 of the project is complete. There is a working combination of main.py and dependencies which all work to pull a csv with basic product info.  <br />

The next step in terms of developing my Web Scraping skills in Python would be to leverage some spiders, or Selenium.  <br />

These different methods would provide alternate functionality & would allow additional product information to be collated by scraping the individual product pages, rather than the predetermined category pages method which defines this solution.

## Sources
## Additional Information
