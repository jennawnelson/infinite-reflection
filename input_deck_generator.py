# written by Jenna Nelson, Feb 2019
#Note: original PNNL Materials Formatted.csv had Li with zaid of '-'. I updated to 3000
#Note: original PNNL Materials Formatted.csv had B with zaid of '-'. I updated to 5000
#Note: original PNNL Materials Formatted.csv had Ba with zaid of '-'. I updated to 56000
#Note: original PNNL Materials Formatted.csv had Ge with zaid of '-'. I updated to 32000
#Note: original PNNL Materials Formatted.csv had Pd with zaid of '-'. I updated to 46000
#Note: original PNNL Materials Formatted.csv had no density for steel stainless 316. I updated to 8.0


import csv

def isotope_csv_reader():
	isotope_mass_list = []
	with open('nuclide_abundances.csv','r') as csv_file:
		csv_reader = csv.reader(csv_file)
		next(csv_reader)
		for line in csv_reader:
			isotope_mass_list.append(line)
	float_isotope_mass_list = []
	for value in isotope_mass_list:
		float_isotope_mass_list.append([float(i) for i in value])
	return(float_isotope_mass_list)


def materials_csv_reader(file):
	csv_list = []
	with open(file,'r') as csv_file:
		csv_reader = csv.reader(csv_file)
		for line in csv_reader:
			csv_list.append(line)
	return csv_list


def separated_materials_csv_list(raw_list):
	separated_list = []
	temp_list = []
	for list in raw_list:
		print(list)
		temp_list.append(list)
		if list == ['','','','']:
			separated_list.append(temp_list)
			temp_list = []
	return separated_list

def format_materials_list(a_csv_list):
	full_materials_list = []
	for materials_set in a_csv_list:
		material_spec = []
		material_spec.append(materials_set[0][0])
		material_spec.append(materials_set[1][0])
		input = []
		print(materials_set)
		for index, lines in enumerate(materials_set[2:]):
			if lines != ['','','','']:
				input.append([float(lines[1]),float(lines[2])])
		material_spec.append(input)
		full_materials_list.append(material_spec)
	return full_materials_list


def isotope_splitter(input,nuclide_abundance_list):
	new_list = []
	for list in input:
		if list[0] == 6000:
			new_list.append([list[0], list[1]])
		elif list[0] % 1000 == 0:
			for sublist in nuclide_abundance_list:
				if list[0] < sublist[0] <= (list[0]+999):
					if sublist[2] > 0:
						new_list.append([sublist[0], list[1]*sublist[2]])
		else:
			new_list.append([list[0], list[1]])
	return(new_list)



raw_materials_list = materials_csv_reader('PNNL Materials Formatted.csv')
separated_materials_list = separated_materials_csv_list(raw_materials_list)
formatted_materials_list = format_materials_list(separated_materials_list)
nuclide_abundance_list = isotope_csv_reader()

for material_description_index,material_description in enumerate(formatted_materials_list):
	split_material = isotope_splitter(material_description[2],nuclide_abundance_list)
	formatted_materials_list[material_description_index][2] = split_material
# print(formatted_materials_list)

thickness = [5, 6]

for material_description in formatted_materials_list:
	material = str(material_description[0])
	density = float(material_description[1]) * -1
	inputs = material_description[2]
	for t in thickness:
		filename = "{}_{}cm".format(str(material.replace(' ','_')), str(t))
		new_line = filename + '\n'
		new_line = new_line + 'c' + '\n'
		new_line = new_line + 'c Reflecting Material, ' + material + '\n'
		new_line = new_line + 'c Shield Thickness (cm), ' + str(t) + '\n'
		new_line = new_line + 'c' + '\n' + 'c' + '\n' + 'c Cell Cards' + '\n'
		new_line = new_line + '1  1 ' + str(density) + '  1  -2    imp:n=1 $ Reflector\n'
		new_line = new_line + '2  0           3  -1    imp:n=1 $ Void below\n'
		new_line = new_line + '3  0           2  -4    imp:n=1 $ Void above\n'
		new_line = new_line + '4  0    # 1 # 2 # 3                   imp:n=0 $ Lower boundary of problem\n\n'
		new_line = new_line + 'c Surface Cards\n'
		new_line = new_line + '1  pz  0.0    $ Bottom of reflector\n'
		new_line = new_line + '2  pz  ' + str(float(t)) + '    $ Top of reflector\n'
		new_line = new_line + '3  pz -2.0    $ Bottom surface of bottom void\n'
		new_line = new_line + '4  pz  ' + str(float(t) + 1.0) + '    $ Top surface of top void\n\n'
		new_line = new_line + 'c Material Cards\nm1'
		if len(inputs) == 1:
			new_line = new_line + '  ' + str(int(inputs[0][0])) + '.80c ' + str(inputs[0][1]*-1) +'\n'
		if len(inputs) > 1:
			new_line = new_line + '  ' + str(int(inputs[0][0])) + '.80c ' + str(inputs[0][1]*-1) + '\n'
			for input in inputs[1:]:
				new_line = new_line + '\t' + str(int(input[0])) + '.80c ' + str(input[1] * -1) + '\n'
		new_line = new_line + 'c Source definition\n'
		new_line = new_line + 'sdef pos=0 0 0  erg=D1 vec=0 0 1  dir=1\n'
		new_line = new_line + 'SP1 -3\n'
		new_line = new_line + 'nps 1000000'
		with open(filename,'w') as f:
			f.write(new_line)
print("Files generated.")