from selenium import webdriver
import time
import pandas as pd


# Set up the browser driver (make sure you have the appropriate driver installed!)
driver = webdriver.Chrome()

# Navigate to Google Scholar
driver.get('https://scholar.google.com/')

# Find the search box and enter "Andrew Ng"
search_box = driver.find_element('name', 'q')
name = input('Enter name: ')
search_box.send_keys(name)
search_box.submit()

# find elements by xpath
profile_links = driver.find_element('xpath', '//*[@id="gs_res_ccl_mid"]/div[1]/h3/a')
profile_links.click()

profile_link = driver.find_element('xpath', '//*[@id="gsc_sa_ccl"]/div[1]/div/div/h3/a')
profile_link.click()

df = pd.DataFrame(columns=['name', 'university', 'interests', 'articleTitle', 'citedBy', 'publicationYear'])
articles_df = pd.DataFrame(columns=['authors', 'publicationDate', 'journal', 'volume', 'issue', 'pages', 'description'])
try:
    name = driver.find_element('id', 'gsc_prf_in').text
except:
    name = 'did not found'
# df.loc[0, 'name'] = name
try:
    university = driver.find_element('xpath', '//*[@id="gsc_prf_i"]/div[2]/a').text
except:
    university = 'did not found'
# df.loc[0, 'university'] = university
try:
    interests = driver.find_element('id', 'gsc_prf_int').text
except:
    interests = 'did not found'
# df.loc[0, 'interests'] = interests

# # loop in each tr by css selector
# print(driver.find_element('css selector', '#gsc_a_b > tr:nth-child({}) > td:nth-child(1)'.format(1)).text)

# Loop through all rows of the table and print out their text
row_num = 1
error = 0
for i in range(100):
    try:
        table = driver.find_element('id', 'gsc_a_b')
        print(row_num)
        article_title = driver.find_element('css selector', '#gsc_a_b > tr:nth-child({}) > td:nth-child(1)'.format(row_num)).text
        article_cited_by = driver.find_element('css selector','#gsc_a_b > tr:nth-child({}) > td:nth-child(2)'.format(row_num)).text
        article_publish_date = driver.find_element('css selector','#gsc_a_b > tr:nth-child({}) > td:nth-child(3)'.format(row_num)).text
        driver.find_element('css selector', '#gsc_a_b > tr:nth-child({}) > td:nth-child(1) > a'.format(row_num)).click()
        try:
            authors = driver.find_element('xpath', '//*[@id="gsc_oci_table"]/div[1]/div[2]').text
            publication_date = driver.find_element('xpath', '//*[@id="gsc_oci_table"]/div[2]/div[2]').text
            journal = driver.find_element('xpath', '//*[@id="gsc_oci_table"]/div[3]/div[2]').text
            volume = driver.find_element('xpath', '//*[@id="gsc_oci_table"]/div[4]/div[2]').text
            issue = driver.find_element('xpath', '//*[@id="gsc_oci_table"]/div[5]/div[2]').text
            pages = driver.find_element('xpath', '//*[@id="gsc_oci_table"]/div[6]/div[2]').text
            description = driver.find_element('xpath', '//*[@id="gsc_oci_table"]/div[7]/div[2]').text
            articles_df.loc[i, 'authors'] = authors
            articles_df.loc[i, 'publicationDate'] = publication_date
            articles_df.loc[i, 'journal'] = journal
            articles_df.loc[i, 'volume'] = volume
            articles_df.loc[i, 'issue'] = issue
            articles_df.loc[i, 'pages'] = pages
            articles_df.loc[i, 'description'] = description
        except:
            print('incomplete article info')
        driver.back()
        #add name and university and interests and article title and cited by and publication year
        df.loc[i, 'name'] = name
        df.loc[i, 'university'] = university
        df.loc[i, 'interests'] = interests
        df.loc[i, 'articleTitle'] = article_title
        df.loc[i, 'citedBy'] = article_cited_by
        df.loc[i, 'publicationYear'] = article_publish_date
        row_num += 1
    except(Exception) as e:
        if error == 3:
            print('finished', error)
            break
        else:
            print('error: {}'.format(error))
            print(e)
            error += 1
            row_num += 1
            continue

df.to_csv('data_{}.csv'.format(name), index=False)
articles_df.to_csv('articles_{}.csv'.format(name), index=False)



# time.sleep(10)

# Close the browser window
driver.quit()
