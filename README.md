# async-vk-bot

Async VK bot builder built with
[trio](https://github.com/python-trio/trio)
and [async-vk-api](https://github.com/Suenweek/async-vk-api).


## Installation

```bash
pip install git+https://github.com/Suenweek/async-vk-bot#egg=async-vk-bot
```


## Usage

```python
import trio
from async_vk_bot import Bot

bot = Bot()

@bot.on('message_new')
async def echo(obj):
    await bot.vk.messages.send(
        peer_id=obj['peer_id'],
        message=obj['text']
    )

if __name__ == '__main__':
    trio.run(bot)
```

For the list of possible event types see
https://vk.com/dev/groups_events.
