import requests as req
import json
from bs4 import BeautifulSoup, SoupStrainer
from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By
from datetime import datetime
from urllib import request
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
from selenium.webdriver.support.ui import Select
import re
import json

# Mapeamento de paises
country_mapping = {
    "Albania": "Albania",
    "Algeria": "Algeria",
    "Argentina": "Argentina",
    "Armenia": "Armenia",
    "Australia": "Australia",
    "Austria": "Austria",
    "Bahamas": "Bahamas",
    "Bahrain": "Bahrain",
    "Bangladesh": "Bangladesh",
    "Barbados": "Barbados",
    "Belarus": "Belarus",
    "Belgium": "Belgium",
    "Belize": "Belize",
    "Benin": "Benin",
    "Bermuda": "Bermuda",
    "Bolivia": "Bolivia",
    "Bosnia Herceg": "Bosnia and Herzegovina",
    "Botswana": "Botswana",
    "Brazil": "Brazil",
    "Brunei": "Brunei",
    "Bulgaria": "Bulgaria",
    "Cambodia": "Cambodia",
    "Canada": "Canada",
    "Cape Verde": "Cape Verde",
    "Chile": "Chile",
    "Colombia": "Colombia",
    "Cook Islands": "Cook Islands",
    "Costa Rica": "Costa Rica",
    "Cote Ivoire": "Ivory Coast",
    "Croatia": "Croatia",
    "Cuba": "Cuba",
    "Cyprus": "Cyprus",
    "Czech Republic": "Czech Republic",
    "Denmark": "Denmark",
    "Dominican Rep": "Dominican Republic",
    "Ecuador": "Ecuador",
    "Egypt": "Egypt",
    "El Salvador": "El Salvador",
    "England": "England",
    "Estonia": "Estonia",
    "Ethiopia": "Ethiopia",
    "Falkland Island": "Falkland Islands",
    "Faroe Islands": "Faroe Islands",
    "Fiji": "Fiji",
    "Finland": "Finland",
    "France": "France",
    "Gabon": "Gabon",
    "Germany": "Germany",
    "Ghana": "Ghana",
    "Greece": "Greece",
    "Greenland": "Greenland",
    "Guatemala": "Guatemala",
    "Hungary": "Hungary",
    "Iceland": "Iceland",
    "India": "India",
    "Indonesia": "Indonesia",
    "Iran": "Iran",
    "Iraq": "Iraq",
    "Ireland": "Ireland",
    "Israel": "Israel",
    "Italy": "Italy",
    "Jamaica": "Jamaica",
    "Japan": "Japan",
    "Jordan": "Jordan",
    "Kazakhstan": "Kazakhstan",
    "Kenya": "Kenya",
    "Kuwait": "Kuwait",
    "Laos": "Laos",
    "Latvia": "Latvia",
    "Lebanon": "Lebanon",
    "Lesotho": "Lesotho",
    "Lithuania": "Lithuania",
    "Luxembourg": "Luxembourg",
    "Malaysia": "Malaysia",
    "Maldives": "Maldives",
    "Malta": "Malta",
    "Mauritius": "Mauritius",
    "Mexico": "Mexico",
    "Moldova": "Moldova",
    "Monaco": "Monaco",
    "Mongolia": "Mongolia",
    "Montenegro": "Montenegro",
    "Morocco": "Morocco",
    "Mozambique": "Mozambique",
    "Myanmar": "Myanmar",
    "Namibia": "Namibia",
    "Nepal": "Nepal",
    "Netherlands": "Netherlands",
    "New Zealand": "New Zealand",
    "Nicaragua": "Nicaragua",
    "Nigeria": "Nigeria",
    "North Ireland": "Northern Ireland",
    "North Korea": "North Korea",
    "North Macedonia": "North Macedonia",
    "Norway": "Norway",
    "Oman": "Oman",
    "Pakistan": "Pakistan",
    "Palestine": "Palestine",
    "Panama": "Panama",
    "Paraguay": "Paraguay",
    "Peoples R China": "China",
    "Peru": "Peru",
    "Philippines": "Philippines",
    "Poland": "Poland",
    "Portugal": "Portugal",
    "Qatar": "Qatar",
    "Romania": "Romania",
    "Russia": "Russia",
    "Saudi Arabia": "Saudi Arabia",
    "Scotland": "Scotland",
    "Senegal": "Senegal",
    "Serbia": "Serbia",
    "Singapore": "Singapore",
    "Slovakia": "Slovakia",
    "Slovenia": "Slovenia",
    "Solomon Islands": "Solomon Islands",
    "South Africa": "South Africa",
    "South Korea": "South Korea",
    "Spain": "Spain",
    "Sri Lanka": "Sri Lanka",
    "Sweden": "Sweden",
    "Switzerland": "Switzerland",
    "Taiwan": "Taiwan",
    "Tanzania": "Tanzania",
    "Thailand": "Thailand",
    "Trinidad Tobago": "Trinidad and Tobago",
    "Tunisia": "Tunisia",
    "Turkey": "Turkey",
    "Turkiye": "Turkey",
    "U Arab Emirates": "United Arab Emirates",
    "Uganda": "Uganda",
    "Ukraine": "Ukraine",
    "Uruguay": "Uruguay",
    "USA": "United States",
    "Uzbekistan": "Uzbekistan",
    "Vanuatu": "Vanuatu",
    "Venezuela": "Venezuela",
    "Vietnam": "Vietnam",
    "Wales": "Wales",
    "Zambia": "Zambia"
}

