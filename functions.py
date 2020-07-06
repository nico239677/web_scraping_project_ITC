def read_link(link):
    """Reads link to manipulate it with BeautifulSoup"""
    # Handles error if link is incorrect
    try:
        r = requests.get(link)
        print('link: \n', link)
    except requests.exceptions.ConnectionError:
        print('URL not valid')
        sys.exit()
    soup = BeautifulSoup(r.content, 'lxml')
    return soup


def add_tag_link_and_year(global_list, string, year_draft):
    """Adds the player draft number and draft year"""
    if string in str(draft.find('a')):
        element = draft.find('a').text if draft.find('a').text else None
        global_list.append(year_draft)
        global_list.append(element)
        return


def add_text_in_tag(global_list, string):
    """Adds player stats depending text in tag"""
    if string in str(draft):
        element     = draft.text if draft.text else None
        global_list.append(element)