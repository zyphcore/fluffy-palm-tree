import requests
from bs4 import BeautifulSoup
import json
import os
from urllib.parse import urljoin
from mimetypes import guess_extension

def fetch_new_books(base_url, output_file="books.json"):
    if os.path.exists(output_file):
        with open(output_file, "r") as file:
            saved_books = json.load(file)  
    else:
        saved_books = []

    saved_titles = {book["title"] for book in saved_books}  

    try:
        response = requests.get(base_url)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error fetching the base URL: {e}")
        return

    soup = BeautifulSoup(response.text, "html.parser")

    edition_box = soup.find("div", class_="editionBox")
    if not edition_box:
        print("No editionBox found on the page.")
        return

    ul_tag = edition_box.find("ul")
    if not ul_tag:
        print("No <ul> tag found in the editionBox.")
        return

    new_books = []  

    for li in ul_tag.find_all("li"):
        link_tag = li.find("a", href=True)
        if link_tag and link_tag["href"].startswith("/artikel"):
            book_url = urljoin(base_url, link_tag["href"])
            print(f"Processing book URL: {book_url}")

            try:
                book_response = requests.get(book_url)
                book_response.raise_for_status()
            except requests.RequestException as e:
                print(f"Error fetching the book URL {book_url}: {e}")
                continue

            book_soup = BeautifulSoup(book_response.text, "html.parser")

            product_container = book_soup.find("div", class_="product-container")
            if not product_container:
                print(f"No product-container found for book URL: {book_url}")
                continue

            img_div = product_container.find("div", class_="boek-product-img")
            if not img_div:
                print(f"No boek-product-img found for book URL: {book_url}")
                continue

            img_tag = img_div.find("img")
            if not img_tag or not img_tag.get("src"):
                print(f"No valid image tag found for book URL: {book_url}")
                continue

            cover_url = urljoin(base_url, img_tag["src"])
            img_folder = "../../assets/img"
            os.makedirs(img_folder, exist_ok=True)

            try:
                img_response = requests.get(cover_url)
                img_response.raise_for_status()
                content_type = img_response.headers.get("Content-Type", "")
                extension = guess_extension(content_type.split(";")[0]) or ".jpg"
            except requests.RequestException as e:
                print(f"Error fetching image {cover_url}: {e}")
                continue

            cover_name = f"{img_folder}/{len(os.listdir(img_folder)) + 34:03}{extension}"

            try:
                with open(cover_name, "wb") as img_file:
                    img_file.write(img_response.content)
                print(f"Saved image: {cover_name}")
            except Exception as e:
                print(f"Error saving image {cover_name}: {e}")
                continue

            detail_container = book_soup.find("div", class_="detail-info-en-info-container")
            if not detail_container:
                print(f"No detail-info-en-info-container found for book URL: {book_url}")
                continue

            boek_info_container = detail_container.find("div", class_="boek-info-container")
            if not boek_info_container:
                print(f"No boek-info-container found for book URL: {book_url}")
                continue

            title_div = boek_info_container.find("div", class_="boek-titel")
            title_tag = title_div.find("h1") if title_div else None
            title = title_tag.text.strip() if title_tag else "Unknown Title"

            if title in saved_titles:
                print(f"Skipping already saved title: {title}")
                continue

            description_div = boek_info_container.find("div", class_="boek-beschrijving")
            description = "".join(description_div.stripped_strings) if description_div else "No description available."

            if not title or not cover_name or not description:
                print(f"Skipping invalid book data for {title}")
                continue

            new_book = { "title": title, "cover": cover_name, "description": description }
            print(f"New book found: {new_book}")

            if title not in saved_titles:
                new_books.append(new_book)  
                saved_titles.add(title)  

    if new_books:
        saved_books.extend(new_books)  

        with open(output_file, "w") as file:
            json.dump(saved_books, file, indent=4)

        print(f"Found {len(new_books)} new books.")
    else:
        print("No new books found.")

fetch_new_books("https://www.hertog.nl/zoeken.aspx?table=Auteur&searchword=Jan+van+den+Dool")