__all__ = ['DiscordMessageProcessor', 'ThreadInfo']

from typing import Dict, List, Optional
import json
import requests
from dataclasses import dataclass, asdict
from copy import deepcopy

def convert_js_to_python(data):
    """Convert JavaScript format to Python format."""
    if isinstance(data, dict):
        return {key: convert_js_to_python(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [convert_js_to_python(item) for item in data]
    elif data == "null":
        return None
    elif data == "true":
        return True
    elif data == "false":
        return False
    else:
        return data

def fetch_thread_messages(thread_id: str, auth_token: str) -> List[dict]:
    """Fetch all messages from a Discord thread."""
    url = f'https://discord.com/api/v9/channels/{thread_id}/messages'
    headers = {
        'Authorization': auth_token,
        'Content-Type': 'application/json'
    }
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            thread_messages = response.json()
            return convert_js_to_python(thread_messages)
        else:
            print(f"Failed to fetch thread messages: {response.status_code}")
            return []
    except Exception as e:
        print(f"Error fetching thread messages: {e}")
        return []

@dataclass
class ThreadInfo:
    thread_id: str
    thread_metadata: dict
    messages: List[str]

class DiscordMessageProcessor:
    def __init__(self, messages: List[dict], auth_token: Optional[str] = None):
        self.auth_token = auth_token
        self.messages = convert_js_to_python(messages)  # Convert on initialization
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
                    # Fetch additional thread messages if auth token is provided
                    if self.auth_token:
                        thread_messages = fetch_thread_messages(thread['id'], self.auth_token)
                        for thread_msg in thread_messages:
                            if thread_msg['id'] not in self.processed_messages:
                                self.processed_messages[thread_msg['id']] = {
                                    **thread_msg,
                                    'references': [],
                                    'children': []
                                }
                                self.threads[thread['id']].messages.append(thread_msg['id'])
                
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

        # Sort messages by timestamp
        sorted_message_ids = sorted(
            thread.messages,
            key=lambda msg_id: self.processed_messages[msg_id]['timestamp']
        )

        # Add all messages in the thread
        for message_id in sorted_message_ids:
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
    



# Example usage:
if __name__ == "__main__":
    # Your Discord auth token
    AUTH_TOKEN = "MjcxMTI3NTMzNjAzMjU4Mzgw.Gr1gpU.1HOfb3rpgneT52bHNhJ1FIyh_RoO5XX5KOBU4I"


    #TODO: NEED TO MAKE THE CHANNEL ID AS A PARAMETER
    #TODO: NEED TO GET THE PROCESSED MESSAGES TO GOOGLE DRIVE

    RESTACK_SUPPORT_CHANNEL="1293665802523902032"
    
    # Make Discord API request to get messages
    response = requests.get(
        f'https://discord.com/api/v9/channels/{RESTACK_SUPPORT_CHANNEL}/messages?limit=100',
        headers={
            'Authorization': AUTH_TOKEN,
            'Content-Type': 'application/json'
        }
    )

    raw_messages = response.json()
    
    
    # Process messages with auth token for thread fetching
    processor = DiscordMessageProcessor(raw_messages, AUTH_TOKEN)
    result = processor.process_messages().generate_drive_documents()
    
    # Save to file
    with open('discord_processed_output.json', 'w') as f:
        json.dump(result, f, indent=2)