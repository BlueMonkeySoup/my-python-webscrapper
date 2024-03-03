from files.walk import FetchItems

# Main fil som ska hämta rabatter från coops hemsida.
# Inget mer ska kodas. Hemsidan har ändrats helt.

start_instance=FetchItems()
start_instance.fetch_website()
start_instance.click_abort()
start_instance.click_show_more_buttons()

start_instance.send_to_file()

