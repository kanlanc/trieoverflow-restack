from restack_ai.function import function, log
from pydantic import BaseModel


@function.defn()
async def discordAgent() -> str:
    try:
        log.info("discordAgent function started")

        discordMessages= [{"type":18,"content":"Problems running `modus dev` with assemblyscript/examples/simple","mentions":[],"mention_roles":[],"attachments":[],"embeds":[],"timestamp":"2025-01-12T22:02:11.409000+00:00","edited_timestamp":None,"flags":32,"components":[],"id":"1328121879604625418","channel_id":"1292948253796466730","author":{"id":"535416794295566358","username":"gmlewis","avatar":"a3dd8fc27b833334b5ca433efa11a0a9","discriminator":"0","public_flags":0,"flags":0,"banner":None,"accent_color":None,"global_name":"Glenn","avatar_decoration_data":None,"banner_color":None,"clan":None,"primary_guild":None},"pinned":False,"mention_everyone":False,"tts":False,"message_reference":{"type":0,"channel_id":"1328121879604625418","guild_id":"1267579648657850441"},"thread":{"id":"1328121879604625418","type":11,"last_message_id":"1328169152174886944","flags":0,"guild_id":"1267579648657850441","name":"Problems running `modus dev` with assemblyscript/examples/simple","parent_id":"1292948253796466730","rate_limit_per_user":0,"bitrate":64000,"user_limit":0,"rtc_region":None,"owner_id":"535416794295566358","thread_metadata":{"archived":False,"archive_timestamp":"2025-01-12T22:02:11.409000+00:00","auto_archive_duration":10080,"locked":False,"create_timestamp":"2025-01-12T22:02:11.409000+00:00"},"message_count":24,"member_count":2,"total_message_sent":24,"member_ids_preview":["535416794295566358","689915733009891363"]},"position":0},{"type":18,"content":"Hypermode Model Errors","mentions":[],"mention_roles":[],"attachments":[],"embeds":[],"timestamp":"2025-01-12T19:06:22.237000+00:00","edited_timestamp":None,"flags":0,"components":[],"id":"1328077633170182179","channel_id":"1292948253796466730","author":{"id":"689915733009891363","username":"mattjohnsonpint","avatar":"0ac66b3f0faa67fff7ed437da96fcdb0","discriminator":"0","public_flags":0,"flags":0,"banner":None,"accent_color":None,"global_name":"Matt Johnson-Pint","avatar_decoration_data":None,"banner_color":None,"clan":None,"primary_guild":None},"pinned":False,"mention_everyone":False,"tts":False,"message_reference":{"type":0,"channel_id":"1328073667925774448","guild_id":"1267579648657850441"},"position":0}]

        return discordMessages
    

    except Exception as e:
        log.error("discordAgent function failed", error=e)
        raise e
