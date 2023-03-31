import sys
import os
sys.path.append("TournamentData/")
from StartGGDataScraper import *

'''
startEventFile("9Moons","9moons-weekly-29-guilty-gear-strive-new-patch-edition","rr-to-bracket","6.11.22")
addEventResults("9Moons","9moons-weekly-30-guilty-gear-strive-1","rr-to-bracket","6.18.22")
addEventResults("9Moons","9moons-monthly-10-guilty-gear-strive-double-elim-bracket-only-1","double-elimination-bracket","6.25.22")
addEventResults("9Moons","9moons-weekly-31-guilty-gear-strive","rr-to-bracket","7.9.22")
addEventResults("9Moons","9moons-weekly-32-guilty-gear-strive","rr-to-bracket","7.16.22")
addEventResults("9Moons","9moons-monthly-11-guilty-gear-strive","double-elimination-bracket","8.13.22")
addEventResults("9Moons","9moons-weekly-33-guilty-gear-strive","double-elimination-bracket","8.20.22")
addEventResults("9Moons","9moons-weekly-34-guilty-gear-strive","double-elimination-bracket","8.27.22")
addEventResults("9Moons","9moons-weekly-35-guilty-gear-strive","double-elimination-bracket","9.3.22")
addEventResults("9Moons","9moons-weekly-36-guilty-gear-strive","double-elimination-bracket","9.10.22")
addEventResults("9Moons","9moons-monthly-12-guilty-gear-strive","double-elimination-bracket","9.17.22")
addEventResults("9Moons","9moons-weekly-37-guilty-gear-strive","double-elimination-bracket","9.24.22")
addEventResults("9Moons","9moons-weekly-38-guilty-gear-strive","double-elimination-bracket","10.1.22")
addEventResults("9Moons","9moons-monthly-13-guilty-gear-strive","double-elimination-bracket","10.8.22")
#addEventResults("9Moons","9moons-weekly-39-make-or-break-qualifier-event","double-elimination-bracket","10.22.22") #Not filled out for top 8, so its excluded
addEventResults("9Moons","9moons-weekly-40-make-or-break-week-2-qualifier","double-elimination-bracket","10.29.22")
addEventResults("9Moons","9moons-weekly-41-make-or-break-final-qualifier","double-elimination-bracket","11.5.22")
addEventResults("9Moons","9moons-weekly-42-guilty-gear-strive","double-elimination-bracket","11.19.22")
addEventResults("9Moons","9moons-weekly-43-guilty-gear-strive","double-elimination-bracket","11.26.22")
addEventResults("9Moons","9moons-monthly-14-300-prize-pool","double-elimination-bracket","12.3.22")
addEventResults("9Moons","9moons-weekly-44-new-patch-tourney","double-elimination-bracket","12.17.22")
addEventResults("9Moons","9moons-monthly-15-benefitting-the-ablegamers-charity","double-elimination-bracket","1.7.23")
addEventResults("9Moons","9moons-weekly-45-crossplay","double-elimination-bracket","1.14.23")
addEventResults("9Moons","9moons-weekly-46-crossplay","double-elimination-bracket","1.21.23")
addEventResults("9Moons","9moons-weekly-47-crossplay","double-elimination-bracket","1.28.23")
addEventResults("9Moons","9moons-monthly-16-benefitting-the-ablegamers-charity-crossplay","double-elimination-bracket","2.11.23")
addEventResults("9Moons","9moons-weekly-48-crossplay-1","double-elimination-bracket","2.25.23")
addEventResults("9Moons","9moons-weekly-48-crossplay","double-elimination-bracket","3.4.23")
addEventResults("9Moons","9moons-weekly-50-crossplay","double-elimination-bracket","3.18.23")
addEventResults("9Moons","9moons-monthly-17-crossplay","double-elimination-bracket","3.25.23")
'''

'''
startSets("9Moons","9moons-weekly-29-guilty-gear-strive-new-patch-edition","rr-to-bracket","6.11.22")
addSets("9Moons","9moons-weekly-30-guilty-gear-strive-1","rr-to-bracket","6.18.22")
addSets("9Moons","9moons-monthly-10-guilty-gear-strive-double-elim-bracket-only-1","double-elimination-bracket","6.25.22")
addSets("9Moons","9moons-weekly-31-guilty-gear-strive","rr-to-bracket","7.9.22")
addSets("9Moons","9moons-weekly-32-guilty-gear-strive","rr-to-bracket","7.16.22")
addSets("9Moons","9moons-monthly-11-guilty-gear-strive","double-elimination-bracket","8.13.22")
addSets("9Moons","9moons-weekly-33-guilty-gear-strive","double-elimination-bracket","8.20.22")
addSets("9Moons","9moons-weekly-34-guilty-gear-strive","double-elimination-bracket","8.27.22")
addSets("9Moons","9moons-weekly-35-guilty-gear-strive","double-elimination-bracket","9.3.22")
addSets("9Moons","9moons-weekly-36-guilty-gear-strive","double-elimination-bracket","9.10.22")
addSets("9Moons","9moons-monthly-12-guilty-gear-strive","double-elimination-bracket","9.17.22")
addSets("9Moons","9moons-weekly-37-guilty-gear-strive","double-elimination-bracket","9.24.22")
addSets("9Moons","9moons-weekly-38-guilty-gear-strive","double-elimination-bracket","10.1.22")
addSets("9Moons","9moons-monthly-13-guilty-gear-strive","double-elimination-bracket","10.8.22")
addSets("9Moons","9moons-weekly-39-make-or-break-qualifier-event","double-elimination-bracket","10.22.22") #Not filled out for top 8, so its excluded
addSets("9Moons","9moons-weekly-40-make-or-break-week-2-qualifier","double-elimination-bracket","10.29.22")
addSets("9Moons","9moons-weekly-41-make-or-break-final-qualifier","double-elimination-bracket","11.5.22")
addSets("9Moons","9moons-weekly-42-guilty-gear-strive","double-elimination-bracket","11.19.22")
addSets("9Moons","9moons-weekly-43-guilty-gear-strive","double-elimination-bracket","11.26.22")
addSets("9Moons","9moons-monthly-14-300-prize-pool","double-elimination-bracket","12.3.22")
addSets("9Moons","9moons-weekly-44-new-patch-tourney","double-elimination-bracket","12.17.22")
addSets("9Moons","9moons-monthly-15-benefitting-the-ablegamers-charity","double-elimination-bracket","1.7.23")
addSets("9Moons","9moons-weekly-45-crossplay","double-elimination-bracket","1.14.23")
addSets("9Moons","9moons-weekly-46-crossplay","double-elimination-bracket","1.21.23")
addSets("9Moons","9moons-weekly-47-crossplay","double-elimination-bracket","1.28.23")
addSets("9Moons","9moons-monthly-16-benefitting-the-ablegamers-charity-crossplay","double-elimination-bracket","2.11.23")
addSets("9Moons","9moons-weekly-48-crossplay-1","double-elimination-bracket","2.25.23")
addSets("9Moons","9moons-weekly-48-crossplay","double-elimination-bracket","3.4.23")
addSets("9Moons","9moons-weekly-50-crossplay","double-elimination-bracket","3.18.23")
addSets("9Moons","9moons-monthly-17-crossplay","double-elimination-bracket","3.25.23")
'''
#print(playerMatchHistory("Vera Caelestis","TournamentData/9Moons/9MoonsSets.txt"))
#print(playerRecords("Vera Caelestis","TournamentData/9Moons/9MoonsSets.txt"))