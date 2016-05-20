# Collecting daily sales data from Unicenta POS

This script has a nice story. The Singapore government hands out generous subsidies to SMEs, in the intention that small enterprises can reduce their startup costs. SMEs purchase certain services or equipment from some service providers and this is fully subsidised by the government up to a quantum of about $5,000 each. The subsidies go by many names -- ICV, PIC and what have you -- but what they all have in common is that they are quite liberally abused by service providers to provide a bare minimum of product at the highest possible premium.

Someone I know owns a retail shop, whose point-of-sales (POS) system fried its motherboard. The technical staff quoted her a price of $500 to replace it, basically tantamount to daylight robbery. I have friends who could build a pretty respectable system for that kind of price, or never mind my nerdy friends, you could buy a Chromebook for that much.  

After she decided not to replace the motherboard, this person commissioned me to find and implement a fix within 24 hours. The reason why there's such an urgent need for a fix is that the retail shop must report its takings to the shopping mall which then collects a cut of the gross turnover. The mall imposes a fine if we fail to report the takings electronically by the POS system. 

Luckily, there was another PC lying around in the shop that we could use, in addition to all the other working accessories such as the thermal printer, cash register and what have you. I had the idea of installing an open source POS system, and found a pretty respectable software called Unicenta (https://sourceforge.net/projects/unicentaopos/). 

## Setting up the rudimentary POS system

This is just a quick guide for anyone who might end up in our situation. 

The thermal receipt printer is an Asterix ST-EP4, and I was able to find a Windows driver for it. It works basically as any ordinary printer. For a while I was flummoxed about how to get it to open the cash register. But it turns out that the thermal printer has a *trigger* that can open the cash drawer either before or after a receipt is printed. There's an option in Windows' printer properties that allows you to change this setting. 

The setup of the Unicenta system is pretty straightforward. There are only two important differences from a standard setup: 

1. The setup defaults to using an Apache DB. To access the data with the script in this repository it is necessary to install MySQL. I first installed MySQL. I also used a utility called HeidiSQL, logged into my local SQL server and created a database for Unicenta (named `unicentaopos`) before running the Unicenta database configuration. 
2. In the setup of the accessories (Unicenta Configuration app), you must set the primary printer to the thermal receipt printer. If the receipt doesn't print then the cash register doesn't open. 

After this we just poked around to see how the system works, created a few products and printed a few receipts. It's not the most user friendly but at this point we were satisfied and relieved. 

## Setting up an environment to report daily sales

The mall has certain requirements for how we electronically report the data: 
* The file name is `storecode`.001 for the first transaction, .002 for the second, etc.
* The contents of each file is a continuous string `storecode``YYYYmmdd``transaction_value`.
* All the files are to be uploaded by FTP to the mall's central system. 

The Python script here queries the database directly, collects the individual transactions and then generates the files into a new (local) folder every day. Effectively this is a local backup. 

It then locates the files generated and uploads it via FTP to a secure location. The way I am storing the passwords is not safe, but I will figure something out later. 

Finally it tabulates the sales total and sends the shop owner an email. This is something the previous POS system used to do. I was not able to figure out how to access the name of the individual item purchased but this information will probably reveal itself one day. 

Once the script is tested, I set up an automated schedule to run this script at the end of the business day. The script can be set to be executable by setting the script to open with Python 2.7 binary by default. I was a bit surprised by how smoothly the scheduling went. I am very much a Mac and Linux person but I have to say Windows' task scheduler is a clear sight better than OS X's `launchd`. 
