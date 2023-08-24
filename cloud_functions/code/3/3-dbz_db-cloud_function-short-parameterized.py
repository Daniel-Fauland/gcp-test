import io
import re
import requests
import time
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime
from google.cloud import storage


def get_content(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    return soup


def get_story_events(content, base_url, blacklist):
    story_events = []
    for row in content.find('div', attrs={'id': 'mw-content-text'}).find_all('a', href=True):
        if row.find('img') and "/wiki/" in row['href'] and row['href'] not in blacklist:
            href = row['href']
            full_path = base_url + href
            story_events.append(full_path)
    return story_events


def read_story_events(story_events):
    # --- Set up dataframe for pandas ---
    my_df = {"Event name": [], "Global release": [], "Japan release": [], "Url": []}
    # Define regex pattern for Date extraction
    pattern = r'(?<!:\s)(?<!\d)\d{1} [A-Za-z]{3} \d{4}|(?<!: )\d{2} [A-Za-z]{3} \d{4}'
    # Iterate over each story event url
    print(f"\tRetreaving information about story events")
    for x, event_url in enumerate(story_events):
        # Get the content of the url
        content = get_content(event_url)
        # Get the title of the page
        title = content.find('span', attrs={'class': 'mw-page-title-main'})
        try:
            if "Discontinued" in title.text: continue
            my_df["Event name"].append(title.text.strip())
        except:
            # Look for title in a different place if no title was found
            title = content.find('h1', attrs={'class': 'page-header__title'})
            try:
                if "Discontinued" in title.text: continue
                my_df["Event name"].append(title.text.strip())
            except:
                my_df["Event name"].append("Unknown")
        my_df["Url"].append(event_url)
        # Find a specific id in the page to limit content
        content_text = content.find('div', attrs={'id': 'mw-content-text'})
        # Iterate over each row
        for row in content_text.div.table.tbody.find_all('tr'):
            # Find all dates that match the regex pattern
            release_dates = re.findall(pattern, str(row))
            if release_dates:
                for i in range(len(release_dates)):
                    # Convert the dates to another format
                    input_date = datetime.strptime(release_dates[i], '%d %b %Y')
                    release_dates[i] = input_date.strftime('%Y-%m-%d')
                    if i == 0:
                        my_df["Japan release"].append(release_dates[i])
                    elif i == 1:
                        my_df["Global release"].append(release_dates[i])
        # If there was no date found insert 'unknown' tag
        if len(my_df["Japan release"]) < len(my_df["Event name"]):
            my_df["Japan release"].append("unknown")
        if len(my_df["Global release"]) < len(my_df["Event name"]):
            my_df["Global release"].append("unknown")
        break
    return my_df


def get_character_list(part_url, type, base_url, blacklist):
    suffix = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    character_url_list = []
    character_name_list = []
    print(f"\tRetrieving character pages for {type}")
    for x, char in enumerate(suffix):
        url = part_url + char
        content = get_content(url)
        for row in content.find('div', attrs={'id': 'mw-content-text'}).find_all('a', href=True):
            if "/wiki/" in row['href'] and row['href'] not in blacklist:
                full_path = base_url + row["href"]
                # If a title does not exist it is not a real character --> skip row
                try:
                    character_name_list.append(row["title"])
                    character_url_list.append(full_path)
                except:
                    continue
        break
    character_url_list_uq = list(dict.fromkeys(character_url_list))
    character_name_list_uq = list(dict.fromkeys(character_name_list))
    return character_url_list_uq, character_name_list_uq


def get_card_rarity_type_id(content, id_pattern, my_df, names, x):
    # --- Find the type and rarity and id of a card ---
    counter = 1
    tables = content.find('div', id='mw-content-text')
    for table in tables.find_all('table'):
        ids = re.findall(id_pattern, str(table))
        if ids:
            # Matched pattern: <center>12345</center>
            char_id = ids[0][8:-9]
            my_df["ID"].append(char_id)
            break
    for table in tables.find_all('table'):
        for row in table.find_all('a', href=True):
            if "/wiki/Category:" in row['href']:
                counter += 1
                type_or_rarity = row['href'][15:]
                if len(type_or_rarity) == 2:
                    my_df["Rarity"].append(type_or_rarity)
                elif len(type_or_rarity) > 3:
                    type_or_rarity = type_or_rarity.split("_")
                    my_df["Class"].append(type_or_rarity[0])
                    my_df["Type"].append(type_or_rarity[1])
            # Add break here to avoid getting types from (non)awakenings as well
            if counter > 2:
                break
        # Add break here to avoid getting types from (non)awakenings as well
        if counter > 2:
                break
                
    # If no rarity/class/id or type was found insert 'na'
    if len(my_df["Name"]) != len(my_df["Rarity"]):
        my_df["Rarity"].append("na")
    if len(my_df["Name"]) != len(my_df["Class"]):
        my_df["Class"].append("na")
    if len(my_df["Name"]) != len(my_df["Type"]):
        my_df["Type"].append("na")
    if len(my_df["Name"]) != len(my_df["ID"]):
        my_df["ID"].append("na")
    return my_df


def get_card_release_date(content, pattern, my_df, x):
    # --- Find the release date of a card ---
    for row in content.find('div', attrs={'class': 'lefttablecard'}):
        release_dates = re.findall(pattern, str(row))
        if release_dates:
            for i in range(len(release_dates)):
                # Convert the dates to another format
                input_date = datetime.strptime(release_dates[i], '%d %b %Y')
                release_dates[i] = input_date.strftime('%Y-%m-%d')
                if len(release_dates) == 1:
                    my_df["Japan release"].append(release_dates[i])
                    my_df["Global release"].append("na")
                    my_df["Japan EZA release"].append("na")
                    my_df["Global EZA release"].append("na")
                elif len(release_dates) == 2:
                    if i == 0:
                        my_df["Japan release"].append(release_dates[i])
                    elif i == 1:
                        my_df["Global release"].append(release_dates[i])
                        my_df["Japan EZA release"].append("na")
                        my_df["Global EZA release"].append("na")
                elif len(release_dates) == 3:
                    if i == 0:
                        my_df["Japan release"].append(release_dates[i])
                    elif i == 1:
                        my_df["Japan EZA release"].append(release_dates[i])
                    elif i == 2:
                        my_df["Global release"].append(release_dates[i])
                        my_df["Global EZA release"].append("na")
                elif len(release_dates) == 4:
                    if i == 0:
                        my_df["Japan release"].append(release_dates[i])
                    elif i == 1:
                        my_df["Japan EZA release"].append(release_dates[i])
                    elif i == 2:
                        my_df["Global release"].append(release_dates[i])
                    elif i == 3:
                        my_df["Global EZA release"].append(release_dates[i])
            try:
                if my_df["Japan EZA release"][x] == "na":
                    my_df["Japan EZA"].append("No")
                else: my_df["Japan EZA"].append("Yes")
                if my_df["Global EZA release"][x] == "na":
                    my_df["Global EZA"].append("No")
                else: my_df["Global EZA"].append("Yes")
            except:
                pass
    return my_df


def get_card_stats(content, my_df, x):
    stats_pattern = r'<center>\d{3,5}</center>'
    stats_pattern_eza = r'<center>\d{4,5}</center>|<center>\d{4,5}\n</center>'
    tables = content.find('div', id='mw-content-text')
    tables = tables.find_all('table')
    stats = []
    stats_eza = []
    flag = True
    # if my_df["Japan EZA"][x] == "No" and my_df["Global EZA"][x] == "No":
    for n in range(len(tables)-1, -1, -1):
        # Find Categories for card
        if "Category.png" in str(tables[n]):
            tr = tables[n].find_all('tr')
            reversed_tr = list(reversed(tr))[0]
            try:
                center_tag = reversed_tr.find('center')
                if center_tag and flag:
                    titles = [a['title'] for a in center_tag.find_all('a')]
                    titles = ', '.join(titles)
                    my_df["Categories"].append(titles)
                    flag = False
            except:
                pass        
        # Find stats for card
        if "Stats.png" in str(tables[n]):  
            ids = re.findall(stats_pattern, str(tables[n]))
            if ids:  # Matched pattern: <center>12345</center>
                for i in ids:
                    char_id = i[8:-9]
                    stats.append(char_id)
                if len(stats) >= 12:
                    stats = stats[-12:]
        # Find EZA stats for card
        if "Extreme_z_awaken_label.png" in str(tables[n]):
            ids = re.findall(stats_pattern_eza, str(tables[n]))
            if ids:
                for i in ids:
                    char_id = i[8:-9]
                    stats_eza.append(char_id) 
                if len(stats_eza) >= 18:
                    stats_eza = stats_eza[-18:]
                    stats_eza = [item.replace('\n', '') for item in stats_eza]   

    try:  # Add normal stats
        my_df["HP 55%"].append(stats[2])
        my_df["HP 100%"].append(stats[3])
        my_df["ATK 55%"].append(stats[6])
        my_df["ATK 100%"].append(stats[7])
        my_df["DEF 55%"].append(stats[10])
        my_df["DEF 100%"].append(stats[11])
    except:
        pass
    try:  # Add EZA stats
        my_df["HP 55% EZA"].append(stats_eza[4])
        my_df["HP 100% EZA"].append(stats_eza[5])
        my_df["ATK 55% EZA"].append(stats_eza[10])
        my_df["ATK 100% EZA"].append(stats_eza[11])
        my_df["DEF 55% EZA"].append(stats_eza[16])
        my_df["DEF 100% EZA"].append(stats_eza[17])
    except:
        pass
    my_df = append_char_na(my_df)
    return my_df


def append_char_na(my_df):
    # If no stats were found insert 'na'
    if len(my_df["Name"]) != len(my_df["HP 55%"]):
        my_df["HP 55%"].append("na")
    if len(my_df["Name"]) != len(my_df["ATK 55%"]):
        my_df["ATK 55%"].append("na")
    if len(my_df["Name"]) != len(my_df["DEF 55%"]):
        my_df["DEF 55%"].append("na")
    if len(my_df["Name"]) != len(my_df["HP 100%"]):
        my_df["HP 100%"].append("na")
    if len(my_df["Name"]) != len(my_df["ATK 100%"]):
        my_df["ATK 100%"].append("na")
    if len(my_df["Name"]) != len(my_df["DEF 100%"]):
        my_df["DEF 100%"].append("na")

    # If no EZA stats were found insert 'na'
    if len(my_df["Name"]) != len(my_df["HP 55% EZA"]):
        my_df["HP 55% EZA"].append("na")
    if len(my_df["Name"]) != len(my_df["ATK 55% EZA"]):
        my_df["ATK 55% EZA"].append("na")
    if len(my_df["Name"]) != len(my_df["DEF 55% EZA"]):
        my_df["DEF 55% EZA"].append("na")
    if len(my_df["Name"]) != len(my_df["HP 100% EZA"]):
        my_df["HP 100% EZA"].append("na")
    if len(my_df["Name"]) != len(my_df["ATK 100% EZA"]):
        my_df["ATK 100% EZA"].append("na")
    if len(my_df["Name"]) != len(my_df["DEF 100% EZA"]):
        my_df["DEF 100% EZA"].append("na")

    # If not Categories were found insert 'na':
    if len(my_df["Name"]) != len(my_df["Categories"]):
        my_df["Categories"].append("na")
    return my_df


def clean_lists(characters, names):
    # --- Remove wrong dokkan entries ---
    blacklist2 = ["User blog:"]
    filtered_characters = []
    filtered_names = []
    for url, name in zip(characters, names):
        if not any(substring in name for substring in blacklist2):
            filtered_characters.append(url)
            filtered_names.append(name)
    return filtered_characters, filtered_names


def read_characters(characters, names):
    my_df = {"Name": [], "Rarity": [], "Class": [], "Type": [], "Global release": [], "Japan release": [], "Global EZA release": [], "Japan EZA release": [], "Global EZA": [], "Japan EZA": [], "HP 55%": [], "ATK 55%": [], "DEF 55%": [], "HP 100%": [], "ATK 100%": [], "DEF 100%": [], "HP 55% EZA": [], "ATK 55% EZA": [], "DEF 55% EZA": [], "HP 100% EZA": [], "ATK 100% EZA": [], "DEF 100% EZA": [], "Categories": [], "ID": [], "Url": []}
    pattern = r'(?<!:\s)(?<!\d)\d{1} [A-Za-z]{3} \d{4}|(?<!: )\d{2} [A-Za-z]{3} \d{4}'
    id_pattern = r'<center>\d{4,5}</center>'
    print(f"\tRetrieving information of characters") 
    for x, name in enumerate(names):
        url = characters[x]    
        my_df["Name"].append(name)
        my_df["Url"].append(url)
        content = get_content(url)
        my_df = get_card_rarity_type_id(content, id_pattern, my_df, names, x)
        my_df = get_card_release_date(content, pattern, my_df, x)
        my_df = get_card_stats(content, my_df, x)
        break
    df = pd.DataFrame.from_dict(my_df)
    return df


def remove_duplicate_characters(df):
    print("\nRemoving duplicate characters...")
    indices_to_delete = []
    nr_chars_before = len(df)
    for index, row in df.iterrows():
        if row['Rarity'] == 'UR' and row['ID'] != 'na':
            next_id = str(int(row['ID']) + 1)
            next_row = df[df['ID'] == next_id]
            if not next_row.empty and next_row.iloc[0]['Rarity'] == 'LR':
                if (
                    row['Class'] == next_row.iloc[0]['Class']
                    and row['Type'] == next_row.iloc[0]['Type']
                    and row['Japan release'] == next_row.iloc[0]['Japan release']
                ):
                    indices_to_delete.append(index)
                elif (
                    row['Class'] == next_row.iloc[0]['Class']
                    and row['Type'] == next_row.iloc[0]['Type']
                    and row['Japan release'] == 'na'
                    and row['Global release'] == next_row.iloc[0]['Global release']
                ):
                    indices_to_delete.append(index)
    df.drop(indices_to_delete, inplace=True)
    nr_chars_after = len(df)
    print(f"\tRemoved {nr_chars_before - nr_chars_after} characters. Total characters found (after cleanup): {nr_chars_after}")
    return df


def export_results(dataframe, kind, fname, storage_client, bucket_name):
    print(f"\nExporting {kind} results...")
    current_timestamp = datetime.now().strftime('%Y_%m_%d')
    # Convert the dictionary to a DataFrame
    df = pd.DataFrame(dataframe)
    csv_data = df.to_csv(index=False)
    excel_buffer = io.BytesIO()
    df.to_excel(excel_buffer, index=False)
    excel_buffer.seek(0)  # Move the cursor to the beginning of the buffer

    cloud_csv_filename = f"dokkan-battle/{current_timestamp}-{fname}.csv"
    cloud_xlsx_filename = f"dokkan-battle/{current_timestamp}-{fname}.xlsx"
    bucket = storage_client.bucket(bucket_name)
    blob_csv = bucket.blob(cloud_csv_filename)
    blob_xlsx = bucket.blob(cloud_xlsx_filename)
    blob_csv.upload_from_string(csv_data, content_type="text/csv")
    blob_xlsx.upload_from_file(excel_buffer, content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    print(f"\tDBZ Dokkan Battle csv file saved at: '{bucket}/{cloud_csv_filename}'")
    print(f"\tDBZ Dokkan Battle excel file saved at: '{bucket}/{cloud_csv_filename}'")


def start_script(request):
    project_id = request.form.get('project_id') 
    bucket_name = request.form.get('bucket_name')  
    if project_id is None or bucket_name is None:
        return 'Error: Missing required parameters. You need the following curl command format:\ncurl -X POST -H "Authorization: bearer $(gcloud auth print-identity-token)" -d "project_id=your-project-id" -d "bucket_name=your-bucket" <cloud-function-url>'
    if project_id == "your-project-id" and bucket_name == "your-bucket":
        project_id = "propane-nomad-396712"
        bucket_name = "de-storage-447"
    storage_client = storage.Client(project=project_id)  
    start_time = time.time()
    print("Starting script:")
    print("Scraping web. This can take a while...")
    base_url = "https://dbz-dokkanbattle.fandom.com"
    story_events_url = "https://dbz-dokkanbattle.fandom.com/wiki/Story_Events"
    character_list_ur_base_url = "https://dbz-dokkanbattle.fandom.com/wiki/Category:UR?from="
    character_list_lr_base_url = "https://dbz-dokkanbattle.fandom.com/wiki/Category:LR?from="
    blacklist = ["/wiki/Category:N", "/wiki/Category:R", "/wiki/Category:SR", "/wiki/Category:SSR", "/wiki/Category:UR", "/wiki/Category:LR", "/wiki/Category:AGL", "/wiki/Category:TEQ", "/wiki/Category:INT", "/wiki/Category:STR", "/wiki/Category:PHY", "/wiki/Rainbow_Ki", "/wiki/Weekly_Events", "/wiki/Bonus_Events", "/wiki/Story_Events", "/wiki/Dragon_Ball_Story", "/wiki/Strike_Events", "/wiki/Dokkan_Events", "/wiki/Special_Events", "/wiki/Limit_Events", "/wiki/Prime_Battle_Events", "/wiki/Extreme_Z-Battle_Events", "/wiki/Challenge_Events", "/wiki/Limited_Events", "/wiki/All_Cards:_(1)001_to_(1)100"]
    story_content = get_content(story_events_url)
    story_events = get_story_events(story_content, base_url, blacklist)
    story_events_df = read_story_events(story_events)
    character_url_list_ur, character_name_list_ur = get_character_list(character_list_ur_base_url, "UR", base_url, blacklist)
    character_url_list_lr, character_name_list_lr = get_character_list(character_list_lr_base_url, "LR", base_url, blacklist)
    character_url_list = character_url_list_ur + character_url_list_lr
    character_name_list = character_name_list_ur + character_name_list_lr
    character_url_list, character_name_list = clean_lists(character_url_list, character_name_list)
    characters_df = read_characters(character_url_list, character_name_list)
    characters_df = remove_duplicate_characters(characters_df)
    export_results(story_events_df, "story events", "dbz_db_story_events", storage_client, bucket_name)  
    export_results(characters_df, "characters", "dbz_db_characters", storage_client, bucket_name)    
    end_time = time.time()
    runtime = end_time - start_time
    print(f"Execution duration: {int(runtime)} seconds")
    return f"Run successfull. Files stored in bucket: {bucket_name} "