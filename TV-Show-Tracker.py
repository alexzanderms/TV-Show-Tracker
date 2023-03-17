import tkinter as tk
import requests
from bs4 import BeautifulSoup

# TV shows data structure
tv_shows = []


def add_tv_show():
    tv_show_title = tv_show_entry.get()
    url = f'https://www.imdb.com/find?q={tv_show_title}&s=tt&ttype=tv&ref_=fn_tv'

    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the link to the TV show page
    link = soup.select_one('.findResult a')
    tv_show_url = 'https://www.imdb.com' + link['href']

    # Fetch the TV show page
    response = requests.get(tv_show_url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract information about the TV show
    title = soup.select_one('.title_wrapper h1').text.strip()
    genre = soup.select_one('.subtext a').text
    plot = soup.select_one('.summary_text').text.strip()

    # Add the TV show to the data structure
    tv_show = {'title': title, 'genre': genre, 'plot': plot, 'episodes': []}
    tv_shows.append(tv_show)

    # Display the TV show information in the GUI
    tv_show_listbox.insert(tk.END, title)


def mark_episode_watched():
    # Get the selected TV show and episode
    selected_tv_show = tv_shows[tv_show_listbox.curselection()[0]]
    selected_episode = selected_tv_show['episodes'][episode_listbox.curselection()[0]]

    # Mark the episode as watched
    selected_episode['watched'] = True

    # Update the episode listbox to show the watched status
    episode_listbox.delete(0, tk.END)
    for episode in selected_tv_show['episodes']:
        episode_text = f"{episode['title']} ({'watched' if episode['watched'] else 'unwatched'})"
        episode_listbox.insert(tk.END, episode_text)


def populate_episodes():
    # Get the selected TV show
    selected_tv_show = tv_shows[tv_show_listbox.curselection()[0]]

    # Populate the episode listbox with the episodes of the selected TV show
    episode_listbox.delete(0, tk.END)
    for i, episode in enumerate(selected_tv_show['episodes']):
        episode_text = f"{episode['title']} ({'watched' if episode['watched'] else 'unwatched'})"
        episode_listbox.insert(tk.END, episode_text)


def add_episode():
    # Get the selected TV show
    selected_tv_show = tv_shows[tv_show_listbox.curselection()[0]]

    # Create a new episode
    episode_title = episode_entry.get()
    episode = {'title': episode_title, 'watched': False}

    # Add the episode to the selected TV show
    selected_tv_show['episodes'].append(episode)

    # Update the episode listbox to show the new episode
    episode_text = f"{episode_title} (unwatched)"
    episode_listbox.insert(tk.END, episode_text)


# Create the GUI
root = tk.Tk()
root.title('TV Show Tracker')
