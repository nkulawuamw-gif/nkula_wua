lines = open('accounting_app/models.py', 'r', encoding='utf-8').readlines()
lines[677] = '        return f"{self.beneficiary.name} - {self.status} - {self.changed_at}"\n'
open('accounting_app/models.py', 'w', encoding='utf-8').writelines(lines)
print('Fixed line 678:', repr(lines[677].rstrip()))