detailed_country_mapping = {
    "Albania": {"Region": "Europe", "Sub-region": "Southern Europe", "Intermediate Region": ""},
    "Algeria": {"Region": "Africa", "Sub-region": "Northern Africa", "Intermediate Region": ""},
    "Argentina": {"Region": "Americas", "Sub-region": "South America", "Intermediate Region": ""},
    "Armenia": {"Region": "Asia", "Sub-region": "Western Asia", "Intermediate Region": ""},
    "Australia": {"Region": "Oceania", "Sub-region": "Australia and New Zealand", "Intermediate Region": ""},
    "Austria": {"Region": "Europe", "Sub-region": "Western Europe", "Intermediate Region": ""},
    "Bahamas": {"Region": "Americas", "Sub-region": "Caribbean", "Intermediate Region": ""},
    "Bahrain": {"Region": "Asia", "Sub-region": "Western Asia", "Intermediate Region": ""},
    "Bangladesh": {"Region": "Asia", "Sub-region": "Southern Asia", "Intermediate Region": ""},
    "Barbados": {"Region": "Americas", "Sub-region": "Caribbean", "Intermediate Region": ""},
    "Belarus": {"Region": "Europe", "Sub-region": "Eastern Europe", "Intermediate Region": ""},
    "Belgium": {"Region": "Europe", "Sub-region": "Western Europe", "Intermediate Region": ""},
    "Belize": {"Region": "Americas", "Sub-region": "Central America", "Intermediate Region": ""},
    "Benin": {"Region": "Africa", "Sub-region": "Western Africa", "Intermediate Region": ""},
    "Bermuda": {"Region": "Americas", "Sub-region": "Northern America", "Intermediate Region": ""},
    "Bolivia": {"Region": "Americas", "Sub-region": "South America", "Intermediate Region": ""},
    "Bosnia and Herzegovina": {"Region": "Europe", "Sub-region": "Southern Europe", "Intermediate Region": ""},
    "Botswana": {"Region": "Africa", "Sub-region": "Southern Africa", "Intermediate Region": ""},
    "Brazil": {"Region": "Americas", "Sub-region": "South America", "Intermediate Region": ""},
    "Brunei": {"Region": "Asia", "Sub-region": "South-Eastern Asia", "Intermediate Region": ""},
    "Bulgaria": {"Region": "Europe", "Sub-region": "Eastern Europe", "Intermediate Region": ""},
    "Cambodia": {"Region": "Asia", "Sub-region": "South-Eastern Asia", "Intermediate Region": ""},
    "Canada": {"Region": "Americas", "Sub-region": "Northern America", "Intermediate Region": ""},
    "Cape Verde": {"Region": "Africa", "Sub-region": "Western Africa", "Intermediate Region": ""},
    "Chile": {"Region": "Americas", "Sub-region": "South America", "Intermediate Region": ""},
    "Colombia": {"Region": "Americas", "Sub-region": "South America", "Intermediate Region": ""},
    "Cook Islands": {"Region": "Oceania", "Sub-region": "Polynesia", "Intermediate Region": ""},
    "Costa Rica": {"Region": "Americas", "Sub-region": "Central America", "Intermediate Region": ""},
    "Ivory Coast": {"Region": "Africa", "Sub-region": "Western Africa", "Intermediate Region": ""},
    "Croatia": {"Region": "Europe", "Sub-region": "Southern Europe", "Intermediate Region": ""},
    "Cuba": {"Region": "Americas", "Sub-region": "Caribbean", "Intermediate Region": ""},
    "Cyprus": {"Region": "Asia", "Sub-region": "Western Asia", "Intermediate Region": ""},
    "Czech Republic": {"Region": "Europe", "Sub-region": "Eastern Europe", "Intermediate Region": ""},
    "Denmark": {"Region": "Europe", "Sub-region": "Northern Europe", "Intermediate Region": ""},
    "Dominican Republic": {"Region": "Americas", "Sub-region": "Caribbean", "Intermediate Region": ""},
    "Ecuador": {"Region": "Americas", "Sub-region": "South America", "Intermediate Region": ""},
    "Egypt": {"Region": "Africa", "Sub-region": "Northern Africa", "Intermediate Region": ""},
    "El Salvador": {"Region": "Americas", "Sub-region": "Central America", "Intermediate Region": ""},
    "England": {"Region": "Europe", "Sub-region": "Northern Europe", "Intermediate Region": ""},
    "Estonia": {"Region": "Europe", "Sub-region": "Northern Europe", "Intermediate Region": ""},
    "Ethiopia": {"Region": "Africa", "Sub-region": "Eastern Africa", "Intermediate Region": ""},
    "Falkland Islands": {"Region": "Americas", "Sub-region": "South America", "Intermediate Region": ""},
    "Faroe Islands": {"Region": "Europe", "Sub-region": "Northern Europe", "Intermediate Region": ""},
    "Fiji": {"Region": "Oceania", "Sub-region": "Melanesia", "Intermediate Region": ""},
    "Finland": {"Region": "Europe", "Sub-region": "Northern Europe", "Intermediate Region": ""},
    "France": {"Region": "Europe", "Sub-region": "Western Europe", "Intermediate Region": ""},
    "Gabon": {"Region": "Africa", "Sub-region": "Central Africa", "Intermediate Region": ""},
    "Germany": {"Region": "Europe", "Sub-region": "Western Europe", "Intermediate Region": ""},
    "Ghana": {"Region": "Africa", "Sub-region": "Western Africa", "Intermediate Region": ""},
    "Greece": {"Region": "Europe", "Sub-region": "Southern Europe", "Intermediate Region": ""},
    "Greenland": {"Region": "Americas", "Sub-region": "Northern America", "Intermediate Region": ""},
    "Guatemala": {"Region": "Americas", "Sub-region": "Central America", "Intermediate Region": ""},
    "Hungary": {"Region": "Europe", "Sub-region": "Eastern Europe", "Intermediate Region": ""},
    "Iceland": {"Region": "Europe", "Sub-region": "Northern Europe", "Intermediate Region": ""},
    "India": {"Region": "Asia", "Sub-region": "Southern Asia", "Intermediate Region": ""},
    "Indonesia": {"Region": "Asia", "Sub-region": "South-Eastern Asia", "Intermediate Region": ""},
    "Iran": {"Region": "Asia", "Sub-region": "Southern Asia", "Intermediate Region": ""},
    "Iraq": {"Region": "Asia", "Sub-region": "Western Asia", "Intermediate Region": ""},
    "Ireland": {"Region": "Europe", "Sub-region": "Northern Europe", "Intermediate Region": ""},
    "Israel": {"Region": "Asia", "Sub-region": "Western Asia", "Intermediate Region": ""},
    "Italy": {"Region": "Europe", "Sub-region": "Southern Europe", "Intermediate Region": ""},
    "Jamaica": {"Region": "Americas", "Sub-region": "Caribbean", "Intermediate Region": ""},
    "Japan": {"Region": "Asia", "Sub-region": "Eastern Asia", "Intermediate Region": ""},
    "Jordan": {"Region": "Asia", "Sub-region": "Western Asia", "Intermediate Region": ""},
    "Kazakhstan": {"Region": "Asia", "Sub-region": "Central Asia", "Intermediate Region": ""},
    "Kenya": {"Region": "Africa", "Sub-region": "Eastern Africa", "Intermediate Region": ""},
    "Kuwait": {"Region": "Asia", "Sub-region": "Western Asia", "Intermediate Region": ""},
    "Laos": {"Region": "Asia", "Sub-region": "South-Eastern Asia", "Intermediate Region": ""},
    "Latvia": {"Region": "Europe", "Sub-region": "Northern Europe", "Intermediate Region": ""},
    "Lebanon": {"Region": "Asia", "Sub-region": "Western Asia", "Intermediate Region": ""},
    "Lesotho": {"Region": "Africa", "Sub-region": "Southern Africa", "Intermediate Region": ""},
    "Lithuania": {"Region": "Europe", "Sub-region": "Northern Europe", "Intermediate Region": ""},
    "Luxembourg": {"Region": "Europe", "Sub-region": "Western Europe", "Intermediate Region": ""},
    "Malaysia": {"Region": "Asia", "Sub-region": "South-Eastern Asia", "Intermediate Region": ""},
    "Maldives": {"Region": "Asia", "Sub-region": "Southern Asia", "Intermediate Region": ""},
    "Malta": {"Region": "Europe", "Sub-region": "Southern Europe", "Intermediate Region": ""},
    "Mauritius": {"Region": "Africa", "Sub-region": "Eastern Africa", "Intermediate Region": ""},
    "Mexico": {"Region": "Americas", "Sub-region": "Central America", "Intermediate Region": ""},
    "Moldova": {"Region": "Europe", "Sub-region": "Eastern Europe", "Intermediate Region": ""},
    "Monaco": {"Region": "Europe", "Sub-region": "Western Europe", "Intermediate Region": ""},
    "Mongolia": {"Region": "Asia", "Sub-region": "Eastern Asia", "Intermediate Region": ""},
    "Montenegro": {"Region": "Europe", "Sub-region": "Southern Europe", "Intermediate Region": ""},
    "Morocco": {"Region": "Africa", "Sub-region": "Northern Africa", "Intermediate Region": ""},
    "Mozambique": {"Region": "Africa", "Sub-region": "Eastern Africa", "Intermediate Region": ""},
    "Myanmar": {"Region": "Asia", "Sub-region": "South-Eastern Asia", "Intermediate Region": ""},
    "Namibia": {"Region": "Africa", "Sub-region": "Southern Africa", "Intermediate Region": ""},
    "Nepal": {"Region": "Asia", "Sub-region": "Southern Asia", "Intermediate Region": ""},
    "Netherlands": {"Region": "Europe", "Sub-region": "Western Europe", "Intermediate Region": ""},
    "New Zealand": {"Region": "Oceania", "Sub-region": "Australia and New Zealand", "Intermediate Region": ""},
    "Nicaragua": {"Region": "Americas", "Sub-region": "Central America", "Intermediate Region": ""},
    "Nigeria": {"Region": "Africa", "Sub-region": "Western Africa", "Intermediate Region": ""},
    "Northern Ireland": {"Region": "Europe", "Sub-region": "Northern Europe", "Intermediate Region": ""},
    "North Korea": {"Region": "Asia", "Sub-region": "Eastern Asia", "Intermediate Region": ""},
    "North Macedonia": {"Region": "Europe", "Sub-region": "Southern Europe", "Intermediate Region": ""},
    "Norway": {"Region": "Europe", "Sub-region": "Northern Europe", "Intermediate Region": ""},
    "Oman": {"Region": "Asia", "Sub-region": "Western Asia", "Intermediate Region": ""},
    "Pakistan": {"Region": "Asia", "Sub-region": "Southern Asia", "Intermediate Region": ""},
    "Palestine": {"Region": "Asia", "Sub-region": "Western Asia", "Intermediate Region": ""},
    "Panama": {"Region": "Americas", "Sub-region": "Central America", "Intermediate Region": ""},
    "Paraguay": {"Region": "Americas", "Sub-region": "South America", "Intermediate Region": ""},
    "China": {"Region": "Asia", "Sub-region": "Eastern Asia", "Intermediate Region": ""},
    "Peru": {"Region": "Americas", "Sub-region": "South America", "Intermediate Region": ""},
    "Philippines": {"Region": "Asia", "Sub-region": "South-Eastern Asia", "Intermediate Region": ""},
    "Poland": {"Region": "Europe", "Sub-region": "Eastern Europe", "Intermediate Region": ""},
    "Portugal": {"Region": "Europe", "Sub-region": "Southern Europe", "Intermediate Region": ""},
    "Qatar": {"Region": "Asia", "Sub-region": "Western Asia", "Intermediate Region": ""},
    "Romania": {"Region": "Europe", "Sub-region": "Eastern Europe", "Intermediate Region": ""},
    "Russia": {"Region": "Europe", "Sub-region": "Eastern Europe", "Intermediate Region": ""},
    "Saudi Arabia": {"Region": "Asia", "Sub-region": "Western Asia", "Intermediate Region": ""},
    "Scotland": {"Region": "Europe", "Sub-region": "Northern Europe", "Intermediate Region": ""},
    "Senegal": {"Region": "Africa", "Sub-region": "Western Africa", "Intermediate Region": ""},
    "Serbia": {"Region": "Europe", "Sub-region": "Southern Europe", "Intermediate Region": ""},
    "Singapore": {"Region": "Asia", "Sub-region": "South-Eastern Asia", "Intermediate Region": ""},
    "Slovakia": {"Region": "Europe", "Sub-region": "Eastern Europe", "Intermediate Region": ""},
    "Slovenia": {"Region": "Europe", "Sub-region": "Southern Europe", "Intermediate Region": ""},
    "Solomon Islands": {"Region": "Oceania", "Sub-region": "Melanesia", "Intermediate Region": ""},
    "South Africa": {"Region": "Africa", "Sub-region": "Southern Africa", "Intermediate Region": ""},
    "South Korea": {"Region": "Asia", "Sub-region": "Eastern Asia", "Intermediate Region": ""},
    "Spain": {"Region": "Europe", "Sub-region": "Southern Europe", "Intermediate Region": ""},
    "Sri Lanka": {"Region": "Asia", "Sub-region": "Southern Asia", "Intermediate Region": ""},
    "Sweden": {"Region": "Europe", "Sub-region": "Northern Europe", "Intermediate Region": ""},
    "Switzerland": {"Region": "Europe", "Sub-region": "Western Europe", "Intermediate Region": ""},
    "Taiwan": {"Region": "Asia", "Sub-region": "Eastern Asia", "Intermediate Region": ""},
    "Tanzania": {"Region": "Africa", "Sub-region": "Eastern Africa", "Intermediate Region": ""},
    "Thailand": {"Region": "Asia", "Sub-region": "South-Eastern Asia", "Intermediate Region": ""},
    "Trinidad and Tobago": {"Region": "Americas", "Sub-region": "Caribbean", "Intermediate Region": ""},
    "Tunisia": {"Region": "Africa", "Sub-region": "Northern Africa", "Intermediate Region": ""},
    "Turkey": {"Region": "Asia", "Sub-region": "Western Asia", "Intermediate Region": ""},
    "United Arab Emirates": {"Region": "Asia", "Sub-region": "Western Asia", "Intermediate Region": ""},
    "Uganda": {"Region": "Africa", "Sub-region": "Eastern Africa", "Intermediate Region": ""},
    "Ukraine": {"Region": "Europe", "Sub-region": "Eastern Europe", "Intermediate Region": ""},
    "Uruguay": {"Region": "Americas", "Sub-region": "South America", "Intermediate Region": ""},
    "United States": {"Region": "Americas", "Sub-region": "Northern America", "Intermediate Region": ""},
    "Uzbekistan": {"Region": "Asia", "Sub-region": "Central Asia", "Intermediate Region": ""},
    "Vanuatu": {"Region": "Oceania", "Sub-region": "Melanesia", "Intermediate Region": ""},
    "Venezuela": {"Region": "Americas", "Sub-region": "South America", "Intermediate Region": ""},
    "Vietnam": {"Region": "Asia", "Sub-region": "South-Eastern Asia", "Intermediate Region": ""},
    "Wales": {"Region": "Europe", "Sub-region": "Northern Europe", "Intermediate Region": ""},
    "Zambia": {"Region": "Africa", "Sub-region": "Eastern Africa", "Intermediate Region": ""}
}


