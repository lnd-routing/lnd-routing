# LND ⚡ Routing

High capacity, high availability, well connected, fast lightning node. 

We aim to become a top liquidity provider for the lightning network.

## Quick and easy

Use `request_channel.py` to request an incoming channel.

## Channel open requests

We have developed a keysend based protocol for paid channel requests. It is based on the keysend messaging protocol.

To request a channel opening, send us a keysend of `(desired_channel_value * 0.0025) + 500` sats with custom records `1667785070=01` (for a public channel) or `1667785070=02` (for a private channel) and `34349339=<node_pubkey>`. You can optionally include a message in record `34349334` as a hex encoded UTF-8 string. Our node will attempt to connect to yours and open a channel within a few seconds.

- Minimum channel size is 100,000 sats. 
- Maxmimum channel size is 1 btc.
- Only one channel per node. If you need a larger one, please close the existing channel first.

Automatic refunds for failed channel openings are issued via keysend to the specified node. 

*Please check your data carefully, refunds are only automatically issued for failed channel openings, not invalid inputs. We highly suggest using `request_channel.py`.*

Our node will attempt to look up and connect to yours, but for best results, connect to us as a peer prior to 
requesting a channel.

`lncli connect 02ab583d430015f3b6b41730434b5fac264901b50199f0b9becc0a98a365f581a9@hgjdgzq7h6e32anpkiveobx4coihxg4buzcevsxqr6lcj35stzszicad.onion:9735`

`lightning-cli connect 02ab583d430015f3b6b41730434b5fac264901b50199f0b9becc0a98a365f581a9@hgjdgzq7h6e32anpkiveobx4coihxg4buzcevsxqr6lcj35stzszicad.onion:9735`

`eclair-cli connect --uri=02ab583d430015f3b6b41730434b5fac264901b50199f0b9becc0a98a365f581a9@hgjdgzq7h6e32anpkiveobx4coihxg4buzcevsxqr6lcj35stzszicad.onion:9735`

We currently only have instructions for paying for channel requests from LND, but the destination node can be running any implementation.

### Template:

Replace the parts containing brackets. We have received several channel requests to the non-existant example nodes.

```
lncli sendpayment --keysend  --amt <(desired_channel_value * 0.0025) + 500> \
--dest 02ab583d430015f3b6b41730434b5fac264901b50199f0b9becc0a98a365f581a9 \
--data 1667785070=01,34349339=<your_node_pubkey>
```

### Examples:
To request a 0.1btc public channel from us to node 0102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f2021:
```
lncli sendpayment --keysend  --amt 25500 \
--dest 02ab583d430015f3b6b41730434b5fac264901b50199f0b9becc0a98a365f581a9 \
--data 1667785070=01,34349339=0102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f2021
```

To request a 0.1btc private channel from us to node 0102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f2021:
```
lncli sendpayment --keysend  --amt 25500 \
--dest 02ab583d430015f3b6b41730434b5fac264901b50199f0b9becc0a98a365f581a9 \
--data 1667785070=02,34349339=0102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f2021
```

To request a 0.2btc public channel from us to node 22232425262728292a2b2c2d2e2f303132333435363738393a3b3c3d3e3f404142 with "Hello LND.Routing" as a message to us:
```
lncli sendpayment --keysend --amt 50500 \
--dest 02ab583d430015f3b6b41730434b5fac264901b50199f0b9becc0a98a365f581a9 \
--data 1667785070=01,34349339=22232425262728292a2b2c2d2e2f303132333435363738393a3b3c3d3e3f404142,34349334=48656c6c6f204c4e442e526f7574696e67`
```

To simply send us a message:
```
lncli sendpayment --keysend --amt 1 \
--dest 02ab583d430015f3b6b41730434b5fac264901b50199f0b9becc0a98a365f581a9 \
--data 34349334=48656c6c6f204c4e442e526f7574696e67`
```


If you have any issues, open one on this repo.

<!--
**lnd-routing/lnd-routing** is a ✨ _special_ ✨ repository because its `README.md` (this file) appears on your GitHub profile.

Here are some ideas to get you started:

- 🔭 I’m currently working on ...
- 🌱 I’m currently learning ...
- 👯 I’m looking to collaborate on ...
- 🤔 I’m looking for help with ...
- 💬 Ask me about ...
- 📫 How to reach me: ...
- 😄 Pronouns: ...
- ⚡ Fun fact: ...
-->
