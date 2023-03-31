import sys
import os
sys.path.append("TournamentData/")
from StartGGDataScraper import *

#Placment Pulls
'''
startEventFile("CLG","run-it-thursdays-2-guilty-gear-strive","guilty-gear-strive-west-coast-top-8","7.14.22")
addEventResults("CLG","run-it-thursdays-4-guilty-gear-strive","guilty-gear-strive-east-coast-ladder-pc","7.28.22")
addEventResults("CLG","run-it-thursdays-4-guilty-gear-strive","guilty-gear-strive-west-coast-ladder-pc","7.28.22")
addEventResults("CLG","run-it-thursdays-9-guilty-gear-strive","guilty-gear-strive-east-coast-ladder-pc","9.8.22")
addEventResults("CLG","run-it-thursdays-9-guilty-gear-strive","guilty-gear-strive-west-coast-ladder-pc","9.8.22")
addEventResults("CLG","run-it-thursdays-12-guilty-gear-strive","guilty-gear-strive-east-coast-ladder-pc","9.29.22")
addEventResults("CLG","run-it-thursdays-12-guilty-gear-strive","guilty-gear-strive-west-coast-ladder-pc","9.29.22")
addEventResults("CLG","run-it-thursdays-14-guilty-gear-strive","guilty-gear-strive-east-coast-ladder-pc","10.13.22")
addEventResults("CLG","run-it-thursdays-14-guilty-gear-strive","guilty-gear-strive-west-coast-ladder-pc","10.13.22")
addEventResults("CLG","run-it-thursdays-19-guilty-gear-strive","guilty-gear-strive-east-coast-ladder-pc","11.17.22")
addEventResults("CLG","run-it-thursdays-19-guilty-gear-strive","guilty-gear-strive-west-coast-ladder-pc","11.17.22")
addEventResults("CLG","run-it-thursdays-21-guilty-gear-strive","guilty-gear-strive-east-coast-ladder-pc","12.8.22")
addEventResults("CLG","run-it-thursdays-21-guilty-gear-strive","guilty-gear-strive-west-coast-ladder-pc","12.8.22")
addEventResults("CLG","run-it-thursdays-23-guilty-gear-strive","guilty-gear-strive-east-coast-ladder-crossplay","12.22.22")
addEventResults("CLG","run-it-thursdays-23-guilty-gear-strive","guilty-gear-strive-west-coast-ladder-crossplay","12.22.22")
addEventResults("CLG","run-it-thursdays-24-guilty-gear-strive","guilty-gear-strive-east-coast-ladder-crossplay","1.5.23")
addEventResults("CLG","run-it-thursdays-24-guilty-gear-strive","guilty-gear-strive-west-coast-ladder-crossplay","1.5.23")
addEventResults("CLG","run-it-thursdays-27-guilty-gear-strive","guilty-gear-strive-east-coast-ladder-crossplay","1.26.23")
addEventResults("CLG","run-it-thursdays-27-guilty-gear-strive","guilty-gear-strive-west-coast-ladder-crossplay","1.26.23")
addEventResults("CLG","run-it-thursdays-30-guilty-gear-strive","guilty-gear-strive-east-coast-ladder-crossplay","2.16.23")
addEventResults("CLG","run-it-thursdays-30-guilty-gear-strive","guilty-gear-strive-west-coast-ladder-crossplay","2.16.23")
addEventResults("CLG","run-it-thursdays-32-guilty-gear-strive","guilty-gear-strive-east-coast-ladder-crossplay","3.2.23")
addEventResults("CLG","run-it-thursdays-32-guilty-gear-strive","guilty-gear-strive-west-coast-ladder-crossplay","3.2.23")
'''

#Set Pulls
'''
startSets("CLG","run-it-thursdays-2-guilty-gear-strive","guilty-gear-strive-west-coast-top-8","7.14.22")
addSets("CLG","run-it-thursdays-4-guilty-gear-strive","guilty-gear-strive-east-coast-ladder-pc","7.28.22")
addSets("CLG","run-it-thursdays-4-guilty-gear-strive","guilty-gear-strive-west-coast-ladder-pc","7.28.22")
addSets("CLG","run-it-thursdays-9-guilty-gear-strive","guilty-gear-strive-east-coast-ladder-pc","9.8.22")
addSets("CLG","run-it-thursdays-9-guilty-gear-strive","guilty-gear-strive-west-coast-ladder-pc","9.8.22")
addSets("CLG","run-it-thursdays-12-guilty-gear-strive","guilty-gear-strive-east-coast-ladder-pc","9.29.22")
addSets("CLG","run-it-thursdays-12-guilty-gear-strive","guilty-gear-strive-west-coast-ladder-pc","9.29.22")
addSets("CLG","run-it-thursdays-14-guilty-gear-strive","guilty-gear-strive-east-coast-ladder-pc","10.13.22")
addSets("CLG","run-it-thursdays-14-guilty-gear-strive","guilty-gear-strive-west-coast-ladder-pc","10.13.22")
addSets("CLG","run-it-thursdays-19-guilty-gear-strive","guilty-gear-strive-east-coast-ladder-pc","11.17.22")
addSets("CLG","run-it-thursdays-19-guilty-gear-strive","guilty-gear-strive-west-coast-ladder-pc","11.17.22")
addSets("CLG","run-it-thursdays-21-guilty-gear-strive","guilty-gear-strive-east-coast-ladder-pc","12.8.22")
addSets("CLG","run-it-thursdays-21-guilty-gear-strive","guilty-gear-strive-west-coast-ladder-pc","12.8.22")
addSets("CLG","run-it-thursdays-23-guilty-gear-strive","guilty-gear-strive-east-coast-ladder-crossplay","12.22.22")
addSets("CLG","run-it-thursdays-23-guilty-gear-strive","guilty-gear-strive-west-coast-ladder-crossplay","12.22.22")
addSets("CLG","run-it-thursdays-24-guilty-gear-strive","guilty-gear-strive-east-coast-ladder-crossplay","1.5.23")
addSets("CLG","run-it-thursdays-24-guilty-gear-strive","guilty-gear-strive-west-coast-ladder-crossplay","1.5.23")
addSets("CLG","run-it-thursdays-27-guilty-gear-strive","guilty-gear-strive-east-coast-ladder-crossplay","1.26.23")
addSets("CLG","run-it-thursdays-27-guilty-gear-strive","guilty-gear-strive-west-coast-ladder-crossplay","1.26.23")
addSets("CLG","run-it-thursdays-30-guilty-gear-strive","guilty-gear-strive-east-coast-ladder-crossplay","2.16.23")
addSets("CLG","run-it-thursdays-30-guilty-gear-strive","guilty-gear-strive-west-coast-ladder-crossplay","2.16.23")
addSets("CLG","run-it-thursdays-32-guilty-gear-strive","guilty-gear-strive-east-coast-ladder-crossplay","3.2.23")
addSets("CLG","run-it-thursdays-32-guilty-gear-strive","guilty-gear-strive-west-coast-ladder-crossplay","3.2.23")
'''

#print(playerMatchHistory("Vera Caelestis","TournamentData/CLG/CLGSets.txt"))
#print(playerRecords("Vera Caelestis","TournamentData/CLG/CLGSets.txt"))