def extract_country_details(address):
    for keyword, country in country_mapping.items():
        if keyword in address:
            country_details = detailed_country_mapping.get(country, {"Region": "Unknown", "Sub-region": "Unknown", "Intermediate Region": "Unknown"})
            return {
                "Country": country,
                "Region": country_details["Region"],
                "Sub-region": country_details["Sub-region"],
                "Intermediate Region": country_details["Intermediate Region"]
            }
    return {
        "Country": "Unknown",
        "Region": "Unknown",
        "Sub-region": "Unknown",
        "Intermediate Region": "Unknown"
    }


def connect_authors_with_institutions(authors_info, institution_info, names_info):
    authors_with_institutions = []
    
    # Check if 'authors' exists; otherwise, handle 'anonymous'
    author_list = names_info.get("authors", [])
    if not author_list and "anonymous" in names_info:
        authors_with_institutions.append({
            "displayName": "[Anonymous]"
        })
        return authors_with_institutions
    
    # Build a lookup dictionary for names_info based on displayName
    names_lookup = {name.get("displayName"): name for name in author_list}

    # Process individual authors (if authors exist)
    for author in authors_info:
        full_name = author.get("full_name")
        if full_name and full_name in names_lookup:
            name_info = names_lookup[full_name]
            author_entry = {
                "displayName": name_info.get("displayName"),
                "wosStandard": name_info.get("wosStandard"),
                "researcherId": name_info.get("researcherId"),
                "related_institutions": []
            }

            # Collect related institutions for authors
            for inst in institution_info:
                # Remove "Institution " from the identifier to match the institution_id format
                institution_id = inst["institution_identifier"].replace("Institucion ", "")
                author_address_ids = author.get("address_ids", [])
                
                # Ensure correct institution matching using address_ids
                if institution_id in author_address_ids:
                    author_entry["related_institutions"].append({
                        "institution_identifier": inst["institution_identifier"]
                    })
                                        
            # Append the processed author with institutions
            authors_with_institutions.append(author_entry)

    return authors_with_institutions

