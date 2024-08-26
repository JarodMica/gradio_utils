import os
import gradio as gr
import socket

def get_available_items(root, valid_extensions=[], directory_only=False) -> list:
    '''
    Find all files or folders in the root folder specifed.  Only looks at the pointed directory, does not walk.
    
    root(str) : The folder you want to look through
    valid_extensions(list) : A list of extension names that are valid for items to return.  Defautls to all files
    directory_only(bool) : If True, return directories only; otherwise return files with valid extensions
    '''
    if directory_only:
        list_of_items = [os.path.join(root, folder) for folder in os.listdir(root) if os.path.isdir(os.path.join(root, folder))]
    else:
        list_of_items = [os.path.join(root, item) for item in os.listdir(root) 
                         if os.path.isfile(os.path.join(root, item)) and 
                         (not valid_extensions or os.path.splitext(item)[1] in valid_extensions)]
    
    return list_of_items

def refresh_dropdown_proxy(*args):
    
    '''
    Pass in positional args as groups of THREE.
    
    The input follows the parameters of get_available_items and the outputs should be specified in the order of gradio elements you want to update in
    
    For example:
    
    some_gradio_button.click(fn=refresh_dropdown_proxy,
                            inputs=[
                                hidden_textbox_ROOT_1, hidden_textbox_VALID_EXTENSIONS_1, hidden_textbox_DIRECTORY_ONLY_1, #Updates gradio_component_1
                                hidden_textbox_ROOT_2, hidden_textbox_VALID_EXTENSIONS_2, hidden_textbox_DIRECTORY_ONLY_2, #Updates gradio_component_2
                                ...
                            ],
                            outputs=[
                                gradio_component_1,
                                gradio_component_2
                            ]
    )
    
    Returns a list of gradio dropdown components
    '''
    
    grouped_proxies = []
    for index in range(0, len(args), 3):
        proxy_pair = args[index:index+3]
        grouped_proxies.append(proxy_pair)
    
    list_of_components = []
    for item in grouped_proxies:
        valid_extensions = [ext.strip() for ext in item[1].strip('[]').split(',')]
        if item[2] == "directory":
            items_list = get_available_items(root=item[0], valid_extensions=valid_extensions, directory_only=True)
        elif item[2] == "files":
            items_list = get_available_items(root=item[0], valid_extensions=valid_extensions, directory_only=False)
        list_of_components.append(gr.Dropdown(items_list))
    print(list_of_components)
    
    if len(list_of_components) <= 1 :
        # gradio.change doesn't like lists if you're only returning one element back
        return list_of_components[0]
    else:
        return list_of_components
    
def get_port_available(start_port=7860, end_port=7865):
    def is_port_in_use(port):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            return sock.connect_ex(('localhost', port)) == 0
    webui_port = None         
    while webui_port == None:
        for i in range (start_port, end_port):
            if is_port_in_use(i):
                print(f"Port {i} is in use, moving 1 up")
            else:
                webui_port = i
                break
    return webui_port