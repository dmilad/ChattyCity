ChattyCity
=========

Project description and goals: 

Our goal with this project was to look at tweet sentiment based on tweeter's location (source) and where they are tweeting about (destination). We hypothesize that there is a bias for or against certain cities based on where the tweeter is from. For example, most residents in Juneau, AL might have a positive sentiment about San Francisco, CA, but residents of Seattle, WA might generally have a negative sentiment toward SF. We could also look at whether sentiment changes based on a number of different variables such as day of week, time of the day, weather, or major events like sports. 

Tools:

We utilized a number of different tools for this project. For gathering, cleansing, and transforming the data, we mostly used Python and a number of different Python libraries. We chose python because we were all at least partially familiar with it and found it easy to work with.

For visualization, we used both Tableau and d3.js. We chose Tableau for the story-telling section because it gave us a lot of flexibility to experiment with the data quickly and look for interesting patterns (although later we came across some limitation, which are further explained in the Tableau section below). For the Explore section of the project, we chose to use d3.js because we needed a tool that gave us more control over the visualization. 

For building the search system, we used Apache Solr and AJAX Solr. We used Solr as an IR solution instead of other search engines (elasticsearch, endeca, etc.) because we wanted an open source solution with a lot of documentation that is used in production.

And finally for the design of the website, we used bootstrap.js.
