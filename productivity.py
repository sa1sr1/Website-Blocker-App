from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button


class WebsiteBlockerApp(App):
    def __init__(self, **kwargs):
        super(WebsiteBlockerApp, self).__init__(**kwargs)
        self.websites = []
        self.valid_domains = ["com", "net", "org", "edu", "gov"]

    def build(self):
        self.title = 'Website Blocker App'

        # Layout
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Website list
        self.website_list = BoxLayout(orientation='vertical', spacing=5)
        layout.add_widget(self.website_list)

        # Website input
        self.website_input = TextInput(multiline=False)
        layout.add_widget(self.website_input)

        # Add website button
        add_button = Button(text='Add Website')
        add_button.bind(on_press=self.add_website)
        layout.add_widget(add_button)

        # Remove website button
        remove_button = Button(text='Remove Website')
        remove_button.bind(on_press=self.remove_website)
        layout.add_widget(remove_button)

        return layout

    def add_website(self, instance):
        website = self.website_input.text
        if website and website.split(".")[-1] in self.valid_domains:
            self.websites.append(website)
            # self.block_websites(True, website)
            self.website_input.text = ''
            self.update_website_list()

    def remove_website(self, instance):
        website = self.website_input.text
        if website in self.websites:
            self.websites.remove(website)
            # self.block_websites(False, website)
            self.update_website_list()

    def update_website_list(self):
        self.website_list.clear_widgets()
        for website in self.websites:
            label = Label(text=website)
            self.website_list.add_widget(label)

    def block_websites(self, block, websites_block):
        redirect = "127.0.0.1"
        hosts_path = "/private/etc/hosts"
        if block:
            with open(hosts_path, 'r+') as hostfile:
                hosts_content = hostfile.read()
                for site in websites_block:
                    if site not in hosts_content:
                        hostfile.write(redirect + ' ' + site + '\n')
        else:
            with open(hosts_path, 'r+') as hostfile:
                lines = hostfile.readlines()
                hostfile.seek(0)
                for line in lines:
                    if not any(site in line for site in websites_block):
                        hostfile.write(line)
                hostfile.truncate()




if __name__ == '__main__':
    WebsiteBlockerApp().run()
