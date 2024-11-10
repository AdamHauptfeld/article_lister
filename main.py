import os
import pandas as pd
from keyworder import keyworder_main

# This program goes through an entire directory (folder) and its subdirectories and creates an excel file listing every file
# whose name follows the pattern: "authornames - articlename.extension"

def main():
    #Get the desired directory from the user and enter new file name and choice to use ai keyworder.
    directory_path = input("Enter path to directory (without quotation marks): ")
    new_name = str(input("Enter name for new file: "))
    
    #Gives users the option to skip the ai keyworder.
    use_keyworder = None
    while use_keyworder is None:
        answer = input("Do you want to use the ai to create keywords for each document? \
Warning: this could take a lot of time. (Y/N): ").strip()
        if answer.upper() == 'Y':
            use_keyworder = True
        elif answer.upper() == "N":
            use_keyworder = False
        else:
            print("\n**You must enter Y or N.**\n")

    #Put the paths of all the files in the directory and its subdirectories in a list.
    file_list = get_file_names(directory_path)
    
    #If yes was chosen, uses AI to create a dictionary with keywords for each file in the list
    if use_keyworder == True:
        keyword_dict = keyword_dictionary_creator(file_list)
    else:
        keyword_dict = None
    
    #Create a list of subslists, where each sublist is a row's worth of content in the eventual table
    file_columns_list = cleaned_list_creator(file_list, keyword_dict)
    
    #create the dataframe
    article_table = table_creator(file_columns_list, use_keyworder)

    #export the dataframe as an xlsx
    print(article_table.head())
    article_table.to_excel(rf'C:\Users\ahaup\OneDrive\Desktop\{new_name}.xlsx', index=False)
    
    
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


#Create a list containing a tuple for each file, each tuple has a file's authors[0], name[1], folder[2], keywords[3] and  extension[4]
#Also, it uses strip() to remove whitespace from the author and article name.
def cleaned_list_creator(list_of_file_names, keyword_dict):
    file_columns_list = []
    index = 0
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
        if keyword_dict is not None:
            article_keywords = keyword_dict[index]
            final_list = [authors.strip(), article_name.strip(), folder_name, article_keywords, extension]
        else:
            final_list = [authors.strip(), article_name.strip(), folder_name, extension]
        file_columns_list.append(final_list)
        index += 1
    
    return file_columns_list


#for each file in file_list, runs the ai keyword creater, and stores the list of keywords in a dictionary
#with the file's index as the key
def keyword_dictionary_creator(file_list):
    index = 0
    keyword_dictionary = {}
    for file_path in file_list:
        keywords = keyworder_main(file_path)
        keyword_dictionary[index] = keywords
        index += 1
    return keyword_dictionary


def table_creator(list_of_item_lists, use_keyworder):
    if use_keyworder == True:    
        article_table = pd.DataFrame(list_of_item_lists, columns=['authors', 'article_name', 'category', 'keywords', 'file_type'])
    else:
        article_table = pd.DataFrame(list_of_item_lists, columns=['authors', 'article_name', 'category', 'file_type'])
    
    return article_table


main()
