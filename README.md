# boxing_scraper
 A small project to gather data from boxrec, boxing's leading website for data on boxer's bout history.
 
 The project has scripts to obtain url's from the website for the top 50 boxers in each weight category,
 before other scripts will gather intended data from the respective pages of each boxer.
 
 Data is saved in a CSV format.
 To evade bans on the website, the scrapingbee was used to rotate residential proxies.
 
 Note: boxer's ratings are constantly updated and so a timestamp of the scraped data would be useful in analysis
# Future plans
 Likely will be scraping individual bout data per boxer, i.e Oleksandry Usyk's individual fights by opponent, method of victory, venue, etc.
 Further, would like to obtain CompuBox or Jabbr data to record the boxer's punch statistics in their respective bouts.
