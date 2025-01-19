from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
from copy import deepcopy
import json




@dataclass
class ThreadInfo:
    thread_id: str
    thread_metadata: dict
    messages: List[str]

class DiscordMessageProcessor:
    def __init__(self, messages: List[dict]):
        self.messages = messages
        self.processed_messages: Dict[str, dict] = {}
        self.threads: Dict[str, ThreadInfo] = {}

    def process_messages(self):
        """Process messages and organize them with their relationships."""
        # First pass: Create a map of all messages
        for message in self.messages:
            self.processed_messages[message['id']] = {
                **message,
                'references': [],
                'children': []
            }

            # If message is part of a thread, organize it
            thread = message.get('thread')
            if thread:
                if thread['id'] not in self.threads:
                    self.threads[thread['id']] = ThreadInfo(
                        thread_id=thread['id'],
                        thread_metadata=thread,
                        messages=[]
                    )
                self.threads[thread['id']].messages.append(message['id'])

        # Second pass: Handle references and build relationships
        for message in self.processed_messages.values():
            message_reference = message.get('message_reference')
            if message_reference:
                parent_id = message_reference.get('message_id')
                parent_message = self.processed_messages.get(parent_id)
                if parent_message:
                    parent_message['children'].append(message['id'])
                    message['references'].append(parent_id)

            referenced_message = message.get('referenced_message')
            if referenced_message:
                message['references'].append(referenced_message['id'])

        return self

    def build_message_document(self, message: dict) -> dict:
        """Build a complete message document including references."""
        doc = deepcopy(message)
        doc['referenced_messages'] = []
        doc['child_messages'] = []

        # Add referenced messages
        for ref_id in message.get('references', []):
            ref_message = self.processed_messages.get(ref_id)
            if ref_message:
                doc['referenced_messages'].append(deepcopy(ref_message))

        # Add child messages
        for child_id in message.get('children', []):
            child_message = self.processed_messages.get(child_id)
            if child_message:
                doc['child_messages'].append(deepcopy(child_message))

        return doc

    def build_thread_document(self, thread: ThreadInfo) -> dict:
        """Build a thread document with all related messages."""
        thread_doc = {
            'thread_info': asdict(thread),
            'messages': []
        }

        # Add all messages in the thread
        for message_id in thread.messages:
            message = self.processed_messages.get(message_id)
            if message:
                thread_doc['messages'].append(
                    self.build_message_document(message)
                )

        return thread_doc

    def generate_drive_documents(self) -> dict:
        """Generate documents ready for Google Drive storage."""
        message_documents = []
        thread_documents = []

        # Create individual message documents
        for message in self.processed_messages.values():
            # Only create individual documents for non-thread messages
            if not message.get('thread'):
                message_documents.append({
                    'type': 'message',
                    'content': self.build_message_document(message)
                })

        # Create thread documents
        for thread in self.threads.values():
            thread_documents.append({
                'type': 'thread',
                'content': self.build_thread_document(thread)
            })

        return {
            'message_documents': message_documents,
            'thread_documents': thread_documents
        }