def connect_corps_with_institutions(corps_info, institution_info, names_info):
    corps_with_institutions = []
    
    # Check if 'corps' exists
    corps_list = names_info.get("corp", [])
    print("corps_list: ", corps_list)
    if not corps_list:
        return corps_with_institutions  # Return empty if no corps data

    # Build a lookup dictionary for names_info based on displayName
    names_lookup = {name.get("displayName"): name for name in corps_list}
    print("names_lookup = ", names_lookup)   
    # Process individual group authors (corps)
    for corp in corps_info:
        display_name = corp.get("display_name")
        print("display_name = ", display_name)
        if display_name and display_name in names_lookup:
            print("chegou aqui 2")    
            name_info = names_lookup[display_name]
            corp_entry = {
                "displayName": name_info.get("displayName"),
                "related_institutions": []
            }

            # Collect related institutions for corp authors
            for inst in institution_info:
                institution_id = inst["institution_identifier"].replace("Institucion ", "")
                if institution_id in corp.get("address_ids", []):
                    corp_entry["related_institutions"].append({
                        "institution_identifier": inst["institution_identifier"]
                    })
            
            corps_with_institutions.append(corp_entry)

    return corps_with_institutions

    
def login_to_periodico_capes(navegador, username, password):
    try:
        # Wait for the institution dropdown to load
        WebDriverWait(navegador, 60).until(
            EC.presence_of_element_located((By.ID, 'info-t'))
        )
        print(f"Current URL (Institution Selection): {navegador.current_url}")
                
        input_field = navegador.find_element(By.ID, 'select-simple')
        input_field.send_keys('UFSCAR')

        select_element = navegador.find_element(By.CSS_SELECTOR, 'label[for="UFSCAR"]')
        if 'UFSCAR' in select_element.text:
            print("chegou ufscar")
            select_element.click()
                            
        # Locate the button
        enviar_button = navegador.find_element(By.ID, 'enviarInstituicaoCafe')

        
        # Click on the 'Enviar' button
        enviar_button = WebDriverWait(navegador, 20).until(
            EC.element_to_be_clickable((By.ID, 'enviarInstituicaoCafe')))
        
        enviar_button.click()
        
        print(f"Current URL (After Institution Submission): {navegador.current_url}")
        
        # Wait for the login form to load
        WebDriverWait(navegador, 20).until(
            EC.presence_of_element_located((By.ID, 'form')))
        
        # Wait for the username field and input username
        username_field = WebDriverWait(navegador, 20).until(
            EC.presence_of_element_located((By.ID, 'username')))
        username_field.send_keys(username)
        
        # Input password
        password_field = navegador.find_element(By.ID, 'password')
        password_field.send_keys(password)

        # Submit the form by clicking the login button
        login_button = navegador.find_element(By.NAME, '_eventId_proceed')
        
        print(f"Current URL (Before Login Button Click): {navegador.current_url}")
        login_button.click()
        
        print(f"Current URL (After Login Button Click): {navegador.current_url}")

        # Wait for the page to load and confirm successful login by checking the specific <p> element
        confirmation_message = WebDriverWait(navegador, 20).until(
            EC.presence_of_element_located((By.XPATH, "//p[contains(., 'UFSCAR')]"))
        )
        
        if confirmation_message:
            print("Login successful. You are accessing the portal through UFSCAR.")
        else:
            print("Login failed. UFSCAR confirmation not found.")
        
    except Exception as e:
        print(f"An error occurred during login: {str(e)}")


