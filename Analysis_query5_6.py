import pandas as pd
import matplotlib.pyplot as plt

# Load the Excel file
file_name = r'C:\Users\User\Desktop\Suli\03_Graz\01_classes\04_Databases\01_exercise\plot.xlsx'  # CHANGE ACCORDING TO

# Load data from the sheets
plot1_data = pd.read_excel(file_name, sheet_name='plot1') #lang-pop
plot3_data = pd.read_excel(file_name, sheet_name='plot2')
plot2_data=plot3_data.head(20)

print(plot1_data.head())
print(plot2_data.head(20))


# language_code   pop_avg    pub_name     avg_pop
plt.figure(figsize=(10,5))
plt.bar(plot1_data['language_code'], plot1_data['pop_avg'], color='skyblue')
plt.xlabel('language_code', fontsize=12)
plt.ylabel('pop_avg', fontsize=12)
plt.title('pop_avg by Publilanguage', fontsize=14)
plt.xticks(rotation=90, ha='right')
plt.tight_layout()
plt.show()


plt.figure(figsize=(10,5))
plt.bar(plot2_data['pub_name'], plot2_data['avg_pop'], color='orange')
plt.xlabel('pub_name', fontsize=12)
plt.ylabel('avg_pop', fontsize=12)
plt.title('avg pop by publisher', fontsize=14)
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()