# Test data
# change null to None and False to False, true to True before processing the messages
test_messages = [{"type":0,"content":"even though technically you could deploy your nextjs with restack, i would advise to have your frontend on vercel and backend on restack cloud. you can always trigger and retrive workflows in nextjs following this https://github.com/restackio/examples-typescript/blob/main/nextjs/src/app/actions/trigger.ts","mentions":[],"mention_roles":[],"attachments":[],"embeds":[{"type":"article","url":"https://github.com/restackio/examples-typescript/blob/main/nextjs/src/app/actions/trigger.ts","title":"examples-typescript/nextjs/src/app/actions/trigger.ts at main \u00b7 res...","description":"Restack AI examples for TypeScript. Contribute to restackio/examples-typescript development by creating an account on GitHub.","color":1975079,"provider":{"name":"GitHub"},"thumbnail":{"url":"https://opengraph.githubassets.com/f408b249f7bba5ea994dd37807f78545db5fa079e8f9c97d9ddeaf0ca1dc2a23/restackio/examples-typescript","proxy_url":"https://images-ext-1.discordapp.net/external/aSwlQa9v-NT7M3Llt6ua8dgs0lEotj20lA5lraRLZ1g/https/opengraph.githubassets.com/f408b249f7bba5ea994dd37807f78545db5fa079e8f9c97d9ddeaf0ca1dc2a23/restackio/examples-typescript","width":1200,"height":600,"placeholder":"vPcFDIJpiaaZh3h1eH8/yUT6Fg==","placeholder_version":1,"flags":0},"content_scan_version":1}],"timestamp":"2025-01-18T10:24:59.842000+00:00","edited_timestamp":None,"flags":0,"components":[],"id":"1330120752489304096","channel_id":"1293665802523902032","author":{"id":"905943889494569000","username":"philipperestack","avatar":"36d0a20557eb8dce3f3fb7c90d9c3f4a","discriminator":"0","public_flags":0,"flags":0,"banner":None,"accent_color":None,"global_name":"Philippe","avatar_decoration_data":None,"banner_color":None,"clan":None,"primary_guild":None},"pinned":False,"mention_everyone":False,"tts":False},{"type":0,"content":"regarding deployment, you can copy this dockerfile in apps/backend https://github.com/restackio/examples-typescript/blob/main/quickstart/Dockerfile . If you follow turborepo you can have dockerfile path point to /apps/backend/Dockerfile and apps/backend","mentions":[],"mention_roles":[],"attachments":[],"embeds":[{"type":"article","url":"https://github.com/restackio/examples-typescript/blob/main/quickstart/Dockerfile","title":"examples-typescript/quickstart/Dockerfile at main \u00b7 restackio/examp...","description":"Restack AI examples for TypeScript. Contribute to restackio/examples-typescript development by creating an account on GitHub.","color":1975079,"provider":{"name":"GitHub"},"thumbnail":{"url":"https://opengraph.githubassets.com/f408b249f7bba5ea994dd37807f78545db5fa079e8f9c97d9ddeaf0ca1dc2a23/restackio/examples-typescript","proxy_url":"https://images-ext-1.discordapp.net/external/aSwlQa9v-NT7M3Llt6ua8dgs0lEotj20lA5lraRLZ1g/https/opengraph.githubassets.com/f408b249f7bba5ea994dd37807f78545db5fa079e8f9c97d9ddeaf0ca1dc2a23/restackio/examples-typescript","width":1200,"height":600,"placeholder":"vPcFDIJpiaaZh3h1eH8/yUT6Fg==","placeholder_version":1,"flags":0},"content_scan_version":1}],"timestamp":"2025-01-18T10:24:03.414000+00:00","edited_timestamp":None,"flags":0,"components":[],"id":"1330120515813376000","channel_id":"1293665802523902032","author":{"id":"905943889494569000","username":"philipperestack","avatar":"36d0a20557eb8dce3f3fb7c90d9c3f4a","discriminator":"0","public_flags":0,"flags":0,"banner":None,"accent_color":None,"global_name":"Philippe","avatar_decoration_data":None,"banner_color":None,"clan":None,"primary_guild":None},"pinned":False,"mention_everyone":False,"tts":False},{"type":19,"content":"Hey <@675081906911707156> , for this i would recommend making a monorepo with turborepo with apps/frontend for your nextjs and apps/backend for your restack services. I have an example here https://github.com/aboutphilippe/autonomous-videocreator-lumaai","mentions":[{"id":"675081906911707156","username":"hawksrevolution","avatar":"ec24fd878e6315a83ee94ba94caba92e","discriminator":"0","public_flags":0,"flags":0,"banner":None,"accent_color":None,"global_name":"Sergiu S","avatar_decoration_data":None,"banner_color":None,"clan":None,"primary_guild":None}],"mention_roles":[],"attachments":[],"embeds":[{"type":"article","url":"https://github.com/aboutphilippe/autonomous-videocreator-lumaai","title":"GitHub - aboutphilippe/autonomous-videocreator-lumaai","description":"Contribute to aboutphilippe/autonomous-videocreator-lumaai development by creating an account on GitHub.","color":1975079,"reference_id":"1330120228889296967","provider":{"name":"GitHub"},"thumbnail":{"url":"https://opengraph.githubassets.com/44c6483cdc4661a866304f3d1c5702cf6d1eaf7020fa953ed966361378cc6fbc/aboutphilippe/autonomous-videocreator-lumaai","proxy_url":"https://images-ext-1.discordapp.net/external/pNBifGJe8MDb3LRjE53I9R2Gm68AUGS6Qly6orDRbtk/https/opengraph.githubassets.com/44c6483cdc4661a866304f3d1c5702cf6d1eaf7020fa953ed966361378cc6fbc/aboutphilippe/autonomous-videocreator-lumaai","width":1200,"height":600,"placeholder":"+/cFDIJKmaaYhnl1eG+Vj1L6GQ==","placeholder_version":1,"flags":0},"content_scan_version":1}],"timestamp":"2025-01-18T10:22:55.006000+00:00","edited_timestamp":None,"flags":0,"components":[],"id":"1330120228889296967","channel_id":"1293665802523902032","author":{"id":"905943889494569000","username":"philipperestack","avatar":"36d0a20557eb8dce3f3fb7c90d9c3f4a","discriminator":"0","public_flags":0,"flags":0,"banner":None,"accent_color":None,"global_name":"Philippe","avatar_decoration_data":None,"banner_color":None,"clan":None,"primary_guild":None},"pinned":False,"mention_everyone":False,"tts":False,"message_reference":{"type":0,"channel_id":"1293665802523902032","message_id":"1330049099361419264","guild_id":"1290621730200485900"},"position":0,"referenced_message":{"type":0,"content":"Hi guys, I have a probably quite stupid question here. I'm trying to create a new stack. We have a repository with a nextJS application. Ideally I'd like to keep a mono-repo architecture and create one new folder in my monorepo called workflows (to create workflows in Javascript). I've connected my github, gave access to restack and clicked on import. However, I am stuck at this stage as I have no idea what Dockerfile I should give and why I need Docker for the managed Restack service. Appreciate your help \ud83d\ude4c","mentions":[],"mention_roles":[],"attachments":[{"id":"1330049099147251772","filename":"image.png","size":214758,"url":"https://cdn.discordapp.com/attachments/1293665802523902032/1330049099147251772/image.png?ex=678d3900&is=678be780&hm=269fb0395c24970b0f53166e28323f0ac913f6749b0db93cd715ce33cb2e6785&","proxy_url":"https://media.discordapp.net/attachments/1293665802523902032/1330049099147251772/image.png?ex=678d3900&is=678be780&hm=269fb0395c24970b0f53166e28323f0ac913f6749b0db93cd715ce33cb2e6785&","width":1302,"height":1752,"content_type":"image/png","content_scan_version":1,"placeholder":"yPcBBQCfJYSKiGapV3lmeDBYh8/J","placeholder_version":1}],"embeds":[],"timestamp":"2025-01-18T05:40:16.405000+00:00","edited_timestamp":None,"flags":32,"components":[],"id":"1330049099361419264","channel_id":"1293665802523902032","author":{"id":"675081906911707156","username":"hawksrevolution","avatar":"ec24fd878e6315a83ee94ba94caba92e","discriminator":"0","public_flags":0,"flags":0,"banner":None,"accent_color":None,"global_name":"Sergiu S","avatar_decoration_data":None,"banner_color":None,"clan":None,"primary_guild":None},"pinned":False,"mention_everyone":False,"tts":False,"thread":{"id":"1330049099361419264","type":11,"last_message_id":"1330078490317295676","flags":0,"guild_id":"1290621730200485900","name":"Restack cloud","parent_id":"1293665802523902032","rate_limit_per_user":0,"bitrate":64000,"user_limit":0,"rtc_region":None,"owner_id":"932662489617928295","thread_metadata":{"archived":False,"archive_timestamp":"2025-01-18T07:34:40.906000+00:00","auto_archive_duration":4320,"locked":False,"create_timestamp":"2025-01-18T07:34:40.906000+00:00"},"message_count":2,"member_count":3,"total_message_sent":2,"member_ids_preview":["675081906911707156","932662489617928295","905943889494569000"]}}},{"type":18,"content":"Restack cloud","mentions":[],"mention_roles":[],"attachments":[],"embeds":[],"timestamp":"2025-01-18T07:34:40.939000+00:00","edited_timestamp":None,"flags":0,"components":[],"id":"1330077891303571563","channel_id":"1293665802523902032","author":{"id":"932662489617928295","username":"martinbachrestack","avatar":"d529f9c44139b9a8a72f2823dbaf2e59","discriminator":"0","public_flags":0,"flags":0,"banner":None,"accent_color":None,"global_name":"Martin Bach [restack.io]","avatar_decoration_data":None,"banner_color":None,"clan":None,"primary_guild":None},"pinned":False,"mention_everyone":False,"tts":False,"message_reference":{"type":0,"channel_id":"1330049099361419264","guild_id":"1290621730200485900"},"position":0},{"type":0,"content":"Hi guys, I have a probably quite stupid question here. I'm trying to create a new stack. We have a repository with a nextJS application. Ideally I'd like to keep a mono-repo architecture and create one new folder in my monorepo called workflows (to create workflows in Javascript). I've connected my github, gave access to restack and clicked on import. However, I am stuck at this stage as I have no idea what Dockerfile I should give and why I need Docker for the managed Restack service. Appreciate your help \ud83d\ude4c","mentions":[],"mention_roles":[],"attachments":[{"id":"1330049099147251772","filename":"image.png","size":214758,"url":"https://cdn.discordapp.com/attachments/1293665802523902032/1330049099147251772/image.png?ex=678d3900&is=678be780&hm=269fb0395c24970b0f53166e28323f0ac913f6749b0db93cd715ce33cb2e6785&","proxy_url":"https://media.discordapp.net/attachments/1293665802523902032/1330049099147251772/image.png?ex=678d3900&is=678be780&hm=269fb0395c24970b0f53166e28323f0ac913f6749b0db93cd715ce33cb2e6785&","width":1302,"height":1752,"content_type":"image/png","content_scan_version":1,"placeholder":"yPcBBQCfJYSKiGapV3lmeDBYh8/J","placeholder_version":1}],"embeds":[],"timestamp":"2025-01-18T05:40:16.405000+00:00","edited_timestamp":None,"flags":32,"components":[],"id":"1330049099361419264","channel_id":"1293665802523902032","author":{"id":"675081906911707156","username":"hawksrevolution","avatar":"ec24fd878e6315a83ee94ba94caba92e","discriminator":"0","public_flags":0,"flags":0,"banner":None,"accent_color":None,"global_name":"Sergiu S","avatar_decoration_data":None,"banner_color":None,"clan":None,"primary_guild":None},"pinned":False,"mention_everyone":False,"tts":False,"thread":{"id":"1330049099361419264","type":11,"last_message_id":"1330078490317295676","flags":0,"guild_id":"1290621730200485900","name":"Restack cloud","parent_id":"1293665802523902032","rate_limit_per_user":0,"bitrate":64000,"user_limit":0,"rtc_region":None,"owner_id":"932662489617928295","thread_metadata":{"archived":False,"archive_timestamp":"2025-01-18T07:34:40.906000+00:00","auto_archive_duration":4320,"locked":False,"create_timestamp":"2025-01-18T07:34:40.906000+00:00"},"message_count":2,"member_count":3,"total_message_sent":2,"member_ids_preview":["675081906911707156","932662489617928295","905943889494569000"]}}]
# Run the processor
processor = DiscordMessageProcessor(test_messages)
result = processor.process_messages().generate_drive_documents()

# Print the results with better formatting
print("\n=== Message Documents ===")
for doc in result['message_documents']:
    print(f"\nMessage ID: {doc['content']['id']}")
    print(f"Content: {doc['content']['content']}")
    print(f"References: {doc['content']['references']}")
    print(f"Children: {doc['content']['children']}")

print("\n=== Thread Documents ===")
for doc in result['thread_documents']:
    print(f"\nThread Name: {doc['content']['thread_info']['thread_metadata']['name']}")
    print(f"Messages in thread: {len(doc['content']['messages'])}")
    for msg in doc['content']['messages']:
        print(f"\n  Message ID: {msg['id']}")
        print(f"  Content: {msg['content'][:100]}...")
        if msg['references']:
            print(f"  References: {msg['references']}")
        if msg['children']:
            print(f"  Children: {msg['children']}")

# Save full output to file for inspection
with open('discord_processed_output.json', 'w') as f:
    json.dump(result, f, indent=2)