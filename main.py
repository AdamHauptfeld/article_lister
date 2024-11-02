import os
import pandas as pd
import openpyxl

# This program goes through an entire directory ("folder") and it's subdirectories and creates an excel file listing every file
# whose name follows the pattern: "authornames - articlename.extension"

# D:\Philosophy\Collected Philosophy Articles

def main():
    #directory_path = input("Enter path to directory (without quotation marks): ")
    directory_path = r'D:\Philosophy\Collected Philosophy Articles'
    file_list = get_file_names(directory_path)
    file_tuples_list = cleaned_tuples_lister(file_list)
    article_table = table_creator(file_tuples_list)
    print(article_table.head())
    article_table.to_excel(r'C:\Users\ahaup\OneDrive\Desktop\philosophy_article_database.xlsx', index=False)


# Returns a list of file paths+names found in the specified folder and its subfolders.
def get_file_names(folder_path):
    first_list = []
    for root, dirs, files in os.walk(folder_path):
        first_list.extend([os.path.join(root, f) for f in files])
    
    file_list = []
    for name in first_list:
        if '-' in name:
            file_list.append(name)
    
    return file_list


#Create a list containing a tuple for each file, each tuple has a file's authors[0], name[1], folder[2] and  extension[3]
#Also, it uses strip() to remove whitespace from the author and article name.
def cleaned_tuples_lister(list_of_file_names):
    file_tuple_list = []
    for name in list_of_file_names:
        split_path_and_name = name.rsplit('\\', 1)
        dir_path = split_path_and_name[0]
        split_folder_from_remaining_path = dir_path.rsplit('\\', 1)
        folder_name = split_folder_from_remaining_path[1]
        split_name_and_extension = split_path_and_name[1].rsplit('.', 1)
        extension = split_name_and_extension[1]
        split_authorname_and_filename = split_name_and_extension[0].split('-', 1)
        authors = split_authorname_and_filename[0]
        article_name = split_authorname_and_filename[1]
        final_tuple = (authors.strip(), article_name.strip(), folder_name, extension)
        file_tuple_list.append(final_tuple)
    
    return file_tuple_list

def table_creator(list_of_4_place_tuples):
    article_table = pd.DataFrame(list_of_4_place_tuples, columns=['authors', 'article_name', 'folder', 'extension'])
    return article_table

main()