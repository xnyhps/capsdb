### What is this?

It is a collection of [XEP-0115 caps](http://xmpp.org/extensions/xep-0115.html) and their hashes, aiming to collect as many hashes that are used as possible.

### What are 'caps'?

Each XMPP client has a number of features and advertises those features to other clients. However, sending a list of features every time someone signs in creates a large overhead. Therefore, clients can hash their features and only publish the hash, making it easy for other clients to cache the features.

### Why publish a list?

Multiple reasons:

* Testing. It can be tricky to correctly implement the hash generation, it helps to have a test suite available that tests against all known clients.
* Pre-loading. By including (some of) the caps in a client, the client can save on bandwith by not needing to perform the initial download and it is protected from preimage attacks.

### Wait, preimage attacks?

[Yes, sadly it is possible to generate different caps packets that have the same hash](http://mail.jabber.org/pipermail/security/2009-July/000812.html). By pre-loading the list, it becomes impossible to carry out a preimage attack against the hashes already pre-loaded.

### Some of these are really old, are you sure they are still used?

Sadly I have no idea. These were gathered over many years, so I'm sure some are now not used anymore, but I don't have a way to check that.

### Can I send pull requests with new caps?

Sure!

### License

capsdb - A collection of XMPP caps with hashes

Written in 2015 by Thijs Alkemade <me@thijsalkema.de>

To the extent possible under law, the author(s) have dedicated all copyright and related and neighboring rights to this software to the public domain worldwide. This software is distributed without any warranty.

You should have received a copy of the CC0 Public Domain Dedication along with this software. If not, see <http://creativecommons.org/publicdomain/zero/1.0/>. 
