from browser import document, console, alert, json

def show(e):
    console.log(e.target.value)
    document['alert-btn'].bind('click', show())