from .name_generator import NameGenerator
from . import abilities
from . import animalsubtypes
from . import skills
from . import animaltypes
import math


class Character:
    abilities = abilities.CharacterAbilities()

    def __init__(self, name=None, animaltype=None, animalsubtype=None, level=1, build_points=10, skills=[], status=[], temp_status=[], erfahrung=0, stealth=False, savers=False):
        self.name = name
        self.animaltype = animaltype
        self.animalsubtype = animalsubtype
        self.level = level
        self.build_points = build_points
        self.skills = skills
        self.update_Skills(self.skills)
        self.status = status
        self.temp_status = temp_status
        self.erfahrung = erfahrung
        self.stealth = stealth
        self.savers = savers

    def exp_needed_for_Level_Up(self):
        constant = 40
        exp_needed = int(round((constant * self.level) * math.sqrt(constant)))
        return exp_needed

    def level_up_check(self):
        if self.get_experience() >= self.exp_needed_for_Level_Up():
            self.LevelUp()

    def get_experience(self):
        return self.erfahrung

    def gain_experience(self, amount):
        self.erfahrung += amount
        self.level_up_check()

    def get_status_max(self, input_string):
        # Gesundheit
        if input_string == 'health':
            return self.status[0]
        # Ausdauer
        elif input_string == 'endu':
            return self.status[1]
        # Magie
        elif input_string == "magic":
            return self.status[2]

    def set_stealth_mode(self, Bool):
        self.stealth = Bool

    def get_stealth_mode(self):
        return self.stealth

    def set_savers_mode(self, Bool):
        self.savers = Bool

    def get_savers_mode(self):
        return self.savers

    def get_status_temp(self, input_string):
        if input_string == 'health':
            return self.temp_status[0]
        elif input_string == 'endu':
            return self.temp_status[1]
        elif input_string == "magic":
            return self.temp_status[2]

    def change_status_temp(self, input_string, Vorzeichen):
        if input_string == 'health':
            if Vorzeichen == '+':
                if self.temp_status[0] < self.status[0]:
                    self.temp_status[0] += 1
            if Vorzeichen == '-':
                if self.temp_status[0] > 0:
                    self.temp_status[0] -= 1
        elif input_string == 'endu':
            if Vorzeichen == '+':
                if self.temp_status[1] < self.status[1]:
                    self.temp_status[1] += 1
            if Vorzeichen == '-':
                if self.temp_status[1] > 0:
                    self.temp_status[1] -= 1
        elif input_string == "magic":
            if Vorzeichen == '+':
                if self.temp_status[2] < self.status[2]:
                    self.temp_status[2] += 1
            if Vorzeichen == '-':
                if self.temp_status[2] > 0:
                    self.temp_status[2] -= 1

    def set_status_initial(self):
        endurancemodifier=(self.get_resi()+self.get_dext())
        magicmodifier=(self.get_int())
        if isinstance(self.animaltype, animaltypes.clsBaer):
            self.status = [20, 40+endurancemodifier, 5+magicmodifier]
            if self.has_Skill(skills.EnduranceCharacterSkill):
                self.status[1] *= 2
        elif isinstance(self.animaltype, animaltypes.clsRobbe):
            self.status = [10, 35+endurancemodifier, 15+magicmodifier]
            if self.has_Skill(skills.EnduranceCharacterSkill):
                self.status[1] *= 20
        self.temp_status = self.status[:]

    def get_str(self):
        return self.abilities.__getattribute__('strength').value

    def get_dext(self):
        return self.abilities.__getattribute__('dexterity').value

    def get_resi(self):
        return self.abilities.__getattribute__('resistance').value

    def get_int(self):
        return self.abilities.__getattribute__('intelligence').value

    def get_Name(self):
        return self.name

    def set_Name(self, name):
        self.name = str(name)

    def get_Skills(self):
        return self.skills

    def set_Skill(self, input_skill):
        self.skills.append(input_skill)

    def get_Level(self):
        level = str(self.level)
        return level

    def set_Type(self, type):
        self.animaltype = type()

    def get_Type(self):
        return self.animaltype

    def set_Subtype(self, animalsubtype):
        self.animalsubtype = animalsubtype()
        self.update_applicable_Skills()
        self.update_Skills(self.skills)

    def get_Subtype(self):
        return self.animalsubtype

    def get_Build_Points(self):
        return self.build_points

    def gain_Build_Points(self, points):
        self.build_points += points

    def lower_Build_Points(self, points):
        self.build_points -= points

    def spend_Build_Points(self, input_ability):
        for ability in abilities.ALL:
            if str(ability.id) == input_ability:
                getattr(self.abilities, ability.id).value += 1
                self.update_applicable_Skills()
                self.update_Skills(self.skills)
                break

    def lose_Build_Points(self, input_ability):
        for ability in abilities.ALL:
            if str(ability.id) == input_ability:
                getattr(self.abilities, ability.id).value -= 1
                self.update_applicable_Skills()
                self.update_Skills(self.skills)
                break

    def Build_Point_Value(self, input_ability):
        for ability in abilities.ALL:
            if str(ability.id) == input_ability:
                return getattr(self.abilities, ability.id).value

    def LevelUp(self):
        num_redo=self.get_status_max("health")-self.get_status_temp("health")
        for i in range(num_redo):
            self.change_status_temp("health", "+")
        num_redo = self.get_status_max("endu") - self.get_status_temp("endu")
        for i in range(num_redo):
            self.change_status_temp("endu", "+")
        for i in range(num_redo):
            self.change_status_temp("magic", "+")

        self.build_points+=1
        if self.level>6:
            self.build_points+=1
        self.level = self.level+1

    def randomize_Name(self):
        name = NameGenerator.generate_name(2, 5)
        self.set_Name(name)

    def update_applicable_Skills(self):
        self.skills = []
        for skill in skills.ALL:
            continues = True
            for subtype in skill.applicable_subtype:
                if (isinstance(self.animalsubtype, subtype)):
                    continues = False
                    break
            if continues:
                continue
            continues = False

            for required_ability, min_value in skill.required_abilities.items():
                if getattr(self.abilities, required_ability.id).value < min_value:
                    continues = True
                    break
            if continues:
                continue
            self.skills.append(skill)

    def update_Skills(self, Liste):
        self.skills = Liste[:]

    def has_Skill(self, input_skill):
        for skill in self.skills:
            if skill == input_skill:
                return True
        return False

# für den Charakterbogen
    def __str__(self):
        content = [
            '## Charakter Bogen',
            '',
            '  - Name: ' + self.name,
            '  - Tierart: ' + str(self.animaltype),
            '  - Farbe: ' + str(self.animalsubtype),
            '',
            '## Statuswerte',
            ''
        ]
        for ability in abilities.ALL:
            content.append('  - ' + ability.name + ': ' +
                           str(getattr(self.abilities, ability.id).value))
        content.extend([
            '',
            '## Fähigkeiten',
            ''
        ])
        if not self.skills:
            content.append('Keine Fähigkeiten verfügbar.')
        else:
            for skill in self.skills:
                content.append('  - ' + skill.name)
        return '\n'.join(content)