# Function to wait for a specific element to load (to ensure JS has rendered content)
def wait_for_page_to_load(navegador):
    try:
        # Wait for a specific element that only exists on the fully-loaded page
        WebDriverWait(navegador, 60).until(
            EC.presence_of_element_located((By.ID, "highcharts-screen-reader-region-before-0"))
        )
        
        print("achou!!!!")
        
    except Exception as e:
        return False
    return True


chromeOptions = webdriver.ChromeOptions()
chromeOptions.binary_location = "./chrome-win64/chrome.exe"
chromeOptions.add_argument('--no-sandbox')
#chromeOptions.add_argument('--headless')
chromeService = webdriver.ChromeService(executable_path="./chromedriver-win64/chromedriver.exe")
navegador = webdriver.Chrome(options=chromeOptions, service=chromeService)

#navegador.get("https://www-periodicos-capes-gov-br.ezl.periodicos.capes.gov.br/index.php/acesso-cafe.html")
navegador.get("https://www.periodicos.capes.gov.br/index.php/acesso-cafe.html")

# Call the login function before iterating through articles
login_to_periodico_capes(navegador, "792188", "Rea!madrid0509")
# URL do endpoint da API
url = 'https://api.clarivate.com/apis/wos-starter/v1/documents'

# Header da requisição, vai com a chave da API
headers = {'X-ApiKey': '4172888afda8e2ae845747596c418a64f9c6585f'}

limit_per_page = 50  # Max limit per page
total_results = 13170  # Total articles from Web of Science response

