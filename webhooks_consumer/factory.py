import json
import random
import requests
from bs4 import BeautifulSoup
from slackclient import SlackClient

from django.conf import settings

class GenericMessageFactory:
    def __init__(self,request_json):
        self.request_json = request_json
        # APIS to look into lateR:
        # https://favqs.com/api
        # https://theysaidso.com/api/#
        # http://paperquotes.com/

    def _get_api_response_or_none(self, url):
        try:
            response = requests.get(api_url, timeout=10)
            contents = response.json()
            return contents
        except:
            return

    def _get_compliment(self):
        api_url = "https://complimentr.com/api"
        contents = self._get_api_response_or_none(self, api_url)
        if contents
            compliment = contents["compliment"]
            return compliment
        return None

    def _get_doggo(self):
        # oh no! doggo is down!
        try:
            api_url = "https://random.dog/woof.json"
            contents = self._get_api_response_or_none(self, api_url)
            if contents and "url" in contents:
                url = contents["url"]
                return url
            return None
        except:
            return self._get_duck()

    def _get_duck(self):
        api_url = "https://random-d.uk/api/v2/random"
        contents = self._get_api_response_or_none(self, api_url)
        if contents
            url = contents["url"]
            return url
        return None

    def _get_sloth(self):
        api_url = "https://sloth.pics/api"
        contents = self._get_api_response_or_none(self, api_url)
        if contents
            url = contents["url"]
            return url
        return None

    # def _get_bunny(self):
    #     #TODO nevermind doesny work maybe with a hedless browesr
    #     # numbers between 1-63 seem to work
    #     bunny_id = random.randint(1,163)
    #     # https://bunnies.media/webm/163.webm
    #     api_url = "https://www.bunnies.io/#{}".format(bunny_id)
    #     # numbers between 1-363 seem to work
    #     contents = requests.get(api_url)
    #     soup = BeautifulSoup(contents.content, 'html.parser')
    #     videos = soup.findAll('video')
    #     if len(videos) > 1:
    #         video = videos[1]
    #         source = video.find('source')
    #         if source:
    #             src = source['src']
    #             if src:
    #                 return src
    #     # if something goes wrong just return a duck

    def _get_kitty(self):
        api_url = "https://api.thecatapi.com/v1/images/search"
        contents = self._get_api_response_or_none(self, api_url)
        if contents
            url = contents[0]["url"]
            return url
        return None

    def _get_pet(self):
        pet_function = random.choice([self._get_kitty, self._get_doggo])
        url = pet_function()
        return url

    def _get_fox(self):
        api_url = "https://randomfox.ca/floof/"
        contents = self._get_api_response_or_none(self, api_url)
        if contents
            url = contents["image"]
            return url
        return None        

    def _get_insult(self):
        api_url = "https://autoinsult.com/index.php?style={}".format(random.randint(0,3))
        contents = requests.get(api_url, timeout=10)
        soup = BeautifulSoup(contents.content, 'html.parser')
        text = soup.find("div", {"id": "insult"}).getText()
        return text

    def _get_taco(self):
        api_url = "http://taco-randomizer.herokuapp.com/random/"
        contents = self._get_api_response_or_none(self, api_url)
        if contents
            text = json.dumps(contents, indent=4, sort_keys=True)
            return text
        return None

    def _parse_telegram_message_obj(self):
        return self.request_json["message"]

    def _parse_telegram_chat_obj(self):
        return self._parse_telegram_message_obj()["chat"]

    def _parse_telegram_chat_id(self):
        t_chat = self._parse_telegram_chat_obj()
        return t_chat.get("id")

    def _parse_telegram_sender_string(self):
        t_chat = self._parse_telegram_chat_obj()
        if "sender" in t_chat:
            obj = t_chat
        else:
            obj = self._parse_telegram_message_obj()["from"]
        return obj.get("first_name")

    def _parse_telegram_message_string(self):
        return self._parse_telegram_message_obj()["text"]

    def _parse_slack_command_message_string(self):
        return self.request_json["text"]

    def _parse_slack_sender_string(self):
        return self.request_json["user_name"]

    def _parse_telegram_command_message_string(self, command_str):
        msg_str = self._parse_telegram_message_string().strip().lower()
        if command_str in msg_str:
            message_list = msg_str.split("/{} ".format(command_str))
            if len(message_list) > 1:
                command_content = message_list[1]
                return command_content
        else:
            raise ValueError(
                "{} not in {}; wrong method called".format(command_str, msg_str)
            )

    def _get_broadcast_message(self):
        # message string may come from Telegram or Slack. Decide which it is and parse accodringly.
        if set(dict(self.request_json).keys()) == set(['update_id', 'message']):
            # Telegram json
            message_list = self._parse_telegram_message_string().split()
            message_text = " ".join(message_list[1:])
            sender = self._parse_telegram_sender_string()
            platform = "Telegram"
            try:
                # so terrible, but circular import issue.
                # or, try to get a more specific channel nickname 
                chat_id = self._parse_telegram_chat_id()
                if chat_id:
                    nicknames = {-1001258758865:"\U0001f6fc", -1001343931693:"⛸"}
                    nickname = nicknames.get(chat_id)
                    if nickname:
                        platform = nickname
            except:
                pass
        else:
            # Slack json
            platform = "Slack"
            message_text = self._parse_slack_command_message_string()
            sender = self._parse_slack_sender_string()
            
        broadcast_msg = "{} on {}: {}".format(
            sender if sender else "", platform, message_text
        )
        return broadcast_msg


    def _send_output(self):
        raise NotImplementedError(
            "_send_output has not been implemented for {}".format(
                self.__class__.__name__
            )
        )



class TelegramMessageFactory(GenericMessageFactory):
    
    def __init__(self, request_json):
        super().__init__(request_json)

    def _build_url(self, api_action):
        url = "https://api.telegram.org/bot{}/{}".format(settings.TELEGRAM_BOT_TOKEN, api_action)
        return url

    def _send_output(self, output_target, output_content):
        has_image_extension = [True for ext in ["jpg", "jpeg", "png", "gif", "mp4", "webm"] if output_content.lower().endswith(".{}".format(ext))]
        if "http" in output_content and any(has_image_extension): # it's a photo 
            data = {"chat_id": output_target, "photo": output_content}
            requests.post(self._build_url(api_action="sendPhoto"), data=data)
        else:
            data = {"chat_id": output_target, "text": output_content, "parse_mode": "Markdown"}
            requests.post(self._build_url(api_action="sendMessage"), data=data)
            
            
class SlackMessageFactory(GenericMessageFactory):

    def __init__(self, request_json):
        super().__init__(request_json)

    def _send_output(self, output_target, output_content):
        slack_client = SlackClient(settings.SLACK_BOT_TOKEN)
        response = slack_client.api_call(
            "chat.postMessage", channel=output_target, text=output_content
        )

