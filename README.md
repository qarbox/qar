
# Qar

Qar is a comprehensive solution for managing your library of movie and TV shows.
It is designed to be installed on a Linux system and provide:

 * A web interface focused on basic tasks like setup and configuration that is
   simple even for less experienced users.

 * [qBittorrent][qbittorrent] for download management. Media downloads happen
   automatically in the background, but users can access the download management
   web interface if you want.

 * Full support for popular VPNs out of the box with simplified setup.

 * Bandwidth and seed rules with guided information to ensure users don't use
   too much bandwidth on accident while also ensuring the health of distributed
   content.

 * [Jellyfin][jellyfin] for media streaming making it highly accessible for PC,
   Android, iOS and smart TVs like Roku to watch.

 * `dockermdns` for publishing docker containers with different `.local` domain
 names each with their own IP address using [mDNS][mdns].

## Installation

If you want to install on an existing Linux server you can run:

    git clone 'https://github.com/qarbox/qar.git'
    cd qar
    sudo ./install.sh

This will install all of the packages needed and prepare the system to be
accessed via `http://qar.local`.

## Security

Qar was designed to keep users safe from many different types of attacks. Most
of the system is separated into containers with access only to the media
content.

In addition Qar helps keep users safe by supporting VPN out of the box and
giving users information about the risks of downloading without a VPN.

[release]: https://github.com/qarbox/qar/releases
[mdns]: https://en.wikipedia.org/wiki/Multicast_DNS
[qbittorrent]: https://www.qbittorrent.org/
[jellyfin]: https://jellyfin.org/