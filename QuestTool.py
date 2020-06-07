import sys
import json
from hiscores import Hiscores

"""
CONSTANTS
Output Key
Green = Doable
Blue = boostable
Red = unboostable and not doable
"""


class QuestTool(object):
    account = 0
    account_name = ''
    quest_points = 0
    combat_level = 0
    quest_data = {}

    def __init__(self, *args):
        data_file = "./questData.json"

        with open(data_file) as json_file:
            self.quest_data = json.load(json_file)
        self.account_name = args[0] if len(
            args) > 0 else Hiscores('jimbo jango')
        self.account = Hiscores(args[0]) if len(
            args) > 0 else Hiscores('jimbo jango')
        self.quest_points = args[1] if len(args) > 1 else 325
        self.combat_level = self.getCBLvl(self.account)

    def getDoableQuests(self):
        '''
        Checks each quest to see if you are able to do it.
        '''
        doable = {}
        for i in self.quest_data:
            if self.meetsRequirements(i):
                doable.update({i: True})
        return doable

    '''
    Returns a dictionary with skills and quests with their respective requirements that are required for completing the quest passed in the argument.
    Returns a dictionary object relating to the quest.
    Recursively calls itself.
    '''

    def getRequirements(self, quest_name):

        cur_quest = self.quest_data[quest_name]

        has_all_level_reqs = True

        quest_incomplete_dict = {'skills': {},
                                 'quests': {}}
        if 'levels' in cur_quest['requirements']:
            for i in cur_quest['requirements']['levels']:

                temp_dict = {}

                if i['skill'] == 'quest':
                    temp_dict.update({i['skill']: i['level'], "quest":
                                      self.quest_points})

                elif i['skill'] == 'combat':
                    temp_dict.update({i['skill']: i['level'], "combat":
                                      self.combat_level})
                else:
                    temp_dict.update({i['skill']: i['level']})

                quest_incomplete_dict['skills'].update(temp_dict)

        if 'quests' in cur_quest['requirements']:
            for i in cur_quest['requirements']['quests']:

                temp_dict = {}
                other_quest = self.getRequirements(i)
                temp_dict.update({i: other_quest})
                quest_incomplete_dict['quests'].update(temp_dict)
        return quest_incomplete_dict

    '''
    Checks the requirements for the quest and if it's possible for the account.
    Returns a Boolean if the quest is possible to complete or not (False or True)
    '''

    def meetsRequirements(self, quest_name):

        if 'subquest of Recipe for Disaster' in quest_name:
            # TODO
            # Pirate Pete Subquest of Recipe for Disaster
            return True
        cur_quest = self.quest_data[quest_name]

        has_all_level_reqs = True
        boost = False
        if "levels" in cur_quest['requirements']:
            for i in cur_quest['requirements']['levels']:
                # if your combat quest points are greater than required
                if i['skill'] == 'quest':
                    if self.quest_points < i['level']:
                        # if you have less than the amount of quest oints required
                        has_all_level_reqs = False

                elif i['skill'] == 'combat':

                    if self.combat_level < i['level']:
                        # if you have a combat level lower than the one required
                        has_all_level_reqs = False
                elif self.account.skills[i['skill']].level >= i['level']:
                    # If you have a level higher than the one required
                    pass
                elif (self.account.skills[i['skill']].level - i['level'] <= 5) and i['boostable'] == True:
                    # If the skill is boostable and the boost is within 5 levels of yours
                    boost = True
                    pass
                else:
                    # print(account.skills[i['skill']].level, " < ", i['level'])
                    has_all_level_reqs = False

        if "quests" in cur_quest['requirements']:
            for i in cur_quest['requirements']['quests']:
                if 'Started ' in i:
                    # Incase quests are formally named with "started" Legend's quests etc...
                    # You have to have the requirements of that quest to start it as well
                    i = i.split('Started ')[1]

                # Recursively calls itself for each quest that is required to complete the current quest.
                if self.meetsRequirements(i) == False:
                    has_all_level_reqs = False
        return has_all_level_reqs

    def getCBLvl(self, acc):
        x = [0.325*(acc.skills['attack'].level + acc.skills['strength'].level), 0.325 *
             (int(3 * acc.skills['ranged'].level / 2)), 0.325*(int(3 * acc.skills['magic'].level / 2))]
        x.sort()

        return int(0.25 * (acc.skills['defence'].level +
                           acc.skills['hitpoints'].level + (acc.skills['prayer'].level/2)) + x[-1])

    def help(self):
        return '-- Your python file can contain a simple configuration like so: --\nfrom quest_checker import QuestTool \nqc = QuestTool(\'jimbo jango\', 300) \nqc.meetsRequirements(\'Regicide\')'

    def __str__(self):
        return 'QuestTool object associated to the account: ' + str(self.account_name) + '\n' +\
            'Account Quest Points: ' + str(self.quest_points) + '\n' +\
            'Account Combat Level: ' + str(self.combat_level)

    def __repr__(self):
        return super().__str__()
