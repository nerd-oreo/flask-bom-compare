from bom import BomCompare

filename = 'test_template_2.xlsx'
columns = ['A','G','H','I','L','O','V','X']


bom_compare = BomCompare()
bom_compare.load_xls(filename=filename,columns=columns)

BOM = bom_compare.BOM_A
for key in BOM:
	print('Key: {}\n{}'.format(key, BOM[key]))