# Calculate total pages required
total_pages = (total_results // limit_per_page) + 1

# Placeholder to store all articles
all_articles_data = []

#page_atual = 154
        
for page in range(1, total_pages + 1):
    # Set up parameters for the API request
    params = {
        'q': "(TI=(microplastic* or nanoplastic* not microplasticity or nanoplasticity not microplasticity)) AND (PY==(2023 OR 2022 OR 2021 OR 2020 OR 2019 OR 2018 OR 2017 OR 2016 OR 2015 OR 2014))",
        'limit': limit_per_page,
        'page': page
    }
    
    # Resposta da API da Wos
    articlesResponse = (req.get(url, headers=headers, params=params)).json()


    for article in articlesResponse["hits"]:
        # Pegando o link de cada artigo
        articleLink = article["links"]["record"]
        
        # Extracting KeyUT from the original URL
        key_ut = articleLink.split("KeyUT=")[1].split("&")[0]  # Extract the KeyUT value
        
        # Construct the new URL
        institutional_url = f"https://www-webofscience-com.ez31.periodicos.capes.gov.br/wos/woscc/full-record/{key_ut}" 
        
        # Abrindo navegador no artigo
        navegador.get(institutional_url)
        
        print("Current URL: ", navegador.current_url)
        
        # Wait for the page to load completely (e.g., JavaScript-rendered content)
        wait_for_page_to_load(navegador)
        
        # Abrindo navegador no artigo
        sleep(2)


        # Buscando HTML
        website = BeautifulSoup(navegador.page_source, 'html.parser')
        # Usando BeautifulSoup para extrair informações
        soup = BeautifulSoup(navegador.page_source, 'html.parser')
            
        # Initialize an empty list to store the extracted information
        authors_info = []

        # Find the div containing all the authors' information
        authors_div = website.find('div', id='SumAuthTa-MainDiv-author-en')
        # Check if the authors' div is found
        if authors_div:
            # Find all the individual author elements within the div
            authors = authors_div.find_all('span', class_='value ng-star-inserted')
            
            for author in authors:
                # Extract the full name
                full_name_element = author.find('span', id=lambda x: x and x.startswith('SumAuthTa-FrAuthStandard-author-en'))
                if full_name_element:
                    full_name = full_name_element.find('span', class_= 'value section-label-data').text.strip()
                else:
                    full_name = None
                
                # Extract all the address identifiers
                address_ids = []
                address_elements = author.find_all('a', id=lambda x: x and x.startswith('SumAuthTa-FrAddrNbr-author-en'))
                for address_element in address_elements:
                    # Extract the address identifier number from the text
                    address_id = re.sub(r'[^\d]', '', address_element.text.strip())  # Keep only numbers
                    if address_id:
                        address_ids.append(address_id)
                
                # Store the extracted information in the list
                authors_info.append({
                    #"display_name": display_name,
                    "full_name": full_name,
                    "address_ids": address_ids
                })

        
        # Initialize an empty list to store the extracted information
        corps_info = []

        # Find the div containing all the authors' information
        corps_div = website.find('div', id='SumAuthTa-MainDiv-corp-en')
        # Check if the authors' div is found
        if corps_div:
            # Find all the individual author elements within the div
            corps = corps_div.find_all('span', class_='value ng-star-inserted')
            
            for corp in corps:
                # Extract the displayed name
                corp_display_name_element = corp.find('a', id=lambda x: x and x.startswith('SumAuthTa-DisplayName-corp-en'))
                if corp_display_name_element:
                    corp_display_name = corp_display_name_element.text.strip()
                else:
                    corp_display_name = None
                
                # Extract all the address identifiers
                corp_address_ids = []
                corps_address_elements = corp.find_all('a', id=lambda x: x and x.startswith('SumAuthTa-FrAddrNbr-corp-en'))
                for corp_address_element in corps_address_elements:
                    # Extract the address identifier number from the text
                    corp_address_id = re.sub(r'[^\d]', '', corp_address_element.text.strip())  # Keep only numbers
                    if corp_address_id:
                        corp_address_ids.append(corp_address_id)
                
                # Store the extracted information in the list
                corps_info.append({
                    "display_name": corp_display_name,
                    "address_ids": corp_address_ids
                })
      
        
        # Buscando a div que está o abstract
        divAbstract = website.find('div', attrs={'class': 'abstract--instance'})
        # Pegando o abstract
        if divAbstract:
            abstract = divAbstract.find('p')
            if abstract:
                article["abstract"] = abstract.text

        # Pegando a data de publicação
        pub_date_element = website.find('span', attrs={'data-ta': 'FullRTa-pubdate'})
        if pub_date_element:
            pub_date_text = pub_date_element.text.strip()
            try:
                # Tenta converter o texto em data
                pub_date = datetime.strptime(pub_date_text, '%b %d %Y').strftime('%Y-%m-%d')
            except ValueError:
                try:
                    # Em caso de ter apenas o mês e ano, tenta converter para data usando o dia como 1
                    pub_date = datetime.strptime(pub_date_text, '%b %Y').strftime('%Y-%m-%d')
                except ValueError:
                    pub_date = None  # se não for nenhum dos casos, apenas adiciona a data como vazia

            article["publication_date"] = pub_date
        
        # Pegando a data de indexação
        indexDate = website.find('span', attrs={'data-ta': 'FullRTa-indexedDate'})
        print("data de index = ",indexDate)
        if indexDate:
            article["index_date"] = indexDate.text
        
        # Pegando a linguagem do artigo
        language = website.find('span', attrs={'data-ta': 'HiddenSecTa-language-0'})
        if language:
            article["language"] = language.text
        
        # Pegando o IDS Number
        idsNumber = website.find('span', attrs={'data-ta': 'HiddenSecTa-recordIds'})
        if idsNumber:
            article["ids_number"] = idsNumber.text
            
        # Pegando as palavras chaves plus
        i = 0
        baseIdKeywordSpan = 'FRkeywordsTa-keyWordsPlusLink-'
        plusKeywords = []
        while True:
            idKeyWordSpan = baseIdKeywordSpan + str(i)
            keywordLabel = website.find('a', id=idKeyWordSpan)
            if not keywordLabel:
                break

            keyword = keywordLabel.find('span')

            if keyword:
                plusKeywords.append((keyword.text).lower())

            i = i + 1

        article["keywords"]["plusKeywords"] = plusKeywords

        # Pegando as categorias do Web of Science
        wos_categories = []
        #baseIdCategorySpan = 'CategoriesTa-WOSCategory-'
        categories = website.find_all('a', attrs={'data-ta': lambda x: x and x.startswith('CategoriesTa-WOSCategory-')})
        for category in categories:
            category_text = category.find('span')
            if category_text:
                wos_categories.append(category_text.text.strip())

        article["wos_categories"] = wos_categories

        # Pegando as categorias/classificações
        categories_section = website.find('div', class_='catg-classification-section ng-star-inserted')
        if categories_section:
            categories = {}
            research_areas = []
            citation_topics = []

            # Research Areas
            research_areas_section = categories_section.find_all('span', attrs={'data-ta': lambda x: x and x.startswith('CategoriesTa-subject-')})
            for area in research_areas_section:
                research_areas.append(area.text.strip())
            
            categories["research_areas"] = research_areas
            
            # Citation Topics
            citation_topics_section = categories_section.find_all('a', attrs={'data-ta': lambda x: x and x.startswith('CategoriesTa-citationTopic-')})
            for topic in citation_topics_section:
                topic_text = topic.text.strip()
                # Split the text and keep only the part after the first space
                clean_topic = ' '.join(topic_text.split(' ')[1:])
                citation_topics.append(clean_topic)
            
            categories["citation_topics"] = citation_topics

            article["categories"] = categories
        
        # Initialize a list to hold the corresponding addresses
        corresponding_addresses = {}
            
        # Find all corresponding address sections
        c_addresses = website.find_all('div', id=lambda x: x and x.startswith('FRAiinTa-RepAddrTitle'))

        # Extract the information
        for c_address in c_addresses:
            try:
                author_name = c_address.find('span', class_='value').text.strip()
                corresponding_addresses["author_name"] = author_name
                
                full_address = c_address.find('span', attrs={'data-ta': lambda x: x and x.startswith('FRAOrgTa-RepAddressFull')}).text.strip()
                corresponding_addresses["full_address"] = full_address
                
                # Extract country details
                corresponding_ad_country_details = extract_country_details(full_address)
                corresponding_addresses["country"] = corresponding_ad_country_details["Country"]
                corresponding_addresses["region"] = corresponding_ad_country_details["Region"]
                corresponding_addresses["sub_region"] = corresponding_ad_country_details["Sub-region"]
                corresponding_addresses["intermediate_region"] = corresponding_ad_country_details["Intermediate Region"]
                
                # Try to find the affiliation if it exists
                affiliation_div = c_address.find_next('div', hidden=True)
                affiliation_name = affiliation_div.find('div',attrs={'data-ta': lambda x: x and x.startswith('FRAOrgTa-RepOrgEnhancedName')}).text.strip() if affiliation_div else 'N/A'
                
                corresponding_addresses["affiliation"] = affiliation_name
                
            except AttributeError as e:
                print(f"An error occurred while processing an address: {e}")

        # Add the corresponding addresses to the article dictionary
        article['corresponding_addresses'] = corresponding_addresses


        # Initialize list to store institution information
        inst = []
        # Primeiro, encontre o elemento <app-full-record-addresses-data>
        address_data_section = website.find('app-full-record-addresses-data')

        if address_data_section:
            # Agora, encontre a div específica dentro desse contexto
            author_info_section = address_data_section.find('div', class_='author-info-section')

            if author_info_section:
                institucion_counter = 1

                # Find all author organization items
                institucion_items = author_info_section.find_all('app-full-record-author-organization')

                for item in institucion_items:
                    # Initialize dictionary to store each author's information
                    institucion_info = {}
                    institucion_info["institution_identifier"] = f"Institucion {institucion_counter}"

                    # Find the address
                    address_tag = item.find('a', class_='no-underline-link margin-left-30--reversible ng-star-inserted')
                    if address_tag:
                        address_span = address_tag.find('span', class_='value padding-right-5--reversible section-label-data')
                        if address_span:
                            address = address_span.text.strip()
                            institucion_info["address"] = address
                            
                            # Extract country details
                            country_details = extract_country_details(address)
                            institucion_info["country"] = country_details["Country"]
                            institucion_info["region"] = country_details["Region"]
                            institucion_info["sub_region"] = country_details["Sub-region"]
                            institucion_info["intermediate_region"] = country_details["Intermediate Region"]

                    # Find affiliations
                    affiliations_divs = item.find_all('div', attrs={'data-ta': lambda value: value and value.startswith('FRAOrgTa-RepOrgEnhancedName-addresses')})
                    affiliations = [aff.text.strip() for aff in affiliations_divs]
                    institucion_info["affiliations"] = affiliations

                    # Add author's information to the list
                    inst.append(institucion_info)
                    institucion_counter += 1

                # Add the list of author information to the article
                article["institucion_info"] = inst


        # Extract "Use in Web of Science" information
        use_in_wos = {}
        usage_180day = website.find('div', attrs={'data-ta': 'FullRRPTa-um-related-180day'})
        if usage_180day:
            use_in_wos['last_180_days'] = usage_180day.text.strip()

        usage_alltime = website.find('div', attrs={'data-ta': 'FullRRPTa-um-related-AllTime'})
        if usage_alltime:
            use_in_wos['since_2013'] = usage_alltime.text.strip()

        article["use_in_wos"] = use_in_wos
        
        # Extract "Times Cited in All Databases" information
        times_cited_all_db = website.find('a', attrs={'data-ta': 'FullRRPTa-wos-citation-network-times-cited-count-link-ALLDB'})
        if times_cited_all_db:
            times_cited_text = times_cited_all_db.find('span', attrs={'data-ta': 'FullRRPTa-citationsLabelPlural-ALLDB'})
            if times_cited_text:
                article["times_cited_all_db"] = times_cited_text.text.strip()
        
        # Extract "Cited References" information
        cited_references = website.find('a', id='FullRRPTa-wos-citation-network-refCountLink')
        if cited_references:
            article["cited_references"] = cited_references.text.strip()
        
        
        # Initialize the journal dictionary
        journal_information = {}

        # Extract the Journal Name
        journal_name_elem = website.find('h2', attrs={'data-ta': 'jcrSidenav-1-main-header'})
        if journal_name_elem:
            journal_information['Journal Name'] = journal_name_elem.text.strip()

        # Extract the ISSN
        issn_elem = website.find('div', class_='journal-content-row margin-top-5 cdx-two-column-grid-container ng-star-inserted')
        if issn_elem:
            issn_elem_text = issn_elem.find('span',class_='value section-label-data text-color')
            if issn_elem_text:
                journal_information['Journal ISSN'] = issn_elem_text.text.strip()
                
        journal_itens = website.find_all('div', class_='journal-content-row cdx-two-column-grid-container ng-star-inserted')

        # Extract the information
        for journal_item in journal_itens:
        
            # Extract eISSN
            eissn_heading = journal_item.find('h3', class_='label cdx-grid-label')
            if eissn_heading and 'eISSN' in eissn_heading.text:
                eissn_value = journal_item.find('span', class_='value section-label-data text-color')
                if eissn_value:
                    journal_information["Journal eISSN"] = eissn_value.text.strip()
                continue  # Skip to the next item if eISSN is found

            # Extract Current Publisher
            publisher_heading = journal_item.find('h3', class_='label cdx-grid-label')
            if publisher_heading and 'Current Publisher' in publisher_heading.text:
                publisher_info = journal_item.find_all('span', class_='section-label-data text-color')
                if publisher_info:
                    journal_information["Journal Current Publisher"] = ''.join([info.text.strip() for info in publisher_info])
                continue  # Skip to the next item if Current Publisher is found
            
            # Extract Journal Impact Factor
            journal_imp_factor_heading = journal_item.find('h3', class_='label cdx-grid-label')
            if journal_imp_factor_heading and 'Journal Impact Factor' in journal_imp_factor_heading.text:
                journal_imp_factor_info = journal_item.find('a', class_='value section-label-data full-record-detail-section-links')
                if journal_imp_factor_info:
                    journal_information["Journal Impact Factor"] = journal_imp_factor_info.text.strip()
                continue  # Skip to the next item if Journal Impact Factor is found

            # Extract Journal Research Areas
            research_areas_heading = journal_item.find('h3', class_='label cdx-grid-label')
            if research_areas_heading and 'Research Areas' in research_areas_heading.text:
                research_areas_info = journal_item.find_all('span', class_='ng-star-inserted')
                if research_areas_info:
                    journal_information["Journal Research Areas"] = '; '.join([area.text.strip() for area in research_areas_info])
                continue  # Skip to the next item if Research Areas are found

            # Extract Journal's Web of Science Categories
            wos_categories_heading = journal_item.find('h3', class_='label cdx-grid-label')
            if wos_categories_heading and 'Web of Science Categories' in wos_categories_heading.text:
                wos_categories_info = journal_item.find_all('span', class_='ng-star-inserted')
                if wos_categories_info:
                    journal_information["Journal Web of Science Categories"] = '; '.join([category.text.strip() for category in wos_categories_info])
            

        # Extrair o Journal Impact Factor de 2023
        impact_factor_2023_elem = website.find('div', id='Sidenav-1-JCR-value')
        if impact_factor_2023_elem:
            journal_information['Journal Impact Factor (2023)'] = impact_factor_2023_elem.text.strip()

        # Extrair o Journal Impact Factor (JIF) de 5 anos
        five_year_jif_elem = website.find('div', id='Sidenav-1-JCR-journal-value')
        if five_year_jif_elem:
            journal_information['5-Year Journal Impact Factor'] = five_year_jif_elem.text.strip()

        # Extrair o Journal Citation Indicator (JCI)
        jci_2022_elem = website.find('div', id='Sidenav-1-JCI-journal-value')
        if jci_2022_elem:
            journal_information['Journal Citation Indicator (2022)'] = jci_2022_elem.text.strip()

        # Extrair o Journal Citation Indicator de 2023
        jci_2023_elem = website.find('div', id='Sidenav-1-JCI-value')
        if jci_2023_elem:
            journal_information['Journal Citation Indicator (2023)'] = jci_2023_elem.text.strip()

        # Extrair informações da categoria JCR
        # Initialize a list to store the extracted JCR categories
        jcr_categories = []

        # Find all category elements with 'data-ta' attributes starting with the base_id_category
        categories = website.find_all('div', attrs={'data-ta': lambda x: x and x.startswith('Sidenav-1-JCR-category-name')})

        # Iterate through each category found
        for index, category in enumerate(categories):
            # Dynamically find the category name, rank, and quartile by constructing the data-ta attribute
            category_name_elem = website.find('div', attrs={'data-ta': f'Sidenav-1-JCR-category-name_{index}'}) 
            category_rank_elem = website.find('td', attrs={'data-ta': f'Sidenav-1-JCR-rank_{index}'})
            category_quartile_elem = website.find('td', attrs={'data-ta': f'Sidenav-1-JCR-quartile_{index}'})

            # Check if all three elements exist before processing
            if category_name_elem and category_rank_elem and category_quartile_elem:
                # Extract and clean the text
                category_name = category_name_elem.text.strip()
                category_rank = category_rank_elem.text.strip()
                category_quartile = category_quartile_elem.text.strip()
                
                # Append the extracted data to the jcr_categories list
                jcr_categories.append({
                    'Category': category_name,
                    'Rank': category_rank,
                    'Quartile': category_quartile
                })

        # Store the extracted JCR categories in the journal_information dictionary
        if jcr_categories:
            journal_information['JCR Categories'] = jcr_categories

        # Extrair informações da categoria JCI
        # Initialize a list to store the extracted JCI categories
        jci_categories = []

        # Find all category elements with 'data-ta' attributes starting with the base_id_category 
        categories_jci = website.find_all('div', attrs={'data-ta': lambda x: x and x.startswith('Sidenav-1-JCI-category-name')}) 

        # Iterate through each category found
        for index, category_jci in enumerate(categories_jci):
            # Dynamically find the category name, rank, and quartile by constructing the data-ta attribute
            category_jci_name_elem = website.find('div', attrs={'data-ta': f'Sidenav-1-JCI-category-name_{index}'})
            category_jci_rank_elem = website.find('td', attrs={'data-ta': f'Sidenav-1-JCI-rank_{index}'}) 
            category_jci_quartile_elem = website.find('td', attrs={'data-ta': f'Sidenav-1-JCI-quartile_{index}'})

            # Check if all three elements exist before processing
            if category_jci_name_elem and category_jci_rank_elem and category_jci_quartile_elem:
                # Extract and clean the text
                category_jci_name = category_jci_name_elem.text.strip()
                category_jci_rank = category_jci_rank_elem.text.strip()
                category_jci_quartile = category_jci_quartile_elem.text.strip()
                
                # Append the extracted data to the jci_categories list
                jci_categories.append({
                    'Category': category_jci_name,
                    'Rank': category_jci_rank,
                    'Quartile': category_jci_quartile
                })

        # Store the extracted JCI categories in the journal_information dictionary
        if jci_categories:
            journal_information['JCI Categories'] = jci_categories
        
        
        # Assign the journal information to the article dictionary
        article['Journal Information'] = journal_information
        
        # Encontrar todos os elementos <rect> que contêm a classificação e os itens citados
        citing_elements = website.find_all('rect', class_='highcharts-point')
        # Inicializar um dicionário para armazenar os citing_items
        citing_items = {}
        if citing_elements:
            for item in citing_elements:
                # Extrair a classificação e o número de citações
                classification = item.get('aria-label').split('classification ')[1].split(' with')[0]
                citing_count = int(item.get('aria-label').split('with ')[1].split(' citing items')[0])

                # Adicionar ao dicionário citing_items
                citing_items[classification] = citing_count

        # Adicionar o dicionário citing_items ao dicionário article
        article['citing_items'] = citing_items
        
        # Conectar autores ou grupos com instituições
        if "authors" in article["names"] or "anonymous" in article["names"]:
            authors_with_institutions = connect_authors_with_institutions(authors_info, inst, article["names"])
            # Adicionar a conexão entre autores e instituições ao dicionário do artigo
            article['authors_with_institutions'] = authors_with_institutions           

        # Verifica separadamente se há grupos (corps)
        if "corp" in article["names"]:
            print("entrou no if 2")
            corps_with_institutions = connect_corps_with_institutions(corps_info, inst, article["names"]) 
            # Adicionar a conexão entre grupos e instituições ao dicionário do artigo
            article['corps_with_institutions'] = corps_with_institutions

                
        # Extract only the "hits" content to avoid extra metadata
        articles_data = articlesResponse.get("hits", [])
        
        with open(f'articles_page_{page}.json', 'w', encoding='utf-8') as f:
            json.dump(articles_data, f, ensure_ascii=False, indent=4)
            
        print(f"Page {page} data saved.")
        
        time.sleep(2)

print("Data export completed.")