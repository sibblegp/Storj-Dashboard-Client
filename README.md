# Storj Dashboard Client

<p align="center">
  <img src="https://s3-us-west-1.amazonaws.com/storjdashgeneral/Screenshot+2017-10-25+18.35.13.png" alt="Dashboard">
</p>

Welcome to the StorJ Dashboard client.  This is the server module for [www.storjdash.com](https://www.storjdash.com/) and can be used to monitor [StorJ](https://storj.io) farming nodes on as many servers as you'd like.  It is provided free of charge.

### This software is currently in beta testing.

### Currently the client only works on Ubuntu and Debian distributions.

### Stop now if you are using any other operating system.

To get started, [register for an account at StorJDash.com](https://www.storjdash.com/register/).  You will need these credentials later.

Next, we need to check that we have a valid version of Python 3 installed.  Run the following command:

```
python3 -V
```

You should see some output like:

```
Python 3.5.2
```

As long as it is above 3.5 you are okay.  If it is not or the command does not run, please google about installing python 3.

Next we need to install the python 3 package manager:

```
sudo apt-get install python3-pip python3-setuptools python3-wheel
```

Now it's time for the fun stuff.  Time to install our StorJ Dashboard Client.

Make sure you run this with pip3 and not pip.

```
sudo pip3 install storjdash
```
It's finally time to set up the client.  First, we need to make sure of a few things.

* You will need to enter your StorJDash login details.  You should have a registered account at [StorjDash](https://www.storjdash.com/).
* All of your configuration files should be in their own directory.
* Your config files should be in standard format without any additional comments.

Let's configure the client.  You may wonder why this requires sudo access.  This is because registration writes a config file to /etc and creates a cron job to hourly submit reports.

```
sudo register_storjdash
```

If all goes well, your server will acknowledge that it has registered and schedule an hourly update for your servers.

Let's kick off your first report!

```
send_storj_reports
```
If all is working, you should see at least one output like this:
```
{'server_uuid': 'caf36562-2b7b-42fa-911f-19c4ea12776f', 'node_capacity': 800000000000.0, 'current_size': 306160401105, 'node_name': 'node1', 'report_uuid': 'dbdf6fb7-6ccc-41e0-a3e5-08229a603dcd', 'storj_node_id': '1438a6ea791f5996fc63b4d180ecadb7ddd1384c'}
```
If you don't see this output or you see an error, seek support below.

### Support

You can obtain support in several ways:

* Private Message @gs in the storjshare or dev channels at the [StorJ Community](https://community.storj.io/)
* Send an email to [support@storjdash.com](mailto:support@storjdash.com)
* Submit an issue on this GitHub repo

Supported Operating Systems:

* Ubuntu 14.*
* Ubuntu 16.*
* Debian 9.*
* Devuan Ascii (9.*)

### Donations

If you enjoy StorJDash, you can support it by donating StorJ Tokens or ETH to:

```
0xabA365D78086b1e9A12555A656AEc0cB92B8f9CA
```
