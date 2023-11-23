import streamlit as st
from time import sleep

'''
Includes
-------------------------------------------
- ColoredHeader
    Shows a header with a colored underline and an optional description.
- Notif
    Shows a notification for a few seconds
- Setup
    Sets up the page config
-------------------------------------------
'''


def ColoredHeader(label : str = "Cool title",description : str = "Cool description",color_name : str = "gold",help : str = "", description_help : str = "") -> None:
    """
    -------------------------------------------
    Shows a header with a colored underline and an optional description.
    -------------------------------------------
    Parameters:
        label (str): The title of the header. [Default: "Cool title"]
        description (str): The description of the header. [Default: "Cool description"]
        color_name (str): The color of the underline. [Default: "gold"]
        help (str): The help text of the title. [Default: nothing]
        description_help (str): The help text of the description. [Default: nothing]
    
    Returns:
        None

    Examples:
        >>> colored_header("Cool title", "Cool description", "gold", "This is the help text of the title", "This is the help text of the description")
        >>> colored_header("Cool title", "Cool description", "gold")

    """
    st.title(
        body=label,
        help=help,
    )
    st.write(
        f'<hr style="background-color: {color_name}; margin-top: 0;'
        ' margin-bottom: 0; height: 3px; border: none; border-radius: 3px;">',
        unsafe_allow_html=True,
    )
    if description:
        st.caption(description,help=description_help)
def Notif(type : str = "success",duration : int = 3, message : str = "None") -> None:
    '''
    -------------------------------------------
    Shows a notification for a few seconds
    -------------------------------------------
    Parameters:
        type (str): The type of the notification. [Default: "success"]
        duration (int): The duration of the notification. [Default: 3]
        message (str): The message of the notification. [Default: "None"]

    Returns:
        None

    Examples:
        >>> Notif("success", 3, "This is a success notification")
        >>> Notif("error", 2, "This is an error notification")
        >>> Notif("warning", 5, "This is a warning notification")
        >>> Notif("info", 3, "This is an info notification")
    '''
    if message == "None":
        message = type 

    if type == "success":
        notif = st.success(message)
    elif type == "error":
        notif = st.error(message)
    elif type == "warning":
        notif = st.warning(message)
    elif type == "info":
        notif = st.info(message)
    else:
        notif = st.write("Notif type not found")
    
    sleep(duration)
    notif.empty()

def Setup(
    page_title: str = None,
    page_icon: str = None,
    layout: str = "centered",
    initial_sidebar_state: str = "auto",
    MenuItems: list = None,
    hide_streamlit_style: bool = True,
    ):
    '''
    -------------------------------------------
    Sets up the page config
    -------------------------------------------
    Parameters:
        page_title (str): The title of the page. [Default: None]
        page_icon (str): The icon of the page. [Default: None]
        layout (str): The layout of the page. [Default: "centered"]
        initial_sidebar_state (str): The initial state of the sidebar. [Default: "auto"]
        MenuItems (list): The items in the menu. [Default: None]
        hide_streamlit_style (bool): Whether to hide the streamlit style. [Default: True]

    Returns:
        None
    '''

    st.set_page_config(
        page_title=page_title,
        page_icon=page_icon,
        layout=layout,
        initial_sidebar_state=initial_sidebar_state,
        menu_items=MenuItems,
    )

    if hide_streamlit_style:
        hide_streamlit_style = """
            <style>
            footer {visibility: hidden;}
            header {font-size: 4rem;}
            </style>
            """
        st.markdown(hide_streamlit_style, unsafe_allow_html=True) 
