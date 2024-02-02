import tkinter as tk
from googlesearch import search
from bs4 import BeautifulSoup
import requests
import webbrowser
from tkinter import messagebox  # Import messagebox separately

def handle_input(input_text):
    input_text = input_text.strip().lower()
    
    if "wiki" in input_text.lower():
        # Remove the "wiki" keyword and any leading/trailing whitespace
        search_query = input_text.lower().replace("wiki", "").strip()
        # Build the API request URL
        api_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{search_query}"
        # Send the API request
        response = requests.get(api_url)
        if response.status_code == 200:
            # Parse the response JSON to get the summary text
            wiki_result = response.json()["extract"]
            return f"{wiki_result}\n\n"
        else:
            return "I'm sorry, I couldn't find any information on Wikipedia about that."
    else:
        # Perform a Google search and extract titles, links, images, and titles from the search results
        results_list = []
        for url in search(input_text, num=5, stop=5, pause=2):
            response = requests.get(url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                title = soup.title.string if soup.title else "No title available"
                image = soup.find('img')['src'] if soup.find('img') else "No image available"
                results_list.append({"Title": title, "Link": url, "Image": image})
        
        return results_list

def search_button_clicked():
    input_text = entry.get()  # Get the text from the entry widget
    results_text.delete(1.0, tk.END)  # Clear previous results
    results = handle_input(input_text)
    if isinstance(results, list):
        for result in results:
            results_text.insert(tk.END, f"\nTitle: {result['Title']}\n")
            # Create clickable hyperlink
            results_text.insert(tk.END, f"Link: {result['Link']}\n", ("link", result['Link']))
            results_text.insert(tk.END, "\n")
          
               
    else:
        results_text.insert(tk.END, f"\n{results}\n")

# Function to handle hyperlink click
def callback(event):
    webbrowser.open_new(event.widget.tag_names(tk.CURRENT)[1])

# Create the main window
root = tk.Tk()
root.title("TermiSearch")

# Disable full-screen, resizing, and maximizing (haven't fixed this as yet.)
root.attributes("-fullscreen", False)
root.resizable(False, False)

# Create and place widgets
label = tk.Label(root, text="Search:")
label.grid(row=0, column=0, sticky="w", padx=5, pady=5)

entry = tk.Entry(root, width=50)
entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")  # Make the entry widget stretch horizontally

search_button = tk.Button(root, text="Search", command=search_button_clicked)
search_button.grid(row=0, column=2, padx=5, pady=5)

# Function to display information about how to use the application
def show_info():
    info_text = "Welcome to TermiSearch!\n\n"
    info_text += "To use the application, simply enter your search query in the entry field and click the Search button.\n"
    info_text += "You can click on the links provided in the search results to open them in your web browser.\n"
    info_text += "If you want to learn more about a topic, you can type 'wiki' followed by your query to get a summary from Wikipedia.\n"
    info_text += "Enjoy searching!\n"
    tk.messagebox.showinfo("Info", info_text)

# Info button to display information about how to use the application
info_button = tk.Button(root, text="Info", command=show_info)
info_button.grid(row=0, column=3, padx=5, pady=5, sticky="e")  # Make the info button stick to the right side

results_text = tk.Text(root, wrap=tk.WORD, width=80, height=20)
results_text.grid(row=1, column=0, columnspan=4, padx=5, pady=5, sticky="nsew")  # Make the Text widget stretch in all directions

# Bind hyperlink click event
results_text.tag_configure("link", foreground="blue", underline=True)
results_text.bind("<Button-1>", callback)

# Run the main event loop
root.mainloop()

