from bom import Bom

filename = 'test-sheets\test_template_l.xlsx'
columns = ['A','G','H','I','L','O','V','X']


bom = Bom()
bom.load_xls(filename=filename,columns=columns)

BOM = bom.BOM
uid_BOM = bom.uid_BOM
for key in uid_BOM:
	print('Key: {}\n{}'.format(key, BOM[key]))