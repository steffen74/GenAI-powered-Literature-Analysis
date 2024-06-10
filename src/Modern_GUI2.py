from src import QueriesAndQueryLogic
from tkinter import filedialog
import customtkinter
import os
from dotenv import load_dotenv
import threading
from pyzotero import zotero
import dotenv

load_dotenv()  # This loads the variables from .env
# TODO put into shared Resources Class TODO save as dotenv
pdf_paths = []


class GUI(customtkinter.CTk):
    def __init__(self, kiosk=False, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if kiosk:
            self.attributes('-fullscreen', True)  # Start in full screen
            self.protocol("WM_DELETE_WINDOW", self.disable_event)  # Disable close button
        else:
            self.geometry("1200x750")  # Adjusted size for better visibility

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.selected_files = []
        self.queries = []

        # Frames with functions
        self.info_frame = MyInfoView(self)
        self.info_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.info_frame.grid_rowconfigure(0, weight=0)
        self.info_frame.grid_columnconfigure(0, weight=0)

        self.tab_view = MyTabView(master=self)
        self.tab_view.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

        self.row_frame = customtkinter.CTkScrollableFrame(self)
        self.row_frame.grid(row=1, column=0, columnspan=2, padx=20, pady=10, sticky="nsew")
        self.row_frame.grid_columnconfigure(1, weight=1)
        self.row_counter = 0
        self.add_preconfigured_queries()

        self.last_frame = customtkinter.CTkFrame(self)
        self.last_frame.grid(row=2, column=0, columnspan=2, padx=20, pady=10, sticky="nsew")
        self.last_frame.grid_columnconfigure(1, weight=1)
        self.create_last_frame_elements()

    def disable_event(self):
        pass  # Do nothing when close button is clicked
    
    def create_last_frame_elements(self):
        # TODO add different output format options
        # label_dropdown_output_format = customtkinter.CTkLabel(self.dropdown_frame, text="Select Output Format:")
        # label_dropdown_output_format.grid(row=0, column=0, padx=10, pady=10)
        # dropdown_output_format = customtkinter.CTkOptionMenu(self.dropdown_frame, values=["PDF", "DOC", "XML", "JSON"])
        # dropdown_output_format.grid(row=0, column=1, padx=10, pady=10)

        # TODO add different LLM options (Christian also wanted the option for local LLMs)
        # dropdown_model = customtkinter.CTkLabel(self.dropdown_frame, text="Select GPT Model:")
        # dropdown_model.grid(row=0, column=2, padx=10, pady=5)
        # optionmenu = customtkinter.CTkOptionMenu(self.dropdown_frame, values=["option 1", "option 2"],command=optionmenu_callback)
        # dropdown_model = customtkinter.CTkOptionMenu(self.dropdown_frame, values=["GPT3.5", "GPT4"])
        # dropdown_model.grid(row=0, column=3, padx=10, pady=5)

        self.add_query_button = customtkinter.CTkButton(self.last_frame, text="Add Custom Query",
                                                        command=self.add_custom_query)
        self.add_query_button.grid(row=0, column=0, padx=10, pady=10)

        self.label_progress_updates = customtkinter.CTkLabel(self.last_frame, text=" ", font=("Maitree", 14))
        self.label_progress_updates.grid(row=0, column=1, padx=10, pady=10)

        self.start_summary_button = customtkinter.CTkButton(self.last_frame, text="Start Summary and Review",
                                                            command=self.summarize)
        self.start_summary_button.grid(row=0, column=2, padx=10, pady=10)

        # quit_button = customtkinter.CTkButton(self.button_frame, text="Quit", command=self.destroy)
        # quit_button.grid(row=0, column=2, pady=10, padx=10, sticky="e")

    def updateProgressLabel(self, update_text):
        self.label_progress_updates.configure(text=update_text)

    def add_preconfigured_queries(self):
        for query in QueriesAndQueryLogic.queries:
            self.add_row_to_query_table(query)

    def add_custom_query(self):
        # Ask the user for input text
        input_text = customtkinter.CTkInputDialog(text="New Query:", title="Enter your question...")

        if input_text:
            self.add_row_to_query_table(input_text.get_input())

    def add_row_to_query_table(self, query):
        # Create a row frame
        # Use Query Checkbox
        var_use_query = customtkinter.IntVar()
        checkbox = customtkinter.CTkCheckBox(self.row_frame, variable=var_use_query, text="Use")
        checkbox.grid(row=self.row_counter, column=0, padx=0, pady=10)

        # Highlight Reference Checkbox
        # var_find_reference = customtkinter.IntVar()
        # checkbox = customtkinter.CTkCheckBox(self.row_frame, variable=var_find_reference, text="Find Reference")
        # checkbox.grid(row=self.row_counter, column=1, padx=5, pady=5)

        textbox = customtkinter.CTkTextbox(master=self.row_frame, wrap="word", corner_radius=0, height=45,
                                           bg_color="transparent", fg_color="transparent", font=("Maitree", 16))
        textbox.grid(row=self.row_counter, column=1, sticky="nsew", pady=5)
        textbox.insert("0.0", text=query)

        # self.queries.append((var_use_query, var_find_reference, query, self.row_counter))
        self.queries.append((var_use_query, query, self.row_counter))
        self.row_counter += 1

    def summarize(self):
        # Implement your summarization logic here
        # For now, just show a message box
        global pdf_paths
        selected_queries = [query for use, query, index in self.queries if use.get() == 1]
        run_llm_thread = threading.Thread(target=QueriesAndQueryLogic.review_papers_and_save,
                                          args=(pdf_paths, selected_queries, os.environ.get("OUTPUT_DIRECTORY"),
                                                self.updateProgressLabel))
        run_llm_thread.start()


class MyInfoView(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # create widgets
        label_greeting = customtkinter.CTkLabel(self,
                                                text="Welcome to our Large Language Model Project Application",
                                                anchor="w",
                                                font=("Maitree", 24))
        label_greeting.grid(row=0, column=0, padx=20, pady=5, sticky="ew")

        label_info = customtkinter.CTkLabel(self,
                                            text="This App is your efficient and cheap way to " +
                                                 "\n - Summarize PDFs " +
                                                 "\n - Chat with your Zotero Library " +
                                                 "\n - Prompt OpenAIs Large Language Models ",
                                            anchor="w",
                                            font=("Maitree", 24))
        label_info.grid(row=2, column=0, padx=20, pady=5, sticky="ew")


class MyTabView(customtkinter.CTkTabview):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure(0, weight=1)
        # create tabs
        settingsTab = self.add("Settings")
        pdfsTab = self.add("Select PDFs")
        zoteroTab = self.add("Use Zotero")

        # add widgets on tabs
        self.settings_frame = MySettingsView(settingsTab)
        self.settings_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.settings_frame.grid_rowconfigure(0, weight=0)

        self.select_pdf_frame = MyPDFView(pdfsTab)
        self.select_pdf_frame.pack()

        self.zotero_frame = MyZoteroView(zoteroTab)
        self.zotero_frame.pack()


class MySettingsView(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        OPEN_AI_API_KEY = os.environ.get('OPEN_AI_API_KEY')
        self.grid_columnconfigure((0, 1), weight=1)
        # create tabs
        self.button_enter_openAI_api_key = customtkinter.CTkButton(self,
                                                                   text="Enter OpenAI API Key",
                                                                   anchor="w",
                                                                   font=("Maitree", 16),
                                                                   command=self.request_OpenAI_API_key)
        self.button_enter_openAI_api_key.grid(row=0, column=0, padx=20, pady=5, sticky="ew")

        self.label_openAI_api_key = customtkinter.CTkLabel(self, text=OPEN_AI_API_KEY[:5]+(len(OPEN_AI_API_KEY)-5)*"*", anchor="w",
                                                           font=("Maitree", 16))
        self.label_openAI_api_key.grid(row=0, column=1, padx=20, pady=0, sticky="ew")
        self.label_openAI_api_key.columnconfigure(1)

        self.button_zotero_api_key = customtkinter.CTkButton(self,
                                                             text="Enter Zotero API Key",
                                                             anchor="w",
                                                             font=("Maitree", 16), command=self.request_Zotero_API_key)
        self.button_zotero_api_key.grid(row=1, column=0, padx=20, pady=5, sticky="ew")

        self.label_zotero_api_key = customtkinter.CTkLabel(self, text=os.environ.get('ZOTERO_API_KEY')[:5]+(len(os.environ.get('ZOTERO_API_KEY'))-5)*"*", anchor="w",
                                                           font=("Maitree", 16))
        self.label_zotero_api_key.grid(row=1, column=1, padx=20, pady=0, sticky="ew")

        self.button_zotero_user_id = customtkinter.CTkButton(self, text="Enter Zotero User ID", anchor="w",
                                                             font=("Maitree", 16), command=self.request_Zotero_user_id)
        self.button_zotero_user_id.grid(row=2, column=0, pady=0, padx=20, sticky="ew")
        self.label_user_id_zotero = customtkinter.CTkLabel(self,
                                                           text=os.environ.get('ZOTERO_USER_ID'),
                                                           anchor="w",
                                                           font=("Maitree", 16))
        self.label_user_id_zotero.grid(row=2, column=1, padx=20, pady=5, sticky="ew")

        self.button_choose_zotero_directory = customtkinter.CTkButton(self, text="Choose Zotero Directory",
                                                                      font=("Maitree", 16),
                                                                      command=self.browse_Zotero_directory)
        self.button_choose_zotero_directory.grid(row=3, column=0, padx=20, pady=5, sticky="ew")
        self.label_zotero_directory = customtkinter.CTkLabel(self, text=os.environ.get('ZOTERO_DIRECTORY'), anchor="w",
                                                             font=("Maitree", 16))
        self.label_zotero_directory.grid(row=3, column=1, padx=20, pady=5, sticky="ew")

        self.button_output_directory = customtkinter.CTkButton(self, text="Select Output Directory",
                                                               font=("Maitree", 16),
                                                               command=self.browse_output_directory)
        self.button_output_directory.grid(row=4, column=0, padx=20, pady=5, sticky="ew")
        self.label_output_directory = customtkinter.CTkLabel(self, text=os.environ.get('OUTPUT_DIRECTORY'), anchor="w",
                                                             font=("Maitree", 16))
        self.label_output_directory.grid(row=4, column=1, padx=20, pady=5, sticky="ew")

    def request_OpenAI_API_key(self):
        # Ask the user for input text
        user_input = customtkinter.CTkInputDialog(text="Enter OpenAI API Key:", title="OpenAI API Key")

        if user_input:
            input_text = user_input.get_input()
            update_dotenv("OPEN_AI_API_KEY", input_text)
            load_dotenv(override=True)
            self.label_openAI_api_key.configure(text='***********')

    def request_Zotero_API_key(self):
        # Ask the user for input text
        user_input = customtkinter.CTkInputDialog(text="Enter Zotero API Key:", title="Zotero API Key")

        if user_input:
            input_text = user_input.get_input()
            update_dotenv("ZOTERO_API_KEY", input_text)
            load_dotenv(override=True)
            self.label_zotero_api_key.configure(text='***********')

    def request_Zotero_user_id(self):
        # Ask the user for input text
        user_input = customtkinter.CTkInputDialog(text="Enter Zotero User ID:", title="Zotero User ID")

        if user_input:
            input_text = user_input.get_input()
            update_dotenv("ZOTERO_USER_ID", input_text)
            load_dotenv(override=True)
            self.label_user_id_zotero.configure(text=os.environ.get('ZOTERO_USER_ID'))

    def browse_Zotero_directory(self):
        zotero_path = filedialog.askdirectory()
        print(zotero_path)
        if zotero_path:
            update_dotenv("ZOTERO_DIRECTORY", zotero_path)
            load_dotenv(override=True)
            self.label_zotero_directory.configure(text=os.environ.get('ZOTERO_DIRECTORY'))
            print(os.environ.get('ZOTERO_DIRECTORY'))

    def browse_output_directory(self):
        output_path = filedialog.askdirectory()
        print(output_path)
        if output_path:
            update_dotenv("OUTPUT_DIRECTORY", output_path)
            load_dotenv(override=True)
            self.label_output_directory.configure(text=os.environ.get('OUTPUT_DIRECTORY'))
            print(os.environ.get('OUTPUT_DIRECTORY'))


class MyPDFView(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.button_select_files = customtkinter.CTkButton(self, text="Select PDF Files", font=("Maitree", 16),
                                                           command=self.select_pdf_files)
        self.button_select_files.pack(expand=True, pady=10)
        self.label_selected_files = customtkinter.CTkLabel(self, text="No PDFs selected", font=("Maitree", 16))
        self.label_selected_files.pack(expand=True, pady=10)

    def select_pdf_files(self):
        global pdf_paths
        file_paths = filedialog.askopenfilenames(filetypes=[("PDF files", "*.pdf")])
        pdf_paths = file_paths
        number_of_pdfs = len(file_paths)
        if number_of_pdfs == 1:
            self.label_selected_files.configure(text=f"{number_of_pdfs} PDF selected")
        else:
            self.label_selected_files.configure(text=f"{number_of_pdfs} PDFs selected")


class MyZoteroView(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure(0, weight=1)
        # create widgets
        self.button_connect_to_zotero = customtkinter.CTkButton(self, text="Connect to Zotero",
                                                                font=("Maitree", 16), command=self.establish_connection)
        self.button_connect_to_zotero.grid(row=0, column=0, padx=10, pady=10, columnspan=2, sticky="nsew")

    def establish_connection(self):
        ZOTERO_API_KEY = os.environ.get("ZOTERO_API_KEY")
        ZOTERO_USER_ID = os.environ.get("ZOTERO_USER_ID")

        self.collection_keys = {}
        self.zot = zotero.Zotero(ZOTERO_USER_ID, 'user', ZOTERO_API_KEY)
        self.collections = self.zot.collections()

        collection_names = ([collection['data']['name'] for collection in self.collections])
        # self.collection_dropdown['values'] = collection_names

        self.dropdown_zotero_collection = customtkinter.CTkOptionMenu(self, font=("Maitree", 16),
                                                                      values=collection_names,
                                                                      command=self.get_pdf_references)
        self.dropdown_zotero_collection.grid(row=2, column=0, padx=5, pady=10, columnspan=2, sticky="nsew")

        for collection in self.collections:
            self.collection_keys[collection['data']['name']] = collection['key']

    def get_pdf_references(self, collection_name):
        collection_key = self.collection_keys[collection_name]
        ZOTERO_DIRECTORY = os.environ.get("ZOTERO_DIRECTORY")
        pdf_refs = []

        try:
            # Get all items in the specified collection
            items = self.zot.collection_items(collection_key)

            # Iterate through items and collect PDF references
            for item in items:
                if item['data'].get('contentType') == 'application/pdf':
                    item_path = ZOTERO_DIRECTORY + '\\' + item['data']['key']
                    item_filename = item['data']['filename']

                    file_path = os.path.join(item_path, item_filename)
                    pdf_refs.append(file_path)

            global pdf_paths
            pdf_paths = pdf_refs
            self.label_number_of_zotero_pdfs = customtkinter.CTkLabel(self, font=("Maitree", 16),
                                                                      text=f"{len(pdf_refs)} PDFs Selected")
            self.label_number_of_zotero_pdfs.grid(row=3, column=0, padx=5, pady=10, columnspan=2, sticky="nsew")

        except Exception as e:
            print(f"Error retrieving PDF references: {e}")
            self.label_number_of_zotero_pdfs = customtkinter.CTkLabel(self, font=("Maitree", 16),
                                                                      text=f"Error retrieving PDF references: {e}")
            self.label_number_of_zotero_pdfs.grid(row=3, column=0, padx=5, pady=10, columnspan=2, sticky="nsew")
            return []

    def show_items(self):
        col_key = self.collection_keys[self.collection_dropdown.get()]
        print(col_key)
        refs = self.get_pdf_references(col_key)
        for r in refs:
            print(r)

    """
    def optionmenu_callback(self, choice):
        print("optionmenu dropdown clicked:", choice)

    optionmenu_var = customtkinter.StringVar(value="option 2")
    optionmenu = customtkinter.CTkOptionMenu(app, values=["option 1", "option 2"],
                                             command=optionmenu_callback,
                                             variable=optionmenu_var)
    """


def update_dotenv(key, new_value):
    # Check if the .env file exists
    if not os.path.isfile('.env'):
        # If it doesn't exist, create it based on the .env_template file
        with open('.env_template', 'r') as template, open('.env', 'w') as env:
            env.write(template.read())

    with open('.env', 'r') as file:
        lines = [line.strip() for line in file]

    # Load the environment variables from the .env file
    load_dotenv('.env')

    # Check if the key already exists in the file
    key_exists = False
    with open('.env', 'w') as file:
        for line in lines:
            if line.startswith(f"{key}="):
                file.write(f"{key}={new_value}\n")
                key_exists = True
            else:
                file.write(line + '\n')

        # If the key does not exist in the file, add it
        if not key_exists:
            file.write(f"{key}={new_value}\n")
