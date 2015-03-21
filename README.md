### What is this?

It is a collection of caps and their hashes, aiming to collect as many hashes that are used as possible.

### What are 'caps'?

Each XMPP client has a number of features and advertises those features to other clients. However, sending a list of features every time someone signs in creates a large overhead. Therefore, clients can hash their features and only publish the hash, making it easy for other clients to cache the features.

### Why publish a list?

Multiple reasons:

* Testing. It can be tricky to correctly implement the hash generation, it helps to have a test suite available that tests against all known clients.
* Pre-loading. By including (some of) the caps in a client, the client can save on bandwith by not needing to perform the initial download and it is protected from collision attacks.

### Wait, collision attacks?

[Yes, sadly it is possible to generate different caps packets that have the same hash](http://mail.jabber.org/pipermail/security/2009-July/000812.html). By pre-loading the list, it becomes impossible to carry out a collision attack against the hashes already pre-loaded.
